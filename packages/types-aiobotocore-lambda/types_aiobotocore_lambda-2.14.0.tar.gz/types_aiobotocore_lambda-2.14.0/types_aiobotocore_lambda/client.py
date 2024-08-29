"""
Type annotations for lambda service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lambda.client import LambdaClient

    session = get_session()
    async with session.create_client("lambda") as client:
        client: LambdaClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ArchitectureType,
    EventSourcePositionType,
    FunctionUrlAuthTypeType,
    InvocationTypeType,
    InvokeModeType,
    LogTypeType,
    PackageTypeType,
    RecursiveLoopType,
    ResponseStreamingInvocationTypeType,
    RuntimeType,
    UpdateRuntimeOnType,
)
from .paginator import (
    ListAliasesPaginator,
    ListCodeSigningConfigsPaginator,
    ListEventSourceMappingsPaginator,
    ListFunctionEventInvokeConfigsPaginator,
    ListFunctionsByCodeSigningConfigPaginator,
    ListFunctionsPaginator,
    ListFunctionUrlConfigsPaginator,
    ListLayersPaginator,
    ListLayerVersionsPaginator,
    ListProvisionedConcurrencyConfigsPaginator,
    ListVersionsByFunctionPaginator,
)
from .type_defs import (
    AddLayerVersionPermissionResponseTypeDef,
    AddPermissionResponseTypeDef,
    AliasConfigurationResponseTypeDef,
    AliasRoutingConfigurationUnionTypeDef,
    AllowedPublishersUnionTypeDef,
    AmazonManagedKafkaEventSourceConfigTypeDef,
    BlobTypeDef,
    CodeSigningPoliciesTypeDef,
    ConcurrencyResponseTypeDef,
    CorsUnionTypeDef,
    CreateCodeSigningConfigResponseTypeDef,
    CreateFunctionUrlConfigResponseTypeDef,
    DeadLetterConfigTypeDef,
    DestinationConfigTypeDef,
    DocumentDBEventSourceConfigTypeDef,
    EmptyResponseMetadataTypeDef,
    EnvironmentTypeDef,
    EphemeralStorageTypeDef,
    EventSourceMappingConfigurationResponseTypeDef,
    FileSystemConfigTypeDef,
    FilterCriteriaUnionTypeDef,
    FunctionCodeTypeDef,
    FunctionConfigurationResponseTypeDef,
    FunctionEventInvokeConfigResponseTypeDef,
    GetAccountSettingsResponseTypeDef,
    GetCodeSigningConfigResponseTypeDef,
    GetFunctionCodeSigningConfigResponseTypeDef,
    GetFunctionConcurrencyResponseTypeDef,
    GetFunctionRecursionConfigResponseTypeDef,
    GetFunctionResponseTypeDef,
    GetFunctionUrlConfigResponseTypeDef,
    GetLayerVersionPolicyResponseTypeDef,
    GetLayerVersionResponseTypeDef,
    GetPolicyResponseTypeDef,
    GetProvisionedConcurrencyConfigResponseTypeDef,
    GetRuntimeManagementConfigResponseTypeDef,
    ImageConfigUnionTypeDef,
    InvocationResponseTypeDef,
    InvokeAsyncResponseTypeDef,
    InvokeWithResponseStreamResponseTypeDef,
    LayerVersionContentInputTypeDef,
    ListAliasesResponseTypeDef,
    ListCodeSigningConfigsResponseTypeDef,
    ListEventSourceMappingsResponseTypeDef,
    ListFunctionEventInvokeConfigsResponseTypeDef,
    ListFunctionsByCodeSigningConfigResponseTypeDef,
    ListFunctionsResponseTypeDef,
    ListFunctionUrlConfigsResponseTypeDef,
    ListLayersResponseTypeDef,
    ListLayerVersionsResponseTypeDef,
    ListProvisionedConcurrencyConfigsResponseTypeDef,
    ListTagsResponseTypeDef,
    ListVersionsByFunctionResponseTypeDef,
    LoggingConfigTypeDef,
    PublishLayerVersionResponseTypeDef,
    PutFunctionCodeSigningConfigResponseTypeDef,
    PutFunctionRecursionConfigResponseTypeDef,
    PutProvisionedConcurrencyConfigResponseTypeDef,
    PutRuntimeManagementConfigResponseTypeDef,
    ScalingConfigTypeDef,
    SelfManagedEventSourceUnionTypeDef,
    SelfManagedKafkaEventSourceConfigTypeDef,
    SnapStartTypeDef,
    SourceAccessConfigurationTypeDef,
    TimestampTypeDef,
    TracingConfigTypeDef,
    UpdateCodeSigningConfigResponseTypeDef,
    UpdateFunctionUrlConfigResponseTypeDef,
    VpcConfigTypeDef,
)
from .waiter import (
    FunctionActiveV2Waiter,
    FunctionActiveWaiter,
    FunctionExistsWaiter,
    FunctionUpdatedV2Waiter,
    FunctionUpdatedWaiter,
    PublishedVersionActiveWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("LambdaClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    CodeSigningConfigNotFoundException: Type[BotocoreClientError]
    CodeStorageExceededException: Type[BotocoreClientError]
    CodeVerificationFailedException: Type[BotocoreClientError]
    EC2AccessDeniedException: Type[BotocoreClientError]
    EC2ThrottledException: Type[BotocoreClientError]
    EC2UnexpectedException: Type[BotocoreClientError]
    EFSIOException: Type[BotocoreClientError]
    EFSMountConnectivityException: Type[BotocoreClientError]
    EFSMountFailureException: Type[BotocoreClientError]
    EFSMountTimeoutException: Type[BotocoreClientError]
    ENILimitReachedException: Type[BotocoreClientError]
    InvalidCodeSignatureException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRequestContentException: Type[BotocoreClientError]
    InvalidRuntimeException: Type[BotocoreClientError]
    InvalidSecurityGroupIDException: Type[BotocoreClientError]
    InvalidSubnetIDException: Type[BotocoreClientError]
    InvalidZipFileException: Type[BotocoreClientError]
    KMSAccessDeniedException: Type[BotocoreClientError]
    KMSDisabledException: Type[BotocoreClientError]
    KMSInvalidStateException: Type[BotocoreClientError]
    KMSNotFoundException: Type[BotocoreClientError]
    PolicyLengthExceededException: Type[BotocoreClientError]
    PreconditionFailedException: Type[BotocoreClientError]
    ProvisionedConcurrencyConfigNotFoundException: Type[BotocoreClientError]
    RecursiveInvocationException: Type[BotocoreClientError]
    RequestTooLargeException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    SnapStartException: Type[BotocoreClientError]
    SnapStartNotReadyException: Type[BotocoreClientError]
    SnapStartTimeoutException: Type[BotocoreClientError]
    SubnetIPAddressLimitReachedException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnsupportedMediaTypeException: Type[BotocoreClientError]


class LambdaClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LambdaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#exceptions)
        """

    async def add_layer_version_permission(
        self,
        *,
        LayerName: str,
        VersionNumber: int,
        StatementId: str,
        Action: str,
        Principal: str,
        OrganizationId: str = ...,
        RevisionId: str = ...,
    ) -> AddLayerVersionPermissionResponseTypeDef:
        """
        Adds permissions to the resource-based policy of a version of an [Lambda
        layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.add_layer_version_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#add_layer_version_permission)
        """

    async def add_permission(
        self,
        *,
        FunctionName: str,
        StatementId: str,
        Action: str,
        Principal: str,
        SourceArn: str = ...,
        SourceAccount: str = ...,
        EventSourceToken: str = ...,
        Qualifier: str = ...,
        RevisionId: str = ...,
        PrincipalOrgID: str = ...,
        FunctionUrlAuthType: FunctionUrlAuthTypeType = ...,
    ) -> AddPermissionResponseTypeDef:
        """
        Grants an Amazon Web Servicesservice, Amazon Web Services account, or Amazon
        Web Services organization permission to use a
        function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.add_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#add_permission)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#close)
        """

    async def create_alias(
        self,
        *,
        FunctionName: str,
        Name: str,
        FunctionVersion: str,
        Description: str = ...,
        RoutingConfig: AliasRoutingConfigurationUnionTypeDef = ...,
    ) -> AliasConfigurationResponseTypeDef:
        """
        Creates an
        [alias](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html)
        for a Lambda function
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.create_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#create_alias)
        """

    async def create_code_signing_config(
        self,
        *,
        AllowedPublishers: AllowedPublishersUnionTypeDef,
        Description: str = ...,
        CodeSigningPolicies: CodeSigningPoliciesTypeDef = ...,
    ) -> CreateCodeSigningConfigResponseTypeDef:
        """
        Creates a code signing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.create_code_signing_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#create_code_signing_config)
        """

    async def create_event_source_mapping(
        self,
        *,
        FunctionName: str,
        EventSourceArn: str = ...,
        Enabled: bool = ...,
        BatchSize: int = ...,
        FilterCriteria: FilterCriteriaUnionTypeDef = ...,
        MaximumBatchingWindowInSeconds: int = ...,
        ParallelizationFactor: int = ...,
        StartingPosition: EventSourcePositionType = ...,
        StartingPositionTimestamp: TimestampTypeDef = ...,
        DestinationConfig: DestinationConfigTypeDef = ...,
        MaximumRecordAgeInSeconds: int = ...,
        BisectBatchOnFunctionError: bool = ...,
        MaximumRetryAttempts: int = ...,
        TumblingWindowInSeconds: int = ...,
        Topics: Sequence[str] = ...,
        Queues: Sequence[str] = ...,
        SourceAccessConfigurations: Sequence[SourceAccessConfigurationTypeDef] = ...,
        SelfManagedEventSource: SelfManagedEventSourceUnionTypeDef = ...,
        FunctionResponseTypes: Sequence[Literal["ReportBatchItemFailures"]] = ...,
        AmazonManagedKafkaEventSourceConfig: AmazonManagedKafkaEventSourceConfigTypeDef = ...,
        SelfManagedKafkaEventSourceConfig: SelfManagedKafkaEventSourceConfigTypeDef = ...,
        ScalingConfig: ScalingConfigTypeDef = ...,
        DocumentDBEventSourceConfig: DocumentDBEventSourceConfigTypeDef = ...,
        KMSKeyArn: str = ...,
    ) -> EventSourceMappingConfigurationResponseTypeDef:
        """
        Creates a mapping between an event source and an Lambda function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.create_event_source_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#create_event_source_mapping)
        """

    async def create_function(
        self,
        *,
        FunctionName: str,
        Role: str,
        Code: FunctionCodeTypeDef,
        Runtime: RuntimeType = ...,
        Handler: str = ...,
        Description: str = ...,
        Timeout: int = ...,
        MemorySize: int = ...,
        Publish: bool = ...,
        VpcConfig: VpcConfigTypeDef = ...,
        PackageType: PackageTypeType = ...,
        DeadLetterConfig: DeadLetterConfigTypeDef = ...,
        Environment: EnvironmentTypeDef = ...,
        KMSKeyArn: str = ...,
        TracingConfig: TracingConfigTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        Layers: Sequence[str] = ...,
        FileSystemConfigs: Sequence[FileSystemConfigTypeDef] = ...,
        ImageConfig: ImageConfigUnionTypeDef = ...,
        CodeSigningConfigArn: str = ...,
        Architectures: Sequence[ArchitectureType] = ...,
        EphemeralStorage: EphemeralStorageTypeDef = ...,
        SnapStart: SnapStartTypeDef = ...,
        LoggingConfig: LoggingConfigTypeDef = ...,
    ) -> FunctionConfigurationResponseTypeDef:
        """
        Creates a Lambda function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.create_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#create_function)
        """

    async def create_function_url_config(
        self,
        *,
        FunctionName: str,
        AuthType: FunctionUrlAuthTypeType,
        Qualifier: str = ...,
        Cors: CorsUnionTypeDef = ...,
        InvokeMode: InvokeModeType = ...,
    ) -> CreateFunctionUrlConfigResponseTypeDef:
        """
        Creates a Lambda function URL with the specified configuration parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.create_function_url_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#create_function_url_config)
        """

    async def delete_alias(self, *, FunctionName: str, Name: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Lambda function
        [alias](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_alias)
        """

    async def delete_code_signing_config(self, *, CodeSigningConfigArn: str) -> Dict[str, Any]:
        """
        Deletes the code signing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_code_signing_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_code_signing_config)
        """

    async def delete_event_source_mapping(
        self, *, UUID: str
    ) -> EventSourceMappingConfigurationResponseTypeDef:
        """
        Deletes an [event source
        mapping](https://docs.aws.amazon.com/lambda/latest/dg/intro-invocation-modes.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_event_source_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_event_source_mapping)
        """

    async def delete_function(
        self, *, FunctionName: str, Qualifier: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Lambda function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_function)
        """

    async def delete_function_code_signing_config(
        self, *, FunctionName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the code signing configuration from the function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_function_code_signing_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_function_code_signing_config)
        """

    async def delete_function_concurrency(
        self, *, FunctionName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a concurrent execution limit from a function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_function_concurrency)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_function_concurrency)
        """

    async def delete_function_event_invoke_config(
        self, *, FunctionName: str, Qualifier: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the configuration for asynchronous invocation for a function, version,
        or
        alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_function_event_invoke_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_function_event_invoke_config)
        """

    async def delete_function_url_config(
        self, *, FunctionName: str, Qualifier: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Lambda function URL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_function_url_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_function_url_config)
        """

    async def delete_layer_version(
        self, *, LayerName: str, VersionNumber: int
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a version of an [Lambda
        layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_layer_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_layer_version)
        """

    async def delete_provisioned_concurrency_config(
        self, *, FunctionName: str, Qualifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the provisioned concurrency configuration for a function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.delete_provisioned_concurrency_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#delete_provisioned_concurrency_config)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#generate_presigned_url)
        """

    async def get_account_settings(self) -> GetAccountSettingsResponseTypeDef:
        """
        Retrieves details about your account's
        [limits](https://docs.aws.amazon.com/lambda/latest/dg/limits.html) and usage in
        an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_account_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_account_settings)
        """

    async def get_alias(self, *, FunctionName: str, Name: str) -> AliasConfigurationResponseTypeDef:
        """
        Returns details about a Lambda function
        [alias](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_alias)
        """

    async def get_code_signing_config(
        self, *, CodeSigningConfigArn: str
    ) -> GetCodeSigningConfigResponseTypeDef:
        """
        Returns information about the specified code signing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_code_signing_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_code_signing_config)
        """

    async def get_event_source_mapping(
        self, *, UUID: str
    ) -> EventSourceMappingConfigurationResponseTypeDef:
        """
        Returns details about an event source mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_event_source_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_event_source_mapping)
        """

    async def get_function(
        self, *, FunctionName: str, Qualifier: str = ...
    ) -> GetFunctionResponseTypeDef:
        """
        Returns information about the function or function version, with a link to
        download the deployment package that's valid for 10
        minutes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_function)
        """

    async def get_function_code_signing_config(
        self, *, FunctionName: str
    ) -> GetFunctionCodeSigningConfigResponseTypeDef:
        """
        Returns the code signing configuration for the specified function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function_code_signing_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_function_code_signing_config)
        """

    async def get_function_concurrency(
        self, *, FunctionName: str
    ) -> GetFunctionConcurrencyResponseTypeDef:
        """
        Returns details about the reserved concurrency configuration for a function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function_concurrency)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_function_concurrency)
        """

    async def get_function_configuration(
        self, *, FunctionName: str, Qualifier: str = ...
    ) -> FunctionConfigurationResponseTypeDef:
        """
        Returns the version-specific settings of a Lambda function or version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_function_configuration)
        """

    async def get_function_event_invoke_config(
        self, *, FunctionName: str, Qualifier: str = ...
    ) -> FunctionEventInvokeConfigResponseTypeDef:
        """
        Retrieves the configuration for asynchronous invocation for a function,
        version, or
        alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function_event_invoke_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_function_event_invoke_config)
        """

    async def get_function_recursion_config(
        self, *, FunctionName: str
    ) -> GetFunctionRecursionConfigResponseTypeDef:
        """
        Returns your function's [recursive loop
        detection](https://docs.aws.amazon.com/lambda/latest/dg/invocation-recursion.html)
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function_recursion_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_function_recursion_config)
        """

    async def get_function_url_config(
        self, *, FunctionName: str, Qualifier: str = ...
    ) -> GetFunctionUrlConfigResponseTypeDef:
        """
        Returns details about a Lambda function URL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function_url_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_function_url_config)
        """

    async def get_layer_version(
        self, *, LayerName: str, VersionNumber: int
    ) -> GetLayerVersionResponseTypeDef:
        """
        Returns information about a version of an [Lambda
        layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html),
        with a link to download the layer archive that's valid for 10
        minutes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_layer_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_layer_version)
        """

    async def get_layer_version_by_arn(self, *, Arn: str) -> GetLayerVersionResponseTypeDef:
        """
        Returns information about a version of an [Lambda
        layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html),
        with a link to download the layer archive that's valid for 10
        minutes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_layer_version_by_arn)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_layer_version_by_arn)
        """

    async def get_layer_version_policy(
        self, *, LayerName: str, VersionNumber: int
    ) -> GetLayerVersionPolicyResponseTypeDef:
        """
        Returns the permission policy for a version of an [Lambda
        layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_layer_version_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_layer_version_policy)
        """

    async def get_policy(
        self, *, FunctionName: str, Qualifier: str = ...
    ) -> GetPolicyResponseTypeDef:
        """
        Returns the [resource-based IAM
        policy](https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html)
        for a function, version, or
        alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_policy)
        """

    async def get_provisioned_concurrency_config(
        self, *, FunctionName: str, Qualifier: str
    ) -> GetProvisionedConcurrencyConfigResponseTypeDef:
        """
        Retrieves the provisioned concurrency configuration for a function's alias or
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_provisioned_concurrency_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_provisioned_concurrency_config)
        """

    async def get_runtime_management_config(
        self, *, FunctionName: str, Qualifier: str = ...
    ) -> GetRuntimeManagementConfigResponseTypeDef:
        """
        Retrieves the runtime management configuration for a function's version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_runtime_management_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_runtime_management_config)
        """

    async def invoke(
        self,
        *,
        FunctionName: str,
        InvocationType: InvocationTypeType = ...,
        LogType: LogTypeType = ...,
        ClientContext: str = ...,
        Payload: BlobTypeDef = ...,
        Qualifier: str = ...,
    ) -> InvocationResponseTypeDef:
        """
        Invokes a Lambda function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#invoke)
        """

    async def invoke_async(
        self, *, FunctionName: str, InvokeArgs: BlobTypeDef
    ) -> InvokeAsyncResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke_async)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#invoke_async)
        """

    async def invoke_with_response_stream(
        self,
        *,
        FunctionName: str,
        InvocationType: ResponseStreamingInvocationTypeType = ...,
        LogType: LogTypeType = ...,
        ClientContext: str = ...,
        Qualifier: str = ...,
        Payload: BlobTypeDef = ...,
    ) -> InvokeWithResponseStreamResponseTypeDef:
        """
        Configure your Lambda functions to stream response payloads back to clients.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke_with_response_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#invoke_with_response_stream)
        """

    async def list_aliases(
        self,
        *,
        FunctionName: str,
        FunctionVersion: str = ...,
        Marker: str = ...,
        MaxItems: int = ...,
    ) -> ListAliasesResponseTypeDef:
        """
        Returns a list of
        [aliases](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html)
        for a Lambda
        function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_aliases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_aliases)
        """

    async def list_code_signing_configs(
        self, *, Marker: str = ..., MaxItems: int = ...
    ) -> ListCodeSigningConfigsResponseTypeDef:
        """
        Returns a list of [code signing
        configurations](https://docs.aws.amazon.com/lambda/latest/dg/configuring-codesigning.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_code_signing_configs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_code_signing_configs)
        """

    async def list_event_source_mappings(
        self,
        *,
        EventSourceArn: str = ...,
        FunctionName: str = ...,
        Marker: str = ...,
        MaxItems: int = ...,
    ) -> ListEventSourceMappingsResponseTypeDef:
        """
        Lists event source mappings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_event_source_mappings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_event_source_mappings)
        """

    async def list_function_event_invoke_configs(
        self, *, FunctionName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListFunctionEventInvokeConfigsResponseTypeDef:
        """
        Retrieves a list of configurations for asynchronous invocation for a function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_function_event_invoke_configs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_function_event_invoke_configs)
        """

    async def list_function_url_configs(
        self, *, FunctionName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListFunctionUrlConfigsResponseTypeDef:
        """
        Returns a list of Lambda function URLs for the specified function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_function_url_configs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_function_url_configs)
        """

    async def list_functions(
        self,
        *,
        MasterRegion: str = ...,
        FunctionVersion: Literal["ALL"] = ...,
        Marker: str = ...,
        MaxItems: int = ...,
    ) -> ListFunctionsResponseTypeDef:
        """
        Returns a list of Lambda functions, with the version-specific configuration of
        each.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_functions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_functions)
        """

    async def list_functions_by_code_signing_config(
        self, *, CodeSigningConfigArn: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListFunctionsByCodeSigningConfigResponseTypeDef:
        """
        List the functions that use the specified code signing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_functions_by_code_signing_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_functions_by_code_signing_config)
        """

    async def list_layer_versions(
        self,
        *,
        LayerName: str,
        CompatibleRuntime: RuntimeType = ...,
        Marker: str = ...,
        MaxItems: int = ...,
        CompatibleArchitecture: ArchitectureType = ...,
    ) -> ListLayerVersionsResponseTypeDef:
        """
        Lists the versions of an [Lambda
        layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_layer_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_layer_versions)
        """

    async def list_layers(
        self,
        *,
        CompatibleRuntime: RuntimeType = ...,
        Marker: str = ...,
        MaxItems: int = ...,
        CompatibleArchitecture: ArchitectureType = ...,
    ) -> ListLayersResponseTypeDef:
        """
        Lists [Lambda
        layers](https://docs.aws.amazon.com/lambda/latest/dg/invocation-layers.html)
        and shows information about the latest version of
        each.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_layers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_layers)
        """

    async def list_provisioned_concurrency_configs(
        self, *, FunctionName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListProvisionedConcurrencyConfigsResponseTypeDef:
        """
        Retrieves a list of provisioned concurrency configurations for a function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_provisioned_concurrency_configs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_provisioned_concurrency_configs)
        """

    async def list_tags(self, *, Resource: str) -> ListTagsResponseTypeDef:
        """
        Returns a function's
        [tags](https://docs.aws.amazon.com/lambda/latest/dg/tagging.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_tags)
        """

    async def list_versions_by_function(
        self, *, FunctionName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListVersionsByFunctionResponseTypeDef:
        """
        Returns a list of
        [versions](https://docs.aws.amazon.com/lambda/latest/dg/versioning-aliases.html),
        with the version-specific configuration of
        each.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_versions_by_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#list_versions_by_function)
        """

    async def publish_layer_version(
        self,
        *,
        LayerName: str,
        Content: LayerVersionContentInputTypeDef,
        Description: str = ...,
        CompatibleRuntimes: Sequence[RuntimeType] = ...,
        LicenseInfo: str = ...,
        CompatibleArchitectures: Sequence[ArchitectureType] = ...,
    ) -> PublishLayerVersionResponseTypeDef:
        """
        Creates an [Lambda
        layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
        from a ZIP
        archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.publish_layer_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#publish_layer_version)
        """

    async def publish_version(
        self,
        *,
        FunctionName: str,
        CodeSha256: str = ...,
        Description: str = ...,
        RevisionId: str = ...,
    ) -> FunctionConfigurationResponseTypeDef:
        """
        Creates a
        [version](https://docs.aws.amazon.com/lambda/latest/dg/versioning-aliases.html)
        from the current code and configuration of a
        function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.publish_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#publish_version)
        """

    async def put_function_code_signing_config(
        self, *, CodeSigningConfigArn: str, FunctionName: str
    ) -> PutFunctionCodeSigningConfigResponseTypeDef:
        """
        Update the code signing configuration for the function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.put_function_code_signing_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#put_function_code_signing_config)
        """

    async def put_function_concurrency(
        self, *, FunctionName: str, ReservedConcurrentExecutions: int
    ) -> ConcurrencyResponseTypeDef:
        """
        Sets the maximum number of simultaneous executions for a function, and reserves
        capacity for that concurrency
        level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.put_function_concurrency)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#put_function_concurrency)
        """

    async def put_function_event_invoke_config(
        self,
        *,
        FunctionName: str,
        Qualifier: str = ...,
        MaximumRetryAttempts: int = ...,
        MaximumEventAgeInSeconds: int = ...,
        DestinationConfig: DestinationConfigTypeDef = ...,
    ) -> FunctionEventInvokeConfigResponseTypeDef:
        """
        Configures options for [asynchronous
        invocation](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html)
        on a function, version, or
        alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.put_function_event_invoke_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#put_function_event_invoke_config)
        """

    async def put_function_recursion_config(
        self, *, FunctionName: str, RecursiveLoop: RecursiveLoopType
    ) -> PutFunctionRecursionConfigResponseTypeDef:
        """
        Sets your function's [recursive loop
        detection](https://docs.aws.amazon.com/lambda/latest/dg/invocation-recursion.html)
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.put_function_recursion_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#put_function_recursion_config)
        """

    async def put_provisioned_concurrency_config(
        self, *, FunctionName: str, Qualifier: str, ProvisionedConcurrentExecutions: int
    ) -> PutProvisionedConcurrencyConfigResponseTypeDef:
        """
        Adds a provisioned concurrency configuration to a function's alias or version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.put_provisioned_concurrency_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#put_provisioned_concurrency_config)
        """

    async def put_runtime_management_config(
        self,
        *,
        FunctionName: str,
        UpdateRuntimeOn: UpdateRuntimeOnType,
        Qualifier: str = ...,
        RuntimeVersionArn: str = ...,
    ) -> PutRuntimeManagementConfigResponseTypeDef:
        """
        Sets the runtime management configuration for a function's version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.put_runtime_management_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#put_runtime_management_config)
        """

    async def remove_layer_version_permission(
        self, *, LayerName: str, VersionNumber: int, StatementId: str, RevisionId: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a statement from the permissions policy for a version of an [Lambda
        layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.remove_layer_version_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#remove_layer_version_permission)
        """

    async def remove_permission(
        self, *, FunctionName: str, StatementId: str, Qualifier: str = ..., RevisionId: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Revokes function-use permission from an Amazon Web Servicesservice or another
        Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.remove_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#remove_permission)
        """

    async def tag_resource(
        self, *, Resource: str, Tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds [tags](https://docs.aws.amazon.com/lambda/latest/dg/tagging.html) to a
        function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#tag_resource)
        """

    async def untag_resource(
        self, *, Resource: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes [tags](https://docs.aws.amazon.com/lambda/latest/dg/tagging.html) from
        a
        function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#untag_resource)
        """

    async def update_alias(
        self,
        *,
        FunctionName: str,
        Name: str,
        FunctionVersion: str = ...,
        Description: str = ...,
        RoutingConfig: AliasRoutingConfigurationUnionTypeDef = ...,
        RevisionId: str = ...,
    ) -> AliasConfigurationResponseTypeDef:
        """
        Updates the configuration of a Lambda function
        [alias](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.update_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#update_alias)
        """

    async def update_code_signing_config(
        self,
        *,
        CodeSigningConfigArn: str,
        Description: str = ...,
        AllowedPublishers: AllowedPublishersUnionTypeDef = ...,
        CodeSigningPolicies: CodeSigningPoliciesTypeDef = ...,
    ) -> UpdateCodeSigningConfigResponseTypeDef:
        """
        Update the code signing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.update_code_signing_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#update_code_signing_config)
        """

    async def update_event_source_mapping(
        self,
        *,
        UUID: str,
        FunctionName: str = ...,
        Enabled: bool = ...,
        BatchSize: int = ...,
        FilterCriteria: FilterCriteriaUnionTypeDef = ...,
        MaximumBatchingWindowInSeconds: int = ...,
        DestinationConfig: DestinationConfigTypeDef = ...,
        MaximumRecordAgeInSeconds: int = ...,
        BisectBatchOnFunctionError: bool = ...,
        MaximumRetryAttempts: int = ...,
        ParallelizationFactor: int = ...,
        SourceAccessConfigurations: Sequence[SourceAccessConfigurationTypeDef] = ...,
        TumblingWindowInSeconds: int = ...,
        FunctionResponseTypes: Sequence[Literal["ReportBatchItemFailures"]] = ...,
        ScalingConfig: ScalingConfigTypeDef = ...,
        DocumentDBEventSourceConfig: DocumentDBEventSourceConfigTypeDef = ...,
        KMSKeyArn: str = ...,
    ) -> EventSourceMappingConfigurationResponseTypeDef:
        """
        Updates an event source mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.update_event_source_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#update_event_source_mapping)
        """

    async def update_function_code(
        self,
        *,
        FunctionName: str,
        ZipFile: BlobTypeDef = ...,
        S3Bucket: str = ...,
        S3Key: str = ...,
        S3ObjectVersion: str = ...,
        ImageUri: str = ...,
        Publish: bool = ...,
        DryRun: bool = ...,
        RevisionId: str = ...,
        Architectures: Sequence[ArchitectureType] = ...,
    ) -> FunctionConfigurationResponseTypeDef:
        """
        Updates a Lambda function's code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.update_function_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#update_function_code)
        """

    async def update_function_configuration(
        self,
        *,
        FunctionName: str,
        Role: str = ...,
        Handler: str = ...,
        Description: str = ...,
        Timeout: int = ...,
        MemorySize: int = ...,
        VpcConfig: VpcConfigTypeDef = ...,
        Environment: EnvironmentTypeDef = ...,
        Runtime: RuntimeType = ...,
        DeadLetterConfig: DeadLetterConfigTypeDef = ...,
        KMSKeyArn: str = ...,
        TracingConfig: TracingConfigTypeDef = ...,
        RevisionId: str = ...,
        Layers: Sequence[str] = ...,
        FileSystemConfigs: Sequence[FileSystemConfigTypeDef] = ...,
        ImageConfig: ImageConfigUnionTypeDef = ...,
        EphemeralStorage: EphemeralStorageTypeDef = ...,
        SnapStart: SnapStartTypeDef = ...,
        LoggingConfig: LoggingConfigTypeDef = ...,
    ) -> FunctionConfigurationResponseTypeDef:
        """
        Modify the version-specific settings of a Lambda function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.update_function_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#update_function_configuration)
        """

    async def update_function_event_invoke_config(
        self,
        *,
        FunctionName: str,
        Qualifier: str = ...,
        MaximumRetryAttempts: int = ...,
        MaximumEventAgeInSeconds: int = ...,
        DestinationConfig: DestinationConfigTypeDef = ...,
    ) -> FunctionEventInvokeConfigResponseTypeDef:
        """
        Updates the configuration for asynchronous invocation for a function, version,
        or
        alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.update_function_event_invoke_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#update_function_event_invoke_config)
        """

    async def update_function_url_config(
        self,
        *,
        FunctionName: str,
        Qualifier: str = ...,
        AuthType: FunctionUrlAuthTypeType = ...,
        Cors: CorsUnionTypeDef = ...,
        InvokeMode: InvokeModeType = ...,
    ) -> UpdateFunctionUrlConfigResponseTypeDef:
        """
        Updates the configuration for a Lambda function URL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.update_function_url_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#update_function_url_config)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_code_signing_configs"]
    ) -> ListCodeSigningConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_source_mappings"]
    ) -> ListEventSourceMappingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_function_event_invoke_configs"]
    ) -> ListFunctionEventInvokeConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_function_url_configs"]
    ) -> ListFunctionUrlConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_functions"]) -> ListFunctionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_functions_by_code_signing_config"]
    ) -> ListFunctionsByCodeSigningConfigPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_layer_versions"]
    ) -> ListLayerVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_layers"]) -> ListLayersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioned_concurrency_configs"]
    ) -> ListProvisionedConcurrencyConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_versions_by_function"]
    ) -> ListVersionsByFunctionPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["function_active"]) -> FunctionActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["function_active_v2"]) -> FunctionActiveV2Waiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["function_exists"]) -> FunctionExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["function_updated"]) -> FunctionUpdatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["function_updated_v2"]) -> FunctionUpdatedV2Waiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["published_version_active"]
    ) -> PublishedVersionActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/#get_waiter)
        """

    async def __aenter__(self) -> "LambdaClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/client/)
        """
