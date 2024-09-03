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
"""Iterate a dataset.

Example use:
    python create_dataset.py -d "~/Datasets/my_new_dataset/"
    python iterate.py -d "~/Datasets/my_new_dataset/"
"""
import asyncio
import argparse
import time
from typing import Any, Dict, Tuple

from perfcounters import TimeCounters
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tqdm import tqdm

from sedpack.io import Dataset
from sedpack.io.types import TFModelT


def time_execution(function,
                   counter_name: str,
                   dataset: Dataset,
                   time_counters: TimeCounters | None,
                   shuffle: int = 0) -> None:
    desc: str = f"warmup_{counter_name}"
    if time_counters is not None:
        desc = counter_name
        time_counters.start(counter_name)

    try:
        function(dataset=dataset, shuffle=shuffle, desc=desc)

        if time_counters is not None:
            time_counters.stop(counter_name)
    except:
        # Delete that counter.
        if time_counters and counter_name in time_counters.counters:
            del time_counters.counters[counter_name]


def iterate(dataset: Dataset, shuffle: int, desc: str) -> None:
    for example in tqdm(dataset.as_numpy_iterator(split="train",
                                                  repeat=False,
                                                  shuffle=shuffle),
                        desc=desc):
        pass


def iterate_as_tfdataset(dataset: Dataset, shuffle: int, desc: str) -> None:
    for example in tqdm(dataset.as_tfdataset(split="train",
                                             repeat=False,
                                             batch_size=0,
                                             shuffle=shuffle),
                        desc=desc):
        pass


def iterate_concurrent(dataset: Dataset, shuffle: int, desc: str) -> None:
    for example in tqdm(dataset.as_numpy_iterator_concurrent(split="train",
                                                             repeat=False,
                                                             shuffle=shuffle),
                        desc=desc):
        pass


async def iterate_async(dataset, time_counters, shuffle: int) -> None:
    """Repeat code from `time_execution`, but avoid counting `asyncio.run` into
    the time.
    """
    counter_name: str = "iterate_async"
    desc: str = f"warmup_{counter_name}"
    if time_counters is not None:
        desc = counter_name
        time_counters.start(counter_name)

    pbar = tqdm(desc=desc)

    try:
        async for example in dataset.as_numpy_iterator_async(split="train",
                                                             repeat=False,
                                                             shuffle=shuffle):
            pbar.update()

        pbar.close()

        if time_counters is not None:
            time_counters.stop(counter_name)
    except:
        # Delete that counter.
        if time_counters and counter_name in time_counters.counters:
            del time_counters.counters[counter_name]


def main() -> None:
    """Iterate a dataset.
    """
    parser = argparse.ArgumentParser(description="Iterate a dataset")
    parser.add_argument("--dataset_directory",
                        "-d",
                        help="Where to load the dataset",
                        required=True)
    args = parser.parse_args()

    dataset = Dataset(args.dataset_directory)  # Load the dataset

    # Avoid a cold start (files might not be in OS filesystem cache). Shard
    # file types compatible with as_numpy_iterator_async is a subset of those
    # compatible with as_numpy_iterator.
    asyncio.run(iterate_async(dataset=dataset, time_counters=None, shuffle=0))

    # Measurements:

    # Performance measurements.
    cnts = TimeCounters()

    # Using tf.data.Dataset pipeline:
    time_execution(iterate_as_tfdataset,
                   counter_name="iterate_as_tfdataset",
                   dataset=dataset,
                   time_counters=cnts,
                   shuffle=0)

    # Multiprocessing.
    time_execution(iterate_concurrent,
                   counter_name="iterate_concurrent",
                   dataset=dataset,
                   time_counters=cnts,
                   shuffle=0)

    # Synchronous call:
    time_execution(function=iterate,
                   counter_name="iterate",
                   dataset=dataset,
                   time_counters=cnts,
                   shuffle=0)

    # Async call (this needs an even loop). Usually a single event loop is
    # created in a program.
    asyncio.run(iterate_async(dataset=dataset, time_counters=cnts, shuffle=0))

    cnts.report(rounding=5)


if __name__ == "__main__":
    main()
