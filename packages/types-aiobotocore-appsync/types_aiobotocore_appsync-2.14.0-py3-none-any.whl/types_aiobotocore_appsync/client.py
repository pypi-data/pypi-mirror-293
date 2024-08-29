"""
Type annotations for appsync service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appsync.client import AppSyncClient

    session = get_session()
    async with session.create_client("appsync") as client:
        client: AppSyncClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ApiCacheTypeType,
    ApiCachingBehaviorType,
    AuthenticationTypeType,
    CacheHealthMetricsConfigType,
    DataSourceLevelMetricsConfigType,
    DataSourceTypeType,
    GraphQLApiIntrospectionConfigType,
    GraphQLApiTypeType,
    GraphQLApiVisibilityType,
    OutputTypeType,
    OwnershipType,
    ResolverKindType,
    ResolverLevelMetricsConfigType,
    TypeDefinitionFormatType,
)
from .paginator import (
    ListApiKeysPaginator,
    ListDataSourcesPaginator,
    ListDomainNamesPaginator,
    ListFunctionsPaginator,
    ListGraphqlApisPaginator,
    ListResolversByFunctionPaginator,
    ListResolversPaginator,
    ListSourceApiAssociationsPaginator,
    ListTypesByAssociationPaginator,
    ListTypesPaginator,
)
from .type_defs import (
    AdditionalAuthenticationProviderTypeDef,
    AppSyncRuntimeTypeDef,
    AssociateApiResponseTypeDef,
    AssociateMergedGraphqlApiResponseTypeDef,
    AssociateSourceGraphqlApiResponseTypeDef,
    BlobTypeDef,
    CachingConfigUnionTypeDef,
    CreateApiCacheResponseTypeDef,
    CreateApiKeyResponseTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateDomainNameResponseTypeDef,
    CreateFunctionResponseTypeDef,
    CreateGraphqlApiResponseTypeDef,
    CreateResolverResponseTypeDef,
    CreateTypeResponseTypeDef,
    DisassociateMergedGraphqlApiResponseTypeDef,
    DisassociateSourceGraphqlApiResponseTypeDef,
    DynamodbDataSourceConfigTypeDef,
    ElasticsearchDataSourceConfigTypeDef,
    EnhancedMetricsConfigTypeDef,
    EvaluateCodeResponseTypeDef,
    EvaluateMappingTemplateResponseTypeDef,
    EventBridgeDataSourceConfigTypeDef,
    GetApiAssociationResponseTypeDef,
    GetApiCacheResponseTypeDef,
    GetDataSourceIntrospectionResponseTypeDef,
    GetDataSourceResponseTypeDef,
    GetDomainNameResponseTypeDef,
    GetFunctionResponseTypeDef,
    GetGraphqlApiEnvironmentVariablesResponseTypeDef,
    GetGraphqlApiResponseTypeDef,
    GetIntrospectionSchemaResponseTypeDef,
    GetResolverResponseTypeDef,
    GetSchemaCreationStatusResponseTypeDef,
    GetSourceApiAssociationResponseTypeDef,
    GetTypeResponseTypeDef,
    HttpDataSourceConfigTypeDef,
    LambdaAuthorizerConfigTypeDef,
    LambdaDataSourceConfigTypeDef,
    ListApiKeysResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDomainNamesResponseTypeDef,
    ListFunctionsResponseTypeDef,
    ListGraphqlApisResponseTypeDef,
    ListResolversByFunctionResponseTypeDef,
    ListResolversResponseTypeDef,
    ListSourceApiAssociationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypesByAssociationResponseTypeDef,
    ListTypesResponseTypeDef,
    LogConfigTypeDef,
    OpenIDConnectConfigTypeDef,
    OpenSearchServiceDataSourceConfigTypeDef,
    PipelineConfigUnionTypeDef,
    PutGraphqlApiEnvironmentVariablesResponseTypeDef,
    RdsDataApiConfigTypeDef,
    RelationalDatabaseDataSourceConfigTypeDef,
    SourceApiAssociationConfigTypeDef,
    StartDataSourceIntrospectionResponseTypeDef,
    StartSchemaCreationResponseTypeDef,
    StartSchemaMergeResponseTypeDef,
    SyncConfigTypeDef,
    UpdateApiCacheResponseTypeDef,
    UpdateApiKeyResponseTypeDef,
    UpdateDataSourceResponseTypeDef,
    UpdateDomainNameResponseTypeDef,
    UpdateFunctionResponseTypeDef,
    UpdateGraphqlApiResponseTypeDef,
    UpdateResolverResponseTypeDef,
    UpdateSourceApiAssociationResponseTypeDef,
    UpdateTypeResponseTypeDef,
    UserPoolConfigTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("AppSyncClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ApiKeyLimitExceededException: Type[BotocoreClientError]
    ApiKeyValidityOutOfBoundsException: Type[BotocoreClientError]
    ApiLimitExceededException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    GraphQLSchemaException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class AppSyncClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppSyncClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#exceptions)
        """

    async def associate_api(self, *, domainName: str, apiId: str) -> AssociateApiResponseTypeDef:
        """
        Maps an endpoint to your custom domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.associate_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#associate_api)
        """

    async def associate_merged_graphql_api(
        self,
        *,
        sourceApiIdentifier: str,
        mergedApiIdentifier: str,
        description: str = ...,
        sourceApiAssociationConfig: SourceApiAssociationConfigTypeDef = ...,
    ) -> AssociateMergedGraphqlApiResponseTypeDef:
        """
        Creates an association between a Merged API and source API using the source
        API's
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.associate_merged_graphql_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#associate_merged_graphql_api)
        """

    async def associate_source_graphql_api(
        self,
        *,
        mergedApiIdentifier: str,
        sourceApiIdentifier: str,
        description: str = ...,
        sourceApiAssociationConfig: SourceApiAssociationConfigTypeDef = ...,
    ) -> AssociateSourceGraphqlApiResponseTypeDef:
        """
        Creates an association between a Merged API and source API using the Merged
        API's
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.associate_source_graphql_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#associate_source_graphql_api)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#close)
        """

    async def create_api_cache(
        self,
        *,
        apiId: str,
        ttl: int,
        apiCachingBehavior: ApiCachingBehaviorType,
        type: ApiCacheTypeType,
        transitEncryptionEnabled: bool = ...,
        atRestEncryptionEnabled: bool = ...,
        healthMetricsConfig: CacheHealthMetricsConfigType = ...,
    ) -> CreateApiCacheResponseTypeDef:
        """
        Creates a cache for the GraphQL API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_api_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#create_api_cache)
        """

    async def create_api_key(
        self, *, apiId: str, description: str = ..., expires: int = ...
    ) -> CreateApiKeyResponseTypeDef:
        """
        Creates a unique key that you can distribute to clients who invoke your API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_api_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#create_api_key)
        """

    async def create_data_source(
        self,
        *,
        apiId: str,
        name: str,
        type: DataSourceTypeType,
        description: str = ...,
        serviceRoleArn: str = ...,
        dynamodbConfig: DynamodbDataSourceConfigTypeDef = ...,
        lambdaConfig: LambdaDataSourceConfigTypeDef = ...,
        elasticsearchConfig: ElasticsearchDataSourceConfigTypeDef = ...,
        openSearchServiceConfig: OpenSearchServiceDataSourceConfigTypeDef = ...,
        httpConfig: HttpDataSourceConfigTypeDef = ...,
        relationalDatabaseConfig: RelationalDatabaseDataSourceConfigTypeDef = ...,
        eventBridgeConfig: EventBridgeDataSourceConfigTypeDef = ...,
        metricsConfig: DataSourceLevelMetricsConfigType = ...,
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a `DataSource` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#create_data_source)
        """

    async def create_domain_name(
        self, *, domainName: str, certificateArn: str, description: str = ...
    ) -> CreateDomainNameResponseTypeDef:
        """
        Creates a custom `DomainName` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_domain_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#create_domain_name)
        """

    async def create_function(
        self,
        *,
        apiId: str,
        name: str,
        dataSourceName: str,
        description: str = ...,
        requestMappingTemplate: str = ...,
        responseMappingTemplate: str = ...,
        functionVersion: str = ...,
        syncConfig: SyncConfigTypeDef = ...,
        maxBatchSize: int = ...,
        runtime: AppSyncRuntimeTypeDef = ...,
        code: str = ...,
    ) -> CreateFunctionResponseTypeDef:
        """
        Creates a `Function` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#create_function)
        """

    async def create_graphql_api(
        self,
        *,
        name: str,
        authenticationType: AuthenticationTypeType,
        logConfig: LogConfigTypeDef = ...,
        userPoolConfig: UserPoolConfigTypeDef = ...,
        openIDConnectConfig: OpenIDConnectConfigTypeDef = ...,
        tags: Mapping[str, str] = ...,
        additionalAuthenticationProviders: Sequence[AdditionalAuthenticationProviderTypeDef] = ...,
        xrayEnabled: bool = ...,
        lambdaAuthorizerConfig: LambdaAuthorizerConfigTypeDef = ...,
        visibility: GraphQLApiVisibilityType = ...,
        apiType: GraphQLApiTypeType = ...,
        mergedApiExecutionRoleArn: str = ...,
        ownerContact: str = ...,
        introspectionConfig: GraphQLApiIntrospectionConfigType = ...,
        queryDepthLimit: int = ...,
        resolverCountLimit: int = ...,
        enhancedMetricsConfig: EnhancedMetricsConfigTypeDef = ...,
    ) -> CreateGraphqlApiResponseTypeDef:
        """
        Creates a `GraphqlApi` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_graphql_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#create_graphql_api)
        """

    async def create_resolver(
        self,
        *,
        apiId: str,
        typeName: str,
        fieldName: str,
        dataSourceName: str = ...,
        requestMappingTemplate: str = ...,
        responseMappingTemplate: str = ...,
        kind: ResolverKindType = ...,
        pipelineConfig: PipelineConfigUnionTypeDef = ...,
        syncConfig: SyncConfigTypeDef = ...,
        cachingConfig: CachingConfigUnionTypeDef = ...,
        maxBatchSize: int = ...,
        runtime: AppSyncRuntimeTypeDef = ...,
        code: str = ...,
        metricsConfig: ResolverLevelMetricsConfigType = ...,
    ) -> CreateResolverResponseTypeDef:
        """
        Creates a `Resolver` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_resolver)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#create_resolver)
        """

    async def create_type(
        self, *, apiId: str, definition: str, format: TypeDefinitionFormatType
    ) -> CreateTypeResponseTypeDef:
        """
        Creates a `Type` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.create_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#create_type)
        """

    async def delete_api_cache(self, *, apiId: str) -> Dict[str, Any]:
        """
        Deletes an `ApiCache` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_api_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#delete_api_cache)
        """

    async def delete_api_key(self, *, apiId: str, id: str) -> Dict[str, Any]:
        """
        Deletes an API key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_api_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#delete_api_key)
        """

    async def delete_data_source(self, *, apiId: str, name: str) -> Dict[str, Any]:
        """
        Deletes a `DataSource` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#delete_data_source)
        """

    async def delete_domain_name(self, *, domainName: str) -> Dict[str, Any]:
        """
        Deletes a custom `DomainName` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_domain_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#delete_domain_name)
        """

    async def delete_function(self, *, apiId: str, functionId: str) -> Dict[str, Any]:
        """
        Deletes a `Function`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#delete_function)
        """

    async def delete_graphql_api(self, *, apiId: str) -> Dict[str, Any]:
        """
        Deletes a `GraphqlApi` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_graphql_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#delete_graphql_api)
        """

    async def delete_resolver(self, *, apiId: str, typeName: str, fieldName: str) -> Dict[str, Any]:
        """
        Deletes a `Resolver` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_resolver)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#delete_resolver)
        """

    async def delete_type(self, *, apiId: str, typeName: str) -> Dict[str, Any]:
        """
        Deletes a `Type` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.delete_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#delete_type)
        """

    async def disassociate_api(self, *, domainName: str) -> Dict[str, Any]:
        """
        Removes an `ApiAssociation` object from a custom domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.disassociate_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#disassociate_api)
        """

    async def disassociate_merged_graphql_api(
        self, *, sourceApiIdentifier: str, associationId: str
    ) -> DisassociateMergedGraphqlApiResponseTypeDef:
        """
        Deletes an association between a Merged API and source API using the source
        API's identifier and the association
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.disassociate_merged_graphql_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#disassociate_merged_graphql_api)
        """

    async def disassociate_source_graphql_api(
        self, *, mergedApiIdentifier: str, associationId: str
    ) -> DisassociateSourceGraphqlApiResponseTypeDef:
        """
        Deletes an association between a Merged API and source API using the Merged
        API's identifier and the association
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.disassociate_source_graphql_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#disassociate_source_graphql_api)
        """

    async def evaluate_code(
        self, *, runtime: AppSyncRuntimeTypeDef, code: str, context: str, function: str = ...
    ) -> EvaluateCodeResponseTypeDef:
        """
        Evaluates the given code and returns the response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.evaluate_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#evaluate_code)
        """

    async def evaluate_mapping_template(
        self, *, template: str, context: str
    ) -> EvaluateMappingTemplateResponseTypeDef:
        """
        Evaluates a given template and returns the response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.evaluate_mapping_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#evaluate_mapping_template)
        """

    async def flush_api_cache(self, *, apiId: str) -> Dict[str, Any]:
        """
        Flushes an `ApiCache` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.flush_api_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#flush_api_cache)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#generate_presigned_url)
        """

    async def get_api_association(self, *, domainName: str) -> GetApiAssociationResponseTypeDef:
        """
        Retrieves an `ApiAssociation` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_api_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_api_association)
        """

    async def get_api_cache(self, *, apiId: str) -> GetApiCacheResponseTypeDef:
        """
        Retrieves an `ApiCache` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_api_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_api_cache)
        """

    async def get_data_source(self, *, apiId: str, name: str) -> GetDataSourceResponseTypeDef:
        """
        Retrieves a `DataSource` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_data_source)
        """

    async def get_data_source_introspection(
        self,
        *,
        introspectionId: str,
        includeModelsSDL: bool = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> GetDataSourceIntrospectionResponseTypeDef:
        """
        Retrieves the record of an existing introspection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_data_source_introspection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_data_source_introspection)
        """

    async def get_domain_name(self, *, domainName: str) -> GetDomainNameResponseTypeDef:
        """
        Retrieves a custom `DomainName` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_domain_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_domain_name)
        """

    async def get_function(self, *, apiId: str, functionId: str) -> GetFunctionResponseTypeDef:
        """
        Get a `Function`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_function)
        """

    async def get_graphql_api(self, *, apiId: str) -> GetGraphqlApiResponseTypeDef:
        """
        Retrieves a `GraphqlApi` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_graphql_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_graphql_api)
        """

    async def get_graphql_api_environment_variables(
        self, *, apiId: str
    ) -> GetGraphqlApiEnvironmentVariablesResponseTypeDef:
        """
        Retrieves the list of environmental variable key-value pairs associated with an
        API by its ID
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_graphql_api_environment_variables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_graphql_api_environment_variables)
        """

    async def get_introspection_schema(
        self, *, apiId: str, format: OutputTypeType, includeDirectives: bool = ...
    ) -> GetIntrospectionSchemaResponseTypeDef:
        """
        Retrieves the introspection schema for a GraphQL API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_introspection_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_introspection_schema)
        """

    async def get_resolver(
        self, *, apiId: str, typeName: str, fieldName: str
    ) -> GetResolverResponseTypeDef:
        """
        Retrieves a `Resolver` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_resolver)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_resolver)
        """

    async def get_schema_creation_status(
        self, *, apiId: str
    ) -> GetSchemaCreationStatusResponseTypeDef:
        """
        Retrieves the current status of a schema creation operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_schema_creation_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_schema_creation_status)
        """

    async def get_source_api_association(
        self, *, mergedApiIdentifier: str, associationId: str
    ) -> GetSourceApiAssociationResponseTypeDef:
        """
        Retrieves a `SourceApiAssociation` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_source_api_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_source_api_association)
        """

    async def get_type(
        self, *, apiId: str, typeName: str, format: TypeDefinitionFormatType
    ) -> GetTypeResponseTypeDef:
        """
        Retrieves a `Type` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_type)
        """

    async def list_api_keys(
        self, *, apiId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListApiKeysResponseTypeDef:
        """
        Lists the API keys for a given API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_api_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_api_keys)
        """

    async def list_data_sources(
        self, *, apiId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists the data sources for a given API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_data_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_data_sources)
        """

    async def list_domain_names(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListDomainNamesResponseTypeDef:
        """
        Lists multiple custom domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_domain_names)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_domain_names)
        """

    async def list_functions(
        self, *, apiId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListFunctionsResponseTypeDef:
        """
        List multiple functions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_functions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_functions)
        """

    async def list_graphql_apis(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        apiType: GraphQLApiTypeType = ...,
        owner: OwnershipType = ...,
    ) -> ListGraphqlApisResponseTypeDef:
        """
        Lists your GraphQL APIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_graphql_apis)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_graphql_apis)
        """

    async def list_resolvers(
        self, *, apiId: str, typeName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListResolversResponseTypeDef:
        """
        Lists the resolvers for a given API and type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_resolvers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_resolvers)
        """

    async def list_resolvers_by_function(
        self, *, apiId: str, functionId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListResolversByFunctionResponseTypeDef:
        """
        List the resolvers that are associated with a specific function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_resolvers_by_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_resolvers_by_function)
        """

    async def list_source_api_associations(
        self, *, apiId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListSourceApiAssociationsResponseTypeDef:
        """
        Lists the `SourceApiAssociationSummary` data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_source_api_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_source_api_associations)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_tags_for_resource)
        """

    async def list_types(
        self,
        *,
        apiId: str,
        format: TypeDefinitionFormatType,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListTypesResponseTypeDef:
        """
        Lists the types for a given API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_types)
        """

    async def list_types_by_association(
        self,
        *,
        mergedApiIdentifier: str,
        associationId: str,
        format: TypeDefinitionFormatType,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListTypesByAssociationResponseTypeDef:
        """
        Lists `Type` objects by the source API association ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.list_types_by_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#list_types_by_association)
        """

    async def put_graphql_api_environment_variables(
        self, *, apiId: str, environmentVariables: Mapping[str, str]
    ) -> PutGraphqlApiEnvironmentVariablesResponseTypeDef:
        """
        Creates a list of environmental variables in an API by its ID value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.put_graphql_api_environment_variables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#put_graphql_api_environment_variables)
        """

    async def start_data_source_introspection(
        self, *, rdsDataApiConfig: RdsDataApiConfigTypeDef = ...
    ) -> StartDataSourceIntrospectionResponseTypeDef:
        """
        Creates a new introspection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.start_data_source_introspection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#start_data_source_introspection)
        """

    async def start_schema_creation(
        self, *, apiId: str, definition: BlobTypeDef
    ) -> StartSchemaCreationResponseTypeDef:
        """
        Adds a new schema to your GraphQL API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.start_schema_creation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#start_schema_creation)
        """

    async def start_schema_merge(
        self, *, associationId: str, mergedApiIdentifier: str
    ) -> StartSchemaMergeResponseTypeDef:
        """
        Initiates a merge operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.start_schema_merge)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#start_schema_merge)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tags a resource with user-supplied tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Untags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#untag_resource)
        """

    async def update_api_cache(
        self,
        *,
        apiId: str,
        ttl: int,
        apiCachingBehavior: ApiCachingBehaviorType,
        type: ApiCacheTypeType,
        healthMetricsConfig: CacheHealthMetricsConfigType = ...,
    ) -> UpdateApiCacheResponseTypeDef:
        """
        Updates the cache for the GraphQL API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_api_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#update_api_cache)
        """

    async def update_api_key(
        self, *, apiId: str, id: str, description: str = ..., expires: int = ...
    ) -> UpdateApiKeyResponseTypeDef:
        """
        Updates an API key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_api_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#update_api_key)
        """

    async def update_data_source(
        self,
        *,
        apiId: str,
        name: str,
        type: DataSourceTypeType,
        description: str = ...,
        serviceRoleArn: str = ...,
        dynamodbConfig: DynamodbDataSourceConfigTypeDef = ...,
        lambdaConfig: LambdaDataSourceConfigTypeDef = ...,
        elasticsearchConfig: ElasticsearchDataSourceConfigTypeDef = ...,
        openSearchServiceConfig: OpenSearchServiceDataSourceConfigTypeDef = ...,
        httpConfig: HttpDataSourceConfigTypeDef = ...,
        relationalDatabaseConfig: RelationalDatabaseDataSourceConfigTypeDef = ...,
        eventBridgeConfig: EventBridgeDataSourceConfigTypeDef = ...,
        metricsConfig: DataSourceLevelMetricsConfigType = ...,
    ) -> UpdateDataSourceResponseTypeDef:
        """
        Updates a `DataSource` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#update_data_source)
        """

    async def update_domain_name(
        self, *, domainName: str, description: str = ...
    ) -> UpdateDomainNameResponseTypeDef:
        """
        Updates a custom `DomainName` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_domain_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#update_domain_name)
        """

    async def update_function(
        self,
        *,
        apiId: str,
        name: str,
        functionId: str,
        dataSourceName: str,
        description: str = ...,
        requestMappingTemplate: str = ...,
        responseMappingTemplate: str = ...,
        functionVersion: str = ...,
        syncConfig: SyncConfigTypeDef = ...,
        maxBatchSize: int = ...,
        runtime: AppSyncRuntimeTypeDef = ...,
        code: str = ...,
    ) -> UpdateFunctionResponseTypeDef:
        """
        Updates a `Function` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#update_function)
        """

    async def update_graphql_api(
        self,
        *,
        apiId: str,
        name: str,
        authenticationType: AuthenticationTypeType,
        logConfig: LogConfigTypeDef = ...,
        userPoolConfig: UserPoolConfigTypeDef = ...,
        openIDConnectConfig: OpenIDConnectConfigTypeDef = ...,
        additionalAuthenticationProviders: Sequence[AdditionalAuthenticationProviderTypeDef] = ...,
        xrayEnabled: bool = ...,
        lambdaAuthorizerConfig: LambdaAuthorizerConfigTypeDef = ...,
        mergedApiExecutionRoleArn: str = ...,
        ownerContact: str = ...,
        introspectionConfig: GraphQLApiIntrospectionConfigType = ...,
        queryDepthLimit: int = ...,
        resolverCountLimit: int = ...,
        enhancedMetricsConfig: EnhancedMetricsConfigTypeDef = ...,
    ) -> UpdateGraphqlApiResponseTypeDef:
        """
        Updates a `GraphqlApi` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_graphql_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#update_graphql_api)
        """

    async def update_resolver(
        self,
        *,
        apiId: str,
        typeName: str,
        fieldName: str,
        dataSourceName: str = ...,
        requestMappingTemplate: str = ...,
        responseMappingTemplate: str = ...,
        kind: ResolverKindType = ...,
        pipelineConfig: PipelineConfigUnionTypeDef = ...,
        syncConfig: SyncConfigTypeDef = ...,
        cachingConfig: CachingConfigUnionTypeDef = ...,
        maxBatchSize: int = ...,
        runtime: AppSyncRuntimeTypeDef = ...,
        code: str = ...,
        metricsConfig: ResolverLevelMetricsConfigType = ...,
    ) -> UpdateResolverResponseTypeDef:
        """
        Updates a `Resolver` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_resolver)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#update_resolver)
        """

    async def update_source_api_association(
        self,
        *,
        associationId: str,
        mergedApiIdentifier: str,
        description: str = ...,
        sourceApiAssociationConfig: SourceApiAssociationConfigTypeDef = ...,
    ) -> UpdateSourceApiAssociationResponseTypeDef:
        """
        Updates some of the configuration choices of a particular source API
        association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_source_api_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#update_source_api_association)
        """

    async def update_type(
        self, *, apiId: str, typeName: str, format: TypeDefinitionFormatType, definition: str = ...
    ) -> UpdateTypeResponseTypeDef:
        """
        Updates a `Type` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.update_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#update_type)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_api_keys"]) -> ListApiKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_domain_names"]
    ) -> ListDomainNamesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_functions"]) -> ListFunctionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_graphql_apis"]
    ) -> ListGraphqlApisPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_resolvers"]) -> ListResolversPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resolvers_by_function"]
    ) -> ListResolversByFunctionPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_source_api_associations"]
    ) -> ListSourceApiAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_types"]) -> ListTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_types_by_association"]
    ) -> ListTypesByAssociationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/#get_paginator)
        """

    async def __aenter__(self) -> "AppSyncClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/client/)
        """
