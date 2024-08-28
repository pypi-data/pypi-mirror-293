from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.rest.rest_client import RestSchema


@dataclass
class Difference:
    """ author semantha, this is a generated class do not change manually! """
    operation: str
    text: str

DifferenceSchema = class_schema(Difference, base_schema=RestSchema)
