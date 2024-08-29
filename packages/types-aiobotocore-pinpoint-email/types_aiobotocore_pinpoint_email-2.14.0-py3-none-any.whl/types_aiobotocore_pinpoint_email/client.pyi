"""
Type annotations for pinpoint-email service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pinpoint_email.client import PinpointEmailClient

    session = get_session()
    async with session.create_client("pinpoint-email") as client:
        client: PinpointEmailClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import BehaviorOnMxFailureType, TlsPolicyType
from .paginator import (
    GetDedicatedIpsPaginator,
    ListConfigurationSetsPaginator,
    ListDedicatedIpPoolsPaginator,
    ListDeliverabilityTestReportsPaginator,
    ListEmailIdentitiesPaginator,
)
from .type_defs import (
    CreateDeliverabilityTestReportResponseTypeDef,
    CreateEmailIdentityResponseTypeDef,
    DeliveryOptionsTypeDef,
    DestinationTypeDef,
    DomainDeliverabilityTrackingOptionUnionTypeDef,
    EmailContentTypeDef,
    EventDestinationDefinitionTypeDef,
    GetAccountResponseTypeDef,
    GetBlacklistReportsResponseTypeDef,
    GetConfigurationSetEventDestinationsResponseTypeDef,
    GetConfigurationSetResponseTypeDef,
    GetDedicatedIpResponseTypeDef,
    GetDedicatedIpsResponseTypeDef,
    GetDeliverabilityDashboardOptionsResponseTypeDef,
    GetDeliverabilityTestReportResponseTypeDef,
    GetDomainDeliverabilityCampaignResponseTypeDef,
    GetDomainStatisticsReportResponseTypeDef,
    GetEmailIdentityResponseTypeDef,
    ListConfigurationSetsResponseTypeDef,
    ListDedicatedIpPoolsResponseTypeDef,
    ListDeliverabilityTestReportsResponseTypeDef,
    ListDomainDeliverabilityCampaignsResponseTypeDef,
    ListEmailIdentitiesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MessageTagTypeDef,
    ReputationOptionsUnionTypeDef,
    SendEmailResponseTypeDef,
    SendingOptionsTypeDef,
    TagTypeDef,
    TimestampTypeDef,
    TrackingOptionsTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("PinpointEmailClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccountSuspendedException: Type[BotocoreClientError]
    AlreadyExistsException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MailFromDomainNotVerifiedException: Type[BotocoreClientError]
    MessageRejected: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    SendingPausedException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class PinpointEmailClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PinpointEmailClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#close)
        """

    async def create_configuration_set(
        self,
        *,
        ConfigurationSetName: str,
        TrackingOptions: TrackingOptionsTypeDef = ...,
        DeliveryOptions: DeliveryOptionsTypeDef = ...,
        ReputationOptions: ReputationOptionsUnionTypeDef = ...,
        SendingOptions: SendingOptionsTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Create a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.create_configuration_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#create_configuration_set)
        """

    async def create_configuration_set_event_destination(
        self,
        *,
        ConfigurationSetName: str,
        EventDestinationName: str,
        EventDestination: EventDestinationDefinitionTypeDef,
    ) -> Dict[str, Any]:
        """
        Create an event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.create_configuration_set_event_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#create_configuration_set_event_destination)
        """

    async def create_dedicated_ip_pool(
        self, *, PoolName: str, Tags: Sequence[TagTypeDef] = ...
    ) -> Dict[str, Any]:
        """
        Create a new pool of dedicated IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.create_dedicated_ip_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#create_dedicated_ip_pool)
        """

    async def create_deliverability_test_report(
        self,
        *,
        FromEmailAddress: str,
        Content: EmailContentTypeDef,
        ReportName: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateDeliverabilityTestReportResponseTypeDef:
        """
        Create a new predictive inbox placement test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.create_deliverability_test_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#create_deliverability_test_report)
        """

    async def create_email_identity(
        self, *, EmailIdentity: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateEmailIdentityResponseTypeDef:
        """
        Verifies an email identity for use with Amazon Pinpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.create_email_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#create_email_identity)
        """

    async def delete_configuration_set(self, *, ConfigurationSetName: str) -> Dict[str, Any]:
        """
        Delete an existing configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.delete_configuration_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#delete_configuration_set)
        """

    async def delete_configuration_set_event_destination(
        self, *, ConfigurationSetName: str, EventDestinationName: str
    ) -> Dict[str, Any]:
        """
        Delete an event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.delete_configuration_set_event_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#delete_configuration_set_event_destination)
        """

    async def delete_dedicated_ip_pool(self, *, PoolName: str) -> Dict[str, Any]:
        """
        Delete a dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.delete_dedicated_ip_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#delete_dedicated_ip_pool)
        """

    async def delete_email_identity(self, *, EmailIdentity: str) -> Dict[str, Any]:
        """
        Deletes an email identity that you previously verified for use with Amazon
        Pinpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.delete_email_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#delete_email_identity)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#generate_presigned_url)
        """

    async def get_account(self) -> GetAccountResponseTypeDef:
        """
        Obtain information about the email-sending status and capabilities of your
        Amazon Pinpoint account in the current AWS
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_account)
        """

    async def get_blacklist_reports(
        self, *, BlacklistItemNames: Sequence[str]
    ) -> GetBlacklistReportsResponseTypeDef:
        """
        Retrieve a list of the blacklists that your dedicated IP addresses appear on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_blacklist_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_blacklist_reports)
        """

    async def get_configuration_set(
        self, *, ConfigurationSetName: str
    ) -> GetConfigurationSetResponseTypeDef:
        """
        Get information about an existing configuration set, including the dedicated IP
        pool that it's associated with, whether or not it's enabled for sending email,
        and
        more.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_configuration_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_configuration_set)
        """

    async def get_configuration_set_event_destinations(
        self, *, ConfigurationSetName: str
    ) -> GetConfigurationSetEventDestinationsResponseTypeDef:
        """
        Retrieve a list of event destinations that are associated with a configuration
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_configuration_set_event_destinations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_configuration_set_event_destinations)
        """

    async def get_dedicated_ip(self, *, Ip: str) -> GetDedicatedIpResponseTypeDef:
        """
        Get information about a dedicated IP address, including the name of the
        dedicated IP pool that it's associated with, as well information about the
        automatic warm-up process for the
        address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_dedicated_ip)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_dedicated_ip)
        """

    async def get_dedicated_ips(
        self, *, PoolName: str = ..., NextToken: str = ..., PageSize: int = ...
    ) -> GetDedicatedIpsResponseTypeDef:
        """
        List the dedicated IP addresses that are associated with your Amazon Pinpoint
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_dedicated_ips)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_dedicated_ips)
        """

    async def get_deliverability_dashboard_options(
        self,
    ) -> GetDeliverabilityDashboardOptionsResponseTypeDef:
        """
        Retrieve information about the status of the Deliverability dashboard for your
        Amazon Pinpoint
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_deliverability_dashboard_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_deliverability_dashboard_options)
        """

    async def get_deliverability_test_report(
        self, *, ReportId: str
    ) -> GetDeliverabilityTestReportResponseTypeDef:
        """
        Retrieve the results of a predictive inbox placement test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_deliverability_test_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_deliverability_test_report)
        """

    async def get_domain_deliverability_campaign(
        self, *, CampaignId: str
    ) -> GetDomainDeliverabilityCampaignResponseTypeDef:
        """
        Retrieve all the deliverability data for a specific campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_domain_deliverability_campaign)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_domain_deliverability_campaign)
        """

    async def get_domain_statistics_report(
        self, *, Domain: str, StartDate: TimestampTypeDef, EndDate: TimestampTypeDef
    ) -> GetDomainStatisticsReportResponseTypeDef:
        """
        Retrieve inbox placement and engagement rates for the domains that you use to
        send
        email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_domain_statistics_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_domain_statistics_report)
        """

    async def get_email_identity(self, *, EmailIdentity: str) -> GetEmailIdentityResponseTypeDef:
        """
        Provides information about a specific identity associated with your Amazon
        Pinpoint account, including the identity's verification status, its DKIM
        authentication status, and its custom Mail-From
        settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_email_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_email_identity)
        """

    async def list_configuration_sets(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListConfigurationSetsResponseTypeDef:
        """
        List all of the configuration sets associated with your Amazon Pinpoint account
        in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.list_configuration_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#list_configuration_sets)
        """

    async def list_dedicated_ip_pools(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListDedicatedIpPoolsResponseTypeDef:
        """
        List all of the dedicated IP pools that exist in your Amazon Pinpoint account
        in the current AWS
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.list_dedicated_ip_pools)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#list_dedicated_ip_pools)
        """

    async def list_deliverability_test_reports(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListDeliverabilityTestReportsResponseTypeDef:
        """
        Show a list of the predictive inbox placement tests that you've performed,
        regardless of their
        statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.list_deliverability_test_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#list_deliverability_test_reports)
        """

    async def list_domain_deliverability_campaigns(
        self,
        *,
        StartDate: TimestampTypeDef,
        EndDate: TimestampTypeDef,
        SubscribedDomain: str,
        NextToken: str = ...,
        PageSize: int = ...,
    ) -> ListDomainDeliverabilityCampaignsResponseTypeDef:
        """
        Retrieve deliverability data for all the campaigns that used a specific domain
        to send email during a specified time
        range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.list_domain_deliverability_campaigns)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#list_domain_deliverability_campaigns)
        """

    async def list_email_identities(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListEmailIdentitiesResponseTypeDef:
        """
        Returns a list of all of the email identities that are associated with your
        Amazon Pinpoint
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.list_email_identities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#list_email_identities)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieve a list of the tags (keys and values) that are associated with a
        specified
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#list_tags_for_resource)
        """

    async def put_account_dedicated_ip_warmup_attributes(
        self, *, AutoWarmupEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Enable or disable the automatic warm-up feature for dedicated IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_account_dedicated_ip_warmup_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_account_dedicated_ip_warmup_attributes)
        """

    async def put_account_sending_attributes(self, *, SendingEnabled: bool = ...) -> Dict[str, Any]:
        """
        Enable or disable the ability of your account to send email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_account_sending_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_account_sending_attributes)
        """

    async def put_configuration_set_delivery_options(
        self,
        *,
        ConfigurationSetName: str,
        TlsPolicy: TlsPolicyType = ...,
        SendingPoolName: str = ...,
    ) -> Dict[str, Any]:
        """
        Associate a configuration set with a dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_configuration_set_delivery_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_configuration_set_delivery_options)
        """

    async def put_configuration_set_reputation_options(
        self, *, ConfigurationSetName: str, ReputationMetricsEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Enable or disable collection of reputation metrics for emails that you send
        using a particular configuration set in a specific AWS
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_configuration_set_reputation_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_configuration_set_reputation_options)
        """

    async def put_configuration_set_sending_options(
        self, *, ConfigurationSetName: str, SendingEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Enable or disable email sending for messages that use a particular
        configuration set in a specific AWS
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_configuration_set_sending_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_configuration_set_sending_options)
        """

    async def put_configuration_set_tracking_options(
        self, *, ConfigurationSetName: str, CustomRedirectDomain: str = ...
    ) -> Dict[str, Any]:
        """
        Specify a custom domain to use for open and click tracking elements in email
        that you send using Amazon
        Pinpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_configuration_set_tracking_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_configuration_set_tracking_options)
        """

    async def put_dedicated_ip_in_pool(
        self, *, Ip: str, DestinationPoolName: str
    ) -> Dict[str, Any]:
        """
        Move a dedicated IP address to an existing dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_dedicated_ip_in_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_dedicated_ip_in_pool)
        """

    async def put_dedicated_ip_warmup_attributes(
        self, *, Ip: str, WarmupPercentage: int
    ) -> Dict[str, Any]:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/pinpoint-email-2018-07-26/PutDedicatedIpWarmupAttributes).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_dedicated_ip_warmup_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_dedicated_ip_warmup_attributes)
        """

    async def put_deliverability_dashboard_option(
        self,
        *,
        DashboardEnabled: bool,
        SubscribedDomains: Sequence[DomainDeliverabilityTrackingOptionUnionTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Enable or disable the Deliverability dashboard for your Amazon Pinpoint account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_deliverability_dashboard_option)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_deliverability_dashboard_option)
        """

    async def put_email_identity_dkim_attributes(
        self, *, EmailIdentity: str, SigningEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Used to enable or disable DKIM authentication for an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_email_identity_dkim_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_email_identity_dkim_attributes)
        """

    async def put_email_identity_feedback_attributes(
        self, *, EmailIdentity: str, EmailForwardingEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Used to enable or disable feedback forwarding for an identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_email_identity_feedback_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_email_identity_feedback_attributes)
        """

    async def put_email_identity_mail_from_attributes(
        self,
        *,
        EmailIdentity: str,
        MailFromDomain: str = ...,
        BehaviorOnMxFailure: BehaviorOnMxFailureType = ...,
    ) -> Dict[str, Any]:
        """
        Used to enable or disable the custom Mail-From domain configuration for an
        email
        identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.put_email_identity_mail_from_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#put_email_identity_mail_from_attributes)
        """

    async def send_email(
        self,
        *,
        Destination: DestinationTypeDef,
        Content: EmailContentTypeDef,
        FromEmailAddress: str = ...,
        ReplyToAddresses: Sequence[str] = ...,
        FeedbackForwardingEmailAddress: str = ...,
        EmailTags: Sequence[MessageTagTypeDef] = ...,
        ConfigurationSetName: str = ...,
    ) -> SendEmailResponseTypeDef:
        """
        Sends an email message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.send_email)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#send_email)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Add one or more tags (keys and values) to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#untag_resource)
        """

    async def update_configuration_set_event_destination(
        self,
        *,
        ConfigurationSetName: str,
        EventDestinationName: str,
        EventDestination: EventDestinationDefinitionTypeDef,
    ) -> Dict[str, Any]:
        """
        Update the configuration of an event destination for a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.update_configuration_set_event_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#update_configuration_set_event_destination)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_dedicated_ips"]
    ) -> GetDedicatedIpsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configuration_sets"]
    ) -> ListConfigurationSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dedicated_ip_pools"]
    ) -> ListDedicatedIpPoolsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deliverability_test_reports"]
    ) -> ListDeliverabilityTestReportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_email_identities"]
    ) -> ListEmailIdentitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/#get_paginator)
        """

    async def __aenter__(self) -> "PinpointEmailClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email.html#PinpointEmail.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/client/)
        """
