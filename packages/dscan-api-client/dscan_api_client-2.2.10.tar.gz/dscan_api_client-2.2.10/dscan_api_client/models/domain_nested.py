from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DomainNested")


@_attrs_define
class DomainNested:
    """
    Attributes:
        id (int):
        name (str):
        is_blocked (Union[None, Unset, bool]):
        enabled (Union[Unset, bool]):
    """

    id: int
    name: str
    is_blocked: Union[None, Unset, bool] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        is_blocked: Union[None, Unset, bool]
        if isinstance(self.is_blocked, Unset):
            is_blocked = UNSET
        else:
            is_blocked = self.is_blocked

        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if is_blocked is not UNSET:
            field_dict["is_blocked"] = is_blocked
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        def _parse_is_blocked(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_blocked = _parse_is_blocked(d.pop("is_blocked", UNSET))

        enabled = d.pop("enabled", UNSET)

        domain_nested = cls(
            id=id,
            name=name,
            is_blocked=is_blocked,
            enabled=enabled,
        )

        domain_nested.additional_properties = d
        return domain_nested

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
