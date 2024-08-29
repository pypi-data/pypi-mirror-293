from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentChatConfig")


@_attrs_define
class AgentChatConfig:
    """
    Attributes:
        chat_endpoint (Union[None, Unset, str]):
    """

    chat_endpoint: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chat_endpoint: Union[None, Unset, str]
        if isinstance(self.chat_endpoint, Unset):
            chat_endpoint = UNSET
        else:
            chat_endpoint = self.chat_endpoint

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if chat_endpoint is not UNSET:
            field_dict["chat_endpoint"] = chat_endpoint

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_chat_endpoint(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        chat_endpoint = _parse_chat_endpoint(d.pop("chat_endpoint", UNSET))

        agent_chat_config = cls(
            chat_endpoint=chat_endpoint,
        )

        agent_chat_config.additional_properties = d
        return agent_chat_config

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
