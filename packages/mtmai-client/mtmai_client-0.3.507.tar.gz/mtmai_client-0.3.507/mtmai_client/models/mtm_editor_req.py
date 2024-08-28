from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MtmEditorReq")


@_attrs_define
class MtmEditorReq:
    """
    Attributes:
        option (str):
        prompt (str):
        command (Union[None, Unset, str]):
    """

    option: str
    prompt: str
    command: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        option = self.option

        prompt = self.prompt

        command: Union[None, Unset, str]
        if isinstance(self.command, Unset):
            command = UNSET
        else:
            command = self.command

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "option": option,
                "prompt": prompt,
            }
        )
        if command is not UNSET:
            field_dict["command"] = command

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        option = d.pop("option")

        prompt = d.pop("prompt")

        def _parse_command(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        command = _parse_command(d.pop("command", UNSET))

        mtm_editor_req = cls(
            option=option,
            prompt=prompt,
            command=command,
        )

        mtm_editor_req.additional_properties = d
        return mtm_editor_req

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
