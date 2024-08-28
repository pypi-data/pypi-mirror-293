import json
import csv
import os
from transformers import AutoTokenizer
from transformers import LlamaTokenizerFast
from lightmodelfactory.util.logger import logger

def load_and_process_dataset(file_path):
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            dataset = json.load(file)
    elif file_path.endswith('.jsonl'):
        dataset = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                dataset.append(json.loads(line))
    elif file_path.endswith('.csv'):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            dataset = [row for row in reader]
    else:
        logger.warning(f"Supported formats are .json, .jsonl, and .csv. {file_path}")
        return None

    return dataset

def concatenate_fields(example):
    combined_text = " ".join(str(value) for value in example.values() if isinstance(value, (str, int, float)))
    return combined_text

def calc_tokens_for_file(file_path, tokenizer):
    dataset = load_and_process_dataset(file_path)
    if dataset is None:
        return 0
    
    token_cnt = 0
    for example in dataset:
        combined_text = concatenate_fields(example)
        tokenized_output = tokenizer(combined_text)
        token_cnt += len(tokenized_output['input_ids'])
    return token_cnt

'''
dateset:sft_dataset
dataset_desc:
'{
    "sft_dataset": {
        "file_name": "/home/atpdata/yljing/resource/nlp/alpaca/alpaca_data_chinese_short_1k/alpaca_data_zh_short_1k.json"
    }
}'
'''
def calc_tokens(dateset, dataset_desc, model_path):
    logger.info(f"dateset:{dateset}, dataset_desc:{dataset_desc}")
    logger.info(f"model_path:{model_path}")
    dataset_desc_str = json.loads(dataset_desc)
    file_paths = {}
    dateset = dateset.strip()
    if ',' in dateset:
        dataset_aliases = dateset.split(",")
    else:
        dataset_aliases = [dateset]
    
    for alias in dataset_aliases:
        alias = alias.strip()
        dataset_info = dataset_desc_str.get(alias, None)
        if dataset_info:
            file_paths[alias] = dataset_info.get("file_name", None)
        else :
            logger.warning(f"Alias not found: {alias}")
    
    logger.info(f"file_paths: {file_paths}")
    if file_paths is None:
        return 0
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    except Exception as e:
        tokenizer = LlamaTokenizerFast.from_pretrained(model_path)

    total_token_cnt = 0

    for alias, file_name in file_paths.items():
        if file_name and os.path.isfile(file_name):
            token = calc_tokens_for_file(file_name, tokenizer)
            total_token_cnt += token
            logger.info(f"Calculated tokens for file '{file_name}', token: {total_token_cnt}")
        elif file_name and os.path.isdir(file_name):
            for dirpath, dirnames, filenames in os.walk(file_name):
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    token = calc_tokens_for_file(full_path, tokenizer)
                    total_token_cnt += token
            logger.info(f"Calculated tokens for path '{file_name}', token: {total_token_cnt}")
        else:
            logger.warning(f"File not found or invalid: {file_name}")
    return total_token_cnt