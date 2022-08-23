import re
import enum
from typing import Dict
from typing import List
from typing import Union
from typing import Literal
from typing import Optional

import keras.layers
import keras.models
from pydantic import Field
from pydantic import BaseModel

from hourglass_tensorflow.types.config.fields import HTFConfigField
from hourglass_tensorflow.types.config.fields import HTFObjectReference

DATA_FORMAT = Union[
    Literal["NHWC"],
    Literal["NCHW"],
]


class HTFModelAsLayers(BaseModel):
    downsampling: keras.layers.Layer
    hourglasses: List[keras.layers.Layer]
    outputs: keras.layers.Layer
    model: keras.models.Model

    class Config:
        arbitrary_types_allowed = True


class HTFModelParams(HTFConfigField):
    name: str = "HourglassNetwork"
    input_size: int = 256
    output_size: int = 64
    stages: int = 4
    stage_filters: int = 128
    output_channels: int = 16
    downsamplings_per_stage: int = 4
    intermediate_supervision: bool = True


class HTFModelConfig(HTFConfigField):
    object: Optional[HTFObjectReference] = Field(
        default_factory=HTFObjectReference(
            source="hourglass_tensorflow.handlers.model.HTFModelHandler"
        )
    )
    build_as_model: bool = False
    data_format: DATA_FORMAT = "NHWC"
    params: Optional[HTFModelParams] = Field(default_factory=HTFModelParams)
