# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import (
    object_list_params,
    object_batch_params,
    object_create_params,
    object_update_params,
    object_delete_all_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.object_get_response import ObjectGetResponse
from ..types.object_list_response import ObjectListResponse
from ..types.object_batch_response import ObjectBatchResponse
from ..types.object_create_response import ObjectCreateResponse
from ..types.object_delete_response import ObjectDeleteResponse
from ..types.object_status_response import ObjectStatusResponse
from ..types.object_update_response import ObjectUpdateResponse
from ..types.object_delete_all_response import ObjectDeleteAllResponse

__all__ = ["ObjectsResource", "AsyncObjectsResource"]


class ObjectsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ObjectsResourceWithRawResponse:
        return ObjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ObjectsResourceWithStreamingResponse:
        return ObjectsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectCreateResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/objects",
            body=maybe_transform(body, object_create_params.ObjectCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectCreateResponse,
        )

    def update(
        self,
        object_id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectUpdateResponse:
        """
        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return self._put(
            f"/objects/{object_id}",
            body=maybe_transform(body, object_update_params.ObjectUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectUpdateResponse,
        )

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        include_metadata: bool | NotGiven = NOT_GIVEN,
        include_object: bool | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectListResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/objects",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "include_metadata": include_metadata,
                        "include_object": include_object,
                        "limit": limit,
                    },
                    object_list_params.ObjectListParams,
                ),
            ),
            cast_to=ObjectListResponse,
        )

    def delete(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteResponse:
        """
        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return self._delete(
            f"/objects/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteResponse,
        )

    def batch(
        self,
        *,
        operations: Iterable[object_batch_params.Operation],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectBatchResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/objects:batch",
            body=maybe_transform({"operations": operations}, object_batch_params.ObjectBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectBatchResponse,
        )

    def delete_all(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteAllResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/objects:deleteAll",
            body=maybe_transform(body, object_delete_all_params.ObjectDeleteAllParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteAllResponse,
        )

    def get(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectGetResponse:
        """
        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return self._get(
            f"/objects/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectGetResponse,
        )

    def status(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectStatusResponse:
        """
        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return self._get(
            f"/objects/{object_id}/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectStatusResponse,
        )


class AsyncObjectsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncObjectsResourceWithRawResponse:
        return AsyncObjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncObjectsResourceWithStreamingResponse:
        return AsyncObjectsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectCreateResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/objects",
            body=await async_maybe_transform(body, object_create_params.ObjectCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectCreateResponse,
        )

    async def update(
        self,
        object_id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectUpdateResponse:
        """
        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return await self._put(
            f"/objects/{object_id}",
            body=await async_maybe_transform(body, object_update_params.ObjectUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectUpdateResponse,
        )

    async def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        include_metadata: bool | NotGiven = NOT_GIVEN,
        include_object: bool | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectListResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/objects",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "include_metadata": include_metadata,
                        "include_object": include_object,
                        "limit": limit,
                    },
                    object_list_params.ObjectListParams,
                ),
            ),
            cast_to=ObjectListResponse,
        )

    async def delete(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteResponse:
        """
        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return await self._delete(
            f"/objects/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteResponse,
        )

    async def batch(
        self,
        *,
        operations: Iterable[object_batch_params.Operation],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectBatchResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/objects:batch",
            body=await async_maybe_transform({"operations": operations}, object_batch_params.ObjectBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectBatchResponse,
        )

    async def delete_all(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteAllResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/objects:deleteAll",
            body=await async_maybe_transform(body, object_delete_all_params.ObjectDeleteAllParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteAllResponse,
        )

    async def get(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectGetResponse:
        """
        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return await self._get(
            f"/objects/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectGetResponse,
        )

    async def status(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectStatusResponse:
        """
        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return await self._get(
            f"/objects/{object_id}/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectStatusResponse,
        )


class ObjectsResourceWithRawResponse:
    def __init__(self, objects: ObjectsResource) -> None:
        self._objects = objects

        self.create = to_raw_response_wrapper(
            objects.create,
        )
        self.update = to_raw_response_wrapper(
            objects.update,
        )
        self.list = to_raw_response_wrapper(
            objects.list,
        )
        self.delete = to_raw_response_wrapper(
            objects.delete,
        )
        self.batch = to_raw_response_wrapper(
            objects.batch,
        )
        self.delete_all = to_raw_response_wrapper(
            objects.delete_all,
        )
        self.get = to_raw_response_wrapper(
            objects.get,
        )
        self.status = to_raw_response_wrapper(
            objects.status,
        )


class AsyncObjectsResourceWithRawResponse:
    def __init__(self, objects: AsyncObjectsResource) -> None:
        self._objects = objects

        self.create = async_to_raw_response_wrapper(
            objects.create,
        )
        self.update = async_to_raw_response_wrapper(
            objects.update,
        )
        self.list = async_to_raw_response_wrapper(
            objects.list,
        )
        self.delete = async_to_raw_response_wrapper(
            objects.delete,
        )
        self.batch = async_to_raw_response_wrapper(
            objects.batch,
        )
        self.delete_all = async_to_raw_response_wrapper(
            objects.delete_all,
        )
        self.get = async_to_raw_response_wrapper(
            objects.get,
        )
        self.status = async_to_raw_response_wrapper(
            objects.status,
        )


class ObjectsResourceWithStreamingResponse:
    def __init__(self, objects: ObjectsResource) -> None:
        self._objects = objects

        self.create = to_streamed_response_wrapper(
            objects.create,
        )
        self.update = to_streamed_response_wrapper(
            objects.update,
        )
        self.list = to_streamed_response_wrapper(
            objects.list,
        )
        self.delete = to_streamed_response_wrapper(
            objects.delete,
        )
        self.batch = to_streamed_response_wrapper(
            objects.batch,
        )
        self.delete_all = to_streamed_response_wrapper(
            objects.delete_all,
        )
        self.get = to_streamed_response_wrapper(
            objects.get,
        )
        self.status = to_streamed_response_wrapper(
            objects.status,
        )


class AsyncObjectsResourceWithStreamingResponse:
    def __init__(self, objects: AsyncObjectsResource) -> None:
        self._objects = objects

        self.create = async_to_streamed_response_wrapper(
            objects.create,
        )
        self.update = async_to_streamed_response_wrapper(
            objects.update,
        )
        self.list = async_to_streamed_response_wrapper(
            objects.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            objects.delete,
        )
        self.batch = async_to_streamed_response_wrapper(
            objects.batch,
        )
        self.delete_all = async_to_streamed_response_wrapper(
            objects.delete_all,
        )
        self.get = async_to_streamed_response_wrapper(
            objects.get,
        )
        self.status = async_to_streamed_response_wrapper(
            objects.status,
        )
