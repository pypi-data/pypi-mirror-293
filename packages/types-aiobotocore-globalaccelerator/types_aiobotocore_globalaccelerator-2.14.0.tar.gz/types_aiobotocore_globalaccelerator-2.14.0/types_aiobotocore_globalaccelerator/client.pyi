"""
Type annotations for globalaccelerator service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_globalaccelerator.client import GlobalAcceleratorClient

    session = get_session()
    async with session.create_client("globalaccelerator") as client:
        client: GlobalAcceleratorClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ClientAffinityType, HealthCheckProtocolType, IpAddressTypeType, ProtocolType
from .paginator import (
    ListAcceleratorsPaginator,
    ListByoipCidrsPaginator,
    ListCrossAccountAttachmentsPaginator,
    ListCrossAccountResourcesPaginator,
    ListCustomRoutingAcceleratorsPaginator,
    ListCustomRoutingEndpointGroupsPaginator,
    ListCustomRoutingListenersPaginator,
    ListCustomRoutingPortMappingsByDestinationPaginator,
    ListCustomRoutingPortMappingsPaginator,
    ListEndpointGroupsPaginator,
    ListListenersPaginator,
)
from .type_defs import (
    AddCustomRoutingEndpointsResponseTypeDef,
    AddEndpointsResponseTypeDef,
    AdvertiseByoipCidrResponseTypeDef,
    CidrAuthorizationContextTypeDef,
    CreateAcceleratorResponseTypeDef,
    CreateCrossAccountAttachmentResponseTypeDef,
    CreateCustomRoutingAcceleratorResponseTypeDef,
    CreateCustomRoutingEndpointGroupResponseTypeDef,
    CreateCustomRoutingListenerResponseTypeDef,
    CreateEndpointGroupResponseTypeDef,
    CreateListenerResponseTypeDef,
    CustomRoutingDestinationConfigurationTypeDef,
    CustomRoutingEndpointConfigurationTypeDef,
    DeprovisionByoipCidrResponseTypeDef,
    DescribeAcceleratorAttributesResponseTypeDef,
    DescribeAcceleratorResponseTypeDef,
    DescribeCrossAccountAttachmentResponseTypeDef,
    DescribeCustomRoutingAcceleratorAttributesResponseTypeDef,
    DescribeCustomRoutingAcceleratorResponseTypeDef,
    DescribeCustomRoutingEndpointGroupResponseTypeDef,
    DescribeCustomRoutingListenerResponseTypeDef,
    DescribeEndpointGroupResponseTypeDef,
    DescribeListenerResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EndpointConfigurationTypeDef,
    EndpointIdentifierTypeDef,
    ListAcceleratorsResponseTypeDef,
    ListByoipCidrsResponseTypeDef,
    ListCrossAccountAttachmentsResponseTypeDef,
    ListCrossAccountResourceAccountsResponseTypeDef,
    ListCrossAccountResourcesResponseTypeDef,
    ListCustomRoutingAcceleratorsResponseTypeDef,
    ListCustomRoutingEndpointGroupsResponseTypeDef,
    ListCustomRoutingListenersResponseTypeDef,
    ListCustomRoutingPortMappingsByDestinationResponseTypeDef,
    ListCustomRoutingPortMappingsResponseTypeDef,
    ListEndpointGroupsResponseTypeDef,
    ListListenersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PortOverrideTypeDef,
    PortRangeTypeDef,
    ProvisionByoipCidrResponseTypeDef,
    ResourceTypeDef,
    TagTypeDef,
    UpdateAcceleratorAttributesResponseTypeDef,
    UpdateAcceleratorResponseTypeDef,
    UpdateCrossAccountAttachmentResponseTypeDef,
    UpdateCustomRoutingAcceleratorAttributesResponseTypeDef,
    UpdateCustomRoutingAcceleratorResponseTypeDef,
    UpdateCustomRoutingListenerResponseTypeDef,
    UpdateEndpointGroupResponseTypeDef,
    UpdateListenerResponseTypeDef,
    WithdrawByoipCidrResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("GlobalAcceleratorClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AcceleratorNotDisabledException: Type[BotocoreClientError]
    AcceleratorNotFoundException: Type[BotocoreClientError]
    AccessDeniedException: Type[BotocoreClientError]
    AssociatedEndpointGroupFoundException: Type[BotocoreClientError]
    AssociatedListenerFoundException: Type[BotocoreClientError]
    AttachmentNotFoundException: Type[BotocoreClientError]
    ByoipCidrNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    EndpointAlreadyExistsException: Type[BotocoreClientError]
    EndpointGroupAlreadyExistsException: Type[BotocoreClientError]
    EndpointGroupNotFoundException: Type[BotocoreClientError]
    EndpointNotFoundException: Type[BotocoreClientError]
    IncorrectCidrStateException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidPortRangeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ListenerNotFoundException: Type[BotocoreClientError]
    TransactionInProgressException: Type[BotocoreClientError]

class GlobalAcceleratorClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlobalAcceleratorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#exceptions)
        """

    async def add_custom_routing_endpoints(
        self,
        *,
        EndpointConfigurations: Sequence[CustomRoutingEndpointConfigurationTypeDef],
        EndpointGroupArn: str,
    ) -> AddCustomRoutingEndpointsResponseTypeDef:
        """
        Associate a virtual private cloud (VPC) subnet endpoint with your custom
        routing
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.add_custom_routing_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#add_custom_routing_endpoints)
        """

    async def add_endpoints(
        self,
        *,
        EndpointConfigurations: Sequence[EndpointConfigurationTypeDef],
        EndpointGroupArn: str,
    ) -> AddEndpointsResponseTypeDef:
        """
        Add endpoints to an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.add_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#add_endpoints)
        """

    async def advertise_byoip_cidr(self, *, Cidr: str) -> AdvertiseByoipCidrResponseTypeDef:
        """
        Advertises an IPv4 address range that is provisioned for use with your Amazon
        Web Services resources through bring your own IP addresses
        (BYOIP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.advertise_byoip_cidr)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#advertise_byoip_cidr)
        """

    async def allow_custom_routing_traffic(
        self,
        *,
        EndpointGroupArn: str,
        EndpointId: str,
        DestinationAddresses: Sequence[str] = ...,
        DestinationPorts: Sequence[int] = ...,
        AllowAllTrafficToEndpoint: bool = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the Amazon EC2 instance (destination) IP addresses and ports for a VPC
        subnet endpoint that can receive traffic for a custom routing
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.allow_custom_routing_traffic)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#allow_custom_routing_traffic)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#close)
        """

    async def create_accelerator(
        self,
        *,
        Name: str,
        IdempotencyToken: str,
        IpAddressType: IpAddressTypeType = ...,
        IpAddresses: Sequence[str] = ...,
        Enabled: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateAcceleratorResponseTypeDef:
        """
        Create an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.create_accelerator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_accelerator)
        """

    async def create_cross_account_attachment(
        self,
        *,
        Name: str,
        IdempotencyToken: str,
        Principals: Sequence[str] = ...,
        Resources: Sequence[ResourceTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateCrossAccountAttachmentResponseTypeDef:
        """
        Create a cross-account attachment in Global Accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.create_cross_account_attachment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_cross_account_attachment)
        """

    async def create_custom_routing_accelerator(
        self,
        *,
        Name: str,
        IdempotencyToken: str,
        IpAddressType: IpAddressTypeType = ...,
        IpAddresses: Sequence[str] = ...,
        Enabled: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateCustomRoutingAcceleratorResponseTypeDef:
        """
        Create a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.create_custom_routing_accelerator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_custom_routing_accelerator)
        """

    async def create_custom_routing_endpoint_group(
        self,
        *,
        ListenerArn: str,
        EndpointGroupRegion: str,
        DestinationConfigurations: Sequence[CustomRoutingDestinationConfigurationTypeDef],
        IdempotencyToken: str,
    ) -> CreateCustomRoutingEndpointGroupResponseTypeDef:
        """
        Create an endpoint group for the specified listener for a custom routing
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.create_custom_routing_endpoint_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_custom_routing_endpoint_group)
        """

    async def create_custom_routing_listener(
        self, *, AcceleratorArn: str, PortRanges: Sequence[PortRangeTypeDef], IdempotencyToken: str
    ) -> CreateCustomRoutingListenerResponseTypeDef:
        """
        Create a listener to process inbound connections from clients to a custom
        routing
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.create_custom_routing_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_custom_routing_listener)
        """

    async def create_endpoint_group(
        self,
        *,
        ListenerArn: str,
        EndpointGroupRegion: str,
        IdempotencyToken: str,
        EndpointConfigurations: Sequence[EndpointConfigurationTypeDef] = ...,
        TrafficDialPercentage: float = ...,
        HealthCheckPort: int = ...,
        HealthCheckProtocol: HealthCheckProtocolType = ...,
        HealthCheckPath: str = ...,
        HealthCheckIntervalSeconds: int = ...,
        ThresholdCount: int = ...,
        PortOverrides: Sequence[PortOverrideTypeDef] = ...,
    ) -> CreateEndpointGroupResponseTypeDef:
        """
        Create an endpoint group for the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.create_endpoint_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_endpoint_group)
        """

    async def create_listener(
        self,
        *,
        AcceleratorArn: str,
        PortRanges: Sequence[PortRangeTypeDef],
        Protocol: ProtocolType,
        IdempotencyToken: str,
        ClientAffinity: ClientAffinityType = ...,
    ) -> CreateListenerResponseTypeDef:
        """
        Create a listener to process inbound connections from clients to an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.create_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_listener)
        """

    async def delete_accelerator(self, *, AcceleratorArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Delete an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.delete_accelerator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_accelerator)
        """

    async def delete_cross_account_attachment(
        self, *, AttachmentArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a cross-account attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.delete_cross_account_attachment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_cross_account_attachment)
        """

    async def delete_custom_routing_accelerator(
        self, *, AcceleratorArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.delete_custom_routing_accelerator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_custom_routing_accelerator)
        """

    async def delete_custom_routing_endpoint_group(
        self, *, EndpointGroupArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an endpoint group from a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.delete_custom_routing_endpoint_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_custom_routing_endpoint_group)
        """

    async def delete_custom_routing_listener(
        self, *, ListenerArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.delete_custom_routing_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_custom_routing_listener)
        """

    async def delete_endpoint_group(self, *, EndpointGroupArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Delete an endpoint group from a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.delete_endpoint_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_endpoint_group)
        """

    async def delete_listener(self, *, ListenerArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Delete a listener from an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.delete_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_listener)
        """

    async def deny_custom_routing_traffic(
        self,
        *,
        EndpointGroupArn: str,
        EndpointId: str,
        DestinationAddresses: Sequence[str] = ...,
        DestinationPorts: Sequence[int] = ...,
        DenyAllTrafficToEndpoint: bool = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the Amazon EC2 instance (destination) IP addresses and ports for a VPC
        subnet endpoint that cannot receive traffic for a custom routing
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.deny_custom_routing_traffic)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#deny_custom_routing_traffic)
        """

    async def deprovision_byoip_cidr(self, *, Cidr: str) -> DeprovisionByoipCidrResponseTypeDef:
        """
        Releases the specified address range that you provisioned to use with your
        Amazon Web Services resources through bring your own IP addresses (BYOIP) and
        deletes the corresponding address
        pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.deprovision_byoip_cidr)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#deprovision_byoip_cidr)
        """

    async def describe_accelerator(
        self, *, AcceleratorArn: str
    ) -> DescribeAcceleratorResponseTypeDef:
        """
        Describe an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.describe_accelerator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_accelerator)
        """

    async def describe_accelerator_attributes(
        self, *, AcceleratorArn: str
    ) -> DescribeAcceleratorAttributesResponseTypeDef:
        """
        Describe the attributes of an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.describe_accelerator_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_accelerator_attributes)
        """

    async def describe_cross_account_attachment(
        self, *, AttachmentArn: str
    ) -> DescribeCrossAccountAttachmentResponseTypeDef:
        """
        Gets configuration information about a cross-account attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.describe_cross_account_attachment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_cross_account_attachment)
        """

    async def describe_custom_routing_accelerator(
        self, *, AcceleratorArn: str
    ) -> DescribeCustomRoutingAcceleratorResponseTypeDef:
        """
        Describe a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.describe_custom_routing_accelerator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_custom_routing_accelerator)
        """

    async def describe_custom_routing_accelerator_attributes(
        self, *, AcceleratorArn: str
    ) -> DescribeCustomRoutingAcceleratorAttributesResponseTypeDef:
        """
        Describe the attributes of a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.describe_custom_routing_accelerator_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_custom_routing_accelerator_attributes)
        """

    async def describe_custom_routing_endpoint_group(
        self, *, EndpointGroupArn: str
    ) -> DescribeCustomRoutingEndpointGroupResponseTypeDef:
        """
        Describe an endpoint group for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.describe_custom_routing_endpoint_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_custom_routing_endpoint_group)
        """

    async def describe_custom_routing_listener(
        self, *, ListenerArn: str
    ) -> DescribeCustomRoutingListenerResponseTypeDef:
        """
        The description of a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.describe_custom_routing_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_custom_routing_listener)
        """

    async def describe_endpoint_group(
        self, *, EndpointGroupArn: str
    ) -> DescribeEndpointGroupResponseTypeDef:
        """
        Describe an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.describe_endpoint_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_endpoint_group)
        """

    async def describe_listener(self, *, ListenerArn: str) -> DescribeListenerResponseTypeDef:
        """
        Describe a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.describe_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_listener)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#generate_presigned_url)
        """

    async def list_accelerators(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAcceleratorsResponseTypeDef:
        """
        List the accelerators for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_accelerators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_accelerators)
        """

    async def list_byoip_cidrs(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListByoipCidrsResponseTypeDef:
        """
        Lists the IP address ranges that were specified in calls to
        [ProvisionByoipCidr](https://docs.aws.amazon.com/global-accelerator/latest/api/ProvisionByoipCidr.html),
        including the current state and a history of state
        changes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_byoip_cidrs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_byoip_cidrs)
        """

    async def list_cross_account_attachments(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListCrossAccountAttachmentsResponseTypeDef:
        """
        List the cross-account attachments that have been created in Global Accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_cross_account_attachments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_cross_account_attachments)
        """

    async def list_cross_account_resource_accounts(
        self,
    ) -> ListCrossAccountResourceAccountsResponseTypeDef:
        """
        List the accounts that have cross-account resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_cross_account_resource_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_cross_account_resource_accounts)
        """

    async def list_cross_account_resources(
        self,
        *,
        ResourceOwnerAwsAccountId: str,
        AcceleratorArn: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListCrossAccountResourcesResponseTypeDef:
        """
        List the cross-account resources available to work with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_cross_account_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_cross_account_resources)
        """

    async def list_custom_routing_accelerators(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListCustomRoutingAcceleratorsResponseTypeDef:
        """
        List the custom routing accelerators for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_custom_routing_accelerators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_accelerators)
        """

    async def list_custom_routing_endpoint_groups(
        self, *, ListenerArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListCustomRoutingEndpointGroupsResponseTypeDef:
        """
        List the endpoint groups that are associated with a listener for a custom
        routing
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_custom_routing_endpoint_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_endpoint_groups)
        """

    async def list_custom_routing_listeners(
        self, *, AcceleratorArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListCustomRoutingListenersResponseTypeDef:
        """
        List the listeners for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_custom_routing_listeners)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_listeners)
        """

    async def list_custom_routing_port_mappings(
        self,
        *,
        AcceleratorArn: str,
        EndpointGroupArn: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListCustomRoutingPortMappingsResponseTypeDef:
        """
        Provides a complete mapping from the public accelerator IP address and port to
        destination EC2 instance IP addresses and ports in the virtual public cloud
        (VPC) subnet endpoint for a custom routing
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_custom_routing_port_mappings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_port_mappings)
        """

    async def list_custom_routing_port_mappings_by_destination(
        self,
        *,
        EndpointId: str,
        DestinationAddress: str,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListCustomRoutingPortMappingsByDestinationResponseTypeDef:
        """
        List the port mappings for a specific EC2 instance (destination) in a VPC
        subnet
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_custom_routing_port_mappings_by_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_port_mappings_by_destination)
        """

    async def list_endpoint_groups(
        self, *, ListenerArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListEndpointGroupsResponseTypeDef:
        """
        List the endpoint groups that are associated with a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_endpoint_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_endpoint_groups)
        """

    async def list_listeners(
        self, *, AcceleratorArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListListenersResponseTypeDef:
        """
        List the listeners for an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_listeners)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_listeners)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags for an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_tags_for_resource)
        """

    async def provision_byoip_cidr(
        self, *, Cidr: str, CidrAuthorizationContext: CidrAuthorizationContextTypeDef
    ) -> ProvisionByoipCidrResponseTypeDef:
        """
        Provisions an IP address range to use with your Amazon Web Services resources
        through bring your own IP addresses (BYOIP) and creates a corresponding address
        pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.provision_byoip_cidr)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#provision_byoip_cidr)
        """

    async def remove_custom_routing_endpoints(
        self, *, EndpointIds: Sequence[str], EndpointGroupArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove endpoints from a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.remove_custom_routing_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#remove_custom_routing_endpoints)
        """

    async def remove_endpoints(
        self, *, EndpointIdentifiers: Sequence[EndpointIdentifierTypeDef], EndpointGroupArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove endpoints from an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.remove_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#remove_endpoints)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Add tags to an accelerator resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove tags from a Global Accelerator resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#untag_resource)
        """

    async def update_accelerator(
        self,
        *,
        AcceleratorArn: str,
        Name: str = ...,
        IpAddressType: IpAddressTypeType = ...,
        IpAddresses: Sequence[str] = ...,
        Enabled: bool = ...,
    ) -> UpdateAcceleratorResponseTypeDef:
        """
        Update an accelerator to make changes, such as the following: * Change the name
        of the
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.update_accelerator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_accelerator)
        """

    async def update_accelerator_attributes(
        self,
        *,
        AcceleratorArn: str,
        FlowLogsEnabled: bool = ...,
        FlowLogsS3Bucket: str = ...,
        FlowLogsS3Prefix: str = ...,
    ) -> UpdateAcceleratorAttributesResponseTypeDef:
        """
        Update the attributes for an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.update_accelerator_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_accelerator_attributes)
        """

    async def update_cross_account_attachment(
        self,
        *,
        AttachmentArn: str,
        Name: str = ...,
        AddPrincipals: Sequence[str] = ...,
        RemovePrincipals: Sequence[str] = ...,
        AddResources: Sequence[ResourceTypeDef] = ...,
        RemoveResources: Sequence[ResourceTypeDef] = ...,
    ) -> UpdateCrossAccountAttachmentResponseTypeDef:
        """
        Update a cross-account attachment to add or remove principals or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.update_cross_account_attachment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_cross_account_attachment)
        """

    async def update_custom_routing_accelerator(
        self,
        *,
        AcceleratorArn: str,
        Name: str = ...,
        IpAddressType: IpAddressTypeType = ...,
        IpAddresses: Sequence[str] = ...,
        Enabled: bool = ...,
    ) -> UpdateCustomRoutingAcceleratorResponseTypeDef:
        """
        Update a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.update_custom_routing_accelerator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_custom_routing_accelerator)
        """

    async def update_custom_routing_accelerator_attributes(
        self,
        *,
        AcceleratorArn: str,
        FlowLogsEnabled: bool = ...,
        FlowLogsS3Bucket: str = ...,
        FlowLogsS3Prefix: str = ...,
    ) -> UpdateCustomRoutingAcceleratorAttributesResponseTypeDef:
        """
        Update the attributes for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.update_custom_routing_accelerator_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_custom_routing_accelerator_attributes)
        """

    async def update_custom_routing_listener(
        self, *, ListenerArn: str, PortRanges: Sequence[PortRangeTypeDef]
    ) -> UpdateCustomRoutingListenerResponseTypeDef:
        """
        Update a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.update_custom_routing_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_custom_routing_listener)
        """

    async def update_endpoint_group(
        self,
        *,
        EndpointGroupArn: str,
        EndpointConfigurations: Sequence[EndpointConfigurationTypeDef] = ...,
        TrafficDialPercentage: float = ...,
        HealthCheckPort: int = ...,
        HealthCheckProtocol: HealthCheckProtocolType = ...,
        HealthCheckPath: str = ...,
        HealthCheckIntervalSeconds: int = ...,
        ThresholdCount: int = ...,
        PortOverrides: Sequence[PortOverrideTypeDef] = ...,
    ) -> UpdateEndpointGroupResponseTypeDef:
        """
        Update an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.update_endpoint_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_endpoint_group)
        """

    async def update_listener(
        self,
        *,
        ListenerArn: str,
        PortRanges: Sequence[PortRangeTypeDef] = ...,
        Protocol: ProtocolType = ...,
        ClientAffinity: ClientAffinityType = ...,
    ) -> UpdateListenerResponseTypeDef:
        """
        Update a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.update_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_listener)
        """

    async def withdraw_byoip_cidr(self, *, Cidr: str) -> WithdrawByoipCidrResponseTypeDef:
        """
        Stops advertising an address range that is provisioned as an address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.withdraw_byoip_cidr)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#withdraw_byoip_cidr)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_accelerators"]
    ) -> ListAcceleratorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_byoip_cidrs"]) -> ListByoipCidrsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cross_account_attachments"]
    ) -> ListCrossAccountAttachmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cross_account_resources"]
    ) -> ListCrossAccountResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_accelerators"]
    ) -> ListCustomRoutingAcceleratorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_endpoint_groups"]
    ) -> ListCustomRoutingEndpointGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_listeners"]
    ) -> ListCustomRoutingListenersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_port_mappings"]
    ) -> ListCustomRoutingPortMappingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_routing_port_mappings_by_destination"]
    ) -> ListCustomRoutingPortMappingsByDestinationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_endpoint_groups"]
    ) -> ListEndpointGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_listeners"]) -> ListListenersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    async def __aenter__(self) -> "GlobalAcceleratorClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/)
        """
