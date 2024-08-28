# !/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: loader
@time: 2024/08/15
@contact: ybyang7@iflytek.com
@site:  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""
import json
import os
from typing import Sequence, Optional, Literal, Union, List, Dict

import datasets.splits
import numpy as np
from datasets import load_dataset, Dataset, IterableDataset, concatenate_datasets, interleave_datasets

#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
from lightmodelfactory.data.data_attr import DatasetAttr

from lightmodelfactory.util.logger import logger
from lightmodelfactory.util.param import DataArguments, TrainingArguments

FILEEXT2TYPE = {
    # "arrow": "arrow",
    "csv": "csv",
    "json": "json",
    "jsonl": "json",
    # "parquet": "parquet",
    "txt": "text",
}


def get_dataset_list(dataset_info, data_args: "DataArguments") -> List["DatasetAttr"]:
    if dataset_info is None:
        raise Exception("No dataset info provided when loading")

    if data_args.dataset is not None:
        dataset_names = [ds.strip() for ds in data_args.dataset.split(",")]
    else:
        dataset_names = []

    dataset_list: List[DatasetAttr] = []
    for name in dataset_names:

        if name not in dataset_info:
            raise ValueError("Undefined dataset {}.".format(name))

        dataset_attr = DatasetAttr("file", dataset_name=dataset_info[name]["file_name"])

        dataset_attr.set_attr("formatting", dataset_info[name], default="alpaca")
        dataset_attr.set_attr("ranking", dataset_info[name], default=False)
        dataset_attr.set_attr("subset", dataset_info[name])
        dataset_attr.set_attr("folder", dataset_info[name])
        dataset_attr.set_attr("num_samples", dataset_info[name])

        if "columns" in dataset_info[name]:
            column_names = ["system", "tools", "images", "chosen", "rejected", "kto_tag"]
            if dataset_attr.formatting == "alpaca":
                column_names.extend(["prompt", "query", "response", "history"])
            else:
                column_names.extend(["messages"])

            for column_name in column_names:
                dataset_attr.set_attr(column_name, dataset_info[name]["columns"])

        if dataset_attr.formatting == "sharegpt" and "tags" in dataset_info[name]:
            tag_names = (
                "role_tag",
                "content_tag",
                "user_tag",
                "assistant_tag",
                "observation_tag",
                "function_tag",
                "system_tag",
            )
            for tag in tag_names:
                dataset_attr.set_attr(tag, dataset_info[name]["tags"])

        dataset_list.append(dataset_attr)

    return dataset_list


def _get_merged_dataset_attrs(
        dataset_names: Optional[Sequence[str]],
        data_args: "DataArguments",
        desc: Dict,
        stage: Literal["pt", "sft", "rm", "ppo", "kto"],
):
    if dataset_names is None:
        return None

    datasets = []
    for dataset_attr in get_dataset_list(desc, data_args):
        if (stage == "rm" and dataset_attr.ranking is False) or (stage != "rm" and dataset_attr.ranking is True):
            raise ValueError("The dataset is not applicable in the current training stage.")
        logger.info(f"Loading {dataset_attr}")
        datasets.append(dataset_attr)

    return datasets


def _get_merged_dataset(
        dataset_names: Optional[Sequence[str]],
        data_args: "DataArguments",
        desc: Dict,
        stage: Literal["pt", "sft", "rm", "ppo", "kto"],
        train_args: "TrainingArguments"
):
    if dataset_names is None:
        return None

    datasets = []
    for dataset_attr in get_dataset_list(desc, data_args):
        if (stage == "rm" and dataset_attr.ranking is False) or (stage != "rm" and dataset_attr.ranking is True):
            raise ValueError("The dataset is not applicable in the current training stage.")
        logger.info(f"Loading {dataset_attr}")
        datasets.append(_load_single_dataset(dataset_attr, data_args))

    return merge_dataset(datasets, data_args, train_args.seed)


def _load_single_dataset(
        dataset_attr: "DatasetAttr",
        data_args: "DataArguments"
) -> Union["Dataset", "IterableDataset"]:
    logger.info("Loading dataset {}...".format(dataset_attr))
    data_path, data_name, data_dir, data_files = None, None, None, None
    if dataset_attr.load_from == "file":
        data_files = []
        local_path = os.path.join("data", dataset_attr.dataset_name)
        if os.path.isdir(local_path):  # is directory
            for file_name in os.listdir(local_path):
                data_files.append(os.path.join(local_path, file_name))
                if data_path is None:
                    data_path = FILEEXT2TYPE.get(file_name.split(".")[-1], None)
                elif data_path != FILEEXT2TYPE.get(file_name.split(".")[-1], None):
                    raise ValueError("File types should be identical.")
        elif os.path.isfile(local_path):  # is file
            data_files.append(local_path)
            data_path = FILEEXT2TYPE.get(local_path.split(".")[-1], None)
        else:
            raise ValueError("File {} not found.".format(local_path))

        if data_path is None:
            raise ValueError("Allowed file types: {}.".format(",".join(FILEEXT2TYPE.keys())))
    else:
        raise NotImplementedError("Unknown load type: {}.".format(dataset_attr.load_from))
    dataset = load_dataset(
        path=data_path,
        name=data_name,
        data_dir=data_dir,
        data_files=data_files,
        split=datasets.splits.Split.TRAIN,
        cache_dir=None,
        token=None,
        streaming=data_args.streaming,
        trust_remote_code=True,
    )

    if data_args.streaming and (dataset_attr.load_from == "file"):  # faster than specifying streaming=True
        dataset = dataset.to_iterable_dataset()  # TODO: add num shards parameter

    if dataset_attr.num_samples is not None and not data_args.streaming:
        target_num = dataset_attr.num_samples
        indexes = np.random.permutation(len(dataset))[:target_num]
        target_num -= len(indexes)
        if target_num > 0:
            expand_indexes = np.random.choice(len(dataset), target_num)
            indexes = np.concatenate((indexes, expand_indexes), axis=0)

        assert len(indexes) == dataset_attr.num_samples, "Sample num mismatched."
        dataset = dataset.select(indexes)
        logger.info("Sampled {} examples from dataset {}.".format(dataset_attr.num_samples, dataset_attr))

    return dataset


def merge_dataset(
        all_datasets: List[Union["Dataset", "IterableDataset"]], data_args: "DataArguments", seed: int
) -> Union["Dataset", "IterableDataset"]:
    if len(all_datasets) == 1:
        return all_datasets[0]
    elif data_args.mix_strategy == "concat":
        if data_args.streaming:
            logger.warning("The samples between different datasets will not be mixed in streaming mode.")

        return concatenate_datasets(all_datasets)
    elif data_args.mix_strategy.startswith("interleave"):
        if not data_args.streaming:
            logger.warning("We recommend using `mix_strategy=concat` in non-streaming mode.")

        return interleave_datasets(
            datasets=all_datasets,
            probabilities=data_args.interleave_probs,
            seed=seed,
            stopping_strategy="first_exhausted" if data_args.mix_strategy.endswith("under") else "all_exhausted",
        )
    else:
        raise ValueError("Unknown mixing strategy.")
