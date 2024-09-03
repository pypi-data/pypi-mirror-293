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
"""Write a dataset using multiprocessing to speed up the dataset creation.

Dataset details:

    A dataset for microscopic peripheral blood cell images for development of automatic recognition systems
    Contributors: Andrea Acevedo, Anna Merino, Santiago Alférez, Ángel Molina, Laura Boldú, José Rodellar

    https://data.mendeley.com/datasets/snkd93bnjr/1
    Licence: CC BY 4.0

    @article{ACEVEDO2019105020,
        title = {Recognition of peripheral blood cell images using convolutional neural networks},
        journal = {Computer Methods and Programs in Biomedicine},
        volume = {180},
        pages = {105020},
        year = {2019},
        issn = {0169-2607},
        doi = {https://doi.org/10.1016/j.cmpb.2019.105020},
        url = {https://www.sciencedirect.com/science/article/pii/S0169260719303578},
        author = {Andrea Acevedo and Santiago Alférez and Anna Merino and Laura Puigví and José Rodellar},
        keywords = {Deep learning, Fine-tuning, Convolutional neural networks, Blood cell morphology, Blood cell automatic recognition},
    }

    Download size: 266 MB
    Converted size: 3.3 GB (since this is saved as arrays and not JPG)

    TODO implement saving JPG bytes and reading using https://keras.io/api/data_loading/image/

Additional packages:
    pip install pillow
"""

import argparse
from pathlib import Path
from typing import Dict, Optional, Tuple, Union
from typing_extensions import get_args

import numpy as np
from PIL import Image
from tqdm import tqdm

from sedpack.io import Attribute, Dataset, DatasetFiller, DatasetStructure, Metadata
from sedpack.io.types import AttributeValueT, CompressionT, SplitT


def fill_dataset(dataset_filler: DatasetFiller,
                 class_mapping: Dict[str, int],
                 raw_files: Path,
                 img_shape: Optional[Tuple[int, int, int]],
                 processes: int = 1,
                 process_id: int = 0,
                 disable_tqdm: bool = False) -> None:
    """Function being passed to Dataset.write_multiprocessing and called in
    another process. This function and all arguments and the return value need
    to be pickleable. Arguments are optimized so that not many arguments are
    being passed between processes. Can be also used as single process.

    Args:

      dataset_filler (DatasetFiller): The context manager for writing
      examples.

      class_mapping (Dict[str, int]): Mapping of a class name into integer.
      Used because class labels are integers.

      raw_files (Path): Path to the directory containing raw images.

      img_shape (Optional[Tuple[int, int, int]]): Shape of the image (not all
      images are 100% the same shape). This function crops. If None then save
      the bytes content of jpg file.

      processes (int): How many processes are being spawned. Used to determine
      which files to add.

      process_id (int): ID of this process. Used to determine which files to
      add.

      disable_tqdm (bool): To let only one of the processes print the progress
      bar. This method is implemented such that rounding gives more work to the
      last process.
    """
    with dataset_filler as filler:

        # Classes are not balanced, put 10% of each class into holdout and 10%
        # into test.
        # Random seed to synchronize all processes.
        rng = np.random.default_rng(123456789)
        for class_name, label in tqdm(class_mapping.items(),
                                      desc="Label",
                                      disable=disable_tqdm):
            # Determine which data are in the holdout (test).
            file_names = np.array(list((raw_files / class_name).glob("*.jpg")))
            rng.shuffle(file_names)

            # 10% for holdout and 10% for test
            test_examples: int = len(file_names) // 10
            fill_list = []
            for i, file_name in enumerate(file_names):
                # Determine which split we are adding this file into.
                split: SplitT = "train"
                if i < test_examples:
                    split = "holdout"
                elif test_examples <= i < 2 * test_examples:
                    split = "test"
                # Remember that this file is saved into the split.
                fill_list.append((file_name, split))

            # BEGIN ADDITIONAL CODE FOR MULTIPROCESSING

            # Divide file_names between processes.
            files_per_process: int = len(file_names) // processes
            begin: int = process_id * files_per_process
            end: int = (process_id + 1) * files_per_process
            if process_id + 1 == processes:
                # Last process takes the rest which has been rounded off.
                end = -1
            # Cut the file_names appropriately.
            fill_list = fill_list[begin:end]

            # END ADDITIONAL CODE FOR MULTIPROCESSING

            # Fill splits
            for file, split in tqdm(fill_list,
                                    desc=class_name,
                                    leave=False,
                                    disable=disable_tqdm):

                img: AttributeValueT
                if img_shape:
                    # Image represented as an array.
                    # Crop the image.
                    img = np.array(Image.open(file))
                    img = img[:img_shape[0], :img_shape[1], :]
                    assert img.shape == img_shape
                else:
                    # Image represented as bytes content of the jpg file.
                    with open(file, "rb") as f:
                        img = f.read()

                # Add example
                filler.write_example(
                    values={
                        "img": img,
                        "class": label,
                        "class_str": class_name,
                        "file_name": file.name,
                    },
                    split=split,
                )


