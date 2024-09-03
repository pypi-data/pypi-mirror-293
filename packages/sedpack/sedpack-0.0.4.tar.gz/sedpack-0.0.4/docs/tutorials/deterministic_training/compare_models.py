# Copyright 2023-2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Set random seeds
# https://keras.io/examples/keras_recipes/reproducibility_recipes/
# TODO:
#   https://github.com/NVIDIA/framework-reproducibility
#   https://github.com/NVIDIA/framework-reproducibility/blob/master/doc/seeder/seeder_tf2.md

SEED = 42

import random
#random.seed(SEED)  # Set by keras.utils.set_random_seed

import numpy as np
#np.random.seed(SEED)  # Set by keras.utils.set_random_seed

import os

os.environ["PYTHONHASHSEED"] = str(SEED)

os.environ["TF_DETERMINISTIC_OPS"] = "1"
os.environ["TF_CUDNN_DETERMINISTIC"] = "1"

import tensorflow as tf
#tf.random.set_seed(SEED)  # Set by keras.utils.set_random_seed
tf.keras.utils.set_random_seed(SEED)

tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.experimental.enable_op_determinism()

import argparse

from tensorflow import keras
from tensorflow.keras import layers

from sedpack.io.types import TFModelT


def compare_weights(model_1: TFModelT, model_2: TFModelT) -> None:
    # Check that there is the same number of layers in both models
    if len(model_1.layers) != len(model_2.layers):
        raise ValueError(
            f"{len(model_1.layers) = } != {len(model_2.layers) = }")

    # Check that all layers are the same
    for layer_1, layer_2 in zip(model_1.layers, model_2.layers):
        # Check that names match
        if layer_1.name != layer_2.name:
            raise ValueError(
                f"Layer name mismatch: {layer_1.name} != {layer_2.name}")

        # Check that their weights are the same
        for w1, w2 in zip(layer_1.weights, layer_2.weights):
            if (w1.numpy() != w2.numpy()).any():
                raise ValueError(f"Weights are different for {layer_1.name}")

    print("Both models have the same weights")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load two models and check that their weights are the same."
    )
    parser.add_argument("--model_1",
                        "-a",
                        help="Where to load model 1",
                        required=True)
    parser.add_argument("--model_2",
                        "-b",
                        help="Where to load model 2",
                        required=True)
    args = parser.parse_args()

    model_1 = keras.models.load_model(args.model_1)
    model_2 = keras.models.load_model(args.model_2)

    compare_weights(model_1, model_2)


if __name__ == "__main__":
    main()
