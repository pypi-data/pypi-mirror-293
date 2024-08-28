
class ErrorCode(object):
    error_unknown = 44000
    error_dataset_format = 44001
    error_dataset_path_empty = 44002
    error_dataset_file_empty = 44003
    error_dataset_row_empty = 44004
    error_dataset_too_few = 44005
    error_dataset_no_found = 44006
    error_model_load = 44101
    error_model_name_not_support = 44102
    error_finetune_not_support = 44201
    error_machine_oom = 44301

class ErrorType(object):
    error_type_value = r'ValueError: (.+)'
    error_type_json = r'json.decoder.JSONDecodeError: (.+)'
    error_type_data_file = r'datasets.data_files.EmptyDatasetError: (.+)'
    error_type_attribute = r'AttributeError: (.+)'
    error_type_type = r'TypeError: (.+)'
    error_type_name = r'NameError: (.+)'
    error_type_syntax = r'SyntaxError: (.+)'
    error_type_file_not_found = r'FileNotFoundError: (.+)'
    error_type_import = r'ImportError: (.+)'
    error_type_io = r'IOError: (.+)'
    error_type_stop_iter = r'StopIteration: (.+)'
    error_type_oom = r'torch.cuda.OutOfMemoryError: (.+)'

class ErrorPattern(object):
    error_dataset_format_pattern_1 = r'Column to remove \[(.*?)\] not in the dataset\. Current columns in the dataset: \[(.*?)\]' 
    error_dataset_format_pattern_2 = r"unsupported operand type\(s\) for \+: '(.+?)' and '(.+?)'"
    error_dataset_format_pattern_3 = r'Column 1 named input_ids expected length (.+?) but got length (.+?)'
    error_dataset_format_check_json = r'Extra data: line (\d+) column (\d+) \(char (\d+)\)'
    error_dataset_path_empty_pattern = r'The directory at (.+?) doesn\'t contain any data files'
    error_dataset_file_empty_pattern = r'An error occurred while generating the dataset'
    error_dataset_row_empty_pattern = r'float division by zero'
    error_dataset_too_few_pattern = r'With n_samples=(.+?), test_size=(.+?) and train_size=None, the resulting train set will be empty. Adjust any of the aforementioned parameters.'
    error_dataset_too_few_pattern = r'With n_samples=(.+?), test_size=(.+?) and train_size=None, the resulting train set will be empty. Adjust any of the aforementioned parameters.'
    error_dataset_nofound_pattern = r'No such dataset'
    error_model_load_pattern_1 = r'Unrecognized configuration class (.+?) for this kind of (.+?).Model type should be one of (.+?)'
    error_model_load_pattern_2 = r'Repo id must be in the form (.+?). Use `repo_type` argument if needed.'
    error_machine_oom_pattern = r'CUDA out of memory. Tried to allocate (.+?)'
    error_finetune_not_support_pattern = r'model finetune_type (.+?) not support'
    error_model_name_not_support_pattern = r'Input model (.+?) is not yet supported'

def match_error_msg(msg:str):
    import re
    msg = str(msg)
    if re.search(ErrorPattern.error_dataset_format_pattern_1,msg):
        return ErrorCode.error_dataset_format
    elif re.search(ErrorPattern.error_dataset_format_pattern_2, msg):
        return ErrorCode.error_dataset_format
    elif re.search(ErrorPattern.error_dataset_format_pattern_3, msg):
        return ErrorCode.error_dataset_format
    elif re.search(ErrorPattern.error_dataset_format_check_json, msg):
        return ErrorCode.error_dataset_format
    elif re.search(ErrorPattern.error_dataset_path_empty_pattern, msg):
        return ErrorCode.error_dataset_path_empty
    elif re.search(ErrorPattern.error_dataset_file_empty_pattern, msg):
        return ErrorCode.error_dataset_file_empty
    elif re.search(ErrorPattern.error_dataset_row_empty_pattern, msg):
        return ErrorCode.error_dataset_row_empty
    elif re.search(ErrorPattern.error_dataset_too_few_pattern, msg):
        return ErrorCode.error_dataset_too_few
    elif re.search(ErrorPattern.error_model_load_pattern_1, msg):
        return ErrorCode.error_model_load
    elif re.search(ErrorPattern.error_model_load_pattern_2, msg):
        return ErrorCode.error_model_load
    elif re.search(ErrorPattern.error_finetune_not_support_pattern, msg):
        return ErrorCode.error_finetune_not_support
    elif re.search(ErrorPattern.error_model_name_not_support_pattern, msg):
        return ErrorCode.error_model_name_not_support
    elif re.search(ErrorPattern.error_machine_oom_pattern, msg):
        return ErrorCode.error_machine_oom
    elif re.search(ErrorPattern.error_dataset_nofound_pattern, msg):
        print(f"###{msg}")
        return ErrorCode.error_dataset_no_found
    else :
        return ErrorCode.error_unknown