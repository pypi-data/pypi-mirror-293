from abc import ABC, abstractclassmethod
from typing import Callable
from lightmodelfactory.util.param import PluginArguments, DataArguments, FinetuningArguments, ModelArguments, \
    TrainingArguments
from lightmodelfactory.util.logger import logger


class PLUGIN(ABC):
    def __init__(self) -> None:
        self.plugin_args: PluginArguments = None
        self.data_args: DataArguments = None
        self.finetune_args: FinetuningArguments = None
        self.model_args: ModelArguments = None
        self.train_args: TrainingArguments = None
        self.metrics_server = None
        pass

    @classmethod
    def build_plugin(cls, plugin_args: PluginArguments,
                     data_args: DataArguments,
                     finetune_args: FinetuningArguments,
                     model_args: ModelArguments,
                     train_args: TrainingArguments):
        from lightmodelfactory.plugins.plugin_build import PluginRg
        cls = PluginRg.get_cls(plugin_args.plugin_name)
        logger.info(f"Finding {plugin_args.plugin_name} cls: {cls}")
        plugin: PLUGIN = cls()
        if plugin is None:
            raise TypeError(f'auto_model is None')
        plugin.plugin_args, plugin.data_args, plugin.finetune_args, plugin.model_args, plugin.train_args = plugin_args, data_args, finetune_args, model_args, train_args
        return plugin

    @abstractclassmethod
    def preprocess(self):
        pass

    @abstractclassmethod
    def get_token(self):
        pass

    @abstractclassmethod
    def get_error(self):
        pass

    @abstractclassmethod
    def start_train(self, train_progress: Callable):
        pass

    @abstractclassmethod
    def stop_train(self):
        pass

    @abstractclassmethod
    def train_postprocess(self):
        pass

    def register_metrics_server(self, metrics_server):
        self.metrics_server = metrics_server