def main() -> None:
    """Example usage of the sedpack library.

    Convert blood cell image dataset into the sedpack format.
    """
    parser = argparse.ArgumentParser(
        description="Convert blood cell image dataset")
    parser.add_argument("--raw",
                        "-r",
                        help="Raw data directory",
                        default="PBC_dataset_normal_DIB")
    parser.add_argument("--converted",
                        "-c",
                        help="Converted dataset directory",
                        default="blood_cell_images")
    parser.add_argument(
        "--processes",
        "-p",
        type=int,
        help="How many processes to use, defaults to 0 for single process.",
        default=0)
    parser.add_argument("--compression",
                        "-z",
                        help="Which compression to use",
                        choices=get_args(CompressionT),
                        default="GZIP")
    parser.add_argument("--format",
                        "-f",
                        help="Save either as array or bytes",
                        choices=["array", "bytes"],
                        default="array")
    args = parser.parse_args()

    # General info about the dataset
    metadata = Metadata(
        description="A dataset for microscopic peripheral blood cell images " \
                    "for development of automatic recognition systems",
        dataset_license="CC BY 4.0",
        custom_metadata={
            "name": "A dataset for microscopic peripheral blood cell images " \
                    "for development of automatic recognition systems",
            "contributors": "Andrea Acevedo, Anna Merino, Santiago Alférez, " \
                            "Ángel Molina, Laura Boldú, José Rodellar",
            "bibtex":
                """@article{ACEVEDO2019105020,
                title = {Recognition of peripheral blood cell images using convolutional neural networks},
                journal = {Computer Methods and Programs in Biomedicine},
                volume = {180},
                pages = {105020},
                year = {2019},
                issn = {0169-2607},
                doi = {https://doi.org/10.1016/j.cmpb.2019.105020},
                url = {https://www.sciencedirect.com/science/article/pii/S0169260719303578},
                author = {Andrea Acevedo and Santiago Alférez and Anna Merino and Laura Puigví and José Rodellar},
                keywords = {Deep learning, Fine-tuning, Convolutional neural networks, Blood cell morphology, Blood cell automatic recognition},
            }""",
            "url":
                "https://data.mendeley.com/datasets/snkd93bnjr/1",
            "licence":
                "CC BY 4.0",
        },
    )

    # Mapping of class name into an integer representation.
    class_mapping = {
        name: i
        for i, name in enumerate([
            "basophil",
            "eosinophil",
            "erythroblast",
            "ig",
            "lymphocyte",
            "monocyte",
            "neutrophil",
            "platelet",
        ])
    }

    # Shape of the images, some are a little larger so we crop them.  We crop
    # at most nine in the first dimension and at most seven in the second.
    img_shape: Optional[Tuple[int, int, int]] = (360, 359, 3)

    # Decide how to save the image.
    img_attribute: Attribute
    if args.format == "array":
        assert img_shape  # Typechecking for not None.
        img_attribute = Attribute(name="img", shape=img_shape, dtype="uint8")
    elif args.format == "bytes":
        img_shape = None
        img_attribute = Attribute(name="img", shape=(), dtype="bytes")
    else:
        raise ValueError("Only supported formats are array, bytes")

    # Attributes of each example
    attributes = [
        img_attribute,
        Attribute(name="class",
                  shape=(),
                  dtype="uint8",
                  custom_metadata={
                      "number_of_classes": len(class_mapping),
                      "mapping_class_name_int": class_mapping,
                  }),
        Attribute(name="class_str", shape=(), dtype="str"),
        Attribute(name="file_name", shape=(), dtype="str"),
    ]

    # Types of attributes stored
    dataset_structure = DatasetStructure(
        saved_data_description=attributes,
        examples_per_shard=64,  # Small shards to allow easier shuffling
        compression=args.compression,
    )

    # Create a new dataset
    dataset = Dataset.create(
        path=args.converted,  # All files are stored here
        metadata=metadata,
        dataset_structure=dataset_structure,
    )

    if args.processes == 0:
        # Single process writing.
        # 58m 13s
        fill_dataset(
            dataset_filler=dataset.filler(),
            class_mapping=class_mapping,
            raw_files=Path(args.raw),
            img_shape=img_shape,
        )
    else:
        # Multiprocess writing.
        # 4m 26s with 16 processes
        # More than 13 times faster.
        custom_arguments = [
            # One can also use custom_kwarguments for better readability.
            [
                class_mapping,
                Path(args.raw),
                img_shape,
                args.processes,
                process_id,
                True,
            ] for process_id in range(args.processes)
        ]
        # Last process prints tqdm progress.
        custom_arguments[-1][-1] = False

        # Write the data.
        dataset.write_multiprocessing(fill_dataset, custom_arguments)


if __name__ == "__main__":
    main()
