# Copyright 2024 Google LLC
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
"""First version of the benchmarking script.

Dataset used for docs/tutorials/writing/multiprocessing_write.py

A dataset for microscopic peripheral blood cell images for development of
automatic recognition systems
Contributors:
  Andrea Acevedo,
  Anna Merino,
  Santiago Alférez,
  Ángel Molina,
  Laura Boldú,
  José Rodellar
"""

import argparse
from dataclasses import dataclass
import io
from pathlib import Path
import time
from typing import Any, Callable, List, Optional, Tuple

import keras
from keras import layers
import numpy as np
from PIL import Image
from tabulate import tabulate
from tqdm import tqdm

import tensorflow as tf

from sedpack.io import Dataset
from sedpack.io.types import ExampleT, TFModelT, TFDatasetT

BATCH_SIZE = 64


@dataclass
class BenchmarkResult:
    name: str
    model_training_time_s: float
    loop_time_s: float
    size_gb: float
    acc_train: float
    acc_val: float
    # Headers for the table of results.
    headers: Tuple[str, ...] = (
        "name",
        "training [s]",
        "one batch [s]",
        "size [GB]",
        "acc [%]",
        "val_acc [%]",
    )

    def to_table_line(self) -> Tuple[str, ...]:
        """Representation of this experiment as a line in the table of results.
        """
        return (
            self.name,
            f"{self.model_training_time_s:0.4f}",
            f"{self.loop_time_s:0.4f}",
            f"{self.size_gb:0.2f}",
            f"{self.acc_train:0.2f}",
            f"{self.acc_val:0.2f}",
        )


def du_gb(path: str) -> float:
    """Return disk usage of a directory in GB.
    """
    path = Path(path)
    du_bytes = sum(f.stat().st_size for f in path.glob("**/*"))
    return du_bytes / 1024**3


def get_model(img_shape: Tuple[int, int, int],
              classes: int,
              print_summary: bool = False) -> TFModelT:
    """Return VGG19 model for fine tuning.
    """
    vgg_model = keras.applications.VGG19(
        include_top=False,
        weights="imagenet",
        input_tensor=None,
        input_shape=img_shape,
        pooling="avg",
        classes=classes,
        classifier_activation="softmax",
    )

    input_layer = layers.Input(shape=img_shape)
    scale_layer = layers.Rescaling(scale=1 / 256, offset=0)

    x = scale_layer(input_layer)
    x = vgg_model(x, training=False)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(16, activation="relu")(x)
    predictions = layers.Dense(8, activation="softmax")(x)

    full_model = keras.models.Model(inputs=input_layer, outputs=predictions)

    full_model.compile(optimizer="adam",
                       loss="categorical_crossentropy",
                       metrics="acc")

    if print_summary:
        full_model.summary()

    return full_model


def from_directory(
        path: Path, img_shape: Tuple[int, int,
                                     int]) -> Tuple[TFDatasetT, TFDatasetT]:
    ds_train, ds_val = keras.utils.image_dataset_from_directory(
        directory=path,
        labels="inferred",
        label_mode="categorical",
        batch_size=BATCH_SIZE,
        image_size=img_shape[:-1],
        seed=42,
        validation_split=0.1,
        subset="both",
    )

    ds_train = ds_train.repeat()
    ds_val = ds_val.repeat()

    return ds_train, ds_val


def from_converted(
        path: Path, img_shape: Tuple[int, int,
                                     int]) -> Tuple[TFDatasetT, TFDatasetT]:
    del img_shape  # unused
    dataset = Dataset(path)

    # TODO add default for this
    def process_record(rec: ExampleT) -> Tuple[Any, Any]:
        output = rec["class"]
        output = keras.layers.CategoryEncoding(num_tokens=8,
                                               output_mode="one_hot")(output)
        img = tf.cast(rec["img"], tf.float32)
        #img = img / 256
        return img, output

    # Load train and validation splits of the dataset
    ds_train = dataset.as_tfdataset(
        "train",
        batch_size=BATCH_SIZE,
        process_record=process_record,
    )
    ds_val = dataset.as_tfdataset(
        "test",  # validation split
        batch_size=BATCH_SIZE,
        process_record=process_record,
    )

    return ds_train, ds_val


