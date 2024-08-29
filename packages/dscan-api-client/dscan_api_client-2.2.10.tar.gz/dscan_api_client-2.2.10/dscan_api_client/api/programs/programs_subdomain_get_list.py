from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.subdomain import Subdomain
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: int,
    *,
    only_online: Union[Unset, bool] = UNSET,
    only_primary: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["only_online"] = only_online

    params["only_primary"] = only_primary

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/programs/{id}/subdomain/get/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["Subdomain"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Subdomain.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["Subdomain"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    only_online: Union[Unset, bool] = UNSET,
    only_primary: Union[Unset, bool] = UNSET,
) -> Response[List["Subdomain"]]:
    """
    Args:
        id (int):
        only_online (Union[Unset, bool]):
        only_primary (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['Subdomain']]
    """

    kwargs = _get_kwargs(
        id=id,
        only_online=only_online,
        only_primary=only_primary,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient,
    only_online: Union[Unset, bool] = UNSET,
    only_primary: Union[Unset, bool] = UNSET,
) -> Optional[List["Subdomain"]]:
    """
    Args:
        id (int):
        only_online (Union[Unset, bool]):
        only_primary (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['Subdomain']
    """

    return sync_detailed(
        id=id,
        client=client,
        only_online=only_online,
        only_primary=only_primary,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    only_online: Union[Unset, bool] = UNSET,
    only_primary: Union[Unset, bool] = UNSET,
) -> Response[List["Subdomain"]]:
    """
    Args:
        id (int):
        only_online (Union[Unset, bool]):
        only_primary (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['Subdomain']]
    """

    kwargs = _get_kwargs(
        id=id,
        only_online=only_online,
        only_primary=only_primary,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient,
    only_online: Union[Unset, bool] = UNSET,
    only_primary: Union[Unset, bool] = UNSET,
) -> Optional[List["Subdomain"]]:
    """
    Args:
        id (int):
        only_online (Union[Unset, bool]):
        only_primary (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['Subdomain']
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            only_online=only_online,
            only_primary=only_primary,
        )
    ).parsed
