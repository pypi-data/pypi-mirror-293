# Copyright 2024 the LlamaFactory team.
#
# This code is inspired by the CarperAI's trlx library.
# https://github.com/CarperAI/trlx/blob/v0.7.0/examples/summarize_rlhf/reward_model/reward_model.py
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# MIT License
#
# Copyright (c) 2022 CarperAI
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
from types import MethodType
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

import torch
from transformers import Trainer

from ...extras.logging import get_logger
from ..callbacks import FixValueHeadModelCallback, PissaConvertCallback, SaveProcessorCallback
from ..trainer_utils import create_custom_optimzer, create_custom_scheduler


if TYPE_CHECKING:
    from transformers import PreTrainedModel, ProcessorMixin
    from transformers.trainer import PredictionOutput

    from ...hparams import FinetuningArguments


logger = get_logger(__name__)


class PairwiseTrainer(Trainer):
    r"""
    Inherits Trainer to compute pairwise loss.
    """

    def __init__(
        self, finetuning_args: "FinetuningArguments", processor: Optional["ProcessorMixin"], **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.finetuning_args = finetuning_args
        self.can_return_loss = True  # override property to return eval_loss
        self.add_callback(FixValueHeadModelCallback)

        if processor is not None:
            self.add_callback(SaveProcessorCallback(processor))

        if finetuning_args.pissa_convert:
            self.add_callback(PissaConvertCallback)

        if finetuning_args.use_badam:
            from badam import BAdamCallback, clip_grad_norm_old_version

            self.accelerator.clip_grad_norm_ = MethodType(clip_grad_norm_old_version, self.accelerator)
            self.add_callback(BAdamCallback)

    def create_optimizer(self) -> "torch.optim.Optimizer":
        if self.optimizer is None:
            self.optimizer = create_custom_optimzer(self.model, self.args, self.finetuning_args)
        return super().create_optimizer()

    def create_scheduler(
        self, num_training_steps: int, optimizer: Optional["torch.optim.Optimizer"] = None
    ) -> "torch.optim.lr_scheduler.LRScheduler":
        create_custom_scheduler(self.args, num_training_steps, optimizer)
        return super().create_scheduler(num_training_steps, optimizer)

    def compute_loss(
        self, model: "PreTrainedModel", inputs: Dict[str, torch.Tensor], return_outputs: bool = False
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, List[torch.Tensor]]]:
        r"""
        Computes pairwise loss. The first n examples are chosen and the last n examples are rejected.

        Subclass and override to inject custom behavior.

        Note that the first element will be removed from the output tuple.
        See: https://github.com/huggingface/transformers/blob/v4.40.0/src/transformers/trainer.py#L3842
        """
        # Compute rewards
        _, _, values = model(**inputs, output_hidden_states=True, return_dict=True)

        unwrapped_model: "PreTrainedModel" = self.accelerator.unwrap_model(self.model)
        if getattr(unwrapped_model.config, "model_type", None) == "chatglm":
            values = torch.transpose(values, 0, 1)

        # Split the inputs and rewards into two parts, chosen and rejected
        batch_size = inputs["input_ids"].size(0) // 2
        chosen_input_ids, rejected_input_ids = inputs["input_ids"][:batch_size], inputs["input_ids"][batch_size:]
        chosen_rewards, rejected_rewards = values[:batch_size], values[batch_size:]
        chosen_scores, rejected_scores = [], []

        # Compute pairwise loss. Only backprop on the different tokens before padding
        loss = 0
        for i in range(batch_size):
            chosen_length = (chosen_input_ids[i] != self.tokenizer.pad_token_id).nonzero()[-1] + 1
            rejected_length = (rejected_input_ids[i] != self.tokenizer.pad_token_id).nonzero()[-1] + 1
            check_divergence = (chosen_input_ids[i] != rejected_input_ids[i]).nonzero()

            if len(check_divergence) == 0:
                end_index = chosen_length
                div_index = end_index - 1
            else:
                end_index = max(chosen_length, rejected_length)
                div_index = check_divergence[0]

            assert div_index > 0
            chosen_trunc_rewards = chosen_rewards[i, div_index:end_index]
            rejected_trunc_rewards = rejected_rewards[i, div_index:end_index]
            if return_outputs:  # use the score on the last token except pad token for inference
                chosen_scores.append(chosen_rewards[i, chosen_length - 1])
                rejected_scores.append(rejected_rewards[i, rejected_length - 1])
            loss += -torch.nn.functional.logsigmoid(chosen_trunc_rewards - rejected_trunc_rewards).mean()

        loss = loss / batch_size
        if return_outputs:
            chosen_scores, rejected_scores = torch.stack(chosen_scores), torch.stack(rejected_scores)
            return loss, [loss, chosen_scores, rejected_scores]

        return loss

    def save_predictions(self, predict_results: "PredictionOutput") -> None:
        r"""
        Saves model predictions to `output_dir`.

        A custom behavior that not contained in Seq2SeqTrainer.
        """
        if not self.is_world_process_zero():
            return

        output_prediction_file = os.path.join(self.args.output_dir, "generated_predictions.jsonl")
        logger.info(f"Saving prediction results to {output_prediction_file}")
        chosen_scores, rejected_scores = predict_results.predictions

        with open(output_prediction_file, "w", encoding="utf-8") as writer:
            res: List[str] = []
            for c_score, r_score in zip(chosen_scores, rejected_scores):
                res.append(json.dumps({"chosen": round(float(c_score), 2), "rejected": round(float(r_score), 2)}))

            writer.write("\n".join(res))
