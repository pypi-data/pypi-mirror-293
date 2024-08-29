"""
Type annotations for iot1click-devices service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot1click_devices.client import IoT1ClickDevicesServiceClient

    session = get_session()
    async with session.create_client("iot1click-devices") as client:
        client: IoT1ClickDevicesServiceClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListDeviceEventsPaginator, ListDevicesPaginator
from .type_defs import (
    ClaimDevicesByClaimCodeResponseTypeDef,
    DescribeDeviceResponseTypeDef,
    DeviceMethodTypeDef,
    EmptyResponseMetadataTypeDef,
    FinalizeDeviceClaimResponseTypeDef,
    GetDeviceMethodsResponseTypeDef,
    InitiateDeviceClaimResponseTypeDef,
    InvokeDeviceMethodResponseTypeDef,
    ListDeviceEventsResponseTypeDef,
    ListDevicesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    TimestampTypeDef,
    UnclaimDeviceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("IoT1ClickDevicesServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    PreconditionFailedException: Type[BotocoreClientError]
    RangeNotSatisfiableException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class IoT1ClickDevicesServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoT1ClickDevicesServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#can_paginate)
        """

    async def claim_devices_by_claim_code(
        self, *, ClaimCode: str
    ) -> ClaimDevicesByClaimCodeResponseTypeDef:
        """
        Adds device(s) to your account (i.e., claim one or more devices) if and only if
        you received a claim code with the
        device(s).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.claim_devices_by_claim_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#claim_devices_by_claim_code)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#close)
        """

    async def describe_device(self, *, DeviceId: str) -> DescribeDeviceResponseTypeDef:
        """
        Given a device ID, returns a DescribeDeviceResponse object describing the
        details of the
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.describe_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#describe_device)
        """

    async def finalize_device_claim(
        self, *, DeviceId: str, Tags: Mapping[str, str] = ...
    ) -> FinalizeDeviceClaimResponseTypeDef:
        """
        Given a device ID, finalizes the claim request for the associated device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.finalize_device_claim)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#finalize_device_claim)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#generate_presigned_url)
        """

    async def get_device_methods(self, *, DeviceId: str) -> GetDeviceMethodsResponseTypeDef:
        """
        Given a device ID, returns the invokable methods associated with the device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.get_device_methods)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#get_device_methods)
        """

    async def initiate_device_claim(self, *, DeviceId: str) -> InitiateDeviceClaimResponseTypeDef:
        """
        Given a device ID, initiates a claim request for the associated device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.initiate_device_claim)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#initiate_device_claim)
        """

    async def invoke_device_method(
        self,
        *,
        DeviceId: str,
        DeviceMethod: DeviceMethodTypeDef = ...,
        DeviceMethodParameters: str = ...,
    ) -> InvokeDeviceMethodResponseTypeDef:
        """
        Given a device ID, issues a request to invoke a named device method (with
        possible
        parameters).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.invoke_device_method)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#invoke_device_method)
        """

    async def list_device_events(
        self,
        *,
        DeviceId: str,
        FromTimeStamp: TimestampTypeDef,
        ToTimeStamp: TimestampTypeDef,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListDeviceEventsResponseTypeDef:
        """
        Using a device ID, returns a DeviceEventsResponse object containing an array of
        events for the
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.list_device_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#list_device_events)
        """

    async def list_devices(
        self, *, DeviceType: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListDevicesResponseTypeDef:
        """
        Lists the 1-Click compatible devices associated with your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.list_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#list_devices)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags associated with the specified resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#list_tags_for_resource)
        """

    async def tag_resource(
        self, *, ResourceArn: str, Tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates the tags associated with the resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#tag_resource)
        """

    async def unclaim_device(self, *, DeviceId: str) -> UnclaimDeviceResponseTypeDef:
        """
        Disassociates a device from your AWS account using its device ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.unclaim_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#unclaim_device)
        """

    async def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Using tag keys, deletes the tags (key/value pairs) associated with the
        specified resource
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#untag_resource)
        """

    async def update_device_state(self, *, DeviceId: str, Enabled: bool = ...) -> Dict[str, Any]:
        """
        Using a Boolean value (true or false), this operation enables or disables the
        device given a device
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.update_device_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#update_device_state)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_events"]
    ) -> ListDeviceEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_devices"]) -> ListDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/#get_paginator)
        """

    async def __aenter__(self) -> "IoT1ClickDevicesServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/client/)
        """
