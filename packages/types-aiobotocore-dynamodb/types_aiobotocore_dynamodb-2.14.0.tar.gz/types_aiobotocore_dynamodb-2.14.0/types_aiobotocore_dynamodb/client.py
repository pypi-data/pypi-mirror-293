"""
Type annotations for dynamodb service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_dynamodb.client import DynamoDBClient

    session = get_session()
    async with session.create_client("dynamodb") as client:
        client: DynamoDBClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    BackupTypeFilterType,
    BillingModeType,
    ConditionalOperatorType,
    ContributorInsightsActionType,
    ExportFormatType,
    ExportTypeType,
    InputCompressionTypeType,
    InputFormatType,
    ReturnConsumedCapacityType,
    ReturnItemCollectionMetricsType,
    ReturnValuesOnConditionCheckFailureType,
    ReturnValueType,
    S3SseAlgorithmType,
    SelectType,
    TableClassType,
)
from .paginator import (
    ListBackupsPaginator,
    ListTablesPaginator,
    ListTagsOfResourcePaginator,
    QueryPaginator,
    ScanPaginator,
)
from .type_defs import (
    AttributeDefinitionTypeDef,
    AttributeValueUpdateTypeDef,
    AutoScalingSettingsUpdateTypeDef,
    BatchExecuteStatementOutputTypeDef,
    BatchGetItemOutputTypeDef,
    BatchStatementRequestTypeDef,
    BatchWriteItemOutputTypeDef,
    ConditionTypeDef,
    CreateBackupOutputTypeDef,
    CreateGlobalTableOutputTypeDef,
    CreateTableOutputTypeDef,
    DeleteBackupOutputTypeDef,
    DeleteItemOutputTypeDef,
    DeleteResourcePolicyOutputTypeDef,
    DeleteTableOutputTypeDef,
    DescribeBackupOutputTypeDef,
    DescribeContinuousBackupsOutputTypeDef,
    DescribeContributorInsightsOutputTypeDef,
    DescribeEndpointsResponseTypeDef,
    DescribeExportOutputTypeDef,
    DescribeGlobalTableOutputTypeDef,
    DescribeGlobalTableSettingsOutputTypeDef,
    DescribeImportOutputTypeDef,
    DescribeKinesisStreamingDestinationOutputTypeDef,
    DescribeLimitsOutputTypeDef,
    DescribeTableOutputTypeDef,
    DescribeTableReplicaAutoScalingOutputTypeDef,
    DescribeTimeToLiveOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableKinesisStreamingConfigurationTypeDef,
    ExecuteStatementOutputTypeDef,
    ExecuteTransactionOutputTypeDef,
    ExpectedAttributeValueTypeDef,
    ExportTableToPointInTimeOutputTypeDef,
    GetItemOutputTypeDef,
    GetResourcePolicyOutputTypeDef,
    GlobalSecondaryIndexAutoScalingUpdateTypeDef,
    GlobalSecondaryIndexUnionTypeDef,
    GlobalSecondaryIndexUpdateTypeDef,
    GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef,
    ImportTableOutputTypeDef,
    IncrementalExportSpecificationUnionTypeDef,
    InputFormatOptionsUnionTypeDef,
    KeysAndAttributesUnionTypeDef,
    KeySchemaElementTypeDef,
    KinesisStreamingDestinationOutputTypeDef,
    ListBackupsOutputTypeDef,
    ListContributorInsightsOutputTypeDef,
    ListExportsOutputTypeDef,
    ListGlobalTablesOutputTypeDef,
    ListImportsOutputTypeDef,
    ListTablesOutputTypeDef,
    ListTagsOfResourceOutputTypeDef,
    LocalSecondaryIndexTypeDef,
    OnDemandThroughputTypeDef,
    ParameterizedStatementTypeDef,
    PointInTimeRecoverySpecificationTypeDef,
    ProvisionedThroughputTypeDef,
    PutItemOutputTypeDef,
    PutResourcePolicyOutputTypeDef,
    QueryOutputTypeDef,
    ReplicaAutoScalingUpdateTypeDef,
    ReplicaSettingsUpdateTypeDef,
    ReplicationGroupUpdateTypeDef,
    ReplicaTypeDef,
    ReplicaUpdateTypeDef,
    RestoreTableFromBackupOutputTypeDef,
    RestoreTableToPointInTimeOutputTypeDef,
    S3BucketSourceTypeDef,
    ScanOutputTypeDef,
    SSESpecificationTypeDef,
    StreamSpecificationTypeDef,
    TableCreationParametersUnionTypeDef,
    TagTypeDef,
    TimestampTypeDef,
    TimeToLiveSpecificationTypeDef,
    TransactGetItemsOutputTypeDef,
    TransactGetItemTypeDef,
    TransactWriteItemsOutputTypeDef,
    TransactWriteItemTypeDef,
    UniversalAttributeValueTypeDef,
    UpdateContinuousBackupsOutputTypeDef,
    UpdateContributorInsightsOutputTypeDef,
    UpdateGlobalTableOutputTypeDef,
    UpdateGlobalTableSettingsOutputTypeDef,
    UpdateItemOutputTypeDef,
    UpdateKinesisStreamingConfigurationTypeDef,
    UpdateKinesisStreamingDestinationOutputTypeDef,
    UpdateTableOutputTypeDef,
    UpdateTableReplicaAutoScalingOutputTypeDef,
    UpdateTimeToLiveOutputTypeDef,
    WriteRequestUnionTypeDef,
)
from .waiter import TableExistsWaiter, TableNotExistsWaiter

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DynamoDBClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BackupInUseException: Type[BotocoreClientError]
    BackupNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConditionalCheckFailedException: Type[BotocoreClientError]
    ContinuousBackupsUnavailableException: Type[BotocoreClientError]
    DuplicateItemException: Type[BotocoreClientError]
    ExportConflictException: Type[BotocoreClientError]
    ExportNotFoundException: Type[BotocoreClientError]
    GlobalTableAlreadyExistsException: Type[BotocoreClientError]
    GlobalTableNotFoundException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    ImportConflictException: Type[BotocoreClientError]
    ImportNotFoundException: Type[BotocoreClientError]
    IndexNotFoundException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidExportTimeException: Type[BotocoreClientError]
    InvalidRestoreTimeException: Type[BotocoreClientError]
    ItemCollectionSizeLimitExceededException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    PointInTimeRecoveryUnavailableException: Type[BotocoreClientError]
    PolicyNotFoundException: Type[BotocoreClientError]
    ProvisionedThroughputExceededException: Type[BotocoreClientError]
    ReplicaAlreadyExistsException: Type[BotocoreClientError]
    ReplicaNotFoundException: Type[BotocoreClientError]
    RequestLimitExceeded: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TableAlreadyExistsException: Type[BotocoreClientError]
    TableInUseException: Type[BotocoreClientError]
    TableNotFoundException: Type[BotocoreClientError]
    TransactionCanceledException: Type[BotocoreClientError]
    TransactionConflictException: Type[BotocoreClientError]
    TransactionInProgressException: Type[BotocoreClientError]


class DynamoDBClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DynamoDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#exceptions)
        """

    async def batch_execute_statement(
        self,
        *,
        Statements: Sequence[BatchStatementRequestTypeDef],
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
    ) -> BatchExecuteStatementOutputTypeDef:
        """
        This operation allows you to perform batch reads or writes on data stored in
        DynamoDB, using
        PartiQL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.batch_execute_statement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#batch_execute_statement)
        """

    async def batch_get_item(
        self,
        *,
        RequestItems: Mapping[str, KeysAndAttributesUnionTypeDef],
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
    ) -> BatchGetItemOutputTypeDef:
        """
        The `BatchGetItem` operation returns the attributes of one or more items from
        one or more
        tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.batch_get_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#batch_get_item)
        """

    async def batch_write_item(
        self,
        *,
        RequestItems: Mapping[str, Sequence[WriteRequestUnionTypeDef]],
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        ReturnItemCollectionMetrics: ReturnItemCollectionMetricsType = ...,
    ) -> BatchWriteItemOutputTypeDef:
        """
        The `BatchWriteItem` operation puts or deletes multiple items in one or more
        tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.batch_write_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#batch_write_item)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#close)
        """

    async def create_backup(self, *, TableName: str, BackupName: str) -> CreateBackupOutputTypeDef:
        """
        Creates a backup for an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_backup)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#create_backup)
        """

    async def create_global_table(
        self, *, GlobalTableName: str, ReplicationGroup: Sequence[ReplicaTypeDef]
    ) -> CreateGlobalTableOutputTypeDef:
        """
        Creates a global table from an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_global_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#create_global_table)
        """

    async def create_table(
        self,
        *,
        AttributeDefinitions: Sequence[AttributeDefinitionTypeDef],
        TableName: str,
        KeySchema: Sequence[KeySchemaElementTypeDef],
        LocalSecondaryIndexes: Sequence[LocalSecondaryIndexTypeDef] = ...,
        GlobalSecondaryIndexes: Sequence[GlobalSecondaryIndexUnionTypeDef] = ...,
        BillingMode: BillingModeType = ...,
        ProvisionedThroughput: ProvisionedThroughputTypeDef = ...,
        StreamSpecification: StreamSpecificationTypeDef = ...,
        SSESpecification: SSESpecificationTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
        TableClass: TableClassType = ...,
        DeletionProtectionEnabled: bool = ...,
        ResourcePolicy: str = ...,
        OnDemandThroughput: OnDemandThroughputTypeDef = ...,
    ) -> CreateTableOutputTypeDef:
        """
        The `CreateTable` operation adds a new table to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#create_table)
        """

    async def delete_backup(self, *, BackupArn: str) -> DeleteBackupOutputTypeDef:
        """
        Deletes an existing backup of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_backup)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#delete_backup)
        """

    async def delete_item(
        self,
        *,
        TableName: str,
        Key: Mapping[str, UniversalAttributeValueTypeDef],
        Expected: Mapping[str, ExpectedAttributeValueTypeDef] = ...,
        ConditionalOperator: ConditionalOperatorType = ...,
        ReturnValues: ReturnValueType = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        ReturnItemCollectionMetrics: ReturnItemCollectionMetricsType = ...,
        ConditionExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
        ExpressionAttributeValues: Mapping[str, UniversalAttributeValueTypeDef] = ...,
        ReturnValuesOnConditionCheckFailure: ReturnValuesOnConditionCheckFailureType = ...,
    ) -> DeleteItemOutputTypeDef:
        """
        Deletes a single item in a table by primary key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#delete_item)
        """

    async def delete_resource_policy(
        self, *, ResourceArn: str, ExpectedRevisionId: str = ...
    ) -> DeleteResourcePolicyOutputTypeDef:
        """
        Deletes the resource-based policy attached to the resource, which can be a
        table or
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#delete_resource_policy)
        """

    async def delete_table(self, *, TableName: str) -> DeleteTableOutputTypeDef:
        """
        The `DeleteTable` operation deletes a table and all of its items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#delete_table)
        """

    async def describe_backup(self, *, BackupArn: str) -> DescribeBackupOutputTypeDef:
        """
        Describes an existing backup of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_backup)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_backup)
        """

    async def describe_continuous_backups(
        self, *, TableName: str
    ) -> DescribeContinuousBackupsOutputTypeDef:
        """
        Checks the status of continuous backups and point in time recovery on the
        specified
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_continuous_backups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_continuous_backups)
        """

    async def describe_contributor_insights(
        self, *, TableName: str, IndexName: str = ...
    ) -> DescribeContributorInsightsOutputTypeDef:
        """
        Returns information about contributor insights for a given table or global
        secondary
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_contributor_insights)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_contributor_insights)
        """

    async def describe_endpoints(self) -> DescribeEndpointsResponseTypeDef:
        """
        Returns the regional endpoint information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_endpoints)
        """

    async def describe_export(self, *, ExportArn: str) -> DescribeExportOutputTypeDef:
        """
        Describes an existing table export.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_export)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_export)
        """

    async def describe_global_table(
        self, *, GlobalTableName: str
    ) -> DescribeGlobalTableOutputTypeDef:
        """
        Returns information about the specified global table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_global_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_global_table)
        """

    async def describe_global_table_settings(
        self, *, GlobalTableName: str
    ) -> DescribeGlobalTableSettingsOutputTypeDef:
        """
        Describes Region-specific settings for a global table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_global_table_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_global_table_settings)
        """

    async def describe_import(self, *, ImportArn: str) -> DescribeImportOutputTypeDef:
        """
        Represents the properties of the import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_import)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_import)
        """

    async def describe_kinesis_streaming_destination(
        self, *, TableName: str
    ) -> DescribeKinesisStreamingDestinationOutputTypeDef:
        """
        Returns information about the status of Kinesis streaming.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_kinesis_streaming_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_kinesis_streaming_destination)
        """

    async def describe_limits(self) -> DescribeLimitsOutputTypeDef:
        """
        Returns the current provisioned-capacity quotas for your Amazon Web Services
        account in a Region, both for the Region as a whole and for any one DynamoDB
        table that you create
        there.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_limits)
        """

    async def describe_table(self, *, TableName: str) -> DescribeTableOutputTypeDef:
        """
        Returns information about the table, including the current status of the table,
        when it was created, the primary key schema, and any indexes on the
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_table)
        """

    async def describe_table_replica_auto_scaling(
        self, *, TableName: str
    ) -> DescribeTableReplicaAutoScalingOutputTypeDef:
        """
        Describes auto scaling settings across replicas of the global table at once.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_table_replica_auto_scaling)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_table_replica_auto_scaling)
        """

    async def describe_time_to_live(self, *, TableName: str) -> DescribeTimeToLiveOutputTypeDef:
        """
        Gives a description of the Time to Live (TTL) status on the specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_time_to_live)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#describe_time_to_live)
        """

    async def disable_kinesis_streaming_destination(
        self,
        *,
        TableName: str,
        StreamArn: str,
        EnableKinesisStreamingConfiguration: EnableKinesisStreamingConfigurationTypeDef = ...,
    ) -> KinesisStreamingDestinationOutputTypeDef:
        """
        Stops replication from the DynamoDB table to the Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.disable_kinesis_streaming_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#disable_kinesis_streaming_destination)
        """

    async def enable_kinesis_streaming_destination(
        self,
        *,
        TableName: str,
        StreamArn: str,
        EnableKinesisStreamingConfiguration: EnableKinesisStreamingConfigurationTypeDef = ...,
    ) -> KinesisStreamingDestinationOutputTypeDef:
        """
        Starts table data replication to the specified Kinesis data stream at a
        timestamp chosen during the enable
        workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.enable_kinesis_streaming_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#enable_kinesis_streaming_destination)
        """

    async def execute_statement(
        self,
        *,
        Statement: str,
        Parameters: Sequence[UniversalAttributeValueTypeDef] = ...,
        ConsistentRead: bool = ...,
        NextToken: str = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        Limit: int = ...,
        ReturnValuesOnConditionCheckFailure: ReturnValuesOnConditionCheckFailureType = ...,
    ) -> ExecuteStatementOutputTypeDef:
        """
        This operation allows you to perform reads and singleton writes on data stored
        in DynamoDB, using
        PartiQL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.execute_statement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#execute_statement)
        """

    async def execute_transaction(
        self,
        *,
        TransactStatements: Sequence[ParameterizedStatementTypeDef],
        ClientRequestToken: str = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
    ) -> ExecuteTransactionOutputTypeDef:
        """
        This operation allows you to perform transactional reads or writes on data
        stored in DynamoDB, using
        PartiQL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.execute_transaction)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#execute_transaction)
        """

    async def export_table_to_point_in_time(
        self,
        *,
        TableArn: str,
        S3Bucket: str,
        ExportTime: TimestampTypeDef = ...,
        ClientToken: str = ...,
        S3BucketOwner: str = ...,
        S3Prefix: str = ...,
        S3SseAlgorithm: S3SseAlgorithmType = ...,
        S3SseKmsKeyId: str = ...,
        ExportFormat: ExportFormatType = ...,
        ExportType: ExportTypeType = ...,
        IncrementalExportSpecification: IncrementalExportSpecificationUnionTypeDef = ...,
    ) -> ExportTableToPointInTimeOutputTypeDef:
        """
        Exports table data to an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.export_table_to_point_in_time)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#export_table_to_point_in_time)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#generate_presigned_url)
        """

    async def get_item(
        self,
        *,
        TableName: str,
        Key: Mapping[str, UniversalAttributeValueTypeDef],
        AttributesToGet: Sequence[str] = ...,
        ConsistentRead: bool = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        ProjectionExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
    ) -> GetItemOutputTypeDef:
        """
        The `GetItem` operation returns a set of attributes for the item with the given
        primary
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#get_item)
        """

    async def get_resource_policy(self, *, ResourceArn: str) -> GetResourcePolicyOutputTypeDef:
        """
        Returns the resource-based policy document attached to the resource, which can
        be a table or stream, in JSON
        format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#get_resource_policy)
        """

    async def import_table(
        self,
        *,
        S3BucketSource: S3BucketSourceTypeDef,
        InputFormat: InputFormatType,
        TableCreationParameters: TableCreationParametersUnionTypeDef,
        ClientToken: str = ...,
        InputFormatOptions: InputFormatOptionsUnionTypeDef = ...,
        InputCompressionType: InputCompressionTypeType = ...,
    ) -> ImportTableOutputTypeDef:
        """
        Imports table data from an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.import_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#import_table)
        """

    async def list_backups(
        self,
        *,
        TableName: str = ...,
        Limit: int = ...,
        TimeRangeLowerBound: TimestampTypeDef = ...,
        TimeRangeUpperBound: TimestampTypeDef = ...,
        ExclusiveStartBackupArn: str = ...,
        BackupType: BackupTypeFilterType = ...,
    ) -> ListBackupsOutputTypeDef:
        """
        List DynamoDB backups that are associated with an Amazon Web Services account
        and weren't made with Amazon Web Services
        Backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_backups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#list_backups)
        """

    async def list_contributor_insights(
        self, *, TableName: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListContributorInsightsOutputTypeDef:
        """
        Returns a list of ContributorInsightsSummary for a table and all its global
        secondary
        indexes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_contributor_insights)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#list_contributor_insights)
        """

    async def list_exports(
        self, *, TableArn: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListExportsOutputTypeDef:
        """
        Lists completed exports within the past 90 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_exports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#list_exports)
        """

    async def list_global_tables(
        self, *, ExclusiveStartGlobalTableName: str = ..., Limit: int = ..., RegionName: str = ...
    ) -> ListGlobalTablesOutputTypeDef:
        """
        Lists all global tables that have a replica in the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_global_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#list_global_tables)
        """

    async def list_imports(
        self, *, TableArn: str = ..., PageSize: int = ..., NextToken: str = ...
    ) -> ListImportsOutputTypeDef:
        """
        Lists completed imports within the past 90 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_imports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#list_imports)
        """

    async def list_tables(
        self, *, ExclusiveStartTableName: str = ..., Limit: int = ...
    ) -> ListTablesOutputTypeDef:
        """
        Returns an array of table names associated with the current account and
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#list_tables)
        """

    async def list_tags_of_resource(
        self, *, ResourceArn: str, NextToken: str = ...
    ) -> ListTagsOfResourceOutputTypeDef:
        """
        List all tags on an Amazon DynamoDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.list_tags_of_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#list_tags_of_resource)
        """

    async def put_item(
        self,
        *,
        TableName: str,
        Item: Mapping[str, UniversalAttributeValueTypeDef],
        Expected: Mapping[str, ExpectedAttributeValueTypeDef] = ...,
        ReturnValues: ReturnValueType = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        ReturnItemCollectionMetrics: ReturnItemCollectionMetricsType = ...,
        ConditionalOperator: ConditionalOperatorType = ...,
        ConditionExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
        ExpressionAttributeValues: Mapping[str, UniversalAttributeValueTypeDef] = ...,
        ReturnValuesOnConditionCheckFailure: ReturnValuesOnConditionCheckFailureType = ...,
    ) -> PutItemOutputTypeDef:
        """
        Creates a new item, or replaces an old item with a new item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#put_item)
        """

    async def put_resource_policy(
        self,
        *,
        ResourceArn: str,
        Policy: str,
        ExpectedRevisionId: str = ...,
        ConfirmRemoveSelfResourceAccess: bool = ...,
    ) -> PutResourcePolicyOutputTypeDef:
        """
        Attaches a resource-based policy document to the resource, which can be a table
        or
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#put_resource_policy)
        """

    async def query(
        self,
        *,
        TableName: str,
        IndexName: str = ...,
        Select: SelectType = ...,
        AttributesToGet: Sequence[str] = ...,
        Limit: int = ...,
        ConsistentRead: bool = ...,
        KeyConditions: Mapping[str, ConditionTypeDef] = ...,
        QueryFilter: Mapping[str, ConditionTypeDef] = ...,
        ConditionalOperator: ConditionalOperatorType = ...,
        ScanIndexForward: bool = ...,
        ExclusiveStartKey: Mapping[str, UniversalAttributeValueTypeDef] = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        ProjectionExpression: str = ...,
        FilterExpression: str = ...,
        KeyConditionExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
        ExpressionAttributeValues: Mapping[str, UniversalAttributeValueTypeDef] = ...,
    ) -> QueryOutputTypeDef:
        """
        You must provide the name of the partition key attribute and a single value for
        that
        attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#query)
        """

    async def restore_table_from_backup(
        self,
        *,
        TargetTableName: str,
        BackupArn: str,
        BillingModeOverride: BillingModeType = ...,
        GlobalSecondaryIndexOverride: Sequence[GlobalSecondaryIndexUnionTypeDef] = ...,
        LocalSecondaryIndexOverride: Sequence[LocalSecondaryIndexTypeDef] = ...,
        ProvisionedThroughputOverride: ProvisionedThroughputTypeDef = ...,
        OnDemandThroughputOverride: OnDemandThroughputTypeDef = ...,
        SSESpecificationOverride: SSESpecificationTypeDef = ...,
    ) -> RestoreTableFromBackupOutputTypeDef:
        """
        Creates a new table from an existing backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.restore_table_from_backup)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#restore_table_from_backup)
        """

    async def restore_table_to_point_in_time(
        self,
        *,
        TargetTableName: str,
        SourceTableArn: str = ...,
        SourceTableName: str = ...,
        UseLatestRestorableTime: bool = ...,
        RestoreDateTime: TimestampTypeDef = ...,
        BillingModeOverride: BillingModeType = ...,
        GlobalSecondaryIndexOverride: Sequence[GlobalSecondaryIndexUnionTypeDef] = ...,
        LocalSecondaryIndexOverride: Sequence[LocalSecondaryIndexTypeDef] = ...,
        ProvisionedThroughputOverride: ProvisionedThroughputTypeDef = ...,
        OnDemandThroughputOverride: OnDemandThroughputTypeDef = ...,
        SSESpecificationOverride: SSESpecificationTypeDef = ...,
    ) -> RestoreTableToPointInTimeOutputTypeDef:
        """
        Restores the specified table to the specified point in time within
        `EarliestRestorableDateTime` and
        `LatestRestorableDateTime`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.restore_table_to_point_in_time)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#restore_table_to_point_in_time)
        """

    async def scan(
        self,
        *,
        TableName: str,
        IndexName: str = ...,
        AttributesToGet: Sequence[str] = ...,
        Limit: int = ...,
        Select: SelectType = ...,
        ScanFilter: Mapping[str, ConditionTypeDef] = ...,
        ConditionalOperator: ConditionalOperatorType = ...,
        ExclusiveStartKey: Mapping[str, UniversalAttributeValueTypeDef] = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        TotalSegments: int = ...,
        Segment: int = ...,
        ProjectionExpression: str = ...,
        FilterExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
        ExpressionAttributeValues: Mapping[str, UniversalAttributeValueTypeDef] = ...,
        ConsistentRead: bool = ...,
    ) -> ScanOutputTypeDef:
        """
        The `Scan` operation returns one or more items and item attributes by accessing
        every item in a table or a secondary
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#scan)
        """

    async def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence[TagTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associate a set of tags with an Amazon DynamoDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#tag_resource)
        """

    async def transact_get_items(
        self,
        *,
        TransactItems: Sequence[TransactGetItemTypeDef],
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
    ) -> TransactGetItemsOutputTypeDef:
        """
        `TransactGetItems` is a synchronous operation that atomically retrieves
        multiple items from one or more tables (but not from indexes) in a single
        account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.transact_get_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#transact_get_items)
        """

    async def transact_write_items(
        self,
        *,
        TransactItems: Sequence[TransactWriteItemTypeDef],
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        ReturnItemCollectionMetrics: ReturnItemCollectionMetricsType = ...,
        ClientRequestToken: str = ...,
    ) -> TransactWriteItemsOutputTypeDef:
        """
        `TransactWriteItems` is a synchronous write operation that groups up to 100
        action
        requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.transact_write_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#transact_write_items)
        """

    async def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the association of tags from an Amazon DynamoDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#untag_resource)
        """

    async def update_continuous_backups(
        self,
        *,
        TableName: str,
        PointInTimeRecoverySpecification: PointInTimeRecoverySpecificationTypeDef,
    ) -> UpdateContinuousBackupsOutputTypeDef:
        """
        `UpdateContinuousBackups` enables or disables point in time recovery for the
        specified
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_continuous_backups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#update_continuous_backups)
        """

    async def update_contributor_insights(
        self,
        *,
        TableName: str,
        ContributorInsightsAction: ContributorInsightsActionType,
        IndexName: str = ...,
    ) -> UpdateContributorInsightsOutputTypeDef:
        """
        Updates the status for contributor insights for a specific table or index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_contributor_insights)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#update_contributor_insights)
        """

    async def update_global_table(
        self, *, GlobalTableName: str, ReplicaUpdates: Sequence[ReplicaUpdateTypeDef]
    ) -> UpdateGlobalTableOutputTypeDef:
        """
        Adds or removes replicas in the specified global table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_global_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#update_global_table)
        """

    async def update_global_table_settings(
        self,
        *,
        GlobalTableName: str,
        GlobalTableBillingMode: BillingModeType = ...,
        GlobalTableProvisionedWriteCapacityUnits: int = ...,
        GlobalTableProvisionedWriteCapacityAutoScalingSettingsUpdate: AutoScalingSettingsUpdateTypeDef = ...,
        GlobalTableGlobalSecondaryIndexSettingsUpdate: Sequence[
            GlobalTableGlobalSecondaryIndexSettingsUpdateTypeDef
        ] = ...,
        ReplicaSettingsUpdate: Sequence[ReplicaSettingsUpdateTypeDef] = ...,
    ) -> UpdateGlobalTableSettingsOutputTypeDef:
        """
        Updates settings for a global table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_global_table_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#update_global_table_settings)
        """

    async def update_item(
        self,
        *,
        TableName: str,
        Key: Mapping[str, UniversalAttributeValueTypeDef],
        AttributeUpdates: Mapping[str, AttributeValueUpdateTypeDef] = ...,
        Expected: Mapping[str, ExpectedAttributeValueTypeDef] = ...,
        ConditionalOperator: ConditionalOperatorType = ...,
        ReturnValues: ReturnValueType = ...,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = ...,
        ReturnItemCollectionMetrics: ReturnItemCollectionMetricsType = ...,
        UpdateExpression: str = ...,
        ConditionExpression: str = ...,
        ExpressionAttributeNames: Mapping[str, str] = ...,
        ExpressionAttributeValues: Mapping[str, UniversalAttributeValueTypeDef] = ...,
        ReturnValuesOnConditionCheckFailure: ReturnValuesOnConditionCheckFailureType = ...,
    ) -> UpdateItemOutputTypeDef:
        """
        Edits an existing item's attributes, or adds a new item to the table if it does
        not already
        exist.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#update_item)
        """

    async def update_kinesis_streaming_destination(
        self,
        *,
        TableName: str,
        StreamArn: str,
        UpdateKinesisStreamingConfiguration: UpdateKinesisStreamingConfigurationTypeDef = ...,
    ) -> UpdateKinesisStreamingDestinationOutputTypeDef:
        """
        The command to update the Kinesis stream destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_kinesis_streaming_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#update_kinesis_streaming_destination)
        """

    async def update_table(
        self,
        *,
        TableName: str,
        AttributeDefinitions: Sequence[AttributeDefinitionTypeDef] = ...,
        BillingMode: BillingModeType = ...,
        ProvisionedThroughput: ProvisionedThroughputTypeDef = ...,
        GlobalSecondaryIndexUpdates: Sequence[GlobalSecondaryIndexUpdateTypeDef] = ...,
        StreamSpecification: StreamSpecificationTypeDef = ...,
        SSESpecification: SSESpecificationTypeDef = ...,
        ReplicaUpdates: Sequence[ReplicationGroupUpdateTypeDef] = ...,
        TableClass: TableClassType = ...,
        DeletionProtectionEnabled: bool = ...,
        OnDemandThroughput: OnDemandThroughputTypeDef = ...,
    ) -> UpdateTableOutputTypeDef:
        """
        Modifies the provisioned throughput settings, global secondary indexes, or
        DynamoDB Streams settings for a given
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#update_table)
        """

    async def update_table_replica_auto_scaling(
        self,
        *,
        TableName: str,
        GlobalSecondaryIndexUpdates: Sequence[GlobalSecondaryIndexAutoScalingUpdateTypeDef] = ...,
        ProvisionedWriteCapacityAutoScalingUpdate: AutoScalingSettingsUpdateTypeDef = ...,
        ReplicaUpdates: Sequence[ReplicaAutoScalingUpdateTypeDef] = ...,
    ) -> UpdateTableReplicaAutoScalingOutputTypeDef:
        """
        Updates auto scaling settings on your global tables at once.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_table_replica_auto_scaling)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#update_table_replica_auto_scaling)
        """

    async def update_time_to_live(
        self, *, TableName: str, TimeToLiveSpecification: TimeToLiveSpecificationTypeDef
    ) -> UpdateTimeToLiveOutputTypeDef:
        """
        The `UpdateTimeToLive` method enables or disables Time to Live (TTL) for the
        specified
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_time_to_live)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#update_time_to_live)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_backups"]) -> ListBackupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tables"]) -> ListTablesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_of_resource"]
    ) -> ListTagsOfResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query"]) -> QueryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["scan"]) -> ScanPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["table_exists"]) -> TableExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["table_not_exists"]) -> TableNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/#get_waiter)
        """

    async def __aenter__(self) -> "DynamoDBClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/client/)
        """
