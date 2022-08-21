import tensorflow as tf
from keras import layers
from keras.layers import Layer

from hourglass_tensorflow.layers.skip import SkipLayer
from hourglass_tensorflow.layers.conv_block import ConvBlockLayer


class ResidualLayer(Layer):
    def __init__(
        self,
        output_filters: int,
        momentum: float = 0.9,
        epsilon: float = 1e-5,
        name: str = None,
        dtype=None,
        dynamic=False,
        trainable: bool = True,
    ) -> None:
        super().__init__(name=name, dtype=dtype, dynamic=dynamic, trainable=trainable)
        # Layers
        self.conv_block = ConvBlockLayer(
            output_filters=output_filters,
            momentum=momentum,
            epsilon=epsilon,
            name="ConvBlock",
            dtype=dtype,
            dynamic=dynamic,
            trainable=trainable,
        )
        self.skip = SkipLayer(
            output_filters=output_filters,
            name="Skip",
            dtype=dtype,
            dynamic=dynamic,
            trainable=trainable,
        )
        self.add = layers.Add(name="Add")

    def call(self, inputs: tf.Tensor, training: bool = False) -> tf.Tensor:
        return self.add(
            [
                self.conv_block(inputs, training=training),
                self.skip(inputs, training=training),
            ]
        )
