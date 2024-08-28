from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.blog_post_update_req import BlogPostUpdateReq
from ...models.blog_post_update_res import BlogPostUpdateRes
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    post_id: str,
    *,
    body: BlogPostUpdateReq,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/api/v1/posts/api/v1/{post_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[BlogPostUpdateRes, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = BlogPostUpdateRes.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BlogPostUpdateRes, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BlogPostUpdateReq,
) -> Response[Union[BlogPostUpdateRes, HTTPValidationError]]:
    """Blog Post Update

    Args:
        post_id (str):
        body (BlogPostUpdateReq):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BlogPostUpdateRes, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BlogPostUpdateReq,
) -> Optional[Union[BlogPostUpdateRes, HTTPValidationError]]:
    """Blog Post Update

    Args:
        post_id (str):
        body (BlogPostUpdateReq):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BlogPostUpdateRes, HTTPValidationError]
    """

    return sync_detailed(
        post_id=post_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BlogPostUpdateReq,
) -> Response[Union[BlogPostUpdateRes, HTTPValidationError]]:
    """Blog Post Update

    Args:
        post_id (str):
        body (BlogPostUpdateReq):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BlogPostUpdateRes, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    post_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BlogPostUpdateReq,
) -> Optional[Union[BlogPostUpdateRes, HTTPValidationError]]:
    """Blog Post Update

    Args:
        post_id (str):
        body (BlogPostUpdateReq):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BlogPostUpdateRes, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            post_id=post_id,
            client=client,
            body=body,
        )
    ).parsed
