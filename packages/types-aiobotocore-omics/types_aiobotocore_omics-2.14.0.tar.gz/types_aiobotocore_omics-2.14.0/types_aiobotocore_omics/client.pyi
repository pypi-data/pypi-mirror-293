"""
Type annotations for omics service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_omics.client import OmicsClient

    session = get_session()
    async with session.create_client("omics") as client:
        client: OmicsClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ETagAlgorithmFamilyType,
    FileTypeType,
    ReadSetFileType,
    ReadSetPartSourceType,
    ReferenceFileType,
    ResourceOwnerType,
    RunLogLevelType,
    RunRetentionModeType,
    RunStatusType,
    StorageTypeType,
    StoreFormatType,
    TaskStatusType,
    WorkflowEngineType,
    WorkflowTypeType,
)
from .paginator import (
    ListAnnotationImportJobsPaginator,
    ListAnnotationStoresPaginator,
    ListAnnotationStoreVersionsPaginator,
    ListMultipartReadSetUploadsPaginator,
    ListReadSetActivationJobsPaginator,
    ListReadSetExportJobsPaginator,
    ListReadSetImportJobsPaginator,
    ListReadSetsPaginator,
    ListReadSetUploadPartsPaginator,
    ListReferenceImportJobsPaginator,
    ListReferencesPaginator,
    ListReferenceStoresPaginator,
    ListRunGroupsPaginator,
    ListRunsPaginator,
    ListRunTasksPaginator,
    ListSequenceStoresPaginator,
    ListSharesPaginator,
    ListVariantImportJobsPaginator,
    ListVariantStoresPaginator,
    ListWorkflowsPaginator,
)
from .type_defs import (
    AcceptShareResponseTypeDef,
    ActivateReadSetFilterTypeDef,
    AnnotationImportItemSourceTypeDef,
    BatchDeleteReadSetResponseTypeDef,
    BlobTypeDef,
    CompleteMultipartReadSetUploadResponseTypeDef,
    CompleteReadSetUploadPartListItemTypeDef,
    CreateAnnotationStoreResponseTypeDef,
    CreateAnnotationStoreVersionResponseTypeDef,
    CreateMultipartReadSetUploadResponseTypeDef,
    CreateReferenceStoreResponseTypeDef,
    CreateRunGroupResponseTypeDef,
    CreateSequenceStoreResponseTypeDef,
    CreateShareResponseTypeDef,
    CreateVariantStoreResponseTypeDef,
    CreateWorkflowResponseTypeDef,
    DeleteAnnotationStoreResponseTypeDef,
    DeleteAnnotationStoreVersionsResponseTypeDef,
    DeleteShareResponseTypeDef,
    DeleteVariantStoreResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportReadSetFilterTypeDef,
    ExportReadSetTypeDef,
    FilterTypeDef,
    FormatOptionsTypeDef,
    GetAnnotationImportResponseTypeDef,
    GetAnnotationStoreResponseTypeDef,
    GetAnnotationStoreVersionResponseTypeDef,
    GetReadSetActivationJobResponseTypeDef,
    GetReadSetExportJobResponseTypeDef,
    GetReadSetImportJobResponseTypeDef,
    GetReadSetMetadataResponseTypeDef,
    GetReadSetResponseTypeDef,
    GetReferenceImportJobResponseTypeDef,
    GetReferenceMetadataResponseTypeDef,
    GetReferenceResponseTypeDef,
    GetReferenceStoreResponseTypeDef,
    GetRunGroupResponseTypeDef,
    GetRunResponseTypeDef,
    GetRunTaskResponseTypeDef,
    GetSequenceStoreResponseTypeDef,
    GetShareResponseTypeDef,
    GetVariantImportResponseTypeDef,
    GetVariantStoreResponseTypeDef,
    GetWorkflowResponseTypeDef,
    ImportReadSetFilterTypeDef,
    ImportReferenceFilterTypeDef,
    ListAnnotationImportJobsFilterTypeDef,
    ListAnnotationImportJobsResponseTypeDef,
    ListAnnotationStoresFilterTypeDef,
    ListAnnotationStoresResponseTypeDef,
    ListAnnotationStoreVersionsFilterTypeDef,
    ListAnnotationStoreVersionsResponseTypeDef,
    ListMultipartReadSetUploadsResponseTypeDef,
    ListReadSetActivationJobsResponseTypeDef,
    ListReadSetExportJobsResponseTypeDef,
    ListReadSetImportJobsResponseTypeDef,
    ListReadSetsResponseTypeDef,
    ListReadSetUploadPartsResponseTypeDef,
    ListReferenceImportJobsResponseTypeDef,
    ListReferencesResponseTypeDef,
    ListReferenceStoresResponseTypeDef,
    ListRunGroupsResponseTypeDef,
    ListRunsResponseTypeDef,
    ListRunTasksResponseTypeDef,
    ListSequenceStoresResponseTypeDef,
    ListSharesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVariantImportJobsFilterTypeDef,
    ListVariantImportJobsResponseTypeDef,
    ListVariantStoresFilterTypeDef,
    ListVariantStoresResponseTypeDef,
    ListWorkflowsResponseTypeDef,
    ReadSetFilterTypeDef,
    ReadSetUploadPartListFilterTypeDef,
    ReferenceFilterTypeDef,
    ReferenceItemTypeDef,
    ReferenceStoreFilterTypeDef,
    SequenceStoreFilterTypeDef,
    SseConfigTypeDef,
    StartAnnotationImportResponseTypeDef,
    StartReadSetActivationJobResponseTypeDef,
    StartReadSetActivationJobSourceItemTypeDef,
    StartReadSetExportJobResponseTypeDef,
    StartReadSetImportJobResponseTypeDef,
    StartReadSetImportJobSourceItemTypeDef,
    StartReferenceImportJobResponseTypeDef,
    StartReferenceImportJobSourceItemTypeDef,
    StartRunResponseTypeDef,
    StartVariantImportResponseTypeDef,
    StoreOptionsUnionTypeDef,
    UpdateAnnotationStoreResponseTypeDef,
    UpdateAnnotationStoreVersionResponseTypeDef,
    UpdateVariantStoreResponseTypeDef,
    UploadReadSetPartResponseTypeDef,
    VariantImportItemSourceTypeDef,
    VersionOptionsUnionTypeDef,
    WorkflowParameterTypeDef,
)
from .waiter import (
    AnnotationImportJobCreatedWaiter,
    AnnotationStoreCreatedWaiter,
    AnnotationStoreDeletedWaiter,
    AnnotationStoreVersionCreatedWaiter,
    AnnotationStoreVersionDeletedWaiter,
    ReadSetActivationJobCompletedWaiter,
    ReadSetExportJobCompletedWaiter,
    ReadSetImportJobCompletedWaiter,
    ReferenceImportJobCompletedWaiter,
    RunCompletedWaiter,
    RunRunningWaiter,
    TaskCompletedWaiter,
    TaskRunningWaiter,
    VariantImportJobCreatedWaiter,
    VariantStoreCreatedWaiter,
    VariantStoreDeletedWaiter,
    WorkflowActiveWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("OmicsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    NotSupportedOperationException: Type[BotocoreClientError]
    RangeNotSatisfiableException: Type[BotocoreClientError]
    RequestTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class OmicsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OmicsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#exceptions)
        """

    async def abort_multipart_read_set_upload(
        self, *, sequenceStoreId: str, uploadId: str
    ) -> Dict[str, Any]:
        """
        Stops a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.abort_multipart_read_set_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#abort_multipart_read_set_upload)
        """

    async def accept_share(self, *, shareId: str) -> AcceptShareResponseTypeDef:
        """
        Accept a resource share request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.accept_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#accept_share)
        """

    async def batch_delete_read_set(
        self, *, ids: Sequence[str], sequenceStoreId: str
    ) -> BatchDeleteReadSetResponseTypeDef:
        """
        Deletes one or more read sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.batch_delete_read_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#batch_delete_read_set)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#can_paginate)
        """

    async def cancel_annotation_import_job(self, *, jobId: str) -> Dict[str, Any]:
        """
        Cancels an annotation import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.cancel_annotation_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#cancel_annotation_import_job)
        """

    async def cancel_run(self, *, id: str) -> EmptyResponseMetadataTypeDef:
        """
        Cancels a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.cancel_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#cancel_run)
        """

    async def cancel_variant_import_job(self, *, jobId: str) -> Dict[str, Any]:
        """
        Cancels a variant import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.cancel_variant_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#cancel_variant_import_job)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#close)
        """

    async def complete_multipart_read_set_upload(
        self,
        *,
        sequenceStoreId: str,
        uploadId: str,
        parts: Sequence[CompleteReadSetUploadPartListItemTypeDef],
    ) -> CompleteMultipartReadSetUploadResponseTypeDef:
        """
        Concludes a multipart upload once you have uploaded all the components.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.complete_multipart_read_set_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#complete_multipart_read_set_upload)
        """

    async def create_annotation_store(
        self,
        *,
        storeFormat: StoreFormatType,
        reference: ReferenceItemTypeDef = ...,
        name: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
        versionName: str = ...,
        sseConfig: SseConfigTypeDef = ...,
        storeOptions: StoreOptionsUnionTypeDef = ...,
    ) -> CreateAnnotationStoreResponseTypeDef:
        """
        Creates an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.create_annotation_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_annotation_store)
        """

    async def create_annotation_store_version(
        self,
        *,
        name: str,
        versionName: str,
        description: str = ...,
        versionOptions: VersionOptionsUnionTypeDef = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateAnnotationStoreVersionResponseTypeDef:
        """
        Creates a new version of an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.create_annotation_store_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_annotation_store_version)
        """

    async def create_multipart_read_set_upload(
        self,
        *,
        sequenceStoreId: str,
        sourceFileType: FileTypeType,
        subjectId: str,
        sampleId: str,
        name: str,
        clientToken: str = ...,
        generatedFrom: str = ...,
        referenceArn: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateMultipartReadSetUploadResponseTypeDef:
        """
        Begins a multipart read set upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.create_multipart_read_set_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_multipart_read_set_upload)
        """

    async def create_reference_store(
        self,
        *,
        name: str,
        description: str = ...,
        sseConfig: SseConfigTypeDef = ...,
        tags: Mapping[str, str] = ...,
        clientToken: str = ...,
    ) -> CreateReferenceStoreResponseTypeDef:
        """
        Creates a reference store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.create_reference_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_reference_store)
        """

    async def create_run_group(
        self,
        *,
        requestId: str,
        name: str = ...,
        maxCpus: int = ...,
        maxRuns: int = ...,
        maxDuration: int = ...,
        tags: Mapping[str, str] = ...,
        maxGpus: int = ...,
    ) -> CreateRunGroupResponseTypeDef:
        """
        You can optionally create a run group to limit the compute resources for the
        runs that you add to the
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.create_run_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_run_group)
        """

    async def create_sequence_store(
        self,
        *,
        name: str,
        description: str = ...,
        sseConfig: SseConfigTypeDef = ...,
        tags: Mapping[str, str] = ...,
        clientToken: str = ...,
        fallbackLocation: str = ...,
        eTagAlgorithmFamily: ETagAlgorithmFamilyType = ...,
    ) -> CreateSequenceStoreResponseTypeDef:
        """
        Creates a sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.create_sequence_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_sequence_store)
        """

    async def create_share(
        self, *, resourceArn: str, principalSubscriber: str, shareName: str = ...
    ) -> CreateShareResponseTypeDef:
        """
        Creates a cross-account shared resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.create_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_share)
        """

    async def create_variant_store(
        self,
        *,
        reference: ReferenceItemTypeDef,
        name: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
        sseConfig: SseConfigTypeDef = ...,
    ) -> CreateVariantStoreResponseTypeDef:
        """
        Creates a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.create_variant_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_variant_store)
        """

    async def create_workflow(
        self,
        *,
        requestId: str,
        name: str = ...,
        description: str = ...,
        engine: WorkflowEngineType = ...,
        definitionZip: BlobTypeDef = ...,
        definitionUri: str = ...,
        main: str = ...,
        parameterTemplate: Mapping[str, WorkflowParameterTypeDef] = ...,
        storageCapacity: int = ...,
        tags: Mapping[str, str] = ...,
        accelerators: Literal["GPU"] = ...,
    ) -> CreateWorkflowResponseTypeDef:
        """
        Creates a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.create_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#create_workflow)
        """

    async def delete_annotation_store(
        self, *, name: str, force: bool = ...
    ) -> DeleteAnnotationStoreResponseTypeDef:
        """
        Deletes an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_annotation_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_annotation_store)
        """

    async def delete_annotation_store_versions(
        self, *, name: str, versions: Sequence[str], force: bool = ...
    ) -> DeleteAnnotationStoreVersionsResponseTypeDef:
        """
        Deletes one or multiple versions of an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_annotation_store_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_annotation_store_versions)
        """

    async def delete_reference(self, *, id: str, referenceStoreId: str) -> Dict[str, Any]:
        """
        Deletes a genome reference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_reference)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_reference)
        """

    async def delete_reference_store(self, *, id: str) -> Dict[str, Any]:
        """
        Deletes a genome reference store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_reference_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_reference_store)
        """

    async def delete_run(self, *, id: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_run)
        """

    async def delete_run_group(self, *, id: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a workflow run group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_run_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_run_group)
        """

    async def delete_sequence_store(self, *, id: str) -> Dict[str, Any]:
        """
        Deletes a sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_sequence_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_sequence_store)
        """

    async def delete_share(self, *, shareId: str) -> DeleteShareResponseTypeDef:
        """
        Deletes a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_share)
        """

    async def delete_variant_store(
        self, *, name: str, force: bool = ...
    ) -> DeleteVariantStoreResponseTypeDef:
        """
        Deletes a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_variant_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_variant_store)
        """

    async def delete_workflow(self, *, id: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.delete_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#delete_workflow)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#generate_presigned_url)
        """

    async def get_annotation_import_job(self, *, jobId: str) -> GetAnnotationImportResponseTypeDef:
        """
        Gets information about an annotation import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_annotation_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_annotation_import_job)
        """

    async def get_annotation_store(self, *, name: str) -> GetAnnotationStoreResponseTypeDef:
        """
        Gets information about an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_annotation_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_annotation_store)
        """

    async def get_annotation_store_version(
        self, *, name: str, versionName: str
    ) -> GetAnnotationStoreVersionResponseTypeDef:
        """
        Retrieves the metadata for an annotation store version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_annotation_store_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_annotation_store_version)
        """

    async def get_read_set(
        self, *, id: str, sequenceStoreId: str, partNumber: int, file: ReadSetFileType = ...
    ) -> GetReadSetResponseTypeDef:
        """
        Gets a file from a read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_read_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set)
        """

    async def get_read_set_activation_job(
        self, *, id: str, sequenceStoreId: str
    ) -> GetReadSetActivationJobResponseTypeDef:
        """
        Gets information about a read set activation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_read_set_activation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set_activation_job)
        """

    async def get_read_set_export_job(
        self, *, sequenceStoreId: str, id: str
    ) -> GetReadSetExportJobResponseTypeDef:
        """
        Gets information about a read set export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_read_set_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set_export_job)
        """

    async def get_read_set_import_job(
        self, *, id: str, sequenceStoreId: str
    ) -> GetReadSetImportJobResponseTypeDef:
        """
        Gets information about a read set import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_read_set_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set_import_job)
        """

    async def get_read_set_metadata(
        self, *, id: str, sequenceStoreId: str
    ) -> GetReadSetMetadataResponseTypeDef:
        """
        Gets details about a read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_read_set_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_read_set_metadata)
        """

    async def get_reference(
        self,
        *,
        id: str,
        referenceStoreId: str,
        partNumber: int,
        range: str = ...,
        file: ReferenceFileType = ...,
    ) -> GetReferenceResponseTypeDef:
        """
        Gets a reference file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_reference)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_reference)
        """

    async def get_reference_import_job(
        self, *, id: str, referenceStoreId: str
    ) -> GetReferenceImportJobResponseTypeDef:
        """
        Gets information about a reference import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_reference_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_reference_import_job)
        """

    async def get_reference_metadata(
        self, *, id: str, referenceStoreId: str
    ) -> GetReferenceMetadataResponseTypeDef:
        """
        Gets information about a genome reference's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_reference_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_reference_metadata)
        """

    async def get_reference_store(self, *, id: str) -> GetReferenceStoreResponseTypeDef:
        """
        Gets information about a reference store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_reference_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_reference_store)
        """

    async def get_run(
        self, *, id: str, export: Sequence[Literal["DEFINITION"]] = ...
    ) -> GetRunResponseTypeDef:
        """
        Gets information about a workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_run)
        """

    async def get_run_group(self, *, id: str) -> GetRunGroupResponseTypeDef:
        """
        Gets information about a workflow run group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_run_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_run_group)
        """

    async def get_run_task(self, *, id: str, taskId: str) -> GetRunTaskResponseTypeDef:
        """
        Gets information about a workflow run task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_run_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_run_task)
        """

    async def get_sequence_store(self, *, id: str) -> GetSequenceStoreResponseTypeDef:
        """
        Gets information about a sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_sequence_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_sequence_store)
        """

    async def get_share(self, *, shareId: str) -> GetShareResponseTypeDef:
        """
        Retrieves the metadata for the specified resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_share)
        """

    async def get_variant_import_job(self, *, jobId: str) -> GetVariantImportResponseTypeDef:
        """
        Gets information about a variant import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_variant_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_variant_import_job)
        """

    async def get_variant_store(self, *, name: str) -> GetVariantStoreResponseTypeDef:
        """
        Gets information about a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_variant_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_variant_store)
        """

    async def get_workflow(
        self,
        *,
        id: str,
        type: WorkflowTypeType = ...,
        export: Sequence[Literal["DEFINITION"]] = ...,
        workflowOwnerId: str = ...,
    ) -> GetWorkflowResponseTypeDef:
        """
        Gets information about a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_workflow)
        """

    async def list_annotation_import_jobs(
        self,
        *,
        maxResults: int = ...,
        ids: Sequence[str] = ...,
        nextToken: str = ...,
        filter: ListAnnotationImportJobsFilterTypeDef = ...,
    ) -> ListAnnotationImportJobsResponseTypeDef:
        """
        Retrieves a list of annotation import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_annotation_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_annotation_import_jobs)
        """

    async def list_annotation_store_versions(
        self,
        *,
        name: str,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ListAnnotationStoreVersionsFilterTypeDef = ...,
    ) -> ListAnnotationStoreVersionsResponseTypeDef:
        """
        Lists the versions of an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_annotation_store_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_annotation_store_versions)
        """

    async def list_annotation_stores(
        self,
        *,
        ids: Sequence[str] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ListAnnotationStoresFilterTypeDef = ...,
    ) -> ListAnnotationStoresResponseTypeDef:
        """
        Retrieves a list of annotation stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_annotation_stores)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_annotation_stores)
        """

    async def list_multipart_read_set_uploads(
        self, *, sequenceStoreId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListMultipartReadSetUploadsResponseTypeDef:
        """
        Lists multipart read set uploads and for in progress uploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_multipart_read_set_uploads)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_multipart_read_set_uploads)
        """

    async def list_read_set_activation_jobs(
        self,
        *,
        sequenceStoreId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ActivateReadSetFilterTypeDef = ...,
    ) -> ListReadSetActivationJobsResponseTypeDef:
        """
        Retrieves a list of read set activation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_read_set_activation_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_set_activation_jobs)
        """

    async def list_read_set_export_jobs(
        self,
        *,
        sequenceStoreId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ExportReadSetFilterTypeDef = ...,
    ) -> ListReadSetExportJobsResponseTypeDef:
        """
        Retrieves a list of read set export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_read_set_export_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_set_export_jobs)
        """

    async def list_read_set_import_jobs(
        self,
        *,
        sequenceStoreId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ImportReadSetFilterTypeDef = ...,
    ) -> ListReadSetImportJobsResponseTypeDef:
        """
        Retrieves a list of read set import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_read_set_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_set_import_jobs)
        """

    async def list_read_set_upload_parts(
        self,
        *,
        sequenceStoreId: str,
        uploadId: str,
        partSource: ReadSetPartSourceType,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ReadSetUploadPartListFilterTypeDef = ...,
    ) -> ListReadSetUploadPartsResponseTypeDef:
        """
        This operation will list all parts in a requested multipart upload for a
        sequence
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_read_set_upload_parts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_set_upload_parts)
        """

    async def list_read_sets(
        self,
        *,
        sequenceStoreId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ReadSetFilterTypeDef = ...,
    ) -> ListReadSetsResponseTypeDef:
        """
        Retrieves a list of read sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_read_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_read_sets)
        """

    async def list_reference_import_jobs(
        self,
        *,
        referenceStoreId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ImportReferenceFilterTypeDef = ...,
    ) -> ListReferenceImportJobsResponseTypeDef:
        """
        Retrieves a list of reference import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_reference_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_reference_import_jobs)
        """

    async def list_reference_stores(
        self,
        *,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ReferenceStoreFilterTypeDef = ...,
    ) -> ListReferenceStoresResponseTypeDef:
        """
        Retrieves a list of reference stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_reference_stores)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_reference_stores)
        """

    async def list_references(
        self,
        *,
        referenceStoreId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: ReferenceFilterTypeDef = ...,
    ) -> ListReferencesResponseTypeDef:
        """
        Retrieves a list of references.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_references)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_references)
        """

    async def list_run_groups(
        self, *, name: str = ..., startingToken: str = ..., maxResults: int = ...
    ) -> ListRunGroupsResponseTypeDef:
        """
        Retrieves a list of run groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_run_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_run_groups)
        """

    async def list_run_tasks(
        self,
        *,
        id: str,
        status: TaskStatusType = ...,
        startingToken: str = ...,
        maxResults: int = ...,
    ) -> ListRunTasksResponseTypeDef:
        """
        Retrieves a list of tasks for a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_run_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_run_tasks)
        """

    async def list_runs(
        self,
        *,
        name: str = ...,
        runGroupId: str = ...,
        startingToken: str = ...,
        maxResults: int = ...,
        status: RunStatusType = ...,
    ) -> ListRunsResponseTypeDef:
        """
        Retrieves a list of runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_runs)
        """

    async def list_sequence_stores(
        self,
        *,
        maxResults: int = ...,
        nextToken: str = ...,
        filter: SequenceStoreFilterTypeDef = ...,
    ) -> ListSequenceStoresResponseTypeDef:
        """
        Retrieves a list of sequence stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_sequence_stores)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_sequence_stores)
        """

    async def list_shares(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        filter: FilterTypeDef = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListSharesResponseTypeDef:
        """
        Retrieves the resource shares associated with an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_shares)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_shares)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_tags_for_resource)
        """

    async def list_variant_import_jobs(
        self,
        *,
        maxResults: int = ...,
        ids: Sequence[str] = ...,
        nextToken: str = ...,
        filter: ListVariantImportJobsFilterTypeDef = ...,
    ) -> ListVariantImportJobsResponseTypeDef:
        """
        Retrieves a list of variant import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_variant_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_variant_import_jobs)
        """

    async def list_variant_stores(
        self,
        *,
        maxResults: int = ...,
        ids: Sequence[str] = ...,
        nextToken: str = ...,
        filter: ListVariantStoresFilterTypeDef = ...,
    ) -> ListVariantStoresResponseTypeDef:
        """
        Retrieves a list of variant stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_variant_stores)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_variant_stores)
        """

    async def list_workflows(
        self,
        *,
        type: WorkflowTypeType = ...,
        name: str = ...,
        startingToken: str = ...,
        maxResults: int = ...,
    ) -> ListWorkflowsResponseTypeDef:
        """
        Retrieves a list of workflows.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.list_workflows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#list_workflows)
        """

    async def start_annotation_import_job(
        self,
        *,
        destinationName: str,
        roleArn: str,
        items: Sequence[AnnotationImportItemSourceTypeDef],
        versionName: str = ...,
        formatOptions: FormatOptionsTypeDef = ...,
        runLeftNormalization: bool = ...,
        annotationFields: Mapping[str, str] = ...,
    ) -> StartAnnotationImportResponseTypeDef:
        """
        Starts an annotation import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.start_annotation_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_annotation_import_job)
        """

    async def start_read_set_activation_job(
        self,
        *,
        sequenceStoreId: str,
        sources: Sequence[StartReadSetActivationJobSourceItemTypeDef],
        clientToken: str = ...,
    ) -> StartReadSetActivationJobResponseTypeDef:
        """
        Activates an archived read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.start_read_set_activation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_read_set_activation_job)
        """

    async def start_read_set_export_job(
        self,
        *,
        sequenceStoreId: str,
        destination: str,
        roleArn: str,
        sources: Sequence[ExportReadSetTypeDef],
        clientToken: str = ...,
    ) -> StartReadSetExportJobResponseTypeDef:
        """
        Exports a read set to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.start_read_set_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_read_set_export_job)
        """

    async def start_read_set_import_job(
        self,
        *,
        sequenceStoreId: str,
        roleArn: str,
        sources: Sequence[StartReadSetImportJobSourceItemTypeDef],
        clientToken: str = ...,
    ) -> StartReadSetImportJobResponseTypeDef:
        """
        Starts a read set import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.start_read_set_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_read_set_import_job)
        """

    async def start_reference_import_job(
        self,
        *,
        referenceStoreId: str,
        roleArn: str,
        sources: Sequence[StartReferenceImportJobSourceItemTypeDef],
        clientToken: str = ...,
    ) -> StartReferenceImportJobResponseTypeDef:
        """
        Starts a reference import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.start_reference_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_reference_import_job)
        """

    async def start_run(
        self,
        *,
        roleArn: str,
        requestId: str,
        workflowId: str = ...,
        workflowType: WorkflowTypeType = ...,
        runId: str = ...,
        name: str = ...,
        runGroupId: str = ...,
        priority: int = ...,
        parameters: Mapping[str, Any] = ...,
        storageCapacity: int = ...,
        outputUri: str = ...,
        logLevel: RunLogLevelType = ...,
        tags: Mapping[str, str] = ...,
        retentionMode: RunRetentionModeType = ...,
        storageType: StorageTypeType = ...,
        workflowOwnerId: str = ...,
    ) -> StartRunResponseTypeDef:
        """
        Starts a workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.start_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_run)
        """

    async def start_variant_import_job(
        self,
        *,
        destinationName: str,
        roleArn: str,
        items: Sequence[VariantImportItemSourceTypeDef],
        runLeftNormalization: bool = ...,
        annotationFields: Mapping[str, str] = ...,
    ) -> StartVariantImportResponseTypeDef:
        """
        Starts a variant import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.start_variant_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#start_variant_import_job)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#untag_resource)
        """

    async def update_annotation_store(
        self, *, name: str, description: str = ...
    ) -> UpdateAnnotationStoreResponseTypeDef:
        """
        Updates an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.update_annotation_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_annotation_store)
        """

    async def update_annotation_store_version(
        self, *, name: str, versionName: str, description: str = ...
    ) -> UpdateAnnotationStoreVersionResponseTypeDef:
        """
        Updates the description of an annotation store version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.update_annotation_store_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_annotation_store_version)
        """

    async def update_run_group(
        self,
        *,
        id: str,
        name: str = ...,
        maxCpus: int = ...,
        maxRuns: int = ...,
        maxDuration: int = ...,
        maxGpus: int = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a run group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.update_run_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_run_group)
        """

    async def update_variant_store(
        self, *, name: str, description: str = ...
    ) -> UpdateVariantStoreResponseTypeDef:
        """
        Updates a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.update_variant_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_variant_store)
        """

    async def update_workflow(
        self, *, id: str, name: str = ..., description: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.update_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#update_workflow)
        """

    async def upload_read_set_part(
        self,
        *,
        sequenceStoreId: str,
        uploadId: str,
        partSource: ReadSetPartSourceType,
        partNumber: int,
        payload: BlobTypeDef,
    ) -> UploadReadSetPartResponseTypeDef:
        """
        This operation uploads a specific part of a read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.upload_read_set_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#upload_read_set_part)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_annotation_import_jobs"]
    ) -> ListAnnotationImportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_annotation_store_versions"]
    ) -> ListAnnotationStoreVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_annotation_stores"]
    ) -> ListAnnotationStoresPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multipart_read_set_uploads"]
    ) -> ListMultipartReadSetUploadsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_activation_jobs"]
    ) -> ListReadSetActivationJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_export_jobs"]
    ) -> ListReadSetExportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_import_jobs"]
    ) -> ListReadSetImportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_upload_parts"]
    ) -> ListReadSetUploadPartsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_read_sets"]) -> ListReadSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reference_import_jobs"]
    ) -> ListReferenceImportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reference_stores"]
    ) -> ListReferenceStoresPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_references"]) -> ListReferencesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_run_groups"]) -> ListRunGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_run_tasks"]) -> ListRunTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_runs"]) -> ListRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sequence_stores"]
    ) -> ListSequenceStoresPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_shares"]) -> ListSharesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_variant_import_jobs"]
    ) -> ListVariantImportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_variant_stores"]
    ) -> ListVariantStoresPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workflows"]) -> ListWorkflowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_import_job_created"]
    ) -> AnnotationImportJobCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_created"]
    ) -> AnnotationStoreCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_deleted"]
    ) -> AnnotationStoreDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_version_created"]
    ) -> AnnotationStoreVersionCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_version_deleted"]
    ) -> AnnotationStoreVersionDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["read_set_activation_job_completed"]
    ) -> ReadSetActivationJobCompletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["read_set_export_job_completed"]
    ) -> ReadSetExportJobCompletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["read_set_import_job_completed"]
    ) -> ReadSetImportJobCompletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["reference_import_job_completed"]
    ) -> ReferenceImportJobCompletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["run_completed"]) -> RunCompletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["run_running"]) -> RunRunningWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["task_completed"]) -> TaskCompletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["task_running"]) -> TaskRunningWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["variant_import_job_created"]
    ) -> VariantImportJobCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["variant_store_created"]
    ) -> VariantStoreCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["variant_store_deleted"]
    ) -> VariantStoreDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["workflow_active"]) -> WorkflowActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/#get_waiter)
        """

    async def __aenter__(self) -> "OmicsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_omics/client/)
        """
