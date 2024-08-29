"""
Type annotations for comprehendmedical service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_comprehendmedical.client import ComprehendMedicalClient

    session = get_session()
    async with session.create_client("comprehendmedical") as client:
        client: ComprehendMedicalClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    ComprehendMedicalAsyncJobFilterTypeDef,
    DescribeEntitiesDetectionV2JobResponseTypeDef,
    DescribeICD10CMInferenceJobResponseTypeDef,
    DescribePHIDetectionJobResponseTypeDef,
    DescribeRxNormInferenceJobResponseTypeDef,
    DescribeSNOMEDCTInferenceJobResponseTypeDef,
    DetectEntitiesResponseTypeDef,
    DetectEntitiesV2ResponseTypeDef,
    DetectPHIResponseTypeDef,
    InferICD10CMResponseTypeDef,
    InferRxNormResponseTypeDef,
    InferSNOMEDCTResponseTypeDef,
    InputDataConfigTypeDef,
    ListEntitiesDetectionV2JobsResponseTypeDef,
    ListICD10CMInferenceJobsResponseTypeDef,
    ListPHIDetectionJobsResponseTypeDef,
    ListRxNormInferenceJobsResponseTypeDef,
    ListSNOMEDCTInferenceJobsResponseTypeDef,
    OutputDataConfigTypeDef,
    StartEntitiesDetectionV2JobResponseTypeDef,
    StartICD10CMInferenceJobResponseTypeDef,
    StartPHIDetectionJobResponseTypeDef,
    StartRxNormInferenceJobResponseTypeDef,
    StartSNOMEDCTInferenceJobResponseTypeDef,
    StopEntitiesDetectionV2JobResponseTypeDef,
    StopICD10CMInferenceJobResponseTypeDef,
    StopPHIDetectionJobResponseTypeDef,
    StopRxNormInferenceJobResponseTypeDef,
    StopSNOMEDCTInferenceJobResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ComprehendMedicalClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidEncodingException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TextSizeLimitExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ComprehendMedicalClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ComprehendMedicalClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#close)
        """

    async def describe_entities_detection_v2_job(
        self, *, JobId: str
    ) -> DescribeEntitiesDetectionV2JobResponseTypeDef:
        """
        Gets the properties associated with a medical entities detection job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.describe_entities_detection_v2_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_entities_detection_v2_job)
        """

    async def describe_icd10_cm_inference_job(
        self, *, JobId: str
    ) -> DescribeICD10CMInferenceJobResponseTypeDef:
        """
        Gets the properties associated with an InferICD10CM job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.describe_icd10_cm_inference_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_icd10_cm_inference_job)
        """

    async def describe_phi_detection_job(
        self, *, JobId: str
    ) -> DescribePHIDetectionJobResponseTypeDef:
        """
        Gets the properties associated with a protected health information (PHI)
        detection
        job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.describe_phi_detection_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_phi_detection_job)
        """

    async def describe_rx_norm_inference_job(
        self, *, JobId: str
    ) -> DescribeRxNormInferenceJobResponseTypeDef:
        """
        Gets the properties associated with an InferRxNorm job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.describe_rx_norm_inference_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_rx_norm_inference_job)
        """

    async def describe_snomedct_inference_job(
        self, *, JobId: str
    ) -> DescribeSNOMEDCTInferenceJobResponseTypeDef:
        """
        Gets the properties associated with an InferSNOMEDCT job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.describe_snomedct_inference_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_snomedct_inference_job)
        """

    async def detect_entities(self, *, Text: str) -> DetectEntitiesResponseTypeDef:
        """
        The `DetectEntities` operation is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.detect_entities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#detect_entities)
        """

    async def detect_entities_v2(self, *, Text: str) -> DetectEntitiesV2ResponseTypeDef:
        """
        Inspects the clinical text for a variety of medical entities and returns
        specific information about them such as entity category, location, and
        confidence score on that
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.detect_entities_v2)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#detect_entities_v2)
        """

    async def detect_phi(self, *, Text: str) -> DetectPHIResponseTypeDef:
        """
        Inspects the clinical text for protected health information (PHI) entities and
        returns the entity category, location, and confidence score for each
        entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.detect_phi)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#detect_phi)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#generate_presigned_url)
        """

    async def infer_icd10_cm(self, *, Text: str) -> InferICD10CMResponseTypeDef:
        """
        InferICD10CM detects medical conditions as entities listed in a patient record
        and links those entities to normalized concept identifiers in the ICD-10-CM
        knowledge base from the Centers for Disease
        Control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.infer_icd10_cm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#infer_icd10_cm)
        """

    async def infer_rx_norm(self, *, Text: str) -> InferRxNormResponseTypeDef:
        """
        InferRxNorm detects medications as entities listed in a patient record and
        links to the normalized concept identifiers in the RxNorm database from the
        National Library of
        Medicine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.infer_rx_norm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#infer_rx_norm)
        """

    async def infer_snomedct(self, *, Text: str) -> InferSNOMEDCTResponseTypeDef:
        """
        InferSNOMEDCT detects possible medical concepts as entities and links them to
        codes from the Systematized Nomenclature of Medicine, Clinical Terms
        (SNOMED-CT) ontology See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/comprehendmedical-2018-10-30/InferSNOMEDCT)
        **Re...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.infer_snomedct)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#infer_snomedct)
        """

    async def list_entities_detection_v2_jobs(
        self,
        *,
        Filter: ComprehendMedicalAsyncJobFilterTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListEntitiesDetectionV2JobsResponseTypeDef:
        """
        Gets a list of medical entity detection jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.list_entities_detection_v2_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_entities_detection_v2_jobs)
        """

    async def list_icd10_cm_inference_jobs(
        self,
        *,
        Filter: ComprehendMedicalAsyncJobFilterTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListICD10CMInferenceJobsResponseTypeDef:
        """
        Gets a list of InferICD10CM jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.list_icd10_cm_inference_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_icd10_cm_inference_jobs)
        """

    async def list_phi_detection_jobs(
        self,
        *,
        Filter: ComprehendMedicalAsyncJobFilterTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListPHIDetectionJobsResponseTypeDef:
        """
        Gets a list of protected health information (PHI) detection jobs you have
        submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.list_phi_detection_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_phi_detection_jobs)
        """

    async def list_rx_norm_inference_jobs(
        self,
        *,
        Filter: ComprehendMedicalAsyncJobFilterTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListRxNormInferenceJobsResponseTypeDef:
        """
        Gets a list of InferRxNorm jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.list_rx_norm_inference_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_rx_norm_inference_jobs)
        """

    async def list_snomedct_inference_jobs(
        self,
        *,
        Filter: ComprehendMedicalAsyncJobFilterTypeDef = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListSNOMEDCTInferenceJobsResponseTypeDef:
        """
        Gets a list of InferSNOMEDCT jobs a user has submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.list_snomedct_inference_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_snomedct_inference_jobs)
        """

    async def start_entities_detection_v2_job(
        self,
        *,
        InputDataConfig: InputDataConfigTypeDef,
        OutputDataConfig: OutputDataConfigTypeDef,
        DataAccessRoleArn: str,
        LanguageCode: Literal["en"],
        JobName: str = ...,
        ClientRequestToken: str = ...,
        KMSKey: str = ...,
    ) -> StartEntitiesDetectionV2JobResponseTypeDef:
        """
        Starts an asynchronous medical entity detection job for a collection of
        documents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.start_entities_detection_v2_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_entities_detection_v2_job)
        """

    async def start_icd10_cm_inference_job(
        self,
        *,
        InputDataConfig: InputDataConfigTypeDef,
        OutputDataConfig: OutputDataConfigTypeDef,
        DataAccessRoleArn: str,
        LanguageCode: Literal["en"],
        JobName: str = ...,
        ClientRequestToken: str = ...,
        KMSKey: str = ...,
    ) -> StartICD10CMInferenceJobResponseTypeDef:
        """
        Starts an asynchronous job to detect medical conditions and link them to the
        ICD-10-CM
        ontology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.start_icd10_cm_inference_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_icd10_cm_inference_job)
        """

    async def start_phi_detection_job(
        self,
        *,
        InputDataConfig: InputDataConfigTypeDef,
        OutputDataConfig: OutputDataConfigTypeDef,
        DataAccessRoleArn: str,
        LanguageCode: Literal["en"],
        JobName: str = ...,
        ClientRequestToken: str = ...,
        KMSKey: str = ...,
    ) -> StartPHIDetectionJobResponseTypeDef:
        """
        Starts an asynchronous job to detect protected health information (PHI).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.start_phi_detection_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_phi_detection_job)
        """

    async def start_rx_norm_inference_job(
        self,
        *,
        InputDataConfig: InputDataConfigTypeDef,
        OutputDataConfig: OutputDataConfigTypeDef,
        DataAccessRoleArn: str,
        LanguageCode: Literal["en"],
        JobName: str = ...,
        ClientRequestToken: str = ...,
        KMSKey: str = ...,
    ) -> StartRxNormInferenceJobResponseTypeDef:
        """
        Starts an asynchronous job to detect medication entities and link them to the
        RxNorm
        ontology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.start_rx_norm_inference_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_rx_norm_inference_job)
        """

    async def start_snomedct_inference_job(
        self,
        *,
        InputDataConfig: InputDataConfigTypeDef,
        OutputDataConfig: OutputDataConfigTypeDef,
        DataAccessRoleArn: str,
        LanguageCode: Literal["en"],
        JobName: str = ...,
        ClientRequestToken: str = ...,
        KMSKey: str = ...,
    ) -> StartSNOMEDCTInferenceJobResponseTypeDef:
        """
        Starts an asynchronous job to detect medical concepts and link them to the
        SNOMED-CT
        ontology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.start_snomedct_inference_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_snomedct_inference_job)
        """

    async def stop_entities_detection_v2_job(
        self, *, JobId: str
    ) -> StopEntitiesDetectionV2JobResponseTypeDef:
        """
        Stops a medical entities detection job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.stop_entities_detection_v2_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_entities_detection_v2_job)
        """

    async def stop_icd10_cm_inference_job(
        self, *, JobId: str
    ) -> StopICD10CMInferenceJobResponseTypeDef:
        """
        Stops an InferICD10CM inference job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.stop_icd10_cm_inference_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_icd10_cm_inference_job)
        """

    async def stop_phi_detection_job(self, *, JobId: str) -> StopPHIDetectionJobResponseTypeDef:
        """
        Stops a protected health information (PHI) detection job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.stop_phi_detection_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_phi_detection_job)
        """

    async def stop_rx_norm_inference_job(
        self, *, JobId: str
    ) -> StopRxNormInferenceJobResponseTypeDef:
        """
        Stops an InferRxNorm inference job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.stop_rx_norm_inference_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_rx_norm_inference_job)
        """

    async def stop_snomedct_inference_job(
        self, *, JobId: str
    ) -> StopSNOMEDCTInferenceJobResponseTypeDef:
        """
        Stops an InferSNOMEDCT inference job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client.stop_snomedct_inference_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_snomedct_inference_job)
        """

    async def __aenter__(self) -> "ComprehendMedicalClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/)
        """
