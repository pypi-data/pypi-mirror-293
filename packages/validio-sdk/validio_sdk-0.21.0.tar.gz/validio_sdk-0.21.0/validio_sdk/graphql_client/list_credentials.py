from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import CredentialId

from .base_model import BaseModel
from .enums import AzureSynapseBackendType, ClickHouseProtocol
from .fragments import CredentialBase


class ListCredentials(BaseModel):
    credentials_list: List[
        Annotated[
            Union[
                "ListCredentialsCredentialsListCredential",
                "ListCredentialsCredentialsListAwsAthenaCredential",
                "ListCredentialsCredentialsListAwsCredential",
                "ListCredentialsCredentialsListAwsRedshiftCredential",
                "ListCredentialsCredentialsListAzureSynapseEntraIdCredential",
                "ListCredentialsCredentialsListAzureSynapseSqlCredential",
                "ListCredentialsCredentialsListClickHouseCredential",
                "ListCredentialsCredentialsListDatabricksCredential",
                "ListCredentialsCredentialsListDbtCloudCredential",
                "ListCredentialsCredentialsListDbtCoreCredential",
                "ListCredentialsCredentialsListGcpCredential",
                "ListCredentialsCredentialsListKafkaSaslSslPlainCredential",
                "ListCredentialsCredentialsListKafkaSslCredential",
                "ListCredentialsCredentialsListLookerCredential",
                "ListCredentialsCredentialsListPostgreSqlCredential",
                "ListCredentialsCredentialsListSnowflakeCredential",
                "ListCredentialsCredentialsListTableauConnectedAppCredential",
                "ListCredentialsCredentialsListTableauPersonalAccessTokenCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="credentialsList")


class ListCredentialsCredentialsListCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListCredentialsCredentialsListAwsAthenaCredential(BaseModel):
    typename__: Literal["AwsAthenaCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAwsAthenaCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListAwsAthenaCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")
    region: str
    query_result_location: str = Field(alias="queryResultLocation")


class ListCredentialsCredentialsListAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAwsCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class ListCredentialsCredentialsListAwsRedshiftCredential(BaseModel):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAwsRedshiftCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListAwsRedshiftCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class ListCredentialsCredentialsListAzureSynapseEntraIdCredential(BaseModel):
    typename__: Literal["AzureSynapseEntraIdCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAzureSynapseEntraIdCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListAzureSynapseEntraIdCredentialConfig(BaseModel):
    client_id: str = Field(alias="clientId")
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class ListCredentialsCredentialsListAzureSynapseSqlCredential(BaseModel):
    typename__: Literal["AzureSynapseSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListAzureSynapseSqlCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListAzureSynapseSqlCredentialConfig(BaseModel):
    username: str
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class ListCredentialsCredentialsListClickHouseCredential(BaseModel):
    typename__: Literal["ClickHouseCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListClickHouseCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListClickHouseCredentialConfig(BaseModel):
    protocol: ClickHouseProtocol
    host: str
    port: int
    username: str
    default_database: str = Field(alias="defaultDatabase")


class ListCredentialsCredentialsListDatabricksCredential(BaseModel):
    typename__: Literal["DatabricksCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListDatabricksCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListDatabricksCredentialConfig(BaseModel):
    host: str
    port: int
    http_path: str = Field(alias="httpPath")


class ListCredentialsCredentialsListDbtCloudCredential(BaseModel):
    typename__: Literal["DbtCloudCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListDbtCloudCredentialConfig"


class ListCredentialsCredentialsListDbtCloudCredentialConfig(BaseModel):
    warehouse_credential: (
        "ListCredentialsCredentialsListDbtCloudCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")
    account_id: str = Field(alias="accountId")
    api_base_url: Optional[str] = Field(alias="apiBaseUrl")


class ListCredentialsCredentialsListDbtCloudCredentialConfigWarehouseCredential(
    CredentialBase
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")


class ListCredentialsCredentialsListDbtCoreCredential(BaseModel):
    typename__: Literal["DbtCoreCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListDbtCoreCredentialConfig"


class ListCredentialsCredentialsListDbtCoreCredentialConfig(BaseModel):
    warehouse_credential: (
        "ListCredentialsCredentialsListDbtCoreCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")


class ListCredentialsCredentialsListDbtCoreCredentialConfigWarehouseCredential(
    CredentialBase
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")


class ListCredentialsCredentialsListGcpCredential(BaseModel):
    typename__: Literal["GcpCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListKafkaSaslSslPlainCredential(BaseModel):
    typename__: Literal["KafkaSaslSslPlainCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListKafkaSaslSslPlainCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListKafkaSaslSslPlainCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    username: str


class ListCredentialsCredentialsListKafkaSslCredential(BaseModel):
    typename__: Literal["KafkaSslCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListKafkaSslCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListKafkaSslCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")


class ListCredentialsCredentialsListLookerCredential(BaseModel):
    typename__: Literal["LookerCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListLookerCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListLookerCredentialConfig(BaseModel):
    base_url: str = Field(alias="baseUrl")
    client_id: str = Field(alias="clientId")


class ListCredentialsCredentialsListPostgreSqlCredential(BaseModel):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListPostgreSqlCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListPostgreSqlCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class ListCredentialsCredentialsListSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListSnowflakeCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListSnowflakeCredentialConfig(BaseModel):
    account: str
    user: str
    role: Optional[str]
    warehouse: Optional[str]
    auth: Optional[
        Annotated[
            Union[
                "ListCredentialsCredentialsListSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair",
                "ListCredentialsCredentialsListSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class ListCredentialsCredentialsListSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair(
    BaseModel
):
    typename__: Literal["SnowflakeCredentialKeyPair"] = Field(alias="__typename")
    user: str


class ListCredentialsCredentialsListSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword(
    BaseModel
):
    typename__: Literal["SnowflakeCredentialUserPassword"] = Field(alias="__typename")
    user: str


class ListCredentialsCredentialsListTableauConnectedAppCredential(BaseModel):
    typename__: Literal["TableauConnectedAppCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListTableauConnectedAppCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListTableauConnectedAppCredentialConfig(BaseModel):
    host: str
    site: str
    user: str
    client_id: str = Field(alias="clientId")
    secret_id: str = Field(alias="secretId")


class ListCredentialsCredentialsListTableauPersonalAccessTokenCredential(BaseModel):
    typename__: Literal["TableauPersonalAccessTokenCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListCredentialsCredentialsListTableauPersonalAccessTokenCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class ListCredentialsCredentialsListTableauPersonalAccessTokenCredentialConfig(
    BaseModel
):
    host: str
    site: str
    token_name: str = Field(alias="tokenName")


ListCredentials.model_rebuild()
ListCredentialsCredentialsListAwsAthenaCredential.model_rebuild()
ListCredentialsCredentialsListAwsCredential.model_rebuild()
ListCredentialsCredentialsListAwsRedshiftCredential.model_rebuild()
ListCredentialsCredentialsListAzureSynapseEntraIdCredential.model_rebuild()
ListCredentialsCredentialsListAzureSynapseSqlCredential.model_rebuild()
ListCredentialsCredentialsListClickHouseCredential.model_rebuild()
ListCredentialsCredentialsListDatabricksCredential.model_rebuild()
ListCredentialsCredentialsListDbtCloudCredential.model_rebuild()
ListCredentialsCredentialsListDbtCloudCredentialConfig.model_rebuild()
ListCredentialsCredentialsListDbtCoreCredential.model_rebuild()
ListCredentialsCredentialsListDbtCoreCredentialConfig.model_rebuild()
ListCredentialsCredentialsListKafkaSaslSslPlainCredential.model_rebuild()
ListCredentialsCredentialsListKafkaSslCredential.model_rebuild()
ListCredentialsCredentialsListLookerCredential.model_rebuild()
ListCredentialsCredentialsListPostgreSqlCredential.model_rebuild()
ListCredentialsCredentialsListSnowflakeCredential.model_rebuild()
ListCredentialsCredentialsListSnowflakeCredentialConfig.model_rebuild()
ListCredentialsCredentialsListTableauConnectedAppCredential.model_rebuild()
ListCredentialsCredentialsListTableauPersonalAccessTokenCredential.model_rebuild()
