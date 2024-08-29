"""
Type annotations for sesv2 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sesv2.client import SESV2Client

    session = get_session()
    async with session.create_client("sesv2") as client:
        client: SESV2Client
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    BehaviorOnMxFailureType,
    ContactLanguageType,
    DkimSigningAttributesOriginType,
    ExportSourceTypeType,
    ImportDestinationTypeType,
    JobStatusType,
    ListRecommendationsFilterKeyType,
    MailTypeType,
    ScalingModeType,
    SuppressionListReasonType,
    TlsPolicyType,
)
from .type_defs import (
    BatchGetMetricDataQueryTypeDef,
    BatchGetMetricDataResponseTypeDef,
    BulkEmailContentTypeDef,
    BulkEmailEntryTypeDef,
    CreateDeliverabilityTestReportResponseTypeDef,
    CreateEmailIdentityResponseTypeDef,
    CreateExportJobResponseTypeDef,
    CreateImportJobResponseTypeDef,
    DeliveryOptionsTypeDef,
    DestinationTypeDef,
    DkimSigningAttributesTypeDef,
    DomainDeliverabilityTrackingOptionUnionTypeDef,
    EmailContentTypeDef,
    EmailTemplateContentTypeDef,
    EventDestinationDefinitionTypeDef,
    ExportDataSourceUnionTypeDef,
    ExportDestinationTypeDef,
    GetAccountResponseTypeDef,
    GetBlacklistReportsResponseTypeDef,
    GetConfigurationSetEventDestinationsResponseTypeDef,
    GetConfigurationSetResponseTypeDef,
    GetContactListResponseTypeDef,
    GetContactResponseTypeDef,
    GetCustomVerificationEmailTemplateResponseTypeDef,
    GetDedicatedIpPoolResponseTypeDef,
    GetDedicatedIpResponseTypeDef,
    GetDedicatedIpsResponseTypeDef,
    GetDeliverabilityDashboardOptionsResponseTypeDef,
    GetDeliverabilityTestReportResponseTypeDef,
    GetDomainDeliverabilityCampaignResponseTypeDef,
    GetDomainStatisticsReportResponseTypeDef,
    GetEmailIdentityPoliciesResponseTypeDef,
    GetEmailIdentityResponseTypeDef,
    GetEmailTemplateResponseTypeDef,
    GetExportJobResponseTypeDef,
    GetImportJobResponseTypeDef,
    GetMessageInsightsResponseTypeDef,
    GetSuppressedDestinationResponseTypeDef,
    ImportDataSourceTypeDef,
    ImportDestinationTypeDef,
    ListConfigurationSetsResponseTypeDef,
    ListContactListsResponseTypeDef,
    ListContactsFilterTypeDef,
    ListContactsResponseTypeDef,
    ListCustomVerificationEmailTemplatesResponseTypeDef,
    ListDedicatedIpPoolsResponseTypeDef,
    ListDeliverabilityTestReportsResponseTypeDef,
    ListDomainDeliverabilityCampaignsResponseTypeDef,
    ListEmailIdentitiesResponseTypeDef,
    ListEmailTemplatesResponseTypeDef,
    ListExportJobsResponseTypeDef,
    ListImportJobsResponseTypeDef,
    ListManagementOptionsTypeDef,
    ListRecommendationsResponseTypeDef,
    ListSuppressedDestinationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MessageTagTypeDef,
    PutEmailIdentityDkimSigningAttributesResponseTypeDef,
    ReputationOptionsUnionTypeDef,
    SendBulkEmailResponseTypeDef,
    SendCustomVerificationEmailResponseTypeDef,
    SendEmailResponseTypeDef,
    SendingOptionsTypeDef,
    SuppressionOptionsUnionTypeDef,
    TagTypeDef,
    TestRenderEmailTemplateResponseTypeDef,
    TimestampTypeDef,
    TopicPreferenceTypeDef,
    TopicTypeDef,
    TrackingOptionsTypeDef,
    VdmAttributesTypeDef,
    VdmOptionsTypeDef,
)

__all__ = ("SESV2Client",)


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
    ConflictException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MailFromDomainNotVerifiedException: Type[BotocoreClientError]
    MessageRejected: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    SendingPausedException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class SESV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SESV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#exceptions)
        """

    async def batch_get_metric_data(
        self, *, Queries: Sequence[BatchGetMetricDataQueryTypeDef]
    ) -> BatchGetMetricDataResponseTypeDef:
        """
        Retrieves batches of metric data collected based on your sending activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.batch_get_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#batch_get_metric_data)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#can_paginate)
        """

    async def cancel_export_job(self, *, JobId: str) -> Dict[str, Any]:
        """
        Cancels an export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.cancel_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#cancel_export_job)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#close)
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
        SuppressionOptions: SuppressionOptionsUnionTypeDef = ...,
        VdmOptions: VdmOptionsTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Create a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_configuration_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_configuration_set)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_configuration_set_event_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_configuration_set_event_destination)
        """

    async def create_contact(
        self,
        *,
        ContactListName: str,
        EmailAddress: str,
        TopicPreferences: Sequence[TopicPreferenceTypeDef] = ...,
        UnsubscribeAll: bool = ...,
        AttributesData: str = ...,
    ) -> Dict[str, Any]:
        """
        Creates a contact, which is an end-user who is receiving the email, and adds
        them to a contact
        list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_contact)
        """

    async def create_contact_list(
        self,
        *,
        ContactListName: str,
        Topics: Sequence[TopicTypeDef] = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Creates a contact list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_contact_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_contact_list)
        """

    async def create_custom_verification_email_template(
        self,
        *,
        TemplateName: str,
        FromEmailAddress: str,
        TemplateSubject: str,
        TemplateContent: str,
        SuccessRedirectionURL: str,
        FailureRedirectionURL: str,
    ) -> Dict[str, Any]:
        """
        Creates a new custom verification email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_custom_verification_email_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_custom_verification_email_template)
        """

    async def create_dedicated_ip_pool(
        self, *, PoolName: str, Tags: Sequence[TagTypeDef] = ..., ScalingMode: ScalingModeType = ...
    ) -> Dict[str, Any]:
        """
        Create a new pool of dedicated IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_dedicated_ip_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_dedicated_ip_pool)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_deliverability_test_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_deliverability_test_report)
        """

    async def create_email_identity(
        self,
        *,
        EmailIdentity: str,
        Tags: Sequence[TagTypeDef] = ...,
        DkimSigningAttributes: DkimSigningAttributesTypeDef = ...,
        ConfigurationSetName: str = ...,
    ) -> CreateEmailIdentityResponseTypeDef:
        """
        Starts the process of verifying an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_email_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_email_identity)
        """

    async def create_email_identity_policy(
        self, *, EmailIdentity: str, PolicyName: str, Policy: str
    ) -> Dict[str, Any]:
        """
        Creates the specified sending authorization policy for the given identity (an
        email address or a
        domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_email_identity_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_email_identity_policy)
        """

    async def create_email_template(
        self, *, TemplateName: str, TemplateContent: EmailTemplateContentTypeDef
    ) -> Dict[str, Any]:
        """
        Creates an email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_email_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_email_template)
        """

    async def create_export_job(
        self,
        *,
        ExportDataSource: ExportDataSourceUnionTypeDef,
        ExportDestination: ExportDestinationTypeDef,
    ) -> CreateExportJobResponseTypeDef:
        """
        Creates an export job for a data source and destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_export_job)
        """

    async def create_import_job(
        self,
        *,
        ImportDestination: ImportDestinationTypeDef,
        ImportDataSource: ImportDataSourceTypeDef,
    ) -> CreateImportJobResponseTypeDef:
        """
        Creates an import job for a data destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.create_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#create_import_job)
        """

    async def delete_configuration_set(self, *, ConfigurationSetName: str) -> Dict[str, Any]:
        """
        Delete an existing configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_configuration_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_configuration_set)
        """

    async def delete_configuration_set_event_destination(
        self, *, ConfigurationSetName: str, EventDestinationName: str
    ) -> Dict[str, Any]:
        """
        Delete an event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_configuration_set_event_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_configuration_set_event_destination)
        """

    async def delete_contact(self, *, ContactListName: str, EmailAddress: str) -> Dict[str, Any]:
        """
        Removes a contact from a contact list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_contact)
        """

    async def delete_contact_list(self, *, ContactListName: str) -> Dict[str, Any]:
        """
        Deletes a contact list and all of the contacts on that list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_contact_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_contact_list)
        """

    async def delete_custom_verification_email_template(
        self, *, TemplateName: str
    ) -> Dict[str, Any]:
        """
        Deletes an existing custom verification email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_custom_verification_email_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_custom_verification_email_template)
        """

    async def delete_dedicated_ip_pool(self, *, PoolName: str) -> Dict[str, Any]:
        """
        Delete a dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_dedicated_ip_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_dedicated_ip_pool)
        """

    async def delete_email_identity(self, *, EmailIdentity: str) -> Dict[str, Any]:
        """
        Deletes an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_email_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_email_identity)
        """

    async def delete_email_identity_policy(
        self, *, EmailIdentity: str, PolicyName: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified sending authorization policy for the given identity (an
        email address or a
        domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_email_identity_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_email_identity_policy)
        """

    async def delete_email_template(self, *, TemplateName: str) -> Dict[str, Any]:
        """
        Deletes an email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_email_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_email_template)
        """

    async def delete_suppressed_destination(self, *, EmailAddress: str) -> Dict[str, Any]:
        """
        Removes an email address from the suppression list for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.delete_suppressed_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#delete_suppressed_destination)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#generate_presigned_url)
        """

    async def get_account(self) -> GetAccountResponseTypeDef:
        """
        Obtain information about the email-sending status and capabilities of your
        Amazon SES account in the current Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_account)
        """

    async def get_blacklist_reports(
        self, *, BlacklistItemNames: Sequence[str]
    ) -> GetBlacklistReportsResponseTypeDef:
        """
        Retrieve a list of the blacklists that your dedicated IP addresses appear on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_blacklist_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_blacklist_reports)
        """

    async def get_configuration_set(
        self, *, ConfigurationSetName: str
    ) -> GetConfigurationSetResponseTypeDef:
        """
        Get information about an existing configuration set, including the dedicated IP
        pool that it's associated with, whether or not it's enabled for sending email,
        and
        more.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_configuration_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_configuration_set)
        """

    async def get_configuration_set_event_destinations(
        self, *, ConfigurationSetName: str
    ) -> GetConfigurationSetEventDestinationsResponseTypeDef:
        """
        Retrieve a list of event destinations that are associated with a configuration
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_configuration_set_event_destinations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_configuration_set_event_destinations)
        """

    async def get_contact(
        self, *, ContactListName: str, EmailAddress: str
    ) -> GetContactResponseTypeDef:
        """
        Returns a contact from a contact list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_contact)
        """

    async def get_contact_list(self, *, ContactListName: str) -> GetContactListResponseTypeDef:
        """
        Returns contact list metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_contact_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_contact_list)
        """

    async def get_custom_verification_email_template(
        self, *, TemplateName: str
    ) -> GetCustomVerificationEmailTemplateResponseTypeDef:
        """
        Returns the custom email verification template for the template name you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_custom_verification_email_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_custom_verification_email_template)
        """

    async def get_dedicated_ip(self, *, Ip: str) -> GetDedicatedIpResponseTypeDef:
        """
        Get information about a dedicated IP address, including the name of the
        dedicated IP pool that it's associated with, as well information about the
        automatic warm-up process for the
        address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_dedicated_ip)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_dedicated_ip)
        """

    async def get_dedicated_ip_pool(self, *, PoolName: str) -> GetDedicatedIpPoolResponseTypeDef:
        """
        Retrieve information about the dedicated pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_dedicated_ip_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_dedicated_ip_pool)
        """

    async def get_dedicated_ips(
        self, *, PoolName: str = ..., NextToken: str = ..., PageSize: int = ...
    ) -> GetDedicatedIpsResponseTypeDef:
        """
        List the dedicated IP addresses that are associated with your Amazon Web
        Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_dedicated_ips)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_dedicated_ips)
        """

    async def get_deliverability_dashboard_options(
        self,
    ) -> GetDeliverabilityDashboardOptionsResponseTypeDef:
        """
        Retrieve information about the status of the Deliverability dashboard for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_deliverability_dashboard_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_deliverability_dashboard_options)
        """

    async def get_deliverability_test_report(
        self, *, ReportId: str
    ) -> GetDeliverabilityTestReportResponseTypeDef:
        """
        Retrieve the results of a predictive inbox placement test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_deliverability_test_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_deliverability_test_report)
        """

    async def get_domain_deliverability_campaign(
        self, *, CampaignId: str
    ) -> GetDomainDeliverabilityCampaignResponseTypeDef:
        """
        Retrieve all the deliverability data for a specific campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_domain_deliverability_campaign)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_domain_deliverability_campaign)
        """

    async def get_domain_statistics_report(
        self, *, Domain: str, StartDate: TimestampTypeDef, EndDate: TimestampTypeDef
    ) -> GetDomainStatisticsReportResponseTypeDef:
        """
        Retrieve inbox placement and engagement rates for the domains that you use to
        send
        email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_domain_statistics_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_domain_statistics_report)
        """

    async def get_email_identity(self, *, EmailIdentity: str) -> GetEmailIdentityResponseTypeDef:
        """
        Provides information about a specific identity, including the identity's
        verification status, sending authorization policies, its DKIM authentication
        status, and its custom Mail-From
        settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_email_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_email_identity)
        """

    async def get_email_identity_policies(
        self, *, EmailIdentity: str
    ) -> GetEmailIdentityPoliciesResponseTypeDef:
        """
        Returns the requested sending authorization policies for the given identity (an
        email address or a
        domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_email_identity_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_email_identity_policies)
        """

    async def get_email_template(self, *, TemplateName: str) -> GetEmailTemplateResponseTypeDef:
        """
        Displays the template object (which includes the subject line, HTML part and
        text part) for the template you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_email_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_email_template)
        """

    async def get_export_job(self, *, JobId: str) -> GetExportJobResponseTypeDef:
        """
        Provides information about an export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_export_job)
        """

    async def get_import_job(self, *, JobId: str) -> GetImportJobResponseTypeDef:
        """
        Provides information about an import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_import_job)
        """

    async def get_message_insights(self, *, MessageId: str) -> GetMessageInsightsResponseTypeDef:
        """
        Provides information about a specific message, including the from address, the
        subject, the recipient address, email tags, as well as events associated with
        the
        message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_message_insights)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_message_insights)
        """

    async def get_suppressed_destination(
        self, *, EmailAddress: str
    ) -> GetSuppressedDestinationResponseTypeDef:
        """
        Retrieves information about a specific email address that's on the suppression
        list for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.get_suppressed_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#get_suppressed_destination)
        """

    async def list_configuration_sets(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListConfigurationSetsResponseTypeDef:
        """
        List all of the configuration sets associated with your account in the current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_configuration_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_configuration_sets)
        """

    async def list_contact_lists(
        self, *, PageSize: int = ..., NextToken: str = ...
    ) -> ListContactListsResponseTypeDef:
        """
        Lists all of the contact lists available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_contact_lists)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_contact_lists)
        """

    async def list_contacts(
        self,
        *,
        ContactListName: str,
        Filter: ListContactsFilterTypeDef = ...,
        PageSize: int = ...,
        NextToken: str = ...,
    ) -> ListContactsResponseTypeDef:
        """
        Lists the contacts present in a specific contact list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_contacts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_contacts)
        """

    async def list_custom_verification_email_templates(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListCustomVerificationEmailTemplatesResponseTypeDef:
        """
        Lists the existing custom verification email templates for your account in the
        current Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_custom_verification_email_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_custom_verification_email_templates)
        """

    async def list_dedicated_ip_pools(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListDedicatedIpPoolsResponseTypeDef:
        """
        List all of the dedicated IP pools that exist in your Amazon Web Services
        account in the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_dedicated_ip_pools)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_dedicated_ip_pools)
        """

    async def list_deliverability_test_reports(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListDeliverabilityTestReportsResponseTypeDef:
        """
        Show a list of the predictive inbox placement tests that you've performed,
        regardless of their
        statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_deliverability_test_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_deliverability_test_reports)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_domain_deliverability_campaigns)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_domain_deliverability_campaigns)
        """

    async def list_email_identities(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListEmailIdentitiesResponseTypeDef:
        """
        Returns a list of all of the email identities that are associated with your
        Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_email_identities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_email_identities)
        """

    async def list_email_templates(
        self, *, NextToken: str = ..., PageSize: int = ...
    ) -> ListEmailTemplatesResponseTypeDef:
        """
        Lists the email templates present in your Amazon SES account in the current
        Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_email_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_email_templates)
        """

    async def list_export_jobs(
        self,
        *,
        NextToken: str = ...,
        PageSize: int = ...,
        ExportSourceType: ExportSourceTypeType = ...,
        JobStatus: JobStatusType = ...,
    ) -> ListExportJobsResponseTypeDef:
        """
        Lists all of the export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_export_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_export_jobs)
        """

    async def list_import_jobs(
        self,
        *,
        ImportDestinationType: ImportDestinationTypeType = ...,
        NextToken: str = ...,
        PageSize: int = ...,
    ) -> ListImportJobsResponseTypeDef:
        """
        Lists all of the import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_import_jobs)
        """

    async def list_recommendations(
        self,
        *,
        Filter: Mapping[ListRecommendationsFilterKeyType, str] = ...,
        NextToken: str = ...,
        PageSize: int = ...,
    ) -> ListRecommendationsResponseTypeDef:
        """
        Lists the recommendations present in your Amazon SES account in the current
        Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_recommendations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_recommendations)
        """

    async def list_suppressed_destinations(
        self,
        *,
        Reasons: Sequence[SuppressionListReasonType] = ...,
        StartDate: TimestampTypeDef = ...,
        EndDate: TimestampTypeDef = ...,
        NextToken: str = ...,
        PageSize: int = ...,
    ) -> ListSuppressedDestinationsResponseTypeDef:
        """
        Retrieves a list of email addresses that are on the suppression list for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_suppressed_destinations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_suppressed_destinations)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieve a list of the tags (keys and values) that are associated with a
        specified
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#list_tags_for_resource)
        """

    async def put_account_dedicated_ip_warmup_attributes(
        self, *, AutoWarmupEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Enable or disable the automatic warm-up feature for dedicated IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_account_dedicated_ip_warmup_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_account_dedicated_ip_warmup_attributes)
        """

    async def put_account_details(
        self,
        *,
        MailType: MailTypeType,
        WebsiteURL: str,
        ContactLanguage: ContactLanguageType = ...,
        UseCaseDescription: str = ...,
        AdditionalContactEmailAddresses: Sequence[str] = ...,
        ProductionAccessEnabled: bool = ...,
    ) -> Dict[str, Any]:
        """
        Update your Amazon SES account details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_account_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_account_details)
        """

    async def put_account_sending_attributes(self, *, SendingEnabled: bool = ...) -> Dict[str, Any]:
        """
        Enable or disable the ability of your account to send email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_account_sending_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_account_sending_attributes)
        """

    async def put_account_suppression_attributes(
        self, *, SuppressedReasons: Sequence[SuppressionListReasonType] = ...
    ) -> Dict[str, Any]:
        """
        Change the settings for the account-level suppression list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_account_suppression_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_account_suppression_attributes)
        """

    async def put_account_vdm_attributes(
        self, *, VdmAttributes: VdmAttributesTypeDef
    ) -> Dict[str, Any]:
        """
        Update your Amazon SES account VDM attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_account_vdm_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_account_vdm_attributes)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_configuration_set_delivery_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_configuration_set_delivery_options)
        """

    async def put_configuration_set_reputation_options(
        self, *, ConfigurationSetName: str, ReputationMetricsEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Enable or disable collection of reputation metrics for emails that you send
        using a particular configuration set in a specific Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_configuration_set_reputation_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_configuration_set_reputation_options)
        """

    async def put_configuration_set_sending_options(
        self, *, ConfigurationSetName: str, SendingEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Enable or disable email sending for messages that use a particular
        configuration set in a specific Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_configuration_set_sending_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_configuration_set_sending_options)
        """

    async def put_configuration_set_suppression_options(
        self,
        *,
        ConfigurationSetName: str,
        SuppressedReasons: Sequence[SuppressionListReasonType] = ...,
    ) -> Dict[str, Any]:
        """
        Specify the account suppression list preferences for a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_configuration_set_suppression_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_configuration_set_suppression_options)
        """

    async def put_configuration_set_tracking_options(
        self, *, ConfigurationSetName: str, CustomRedirectDomain: str = ...
    ) -> Dict[str, Any]:
        """
        Specify a custom domain to use for open and click tracking elements in email
        that you
        send.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_configuration_set_tracking_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_configuration_set_tracking_options)
        """

    async def put_configuration_set_vdm_options(
        self, *, ConfigurationSetName: str, VdmOptions: VdmOptionsTypeDef = ...
    ) -> Dict[str, Any]:
        """
        Specify VDM preferences for email that you send using the configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_configuration_set_vdm_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_configuration_set_vdm_options)
        """

    async def put_dedicated_ip_in_pool(
        self, *, Ip: str, DestinationPoolName: str
    ) -> Dict[str, Any]:
        """
        Move a dedicated IP address to an existing dedicated IP pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_dedicated_ip_in_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_dedicated_ip_in_pool)
        """

    async def put_dedicated_ip_pool_scaling_attributes(
        self, *, PoolName: str, ScalingMode: ScalingModeType
    ) -> Dict[str, Any]:
        """
        Used to convert a dedicated IP pool to a different scaling mode.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_dedicated_ip_pool_scaling_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_dedicated_ip_pool_scaling_attributes)
        """

    async def put_dedicated_ip_warmup_attributes(
        self, *, Ip: str, WarmupPercentage: int
    ) -> Dict[str, Any]:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/sesv2-2019-09-27/PutDedicatedIpWarmupAttributes).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_dedicated_ip_warmup_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_dedicated_ip_warmup_attributes)
        """

    async def put_deliverability_dashboard_option(
        self,
        *,
        DashboardEnabled: bool,
        SubscribedDomains: Sequence[DomainDeliverabilityTrackingOptionUnionTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Enable or disable the Deliverability dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_deliverability_dashboard_option)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_deliverability_dashboard_option)
        """

    async def put_email_identity_configuration_set_attributes(
        self, *, EmailIdentity: str, ConfigurationSetName: str = ...
    ) -> Dict[str, Any]:
        """
        Used to associate a configuration set with an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_email_identity_configuration_set_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_email_identity_configuration_set_attributes)
        """

    async def put_email_identity_dkim_attributes(
        self, *, EmailIdentity: str, SigningEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Used to enable or disable DKIM authentication for an email identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_email_identity_dkim_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_email_identity_dkim_attributes)
        """

    async def put_email_identity_dkim_signing_attributes(
        self,
        *,
        EmailIdentity: str,
        SigningAttributesOrigin: DkimSigningAttributesOriginType,
        SigningAttributes: DkimSigningAttributesTypeDef = ...,
    ) -> PutEmailIdentityDkimSigningAttributesResponseTypeDef:
        """
        Used to configure or change the DKIM authentication settings for an email
        domain
        identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_email_identity_dkim_signing_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_email_identity_dkim_signing_attributes)
        """

    async def put_email_identity_feedback_attributes(
        self, *, EmailIdentity: str, EmailForwardingEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Used to enable or disable feedback forwarding for an identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_email_identity_feedback_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_email_identity_feedback_attributes)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_email_identity_mail_from_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_email_identity_mail_from_attributes)
        """

    async def put_suppressed_destination(
        self, *, EmailAddress: str, Reason: SuppressionListReasonType
    ) -> Dict[str, Any]:
        """
        Adds an email address to the suppression list for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.put_suppressed_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#put_suppressed_destination)
        """

    async def send_bulk_email(
        self,
        *,
        DefaultContent: BulkEmailContentTypeDef,
        BulkEmailEntries: Sequence[BulkEmailEntryTypeDef],
        FromEmailAddress: str = ...,
        FromEmailAddressIdentityArn: str = ...,
        ReplyToAddresses: Sequence[str] = ...,
        FeedbackForwardingEmailAddress: str = ...,
        FeedbackForwardingEmailAddressIdentityArn: str = ...,
        DefaultEmailTags: Sequence[MessageTagTypeDef] = ...,
        ConfigurationSetName: str = ...,
    ) -> SendBulkEmailResponseTypeDef:
        """
        Composes an email message to multiple destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.send_bulk_email)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#send_bulk_email)
        """

    async def send_custom_verification_email(
        self, *, EmailAddress: str, TemplateName: str, ConfigurationSetName: str = ...
    ) -> SendCustomVerificationEmailResponseTypeDef:
        """
        Adds an email address to the list of identities for your Amazon SES account in
        the current Amazon Web Services Region and attempts to verify
        it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.send_custom_verification_email)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#send_custom_verification_email)
        """

    async def send_email(
        self,
        *,
        Content: EmailContentTypeDef,
        FromEmailAddress: str = ...,
        FromEmailAddressIdentityArn: str = ...,
        Destination: DestinationTypeDef = ...,
        ReplyToAddresses: Sequence[str] = ...,
        FeedbackForwardingEmailAddress: str = ...,
        FeedbackForwardingEmailAddressIdentityArn: str = ...,
        EmailTags: Sequence[MessageTagTypeDef] = ...,
        ConfigurationSetName: str = ...,
        ListManagementOptions: ListManagementOptionsTypeDef = ...,
    ) -> SendEmailResponseTypeDef:
        """
        Sends an email message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.send_email)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#send_email)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Add one or more tags (keys and values) to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#tag_resource)
        """

    async def test_render_email_template(
        self, *, TemplateName: str, TemplateData: str
    ) -> TestRenderEmailTemplateResponseTypeDef:
        """
        Creates a preview of the MIME content of an email when provided with a template
        and a set of replacement
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.test_render_email_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#test_render_email_template)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#untag_resource)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.update_configuration_set_event_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#update_configuration_set_event_destination)
        """

    async def update_contact(
        self,
        *,
        ContactListName: str,
        EmailAddress: str,
        TopicPreferences: Sequence[TopicPreferenceTypeDef] = ...,
        UnsubscribeAll: bool = ...,
        AttributesData: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a contact's preferences for a list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.update_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#update_contact)
        """

    async def update_contact_list(
        self, *, ContactListName: str, Topics: Sequence[TopicTypeDef] = ..., Description: str = ...
    ) -> Dict[str, Any]:
        """
        Updates contact list metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.update_contact_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#update_contact_list)
        """

    async def update_custom_verification_email_template(
        self,
        *,
        TemplateName: str,
        FromEmailAddress: str,
        TemplateSubject: str,
        TemplateContent: str,
        SuccessRedirectionURL: str,
        FailureRedirectionURL: str,
    ) -> Dict[str, Any]:
        """
        Updates an existing custom verification email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.update_custom_verification_email_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#update_custom_verification_email_template)
        """

    async def update_email_identity_policy(
        self, *, EmailIdentity: str, PolicyName: str, Policy: str
    ) -> Dict[str, Any]:
        """
        Updates the specified sending authorization policy for the given identity (an
        email address or a
        domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.update_email_identity_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#update_email_identity_policy)
        """

    async def update_email_template(
        self, *, TemplateName: str, TemplateContent: EmailTemplateContentTypeDef
    ) -> Dict[str, Any]:
        """
        Updates an email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client.update_email_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/#update_email_template)
        """

    async def __aenter__(self) -> "SESV2Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2.html#SESV2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/client/)
        """
