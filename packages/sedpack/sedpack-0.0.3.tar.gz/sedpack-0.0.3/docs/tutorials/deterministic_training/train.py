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
# Check TF_ENABLE_ONEDNN_OPTS=0 for CPU training: https://blog.tensorflow.org/2022/05/whats-new-in-tensorflow-29.html

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

import argparse

from tensorflow import keras
from tensorflow.keras import layers

from sedpack.io.types import TFModelT


def train_model() -> TFModelT:
    input_shape = (28, 28)
    num_classes = 10

    # Fill in examples
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    input_data = tf.keras.Input(shape=input_shape, name="input")

    x = input_data
    x = layers.Reshape((*input_shape, 1))(x)
    x = layers.Conv2D(32, kernel_size=(3, 3), activation="relu")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Conv2D(64, kernel_size=(3, 3), activation="relu")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Flatten()(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(num_classes, activation="softmax", name="digit")(x)

    model = tf.keras.Model(inputs=input_data, outputs=x)

    model.summary()
    model.compile(loss="categorical_crossentropy",
                  optimizer="adam",
                  metrics=["accuracy"])

    steps_per_epoch = 100
    epochs = 10
    history = model.fit(
        x_train,
        y_train,
        validation_split=0.1,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
    )
    return model


def main() -> None:
    # Check that random seeds are set
    assert random.randint(0, 50) == 40
    assert np.random.randint(50) == 38
    assert tf.random.uniform((), 0, 50, dtype=tf.int32).numpy().tolist() == 37

    parser = argparse.ArgumentParser(
        description="Deterministically train a model")
    parser.add_argument("--save_model_to",
                        "-m",
                        help="Where to save the model",
                        required=True)
    args = parser.parse_args()
    model = train_model()
    model.save(args.save_model_to)


if __name__ == "__main__":
    main()
