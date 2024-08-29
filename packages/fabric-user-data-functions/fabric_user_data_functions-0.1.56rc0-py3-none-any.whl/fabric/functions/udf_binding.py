# flake8: noqa: I005
import datetime
from typing import Any, Callable, Dict, List, Optional, Union, \
    Iterable
from azure.functions.decorators.core import DataType, InputBinding
import azure
from pydoc import locate
from collections import namedtuple
import json
from enum import IntEnum 
from azure.functions import HttpResponse

class UdfResponse(HttpResponse):
    pass

class UdfPropertyInput(InputBinding):
    @staticmethod
    def get_binding_name() -> str:
        return 'UdfProperty'
    
    def __init__(self,
                name: str,
                parameterName: str,
                typeName: Optional[str] = None,
                data_type: Optional[DataType] = DataType.STRING,
                **kwargs):
        super().__init__(name, data_type)


# The input converter that automatically gets registered in the function app.
class UdfPropertyConverter(azure.functions.meta.InConverter, binding='UdfProperty'):
    def try_convert_tuple(value: object) -> tuple:
        if isinstance(value, str):
            # this is the case if the tuple is passed as a string e.g., '[1,2,3]'
            value_as_json = json.loads(value)
            return tuple(value_as_json)

        return tuple(value)
    
    def try_convert_set(value: object) -> tuple:
        if isinstance(value, str):
            # this is the case if the set is passed as a string e.g., '[1,2,3]'
            value_as_json = json.loads(value)
            return set(value_as_json)

        return set(value)

    special_types = {
        "datetime": datetime.datetime.fromisoformat,
        "list": json.loads,
        "dict": json.loads,
        "set": try_convert_set,
        "tuple": try_convert_tuple
    }

    @classmethod
    def check_input_type_annotation(cls, pytype: type) -> bool:
        return True

    @classmethod
    def decode(cls, data, *,
               trigger_metadata) -> Any:
        if data is not None and data.type == 'string' and data.value is not None:
            body = json.loads(data.value)
        else:
            raise NotImplementedError(
                'unable to load data successfully for udf property')
        return tryconvert(body['PropertyType'], body['PropertyJsonValue'])


def tryconvert(property_type: str, property_json_value: str):
    if not property_json_value:  # This can happen if/when the value is empty, so we should return None
        return None
    value_as_json = json.loads(property_json_value)
    if not value_as_json:
        return None
    
    prop_type = locate(property_type)
    try:
        if prop_type.__name__ in UdfPropertyConverter.special_types:
            constructor = UdfPropertyConverter.special_types[prop_type.__name__]
            return constructor(value_as_json)
        return prop_type(value_as_json)
    except (ValueError, TypeError, json.JSONDecodeError): 
        # We can get ValueError, JSONDecodeError, and TypeError due to the special_types that have json.loads
        pass

    return value_as_json

