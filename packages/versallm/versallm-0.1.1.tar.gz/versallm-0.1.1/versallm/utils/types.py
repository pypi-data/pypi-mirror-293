from typing import Union, TypedDict, Literal


# Define the structure of the dictionary option using TypedDict
class Function(TypedDict):
    type: Literal["function"]
    function: dict[str, str]


# Define tool_choice type using Union
ToolChoiceType = Union[
    Literal['auto', 'none', 'required'],
    Function
]