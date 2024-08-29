# Copyright 2022 Ashley R. Thomas
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Support json encoding/decoding of multiple classes via use of single
instance of MultiEncoderDecoder.
"""
from typing import Callable
import json
import dataclasses


class MultiEncoderDecoder:
    """An instance of MultiEncoderDecoder can json encode/decode one or more
    classes. Call add_def() to inform this instance of each such class.
    """

    # pylint: disable=missing-class-docstring
    # pylint: disable=protected-access

    class Definition:
        def __init__(
            self,
            class_type: type,
            to_dict_method: Callable[[object], dict],
            from_dict_method: Callable[[object, object], None],
            constructor_arg_names: list[str],
        ):
            self.class_type = class_type
            self.to_dict_method = to_dict_method
            self.from_dict_method = from_dict_method
            self.constructor_arg_names = constructor_arg_names

    def __init__(self):
        self.enc_dec_defs = list()

    def add_def(
        self,
        class_type: type,
        to_dict_method: Callable[[object], dict],
        from_dict_method: Callable[[object, object], None],
        constructor_arg_names: list[str],
    ):
        """Inform this instance to include the specified class
        in its encoding/decoding efforts.
        """
        self.enc_dec_defs.append(
            MultiEncoderDecoder.Definition(
                class_type=class_type,
                to_dict_method=to_dict_method,
                from_dict_method=from_dict_method,
                constructor_arg_names=constructor_arg_names,
            )
        )

    def get_json_encoder_class(self):
        """Return a json.JSONEncoder to use is json.* calls
        accepting an encoder.
        """

        class CustomEncoder(json.JSONEncoder):
            owner = self

            def default(self, o):
                d = CustomEncoder.owner._default(o) 
                if not d:
                    return json.JSONEncoder.default(self, o)
                return d

        return CustomEncoder

    def get_json_decoder_class(self):
        """Returns a json.JSONDecoder to use in json.* calls
        accepting a decoder.
        """

        # pylint: disable=missing-class-docstring
        # pylint: disable=protected-access
        # pylint: disable=method-hidden

        class CustomDecoder(json.JSONDecoder):
            owner = self

            def __init__(self, *args, **kwargs):
                json.JSONDecoder.__init__(
                    self, object_hook=self._obj_hook_func, *args, **kwargs
                )

            def _obj_hook_func(self, obj):
                return CustomDecoder.owner._owner_obj_hook_func(
                    obj
                )

        return CustomDecoder

    def _default(self, obj):
        enc_dec_def: MultiEncoderDecoder.Definition
        for enc_dec_def in self.enc_dec_defs:
            if isinstance(obj, enc_dec_def.class_type):
                v = enc_dec_def.to_dict_method(obj)
                if isinstance(v, dict):
                    v["_type"] = enc_dec_def.class_type.__name__
                return v
        return None

    def _owner_obj_hook_func(self, obj):
        if "_type" not in obj:
            return obj
        obj_type_str = obj["_type"]
        enc_dec_def: MultiEncoderDecoder.Definition
        for enc_dec_def in self.enc_dec_defs:
            if enc_dec_def.class_type.__name__ == obj_type_str:
                args = [obj[k] for k in enc_dec_def.constructor_arg_names]
                o = enc_dec_def.class_type(*args)
                enc_dec_def.from_dict_method(o, obj)
                return o
        return obj


def create_dataclass_json_encoder(data_cls, is_strict: bool = True) -> json.JSONEncoder:
    """Create a json.JSONEncoder to handle serialization of a dataclass data_cls.
    This is useful for simple cases where a single dataclass is serialized as
    a single instance, or multiple instances in an list.

    Args:
        data_cls (dataclass): A user-defined dataclass.
        is_strict (bool, optional): If True, an a TypeError is raised if the encoder
            is asked to encode anything other than data_cls. Defaults to True.

    Raises:
        ValueError: If the specified data_cls is not a dataclass.
        TypeError: If, during encoding, the object tp encode is not an instance of data_cls.

    Returns:
        json.JSONEncoder: The encoder to encode the data_cls instances.
    """
    if not dataclasses.is_dataclass(data_cls):
        raise ValueError(f"Not a dataclass: cls={data_cls}")
    class Encoder(json.JSONEncoder): # pylint: disable=missing-class-docstring
        def default(self, o):
            if not isinstance(o, data_cls):
                if is_strict:
                    raise TypeError(
                        f"cannot identify dataclass for encoding: "
                        f"The obj ({o}) does not appear to be data_cls ({data_cls})"
                    )
                return json.JSONEncoder.default(self, o)
            obj_dict = { "_type" : data_cls.__name__}
            obj_dict.update(dataclasses.asdict(o))
            return obj_dict
    return Encoder


def create_dataclass_json_decoder(data_cls, is_strict: bool = True) -> json.JSONDecoder:
    """Create a json.JSONDecoder to handle deserialization of serialized data_cls
    instances.

    Args:
        data_cls (dataclass): A user-defined dataclass.
        is_strict (bool, optional): If True, an a TypeError is raised if the encoder
            is asked to decode anything other than data_cls. Defaults to True.

    Raises:
        ValueError: If the specified data_cls is not a dataclass.
        TypeError: If, during decoding, the object to decode is not an instance of data_cls.

    Returns:
        json.JSONDecoder: The decoder to decode the data_cls instances.
    """

    # pylint: disable=missing-class-docstring
    # pylint: disable=missing-function-docstring

    if not dataclasses.is_dataclass(data_cls):
        raise ValueError(f"Not a dataclass: cls={data_cls}")
    class Decoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.obj_hook_func, *args, **kwargs)
        def obj_hook_func(self, obj):
            if "_type" not in obj or obj["_type"] != data_cls.__name__:
                if is_strict:
                    raise TypeError(
                        f"cannot identify dataclass for deocding: "
                        f"The dict ({obj}) does not appear to be data_cls ({data_cls})"
                    )
                return obj
            args = {}
            for field in dataclasses.fields(data_cls):
                if field.name in obj:
                    args[field.name] = obj[field.name]
            return data_cls(**args)
    return Decoder
