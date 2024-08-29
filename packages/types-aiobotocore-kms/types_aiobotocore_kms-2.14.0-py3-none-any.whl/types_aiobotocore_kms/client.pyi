"""
Type annotations for kms service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kms.client import KMSClient

    session = get_session()
    async with session.create_client("kms") as client:
        client: KMSClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AlgorithmSpecType,
    CustomerMasterKeySpecType,
    CustomKeyStoreTypeType,
    DataKeyPairSpecType,
    DataKeySpecType,
    EncryptionAlgorithmSpecType,
    ExpirationModelTypeType,
    GrantOperationType,
    KeySpecType,
    KeyUsageTypeType,
    MacAlgorithmSpecType,
    MessageTypeType,
    OriginTypeType,
    SigningAlgorithmSpecType,
    WrappingKeySpecType,
    XksProxyConnectivityTypeType,
)
from .paginator import (
    DescribeCustomKeyStoresPaginator,
    ListAliasesPaginator,
    ListGrantsPaginator,
    ListKeyPoliciesPaginator,
    ListKeyRotationsPaginator,
    ListKeysPaginator,
    ListResourceTagsPaginator,
    ListRetirableGrantsPaginator,
)
from .type_defs import (
    BlobTypeDef,
    CancelKeyDeletionResponseTypeDef,
    CreateCustomKeyStoreResponseTypeDef,
    CreateGrantResponseTypeDef,
    CreateKeyResponseTypeDef,
    DecryptResponseTypeDef,
    DeriveSharedSecretResponseTypeDef,
    DescribeCustomKeyStoresResponseTypeDef,
    DescribeKeyResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EncryptResponseTypeDef,
    GenerateDataKeyPairResponseTypeDef,
    GenerateDataKeyPairWithoutPlaintextResponseTypeDef,
    GenerateDataKeyResponseTypeDef,
    GenerateDataKeyWithoutPlaintextResponseTypeDef,
    GenerateMacResponseTypeDef,
    GenerateRandomResponseTypeDef,
    GetKeyPolicyResponseTypeDef,
    GetKeyRotationStatusResponseTypeDef,
    GetParametersForImportResponseTypeDef,
    GetPublicKeyResponseTypeDef,
    GrantConstraintsUnionTypeDef,
    ListAliasesResponseTypeDef,
    ListGrantsResponseTypeDef,
    ListKeyPoliciesResponseTypeDef,
    ListKeyRotationsResponseTypeDef,
    ListKeysResponseTypeDef,
    ListResourceTagsResponseTypeDef,
    RecipientInfoTypeDef,
    ReEncryptResponseTypeDef,
    ReplicateKeyResponseTypeDef,
    RotateKeyOnDemandResponseTypeDef,
    ScheduleKeyDeletionResponseTypeDef,
    SignResponseTypeDef,
    TagTypeDef,
    TimestampTypeDef,
    VerifyMacResponseTypeDef,
    VerifyResponseTypeDef,
    XksProxyAuthenticationCredentialTypeTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("KMSClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CloudHsmClusterInUseException: Type[BotocoreClientError]
    CloudHsmClusterInvalidConfigurationException: Type[BotocoreClientError]
    CloudHsmClusterNotActiveException: Type[BotocoreClientError]
    CloudHsmClusterNotFoundException: Type[BotocoreClientError]
    CloudHsmClusterNotRelatedException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CustomKeyStoreHasCMKsException: Type[BotocoreClientError]
    CustomKeyStoreInvalidStateException: Type[BotocoreClientError]
    CustomKeyStoreNameInUseException: Type[BotocoreClientError]
    CustomKeyStoreNotFoundException: Type[BotocoreClientError]
    DependencyTimeoutException: Type[BotocoreClientError]
    DisabledException: Type[BotocoreClientError]
    DryRunOperationException: Type[BotocoreClientError]
    ExpiredImportTokenException: Type[BotocoreClientError]
    IncorrectKeyException: Type[BotocoreClientError]
    IncorrectKeyMaterialException: Type[BotocoreClientError]
    IncorrectTrustAnchorException: Type[BotocoreClientError]
    InvalidAliasNameException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidCiphertextException: Type[BotocoreClientError]
    InvalidGrantIdException: Type[BotocoreClientError]
    InvalidGrantTokenException: Type[BotocoreClientError]
    InvalidImportTokenException: Type[BotocoreClientError]
    InvalidKeyUsageException: Type[BotocoreClientError]
    InvalidMarkerException: Type[BotocoreClientError]
    KMSInternalException: Type[BotocoreClientError]
    KMSInvalidMacException: Type[BotocoreClientError]
    KMSInvalidSignatureException: Type[BotocoreClientError]
    KMSInvalidStateException: Type[BotocoreClientError]
    KeyUnavailableException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TagException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]
    XksKeyAlreadyInUseException: Type[BotocoreClientError]
    XksKeyInvalidConfigurationException: Type[BotocoreClientError]
    XksKeyNotFoundException: Type[BotocoreClientError]
    XksProxyIncorrectAuthenticationCredentialException: Type[BotocoreClientError]
    XksProxyInvalidConfigurationException: Type[BotocoreClientError]
    XksProxyInvalidResponseException: Type[BotocoreClientError]
    XksProxyUriEndpointInUseException: Type[BotocoreClientError]
    XksProxyUriInUseException: Type[BotocoreClientError]
    XksProxyUriUnreachableException: Type[BotocoreClientError]
    XksProxyVpcEndpointServiceInUseException: Type[BotocoreClientError]
    XksProxyVpcEndpointServiceInvalidConfigurationException: Type[BotocoreClientError]
    XksProxyVpcEndpointServiceNotFoundException: Type[BotocoreClientError]

class KMSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KMSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#can_paginate)
        """

    async def cancel_key_deletion(self, *, KeyId: str) -> CancelKeyDeletionResponseTypeDef:
        """
        Cancels the deletion of a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.cancel_key_deletion)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#cancel_key_deletion)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#close)
        """

    async def connect_custom_key_store(self, *, CustomKeyStoreId: str) -> Dict[str, Any]:
        """
        Connects or reconnects a [custom key
        store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-overview.html)
        to its backing key
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.connect_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#connect_custom_key_store)
        """

    async def create_alias(
        self, *, AliasName: str, TargetKeyId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a friendly name for a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.create_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_alias)
        """

    async def create_custom_key_store(
        self,
        *,
        CustomKeyStoreName: str,
        CloudHsmClusterId: str = ...,
        TrustAnchorCertificate: str = ...,
        KeyStorePassword: str = ...,
        CustomKeyStoreType: CustomKeyStoreTypeType = ...,
        XksProxyUriEndpoint: str = ...,
        XksProxyUriPath: str = ...,
        XksProxyVpcEndpointServiceName: str = ...,
        XksProxyAuthenticationCredential: XksProxyAuthenticationCredentialTypeTypeDef = ...,
        XksProxyConnectivity: XksProxyConnectivityTypeType = ...,
    ) -> CreateCustomKeyStoreResponseTypeDef:
        """
        Creates a [custom key
        store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-overview.html)
        backed by a key store that you own and
        manage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.create_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_custom_key_store)
        """

    async def create_grant(
        self,
        *,
        KeyId: str,
        GranteePrincipal: str,
        Operations: Sequence[GrantOperationType],
        RetiringPrincipal: str = ...,
        Constraints: GrantConstraintsUnionTypeDef = ...,
        GrantTokens: Sequence[str] = ...,
        Name: str = ...,
        DryRun: bool = ...,
    ) -> CreateGrantResponseTypeDef:
        """
        Adds a grant to a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.create_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_grant)
        """

    async def create_key(
        self,
        *,
        Policy: str = ...,
        Description: str = ...,
        KeyUsage: KeyUsageTypeType = ...,
        CustomerMasterKeySpec: CustomerMasterKeySpecType = ...,
        KeySpec: KeySpecType = ...,
        Origin: OriginTypeType = ...,
        CustomKeyStoreId: str = ...,
        BypassPolicyLockoutSafetyCheck: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
        MultiRegion: bool = ...,
        XksKeyId: str = ...,
    ) -> CreateKeyResponseTypeDef:
        """
        Creates a unique customer managed [KMS
        key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms-keys)
        in your Amazon Web Services account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.create_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_key)
        """

    async def decrypt(
        self,
        *,
        CiphertextBlob: BlobTypeDef,
        EncryptionContext: Mapping[str, str] = ...,
        GrantTokens: Sequence[str] = ...,
        KeyId: str = ...,
        EncryptionAlgorithm: EncryptionAlgorithmSpecType = ...,
        Recipient: RecipientInfoTypeDef = ...,
        DryRun: bool = ...,
    ) -> DecryptResponseTypeDef:
        """
        Decrypts ciphertext that was encrypted by a KMS key using any of the following
        operations: *  Encrypt *  GenerateDataKey *  GenerateDataKeyPair *
        GenerateDataKeyWithoutPlaintext *  GenerateDataKeyPairWithoutPlaintext You can
        use this operation to decrypt ciphertext that was
        enc...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.decrypt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#decrypt)
        """

    async def delete_alias(self, *, AliasName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.delete_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#delete_alias)
        """

    async def delete_custom_key_store(self, *, CustomKeyStoreId: str) -> Dict[str, Any]:
        """
        Deletes a [custom key
        store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-overview.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.delete_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#delete_custom_key_store)
        """

    async def delete_imported_key_material(self, *, KeyId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes key material that was previously imported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.delete_imported_key_material)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#delete_imported_key_material)
        """

    async def derive_shared_secret(
        self,
        *,
        KeyId: str,
        KeyAgreementAlgorithm: Literal["ECDH"],
        PublicKey: BlobTypeDef,
        GrantTokens: Sequence[str] = ...,
        DryRun: bool = ...,
        Recipient: RecipientInfoTypeDef = ...,
    ) -> DeriveSharedSecretResponseTypeDef:
        """
        Derives a shared secret using a key agreement algorithm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.derive_shared_secret)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#derive_shared_secret)
        """

    async def describe_custom_key_stores(
        self,
        *,
        CustomKeyStoreId: str = ...,
        CustomKeyStoreName: str = ...,
        Limit: int = ...,
        Marker: str = ...,
    ) -> DescribeCustomKeyStoresResponseTypeDef:
        """
        Gets information about [custom key
        stores](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-overview.html)
        in the account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.describe_custom_key_stores)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#describe_custom_key_stores)
        """

    async def describe_key(
        self, *, KeyId: str, GrantTokens: Sequence[str] = ...
    ) -> DescribeKeyResponseTypeDef:
        """
        Provides detailed information about a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.describe_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#describe_key)
        """

    async def disable_key(self, *, KeyId: str) -> EmptyResponseMetadataTypeDef:
        """
        Sets the state of a KMS key to disabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.disable_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#disable_key)
        """

    async def disable_key_rotation(self, *, KeyId: str) -> EmptyResponseMetadataTypeDef:
        """
        Disables [automatic rotation of the key
        material](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)
        of the specified symmetric encryption KMS
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.disable_key_rotation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#disable_key_rotation)
        """

    async def disconnect_custom_key_store(self, *, CustomKeyStoreId: str) -> Dict[str, Any]:
        """
        Disconnects the [custom key
        store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-overview.html)
        from its backing key
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.disconnect_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#disconnect_custom_key_store)
        """

    async def enable_key(self, *, KeyId: str) -> EmptyResponseMetadataTypeDef:
        """
        Sets the key state of a KMS key to enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.enable_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#enable_key)
        """

    async def enable_key_rotation(
        self, *, KeyId: str, RotationPeriodInDays: int = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables [automatic rotation of the key
        material](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html#rotating-keys-enable-disable)
        of the specified symmetric encryption KMS
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.enable_key_rotation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#enable_key_rotation)
        """

    async def encrypt(
        self,
        *,
        KeyId: str,
        Plaintext: BlobTypeDef,
        EncryptionContext: Mapping[str, str] = ...,
        GrantTokens: Sequence[str] = ...,
        EncryptionAlgorithm: EncryptionAlgorithmSpecType = ...,
        DryRun: bool = ...,
    ) -> EncryptResponseTypeDef:
        """
        Encrypts plaintext of up to 4,096 bytes using a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.encrypt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#encrypt)
        """

    async def generate_data_key(
        self,
        *,
        KeyId: str,
        EncryptionContext: Mapping[str, str] = ...,
        NumberOfBytes: int = ...,
        KeySpec: DataKeySpecType = ...,
        GrantTokens: Sequence[str] = ...,
        Recipient: RecipientInfoTypeDef = ...,
        DryRun: bool = ...,
    ) -> GenerateDataKeyResponseTypeDef:
        """
        Returns a unique symmetric data key for use outside of KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_data_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key)
        """

    async def generate_data_key_pair(
        self,
        *,
        KeyId: str,
        KeyPairSpec: DataKeyPairSpecType,
        EncryptionContext: Mapping[str, str] = ...,
        GrantTokens: Sequence[str] = ...,
        Recipient: RecipientInfoTypeDef = ...,
        DryRun: bool = ...,
    ) -> GenerateDataKeyPairResponseTypeDef:
        """
        Returns a unique asymmetric data key pair for use outside of KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_data_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key_pair)
        """

    async def generate_data_key_pair_without_plaintext(
        self,
        *,
        KeyId: str,
        KeyPairSpec: DataKeyPairSpecType,
        EncryptionContext: Mapping[str, str] = ...,
        GrantTokens: Sequence[str] = ...,
        DryRun: bool = ...,
    ) -> GenerateDataKeyPairWithoutPlaintextResponseTypeDef:
        """
        Returns a unique asymmetric data key pair for use outside of KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_data_key_pair_without_plaintext)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key_pair_without_plaintext)
        """

    async def generate_data_key_without_plaintext(
        self,
        *,
        KeyId: str,
        EncryptionContext: Mapping[str, str] = ...,
        KeySpec: DataKeySpecType = ...,
        NumberOfBytes: int = ...,
        GrantTokens: Sequence[str] = ...,
        DryRun: bool = ...,
    ) -> GenerateDataKeyWithoutPlaintextResponseTypeDef:
        """
        Returns a unique symmetric data key for use outside of KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_data_key_without_plaintext)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key_without_plaintext)
        """

    async def generate_mac(
        self,
        *,
        Message: BlobTypeDef,
        KeyId: str,
        MacAlgorithm: MacAlgorithmSpecType,
        GrantTokens: Sequence[str] = ...,
        DryRun: bool = ...,
    ) -> GenerateMacResponseTypeDef:
        """
        Generates a hash-based message authentication code (HMAC) for a message using
        an HMAC KMS key and a MAC algorithm that the key
        supports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_mac)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_mac)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_presigned_url)
        """

    async def generate_random(
        self,
        *,
        NumberOfBytes: int = ...,
        CustomKeyStoreId: str = ...,
        Recipient: RecipientInfoTypeDef = ...,
    ) -> GenerateRandomResponseTypeDef:
        """
        Returns a random byte string that is cryptographically secure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_random)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_random)
        """

    async def get_key_policy(
        self, *, KeyId: str, PolicyName: str = ...
    ) -> GetKeyPolicyResponseTypeDef:
        """
        Gets a key policy attached to the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_key_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_key_policy)
        """

    async def get_key_rotation_status(self, *, KeyId: str) -> GetKeyRotationStatusResponseTypeDef:
        """
        Provides detailed information about the rotation status for a KMS key,
        including whether [automatic rotation of the key
        material](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)
        is enabled for the specified KMS key, the `rotation period
        <https://docs.aws.amazon.com/kms/...`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_key_rotation_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_key_rotation_status)
        """

    async def get_parameters_for_import(
        self,
        *,
        KeyId: str,
        WrappingAlgorithm: AlgorithmSpecType,
        WrappingKeySpec: WrappingKeySpecType,
    ) -> GetParametersForImportResponseTypeDef:
        """
        Returns the public key and an import token you need to import or reimport key
        material for a KMS
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_parameters_for_import)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_parameters_for_import)
        """

    async def get_public_key(
        self, *, KeyId: str, GrantTokens: Sequence[str] = ...
    ) -> GetPublicKeyResponseTypeDef:
        """
        Returns the public key of an asymmetric KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_public_key)
        """

    async def import_key_material(
        self,
        *,
        KeyId: str,
        ImportToken: BlobTypeDef,
        EncryptedKeyMaterial: BlobTypeDef,
        ValidTo: TimestampTypeDef = ...,
        ExpirationModel: ExpirationModelTypeType = ...,
    ) -> Dict[str, Any]:
        """
        Imports or reimports key material into an existing KMS key that was created
        without key
        material.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.import_key_material)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#import_key_material)
        """

    async def list_aliases(
        self, *, KeyId: str = ..., Limit: int = ..., Marker: str = ...
    ) -> ListAliasesResponseTypeDef:
        """
        Gets a list of aliases in the caller's Amazon Web Services account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_aliases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_aliases)
        """

    async def list_grants(
        self,
        *,
        KeyId: str,
        Limit: int = ...,
        Marker: str = ...,
        GrantId: str = ...,
        GranteePrincipal: str = ...,
    ) -> ListGrantsResponseTypeDef:
        """
        Gets a list of all grants for the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_grants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_grants)
        """

    async def list_key_policies(
        self, *, KeyId: str, Limit: int = ..., Marker: str = ...
    ) -> ListKeyPoliciesResponseTypeDef:
        """
        Gets the names of the key policies that are attached to a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_key_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_key_policies)
        """

    async def list_key_rotations(
        self, *, KeyId: str, Limit: int = ..., Marker: str = ...
    ) -> ListKeyRotationsResponseTypeDef:
        """
        Returns information about all completed key material rotations for the
        specified KMS
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_key_rotations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_key_rotations)
        """

    async def list_keys(self, *, Limit: int = ..., Marker: str = ...) -> ListKeysResponseTypeDef:
        """
        Gets a list of all KMS keys in the caller's Amazon Web Services account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_keys)
        """

    async def list_resource_tags(
        self, *, KeyId: str, Limit: int = ..., Marker: str = ...
    ) -> ListResourceTagsResponseTypeDef:
        """
        Returns all tags on the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_resource_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_resource_tags)
        """

    async def list_retirable_grants(
        self, *, RetiringPrincipal: str, Limit: int = ..., Marker: str = ...
    ) -> ListGrantsResponseTypeDef:
        """
        Returns information about all grants in the Amazon Web Services account and
        Region that have the specified retiring
        principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_retirable_grants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_retirable_grants)
        """

    async def put_key_policy(
        self,
        *,
        KeyId: str,
        Policy: str,
        PolicyName: str = ...,
        BypassPolicyLockoutSafetyCheck: bool = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches a key policy to the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.put_key_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#put_key_policy)
        """

    async def re_encrypt(
        self,
        *,
        CiphertextBlob: BlobTypeDef,
        DestinationKeyId: str,
        SourceEncryptionContext: Mapping[str, str] = ...,
        SourceKeyId: str = ...,
        DestinationEncryptionContext: Mapping[str, str] = ...,
        SourceEncryptionAlgorithm: EncryptionAlgorithmSpecType = ...,
        DestinationEncryptionAlgorithm: EncryptionAlgorithmSpecType = ...,
        GrantTokens: Sequence[str] = ...,
        DryRun: bool = ...,
    ) -> ReEncryptResponseTypeDef:
        """
        Decrypts ciphertext and then reencrypts it entirely within KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.re_encrypt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#re_encrypt)
        """

    async def replicate_key(
        self,
        *,
        KeyId: str,
        ReplicaRegion: str,
        Policy: str = ...,
        BypassPolicyLockoutSafetyCheck: bool = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> ReplicateKeyResponseTypeDef:
        """
        Replicates a multi-Region key into the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.replicate_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#replicate_key)
        """

    async def retire_grant(
        self, *, GrantToken: str = ..., KeyId: str = ..., GrantId: str = ..., DryRun: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.retire_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#retire_grant)
        """

    async def revoke_grant(
        self, *, KeyId: str, GrantId: str, DryRun: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.revoke_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#revoke_grant)
        """

    async def rotate_key_on_demand(self, *, KeyId: str) -> RotateKeyOnDemandResponseTypeDef:
        """
        Immediately initiates rotation of the key material of the specified symmetric
        encryption KMS
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.rotate_key_on_demand)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#rotate_key_on_demand)
        """

    async def schedule_key_deletion(
        self, *, KeyId: str, PendingWindowInDays: int = ...
    ) -> ScheduleKeyDeletionResponseTypeDef:
        """
        Schedules the deletion of a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.schedule_key_deletion)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#schedule_key_deletion)
        """

    async def sign(
        self,
        *,
        KeyId: str,
        Message: BlobTypeDef,
        SigningAlgorithm: SigningAlgorithmSpecType,
        MessageType: MessageTypeType = ...,
        GrantTokens: Sequence[str] = ...,
        DryRun: bool = ...,
    ) -> SignResponseTypeDef:
        """
        Creates a [digital signature](https://en.wikipedia.org/wiki/Digital_signature)
        for a message or message digest by using the private key in an asymmetric
        signing KMS
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.sign)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#sign)
        """

    async def tag_resource(
        self, *, KeyId: str, Tags: Sequence[TagTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or edits tags on a [customer managed
        key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#tag_resource)
        """

    async def untag_resource(
        self, *, KeyId: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes tags from a [customer managed
        key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#untag_resource)
        """

    async def update_alias(
        self, *, AliasName: str, TargetKeyId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates an existing KMS alias with a different KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.update_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_alias)
        """

    async def update_custom_key_store(
        self,
        *,
        CustomKeyStoreId: str,
        NewCustomKeyStoreName: str = ...,
        KeyStorePassword: str = ...,
        CloudHsmClusterId: str = ...,
        XksProxyUriEndpoint: str = ...,
        XksProxyUriPath: str = ...,
        XksProxyVpcEndpointServiceName: str = ...,
        XksProxyAuthenticationCredential: XksProxyAuthenticationCredentialTypeTypeDef = ...,
        XksProxyConnectivity: XksProxyConnectivityTypeType = ...,
    ) -> Dict[str, Any]:
        """
        Changes the properties of a custom key store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.update_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_custom_key_store)
        """

    async def update_key_description(
        self, *, KeyId: str, Description: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the description of a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.update_key_description)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_key_description)
        """

    async def update_primary_region(
        self, *, KeyId: str, PrimaryRegion: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the primary key of a multi-Region key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.update_primary_region)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_primary_region)
        """

    async def verify(
        self,
        *,
        KeyId: str,
        Message: BlobTypeDef,
        Signature: BlobTypeDef,
        SigningAlgorithm: SigningAlgorithmSpecType,
        MessageType: MessageTypeType = ...,
        GrantTokens: Sequence[str] = ...,
        DryRun: bool = ...,
    ) -> VerifyResponseTypeDef:
        """
        Verifies a digital signature that was generated by the  Sign operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.verify)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#verify)
        """

    async def verify_mac(
        self,
        *,
        Message: BlobTypeDef,
        KeyId: str,
        MacAlgorithm: MacAlgorithmSpecType,
        Mac: BlobTypeDef,
        GrantTokens: Sequence[str] = ...,
        DryRun: bool = ...,
    ) -> VerifyMacResponseTypeDef:
        """
        Verifies the hash-based message authentication code (HMAC) for a specified
        message, HMAC KMS key, and MAC
        algorithm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.verify_mac)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#verify_mac)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_custom_key_stores"]
    ) -> DescribeCustomKeyStoresPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_grants"]) -> ListGrantsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_key_policies"]
    ) -> ListKeyPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_key_rotations"]
    ) -> ListKeyRotationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_keys"]) -> ListKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_tags"]
    ) -> ListResourceTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_retirable_grants"]
    ) -> ListRetirableGrantsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    async def __aenter__(self) -> "KMSClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)
        """