def from_converted_bytes(
        path: Path, img_shape: Tuple[int, int,
                                     int]) -> Tuple[TFDatasetT, TFDatasetT]:
    dataset = Dataset(path)

    # TODO add default for this
    def process_record(rec: ExampleT) -> Tuple[Any, Any]:
        output = rec["class"]
        output = keras.layers.CategoryEncoding(num_tokens=8,
                                               output_mode="one_hot")(output)
        img = rec["img"]
        # TODO generic tf.io.decode_image ?
        img = tf.io.decode_jpeg(img)
        img = tf.image.convert_image_dtype(img, tf.float32)
        # Crop the image
        img = tf.image.resize(img, img_shape[:-1])
        # Rescale
        #img = img / 256
        return img, output

    # Load train and validation splits of the dataset
    ds_train = dataset.as_tfdataset(
        "train",
        batch_size=BATCH_SIZE,
        process_record=process_record,
    )
    ds_val = dataset.as_tfdataset(
        "test",  # validation split
        batch_size=BATCH_SIZE,
        process_record=process_record,
    )

    return ds_train, ds_val


def single_experiment(path: str, experiment_name: str,
                      get_dataset: Callable[[Path, Tuple[int, int, int]],
                                            Tuple[TFDatasetT, TFDatasetT]],
                      verbose: bool) -> BenchmarkResult:
    img_shape = (360, 359, 3)

    model = get_model(
        img_shape,
        8,  # classes
        print_summary=verbose)

    # Model training time
    begin = time.perf_counter()
    ds_train, ds_val = get_dataset(Path(path), img_shape)
    history = model.fit(ds_train,
                        validation_data=ds_val,
                        steps_per_epoch=100,
                        validation_steps=10,
                        epochs=5)
    acc = history.history["acc"][-1]
    val_acc = history.history["val_acc"][-1]
    end = time.perf_counter()
    model_training_duration = end - begin

    # 1_000 batches
    begin = time.perf_counter()
    ds_train, ds_val = get_dataset(Path(path), img_shape)
    for _ in ds_train.take(1_000):
        pass
    end = time.perf_counter()
    loop_time_duration = end - begin

    return BenchmarkResult(
        name=experiment_name,
        model_training_time_s=model_training_duration,
        loop_time_s=loop_time_duration,
        size_gb=du_gb(path),
        acc_train=100 * acc,
        acc_val=100 * val_acc,
    )


def benchmark(args: argparse.Namespace) -> None:
    table = []

    if args.uncompressed:
        # Converted dataset represented as jpg bytes without shard compression.
        table.append(
            single_experiment(path=args.uncompressed,
                              experiment_name="sedpack_bytes_uncompressed",
                              get_dataset=from_converted_bytes,
                              verbose=args.verbose).to_table_line())

    if args.bytes:
        # Converted dataset represented as jpg bytes with shard compression.
        table.append(
            single_experiment(path=args.bytes,
                              experiment_name="sedpack_bytes",
                              get_dataset=from_converted_bytes,
                              verbose=args.verbose).to_table_line())

    if args.raw:
        # keras.image_dataset_from_directory
        table.append(
            single_experiment(path=args.raw,
                              experiment_name="from_directory",
                              get_dataset=from_directory,
                              verbose=args.verbose).to_table_line())

    if args.converted:
        # sedpack_array version
        table.append(
            single_experiment(path=args.converted,
                              experiment_name="sedpack_array",
                              get_dataset=from_converted,
                              verbose=args.verbose).to_table_line())

    print("")
    print(tabulate(table, headers=BenchmarkResult.headers))


def main():
    parser = argparse.ArgumentParser(
        description="Compare performance of several possibilities of saving " \
                    "the same image dataset. Each argument is optional path " \
                    "to the dataset stored in the corresponding format. If " \
                    "not provided it does not get profiled.")
    parser.add_argument(
        "--raw",
        "-r",
        help="Directory containing a subdirectory for each class and all " \
             "images of that class in the corresponding subdirectory.",
        type=lambda p: Path(p) if p else None,
        default=None,
        required=False,
    )
    parser.add_argument(
        "--converted",
        "-c",
        help="sedpack.io.Dataset version of the images, encoded as " \
             "array, each of them of shape (360, 359, 3).",
        type=lambda p: Path(p) if p else None,
        default=None,
        required=False,
    )
    parser.add_argument(
        "--bytes",
        "-b",
        help="sedpack.io.Dataset version of the dataset, images stored " \
             "as JPEG bytes.",
        type=lambda p: Path(p) if p else None,
        default=None,
        required=False,
    )
    parser.add_argument(
        "--uncompressed",
        "-u",
        help="sedpack.io.Dataset version of the dataset, images stored " \
             "as JPEG bytes, no shard file compression.",
        type=lambda p: Path(p) if p else None,
        default=None,
        required=False,
    )
    parser.add_argument("--verbose",
                        "-v",
                        help="Verbose (e.g., print model summary)",
                        type=bool,
                        required=False,
                        default=False)
    args = parser.parse_args()

    benchmark(args)


if __name__ == "__main__":
    main()
