import keras
import tensorflow as tf

import mlable.ops

# GENERIC #####################################################################

@keras.saving.register_keras_serializable(package='layers')
class Reshape(tf.keras.layers.Layer):
    def __init__(
        self,
        target_shape: tuple,
        **kwargs
    ) -> None:
        super(Reshape, self).__init__(**kwargs)
        self._config = {'target_shape': target_shape}

    def call(self, inputs: tf.Tensor, **kwargs) -> tf.Tensor:
        return tf.reshape(inputs, self._config['target_shape'])

    def get_config(self) -> dict:
        __config = super(Reshape, self).get_config()
        __config.update(self._config)
        return __config

    @classmethod
    def from_config(cls, config) -> tf.keras.layers.Layer:
        return cls(**config)

# DIVIDE ######################################################################

@keras.saving.register_keras_serializable(package='layers')
class Divide(tf.keras.layers.Layer):
    def __init__(
        self,
        input_axis: int, # relative to the NEW shape / rank
        output_axis: int, # same
        factor: int,
        insert: bool=False,
        **kwargs
    ) -> None:
        super(Divide, self).__init__(**kwargs)
        self._config = {
            'input_axis': input_axis,
            'output_axis': output_axis,
            'factor': factor,
            'insert': insert,}

    def call(self, inputs: tf.Tensor) -> tf.Tensor:
        # move data from axis 0 to axis 1
        return mlable.ops.divide(data=inputs, **self._config)

    def get_config(self) -> dict:
        __config = super(Divide, self).get_config()
        __config.update(self._config)
        return __config

    @classmethod
    def from_config(cls, config) -> tf.keras.layers.Layer:
        return cls(**config)

# MERGE #######################################################################

@keras.saving.register_keras_serializable(package='layers')
class Merge(tf.keras.layers.Layer):
    def __init__(
        self,
        left_axis: int=-2,
        right_axis: int=-1,
        left: bool=True,
        **kwargs
    ) -> None:
        super(Merge, self).__init__(**kwargs)
        self._config = {
            'left_axis': left_axis,
            'right_axis': right_axis,
            'left': left,}

    def call(self, inputs: tf.Tensor) -> tf.Tensor:
        # merge the two axes
        return mlable.ops.merge(data=inputs, **self._config)

    def get_config(self) -> dict:
        __config = super(Merge, self).get_config()
        __config.update(self._config)
        return __config

    @classmethod
    def from_config(cls, config) -> tf.keras.layers.Layer:
        return cls(**config)
