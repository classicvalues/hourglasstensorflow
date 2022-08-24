from abc import abstractmethod
from typing import Any
from typing import Set
from typing import Dict
from typing import List
from typing import Type
from typing import Tuple
from typing import Union
from typing import TypeVar
from typing import Iterable
from typing import Optional

import tensorflow as tf
from keras.losses import Loss
from keras.models import Model
from keras.metrics import Metric
from keras.optimizers import Optimizer
from keras.optimizers.schedules.learning_rate_schedule import LearningRateSchedule

from hourglass_tensorflow.handlers.meta import _HTFHandler
from hourglass_tensorflow.utils._errors import BadConfigurationError
from hourglass_tensorflow.types.config.train import HTFTrainConfig
from hourglass_tensorflow.types.config.fields import HTFObjectReference

# region Abstract Class

R = TypeVar("R")


class _HTFTrainHandler(_HTFHandler):
    def __init__(
        self,
        config: HTFTrainConfig,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(config=config, *args, **kwargs)
        self._epochs: int = None
        self._epoch_size: int = None
        self._batch_size: int = None
        self._learning_rate: Union[
            HTFObjectReference[LearningRateSchedule], float
        ] = None
        self._loss: Union[HTFObjectReference[Loss], str] = None
        self._optimizer: Union[HTFObjectReference[Optimizer], str] = None
        self._metrics: List[HTFObjectReference[Metric]] = None

    @property
    def config(self) -> HTFTrainConfig:
        return self._config

    @abstractmethod
    def compile(self, model: Model, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def fit(
        self,
        model: Model,
        train_dataset: tf.data.Dataset = None,
        test_dataset: tf.data.Dataset = None,
        validation_dataset: tf.data.Dataset = None,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError

    def run(self, *args, **kwargs) -> None:
        self.compile(*args, **kwargs)
        self.fit(*args, **kwargs)


# enregion

# region Handler


class HTFModelHandler(_HTFTrainHandler):
    def _instantiate(self, obj: HTFObjectReference[R]) -> R:
        if isinstance(obj, HTFObjectReference):
            return obj.init()
        else:
            return obj

    def init_handler(self, *args, **kwargs) -> None:
        self._epochs = self.config.epochs
        self._epoch_size = self.config.epoch_size
        self._batch_size = self.config.batch_size
        self._learning_rate = self._instantiate(self.config.learning_rate)
        self._loss = self._instantiate(self.config.loss)
        self._optimizer = self._instantiate(self.config.optimizer)
        self._metrics = [obj.init() for obj in self.config.metrics]

    def compile(self, model: Model, *args, **kwargs) -> None:
        model.compile(optimizer=self._optimizer, metrics=self._metrics, loss=self._loss)

    def fit(
        self,
        model: Model,
        train_dataset: tf.data.Dataset = None,
        test_dataset: tf.data.Dataset = None,
        validation_dataset: tf.data.Dataset = None,
        *args,
        **kwargs,
    ) -> None:

        model.fit(
            train_dataset,
        )


# endregion
