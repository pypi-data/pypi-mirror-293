from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChatBotUiState")


@_attrs_define
class ChatBotUiState:
    """
    Attributes:
        is_open_agent_rag_view (Union[None, Unset, bool]):
        thread_id (Union[None, Unset, str]):
        is_dev (Union[None, Unset, bool]):
        is_open_rag_ui (Union[None, Unset, bool]):
    """

    is_open_agent_rag_view: Union[None, Unset, bool] = UNSET
    thread_id: Union[None, Unset, str] = UNSET
    is_dev: Union[None, Unset, bool] = UNSET
    is_open_rag_ui: Union[None, Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_open_agent_rag_view: Union[None, Unset, bool]
        if isinstance(self.is_open_agent_rag_view, Unset):
            is_open_agent_rag_view = UNSET
        else:
            is_open_agent_rag_view = self.is_open_agent_rag_view

        thread_id: Union[None, Unset, str]
        if isinstance(self.thread_id, Unset):
            thread_id = UNSET
        else:
            thread_id = self.thread_id

        is_dev: Union[None, Unset, bool]
        if isinstance(self.is_dev, Unset):
            is_dev = UNSET
        else:
            is_dev = self.is_dev

        is_open_rag_ui: Union[None, Unset, bool]
        if isinstance(self.is_open_rag_ui, Unset):
            is_open_rag_ui = UNSET
        else:
            is_open_rag_ui = self.is_open_rag_ui

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_open_agent_rag_view is not UNSET:
            field_dict["isOpenAgentRagView"] = is_open_agent_rag_view
        if thread_id is not UNSET:
            field_dict["threadId"] = thread_id
        if is_dev is not UNSET:
            field_dict["isDev"] = is_dev
        if is_open_rag_ui is not UNSET:
            field_dict["isOpenRagUi"] = is_open_rag_ui

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_is_open_agent_rag_view(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_open_agent_rag_view = _parse_is_open_agent_rag_view(d.pop("isOpenAgentRagView", UNSET))

        def _parse_thread_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thread_id = _parse_thread_id(d.pop("threadId", UNSET))

        def _parse_is_dev(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_dev = _parse_is_dev(d.pop("isDev", UNSET))

        def _parse_is_open_rag_ui(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_open_rag_ui = _parse_is_open_rag_ui(d.pop("isOpenRagUi", UNSET))

        chat_bot_ui_state = cls(
            is_open_agent_rag_view=is_open_agent_rag_view,
            thread_id=thread_id,
            is_dev=is_dev,
            is_open_rag_ui=is_open_rag_ui,
        )

        chat_bot_ui_state.additional_properties = d
        return chat_bot_ui_state

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
