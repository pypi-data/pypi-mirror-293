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
"""Download the MNIST dataset and save it in dataset-lib format.

Example use:
    python mnist_save.py -d "~/Datasets/mnist_dataset/"
    python iterate.py -d "~/Datasets/mnist_dataset/"
"""

import argparse
import random
from typing import get_args

from tensorflow import keras
from tqdm import tqdm

from sedpack.io import Dataset, Metadata, DatasetStructure, Attribute
from sedpack.io.types import CompressionT, ShardFileTypeT, SplitT


def main() -> None:
    """Convert the MNIST dataset into sedpack format.
    """
    parser = argparse.ArgumentParser(
        description="Convert MNIST dataset into dataset-lib format")
    parser.add_argument("--dataset_directory",
                        "-d",
                        help="Where to save the dataset",
                        required=True)
    parser.add_argument(
        "--compression",
        "-c",
        help="Which compression algorithm to use for the shards",
        choices=get_args(CompressionT),
        default="ZIP")
    parser.add_argument("--shard_file_type",
                        "-t",
                        help="Technology to save shard files",
                        choices=get_args(ShardFileTypeT),
                        default="tfrec")
    args = parser.parse_args()

    # General info about the dataset
    metadata = Metadata(
        description="MNIST dataset in the sedpack format",
        dataset_license="""
        Yann LeCun and Corinna Cortes hold the copyright of MNIST dataset, which is
        a derivative work from original NIST datasets. MNIST dataset is made
        available under the terms of the Creative Commons Attribution-Share Alike
        3.0 license.
        """,
        custom_metadata={
            "list of authors": ["Yann LeCun", "Corinna Cortes"],
        },
    )

    # Types of attributes stored
    dataset_structure = DatasetStructure(
        saved_data_description=[
            Attribute(
                name="input",
                shape=(28, 28),
                dtype="float16",
            ),
            Attribute(
                name="digit",
                shape=(),
                dtype="int8",
            ),
        ],
        shard_file_type=args.shard_file_type,
        compression=args.compression,
    )

    # Create a new dataset
    dataset = Dataset.create(
        path=args.dataset_directory,  # All files are stored here
        metadata=metadata,
        dataset_structure=dataset_structure,
    )

    # Fill in examples
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    # DatasetFiller makes sure that all shard files are written properly
    # when exiting the context.
    with dataset.filler() as dataset_filler:
        # Determine which data are in the holdout (test)
        assert len(x_test) == len(y_test)
        for i in tqdm(range(len(x_test)), desc="holdout"):
            dataset_filler.write_example(
                values={
                    "input": x_test[i],
                    "digit": y_test[i],
                },
                split="holdout",
            )

        # Randomly assign 10% of validation and the rest is training
        assert len(x_train) == len(y_train)
        train_indices: list[int] = list(range(len(x_train)))
        random.shuffle(train_indices)
        validation_split_position: int = int(len(x_train) * 0.1)
        for index_position, index in enumerate(
                tqdm(train_indices, desc='train and val')):
            split = "test" if index_position < validation_split_position else "train"
            dataset_filler.write_example(
                values={
                    "input": x_train[index],
                    "digit": y_train[index],
                },
                split=split,
            )


if __name__ == "__main__":
    main()
