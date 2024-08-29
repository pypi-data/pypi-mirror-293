"""
Type annotations for imagebuilder service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_imagebuilder.client import ImagebuilderClient

    session = get_session()
    async with session.create_client("imagebuilder") as client:
        client: ImagebuilderClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ComponentTypeType,
    LifecyclePolicyResourceTypeType,
    LifecyclePolicyStatusType,
    OwnershipType,
    PipelineStatusType,
    PlatformType,
    WorkflowStepActionTypeType,
    WorkflowTypeType,
)
from .type_defs import (
    AdditionalInstanceConfigurationTypeDef,
    CancelImageCreationResponseTypeDef,
    CancelLifecycleExecutionResponseTypeDef,
    ComponentConfigurationUnionTypeDef,
    CreateComponentResponseTypeDef,
    CreateContainerRecipeResponseTypeDef,
    CreateDistributionConfigurationResponseTypeDef,
    CreateImagePipelineResponseTypeDef,
    CreateImageRecipeResponseTypeDef,
    CreateImageResponseTypeDef,
    CreateInfrastructureConfigurationResponseTypeDef,
    CreateLifecyclePolicyResponseTypeDef,
    CreateWorkflowResponseTypeDef,
    DeleteComponentResponseTypeDef,
    DeleteContainerRecipeResponseTypeDef,
    DeleteDistributionConfigurationResponseTypeDef,
    DeleteImagePipelineResponseTypeDef,
    DeleteImageRecipeResponseTypeDef,
    DeleteImageResponseTypeDef,
    DeleteInfrastructureConfigurationResponseTypeDef,
    DeleteLifecyclePolicyResponseTypeDef,
    DeleteWorkflowResponseTypeDef,
    DistributionUnionTypeDef,
    FilterTypeDef,
    GetComponentPolicyResponseTypeDef,
    GetComponentResponseTypeDef,
    GetContainerRecipePolicyResponseTypeDef,
    GetContainerRecipeResponseTypeDef,
    GetDistributionConfigurationResponseTypeDef,
    GetImagePipelineResponseTypeDef,
    GetImagePolicyResponseTypeDef,
    GetImageRecipePolicyResponseTypeDef,
    GetImageRecipeResponseTypeDef,
    GetImageResponseTypeDef,
    GetInfrastructureConfigurationResponseTypeDef,
    GetLifecycleExecutionResponseTypeDef,
    GetLifecyclePolicyResponseTypeDef,
    GetWorkflowExecutionResponseTypeDef,
    GetWorkflowResponseTypeDef,
    GetWorkflowStepExecutionResponseTypeDef,
    ImageScanFindingsFilterTypeDef,
    ImageScanningConfigurationUnionTypeDef,
    ImageTestsConfigurationTypeDef,
    ImportComponentResponseTypeDef,
    ImportVmImageResponseTypeDef,
    InstanceBlockDeviceMappingTypeDef,
    InstanceConfigurationUnionTypeDef,
    InstanceMetadataOptionsTypeDef,
    LifecyclePolicyDetailUnionTypeDef,
    LifecyclePolicyResourceSelectionUnionTypeDef,
    ListComponentBuildVersionsResponseTypeDef,
    ListComponentsResponseTypeDef,
    ListContainerRecipesResponseTypeDef,
    ListDistributionConfigurationsResponseTypeDef,
    ListImageBuildVersionsResponseTypeDef,
    ListImagePackagesResponseTypeDef,
    ListImagePipelineImagesResponseTypeDef,
    ListImagePipelinesResponseTypeDef,
    ListImageRecipesResponseTypeDef,
    ListImageScanFindingAggregationsResponseTypeDef,
    ListImageScanFindingsResponseTypeDef,
    ListImagesResponseTypeDef,
    ListInfrastructureConfigurationsResponseTypeDef,
    ListLifecycleExecutionResourcesResponseTypeDef,
    ListLifecycleExecutionsResponseTypeDef,
    ListLifecyclePoliciesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWaitingWorkflowStepsResponseTypeDef,
    ListWorkflowBuildVersionsResponseTypeDef,
    ListWorkflowExecutionsResponseTypeDef,
    ListWorkflowsResponseTypeDef,
    ListWorkflowStepExecutionsResponseTypeDef,
    LoggingTypeDef,
    PutComponentPolicyResponseTypeDef,
    PutContainerRecipePolicyResponseTypeDef,
    PutImagePolicyResponseTypeDef,
    PutImageRecipePolicyResponseTypeDef,
    ResourceStateTypeDef,
    ResourceStateUpdateExclusionRulesTypeDef,
    ResourceStateUpdateIncludeResourcesTypeDef,
    ScheduleTypeDef,
    SendWorkflowStepActionResponseTypeDef,
    StartImagePipelineExecutionResponseTypeDef,
    StartResourceStateUpdateResponseTypeDef,
    TargetContainerRepositoryTypeDef,
    TimestampTypeDef,
    UpdateDistributionConfigurationResponseTypeDef,
    UpdateImagePipelineResponseTypeDef,
    UpdateInfrastructureConfigurationResponseTypeDef,
    UpdateLifecyclePolicyResponseTypeDef,
    WorkflowConfigurationUnionTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ImagebuilderClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    CallRateLimitExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidVersionNumberException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceDependencyException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]


class ImagebuilderClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ImagebuilderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#can_paginate)
        """

    async def cancel_image_creation(
        self, *, imageBuildVersionArn: str, clientToken: str
    ) -> CancelImageCreationResponseTypeDef:
        """
        CancelImageCreation cancels the creation of Image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.cancel_image_creation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#cancel_image_creation)
        """

    async def cancel_lifecycle_execution(
        self, *, lifecycleExecutionId: str, clientToken: str
    ) -> CancelLifecycleExecutionResponseTypeDef:
        """
        Cancel a specific image lifecycle policy runtime instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.cancel_lifecycle_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#cancel_lifecycle_execution)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#close)
        """

    async def create_component(
        self,
        *,
        name: str,
        semanticVersion: str,
        platform: PlatformType,
        clientToken: str,
        description: str = ...,
        changeDescription: str = ...,
        supportedOsVersions: Sequence[str] = ...,
        data: str = ...,
        uri: str = ...,
        kmsKeyId: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateComponentResponseTypeDef:
        """
        Creates a new component that can be used to build, validate, test, and assess
        your
        image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.create_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_component)
        """

    async def create_container_recipe(
        self,
        *,
        containerType: Literal["DOCKER"],
        name: str,
        semanticVersion: str,
        components: Sequence[ComponentConfigurationUnionTypeDef],
        parentImage: str,
        targetRepository: TargetContainerRepositoryTypeDef,
        clientToken: str,
        description: str = ...,
        instanceConfiguration: InstanceConfigurationUnionTypeDef = ...,
        dockerfileTemplateData: str = ...,
        dockerfileTemplateUri: str = ...,
        platformOverride: PlatformType = ...,
        imageOsVersionOverride: str = ...,
        tags: Mapping[str, str] = ...,
        workingDirectory: str = ...,
        kmsKeyId: str = ...,
    ) -> CreateContainerRecipeResponseTypeDef:
        """
        Creates a new container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.create_container_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_container_recipe)
        """

    async def create_distribution_configuration(
        self,
        *,
        name: str,
        distributions: Sequence[DistributionUnionTypeDef],
        clientToken: str,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateDistributionConfigurationResponseTypeDef:
        """
        Creates a new distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.create_distribution_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_distribution_configuration)
        """

    async def create_image(
        self,
        *,
        infrastructureConfigurationArn: str,
        clientToken: str,
        imageRecipeArn: str = ...,
        containerRecipeArn: str = ...,
        distributionConfigurationArn: str = ...,
        imageTestsConfiguration: ImageTestsConfigurationTypeDef = ...,
        enhancedImageMetadataEnabled: bool = ...,
        tags: Mapping[str, str] = ...,
        imageScanningConfiguration: ImageScanningConfigurationUnionTypeDef = ...,
        workflows: Sequence[WorkflowConfigurationUnionTypeDef] = ...,
        executionRole: str = ...,
    ) -> CreateImageResponseTypeDef:
        """
        Creates a new image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.create_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_image)
        """

    async def create_image_pipeline(
        self,
        *,
        name: str,
        infrastructureConfigurationArn: str,
        clientToken: str,
        description: str = ...,
        imageRecipeArn: str = ...,
        containerRecipeArn: str = ...,
        distributionConfigurationArn: str = ...,
        imageTestsConfiguration: ImageTestsConfigurationTypeDef = ...,
        enhancedImageMetadataEnabled: bool = ...,
        schedule: ScheduleTypeDef = ...,
        status: PipelineStatusType = ...,
        tags: Mapping[str, str] = ...,
        imageScanningConfiguration: ImageScanningConfigurationUnionTypeDef = ...,
        workflows: Sequence[WorkflowConfigurationUnionTypeDef] = ...,
        executionRole: str = ...,
    ) -> CreateImagePipelineResponseTypeDef:
        """
        Creates a new image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.create_image_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_image_pipeline)
        """

    async def create_image_recipe(
        self,
        *,
        name: str,
        semanticVersion: str,
        components: Sequence[ComponentConfigurationUnionTypeDef],
        parentImage: str,
        clientToken: str,
        description: str = ...,
        blockDeviceMappings: Sequence[InstanceBlockDeviceMappingTypeDef] = ...,
        tags: Mapping[str, str] = ...,
        workingDirectory: str = ...,
        additionalInstanceConfiguration: AdditionalInstanceConfigurationTypeDef = ...,
    ) -> CreateImageRecipeResponseTypeDef:
        """
        Creates a new image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.create_image_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_image_recipe)
        """

    async def create_infrastructure_configuration(
        self,
        *,
        name: str,
        instanceProfileName: str,
        clientToken: str,
        description: str = ...,
        instanceTypes: Sequence[str] = ...,
        securityGroupIds: Sequence[str] = ...,
        subnetId: str = ...,
        logging: LoggingTypeDef = ...,
        keyPair: str = ...,
        terminateInstanceOnFailure: bool = ...,
        snsTopicArn: str = ...,
        resourceTags: Mapping[str, str] = ...,
        instanceMetadataOptions: InstanceMetadataOptionsTypeDef = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateInfrastructureConfigurationResponseTypeDef:
        """
        Creates a new infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.create_infrastructure_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_infrastructure_configuration)
        """

    async def create_lifecycle_policy(
        self,
        *,
        name: str,
        executionRole: str,
        resourceType: LifecyclePolicyResourceTypeType,
        policyDetails: Sequence[LifecyclePolicyDetailUnionTypeDef],
        resourceSelection: LifecyclePolicyResourceSelectionUnionTypeDef,
        clientToken: str,
        description: str = ...,
        status: LifecyclePolicyStatusType = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateLifecyclePolicyResponseTypeDef:
        """
        Create a lifecycle policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.create_lifecycle_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_lifecycle_policy)
        """

    async def create_workflow(
        self,
        *,
        name: str,
        semanticVersion: str,
        clientToken: str,
        type: WorkflowTypeType,
        description: str = ...,
        changeDescription: str = ...,
        data: str = ...,
        uri: str = ...,
        kmsKeyId: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateWorkflowResponseTypeDef:
        """
        Create a new workflow or a new version of an existing workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.create_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#create_workflow)
        """

    async def delete_component(
        self, *, componentBuildVersionArn: str
    ) -> DeleteComponentResponseTypeDef:
        """
        Deletes a component build version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.delete_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_component)
        """

    async def delete_container_recipe(
        self, *, containerRecipeArn: str
    ) -> DeleteContainerRecipeResponseTypeDef:
        """
        Deletes a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.delete_container_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_container_recipe)
        """

    async def delete_distribution_configuration(
        self, *, distributionConfigurationArn: str
    ) -> DeleteDistributionConfigurationResponseTypeDef:
        """
        Deletes a distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.delete_distribution_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_distribution_configuration)
        """

    async def delete_image(self, *, imageBuildVersionArn: str) -> DeleteImageResponseTypeDef:
        """
        Deletes an Image Builder image resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.delete_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_image)
        """

    async def delete_image_pipeline(
        self, *, imagePipelineArn: str
    ) -> DeleteImagePipelineResponseTypeDef:
        """
        Deletes an image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.delete_image_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_image_pipeline)
        """

    async def delete_image_recipe(self, *, imageRecipeArn: str) -> DeleteImageRecipeResponseTypeDef:
        """
        Deletes an image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.delete_image_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_image_recipe)
        """

    async def delete_infrastructure_configuration(
        self, *, infrastructureConfigurationArn: str
    ) -> DeleteInfrastructureConfigurationResponseTypeDef:
        """
        Deletes an infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.delete_infrastructure_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_infrastructure_configuration)
        """

    async def delete_lifecycle_policy(
        self, *, lifecyclePolicyArn: str
    ) -> DeleteLifecyclePolicyResponseTypeDef:
        """
        Delete the specified lifecycle policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.delete_lifecycle_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_lifecycle_policy)
        """

    async def delete_workflow(
        self, *, workflowBuildVersionArn: str
    ) -> DeleteWorkflowResponseTypeDef:
        """
        Deletes a specific workflow resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.delete_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#delete_workflow)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#generate_presigned_url)
        """

    async def get_component(self, *, componentBuildVersionArn: str) -> GetComponentResponseTypeDef:
        """
        Gets a component object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_component)
        """

    async def get_component_policy(self, *, componentArn: str) -> GetComponentPolicyResponseTypeDef:
        """
        Gets a component policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_component_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_component_policy)
        """

    async def get_container_recipe(
        self, *, containerRecipeArn: str
    ) -> GetContainerRecipeResponseTypeDef:
        """
        Retrieves a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_container_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_container_recipe)
        """

    async def get_container_recipe_policy(
        self, *, containerRecipeArn: str
    ) -> GetContainerRecipePolicyResponseTypeDef:
        """
        Retrieves the policy for a container recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_container_recipe_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_container_recipe_policy)
        """

    async def get_distribution_configuration(
        self, *, distributionConfigurationArn: str
    ) -> GetDistributionConfigurationResponseTypeDef:
        """
        Gets a distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_distribution_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_distribution_configuration)
        """

    async def get_image(self, *, imageBuildVersionArn: str) -> GetImageResponseTypeDef:
        """
        Gets an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image)
        """

    async def get_image_pipeline(self, *, imagePipelineArn: str) -> GetImagePipelineResponseTypeDef:
        """
        Gets an image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_image_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_pipeline)
        """

    async def get_image_policy(self, *, imageArn: str) -> GetImagePolicyResponseTypeDef:
        """
        Gets an image policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_image_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_policy)
        """

    async def get_image_recipe(self, *, imageRecipeArn: str) -> GetImageRecipeResponseTypeDef:
        """
        Gets an image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_image_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_recipe)
        """

    async def get_image_recipe_policy(
        self, *, imageRecipeArn: str
    ) -> GetImageRecipePolicyResponseTypeDef:
        """
        Gets an image recipe policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_image_recipe_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_image_recipe_policy)
        """

    async def get_infrastructure_configuration(
        self, *, infrastructureConfigurationArn: str
    ) -> GetInfrastructureConfigurationResponseTypeDef:
        """
        Gets an infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_infrastructure_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_infrastructure_configuration)
        """

    async def get_lifecycle_execution(
        self, *, lifecycleExecutionId: str
    ) -> GetLifecycleExecutionResponseTypeDef:
        """
        Get the runtime information that was logged for a specific runtime instance of
        the lifecycle
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_lifecycle_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_lifecycle_execution)
        """

    async def get_lifecycle_policy(
        self, *, lifecyclePolicyArn: str
    ) -> GetLifecyclePolicyResponseTypeDef:
        """
        Get details for the specified image lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_lifecycle_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_lifecycle_policy)
        """

    async def get_workflow(self, *, workflowBuildVersionArn: str) -> GetWorkflowResponseTypeDef:
        """
        Get a workflow resource object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_workflow)
        """

    async def get_workflow_execution(
        self, *, workflowExecutionId: str
    ) -> GetWorkflowExecutionResponseTypeDef:
        """
        Get the runtime information that was logged for a specific runtime instance of
        the
        workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_workflow_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_workflow_execution)
        """

    async def get_workflow_step_execution(
        self, *, stepExecutionId: str
    ) -> GetWorkflowStepExecutionResponseTypeDef:
        """
        Get the runtime information that was logged for a specific runtime instance of
        the workflow
        step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.get_workflow_step_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#get_workflow_step_execution)
        """

    async def import_component(
        self,
        *,
        name: str,
        semanticVersion: str,
        type: ComponentTypeType,
        format: Literal["SHELL"],
        platform: PlatformType,
        clientToken: str,
        description: str = ...,
        changeDescription: str = ...,
        data: str = ...,
        uri: str = ...,
        kmsKeyId: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> ImportComponentResponseTypeDef:
        """
        Imports a component and transforms its data into a component document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.import_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#import_component)
        """

    async def import_vm_image(
        self,
        *,
        name: str,
        semanticVersion: str,
        platform: PlatformType,
        vmImportTaskId: str,
        clientToken: str,
        description: str = ...,
        osVersion: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> ImportVmImageResponseTypeDef:
        """
        When you export your virtual machine (VM) from its virtualization environment,
        that process creates a set of one or more disk container files that act as
        snapshots of your VM's environment, settings, and
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.import_vm_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#import_vm_image)
        """

    async def list_component_build_versions(
        self, *, componentVersionArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListComponentBuildVersionsResponseTypeDef:
        """
        Returns the list of component build versions for the specified semantic version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_component_build_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_component_build_versions)
        """

    async def list_components(
        self,
        *,
        owner: OwnershipType = ...,
        filters: Sequence[FilterTypeDef] = ...,
        byName: bool = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListComponentsResponseTypeDef:
        """
        Returns the list of components that can be filtered by name, or by using the
        listed `filters` to streamline
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_components)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_components)
        """

    async def list_container_recipes(
        self,
        *,
        owner: OwnershipType = ...,
        filters: Sequence[FilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListContainerRecipesResponseTypeDef:
        """
        Returns a list of container recipes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_container_recipes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_container_recipes)
        """

    async def list_distribution_configurations(
        self, *, filters: Sequence[FilterTypeDef] = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListDistributionConfigurationsResponseTypeDef:
        """
        Returns a list of distribution configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_distribution_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_distribution_configurations)
        """

    async def list_image_build_versions(
        self,
        *,
        imageVersionArn: str,
        filters: Sequence[FilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListImageBuildVersionsResponseTypeDef:
        """
        Returns a list of image build versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_image_build_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_build_versions)
        """

    async def list_image_packages(
        self, *, imageBuildVersionArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListImagePackagesResponseTypeDef:
        """
        List the Packages that are associated with an Image Build Version, as
        determined by Amazon Web Services Systems Manager Inventory at build
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_image_packages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_packages)
        """

    async def list_image_pipeline_images(
        self,
        *,
        imagePipelineArn: str,
        filters: Sequence[FilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListImagePipelineImagesResponseTypeDef:
        """
        Returns a list of images created by the specified pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_image_pipeline_images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_pipeline_images)
        """

    async def list_image_pipelines(
        self, *, filters: Sequence[FilterTypeDef] = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListImagePipelinesResponseTypeDef:
        """
        Returns a list of image pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_image_pipelines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_pipelines)
        """

    async def list_image_recipes(
        self,
        *,
        owner: OwnershipType = ...,
        filters: Sequence[FilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListImageRecipesResponseTypeDef:
        """
        Returns a list of image recipes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_image_recipes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_recipes)
        """

    async def list_image_scan_finding_aggregations(
        self, *, filter: FilterTypeDef = ..., nextToken: str = ...
    ) -> ListImageScanFindingAggregationsResponseTypeDef:
        """
        Returns a list of image scan aggregations for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_image_scan_finding_aggregations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_scan_finding_aggregations)
        """

    async def list_image_scan_findings(
        self,
        *,
        filters: Sequence[ImageScanFindingsFilterTypeDef] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListImageScanFindingsResponseTypeDef:
        """
        Returns a list of image scan findings for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_image_scan_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_image_scan_findings)
        """

    async def list_images(
        self,
        *,
        owner: OwnershipType = ...,
        filters: Sequence[FilterTypeDef] = ...,
        byName: bool = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        includeDeprecated: bool = ...,
    ) -> ListImagesResponseTypeDef:
        """
        Returns the list of images that you have access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_images)
        """

    async def list_infrastructure_configurations(
        self, *, filters: Sequence[FilterTypeDef] = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListInfrastructureConfigurationsResponseTypeDef:
        """
        Returns a list of infrastructure configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_infrastructure_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_infrastructure_configurations)
        """

    async def list_lifecycle_execution_resources(
        self,
        *,
        lifecycleExecutionId: str,
        parentResourceId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListLifecycleExecutionResourcesResponseTypeDef:
        """
        List resources that the runtime instance of the image lifecycle identified for
        lifecycle
        actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_lifecycle_execution_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_lifecycle_execution_resources)
        """

    async def list_lifecycle_executions(
        self, *, resourceArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListLifecycleExecutionsResponseTypeDef:
        """
        Get the lifecycle runtime history for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_lifecycle_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_lifecycle_executions)
        """

    async def list_lifecycle_policies(
        self, *, filters: Sequence[FilterTypeDef] = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListLifecyclePoliciesResponseTypeDef:
        """
        Get a list of lifecycle policies in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_lifecycle_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_lifecycle_policies)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the list of tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_tags_for_resource)
        """

    async def list_waiting_workflow_steps(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListWaitingWorkflowStepsResponseTypeDef:
        """
        Get a list of workflow steps that are waiting for action for workflows in your
        Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_waiting_workflow_steps)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_waiting_workflow_steps)
        """

    async def list_workflow_build_versions(
        self, *, workflowVersionArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkflowBuildVersionsResponseTypeDef:
        """
        Returns a list of build versions for a specific workflow resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_workflow_build_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflow_build_versions)
        """

    async def list_workflow_executions(
        self, *, imageBuildVersionArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkflowExecutionsResponseTypeDef:
        """
        Returns a list of workflow runtime instance metadata objects for a specific
        image build
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_workflow_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflow_executions)
        """

    async def list_workflow_step_executions(
        self, *, workflowExecutionId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkflowStepExecutionsResponseTypeDef:
        """
        Returns runtime data for each step in a runtime instance of the workflow that
        you specify in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_workflow_step_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflow_step_executions)
        """

    async def list_workflows(
        self,
        *,
        owner: OwnershipType = ...,
        filters: Sequence[FilterTypeDef] = ...,
        byName: bool = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListWorkflowsResponseTypeDef:
        """
        Lists workflow build versions based on filtering parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.list_workflows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#list_workflows)
        """

    async def put_component_policy(
        self, *, componentArn: str, policy: str
    ) -> PutComponentPolicyResponseTypeDef:
        """
        Applies a policy to a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.put_component_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_component_policy)
        """

    async def put_container_recipe_policy(
        self, *, containerRecipeArn: str, policy: str
    ) -> PutContainerRecipePolicyResponseTypeDef:
        """
        Applies a policy to a container image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.put_container_recipe_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_container_recipe_policy)
        """

    async def put_image_policy(
        self, *, imageArn: str, policy: str
    ) -> PutImagePolicyResponseTypeDef:
        """
        Applies a policy to an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.put_image_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_image_policy)
        """

    async def put_image_recipe_policy(
        self, *, imageRecipeArn: str, policy: str
    ) -> PutImageRecipePolicyResponseTypeDef:
        """
        Applies a policy to an image recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.put_image_recipe_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#put_image_recipe_policy)
        """

    async def send_workflow_step_action(
        self,
        *,
        stepExecutionId: str,
        imageBuildVersionArn: str,
        action: WorkflowStepActionTypeType,
        clientToken: str,
        reason: str = ...,
    ) -> SendWorkflowStepActionResponseTypeDef:
        """
        Pauses or resumes image creation when the associated workflow runs a
        `WaitForAction`
        step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.send_workflow_step_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#send_workflow_step_action)
        """

    async def start_image_pipeline_execution(
        self, *, imagePipelineArn: str, clientToken: str
    ) -> StartImagePipelineExecutionResponseTypeDef:
        """
        Manually triggers a pipeline to create an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.start_image_pipeline_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#start_image_pipeline_execution)
        """

    async def start_resource_state_update(
        self,
        *,
        resourceArn: str,
        state: ResourceStateTypeDef,
        clientToken: str,
        executionRole: str = ...,
        includeResources: ResourceStateUpdateIncludeResourcesTypeDef = ...,
        exclusionRules: ResourceStateUpdateExclusionRulesTypeDef = ...,
        updateAt: TimestampTypeDef = ...,
    ) -> StartResourceStateUpdateResponseTypeDef:
        """
        Begin asynchronous resource state update for lifecycle changes to the specified
        image
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.start_resource_state_update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#start_resource_state_update)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#untag_resource)
        """

    async def update_distribution_configuration(
        self,
        *,
        distributionConfigurationArn: str,
        distributions: Sequence[DistributionUnionTypeDef],
        clientToken: str,
        description: str = ...,
    ) -> UpdateDistributionConfigurationResponseTypeDef:
        """
        Updates a new distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.update_distribution_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_distribution_configuration)
        """

    async def update_image_pipeline(
        self,
        *,
        imagePipelineArn: str,
        infrastructureConfigurationArn: str,
        clientToken: str,
        description: str = ...,
        imageRecipeArn: str = ...,
        containerRecipeArn: str = ...,
        distributionConfigurationArn: str = ...,
        imageTestsConfiguration: ImageTestsConfigurationTypeDef = ...,
        enhancedImageMetadataEnabled: bool = ...,
        schedule: ScheduleTypeDef = ...,
        status: PipelineStatusType = ...,
        imageScanningConfiguration: ImageScanningConfigurationUnionTypeDef = ...,
        workflows: Sequence[WorkflowConfigurationUnionTypeDef] = ...,
        executionRole: str = ...,
    ) -> UpdateImagePipelineResponseTypeDef:
        """
        Updates an image pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.update_image_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_image_pipeline)
        """

    async def update_infrastructure_configuration(
        self,
        *,
        infrastructureConfigurationArn: str,
        instanceProfileName: str,
        clientToken: str,
        description: str = ...,
        instanceTypes: Sequence[str] = ...,
        securityGroupIds: Sequence[str] = ...,
        subnetId: str = ...,
        logging: LoggingTypeDef = ...,
        keyPair: str = ...,
        terminateInstanceOnFailure: bool = ...,
        snsTopicArn: str = ...,
        resourceTags: Mapping[str, str] = ...,
        instanceMetadataOptions: InstanceMetadataOptionsTypeDef = ...,
    ) -> UpdateInfrastructureConfigurationResponseTypeDef:
        """
        Updates a new infrastructure configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.update_infrastructure_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_infrastructure_configuration)
        """

    async def update_lifecycle_policy(
        self,
        *,
        lifecyclePolicyArn: str,
        executionRole: str,
        resourceType: LifecyclePolicyResourceTypeType,
        policyDetails: Sequence[LifecyclePolicyDetailUnionTypeDef],
        resourceSelection: LifecyclePolicyResourceSelectionUnionTypeDef,
        clientToken: str,
        description: str = ...,
        status: LifecyclePolicyStatusType = ...,
    ) -> UpdateLifecyclePolicyResponseTypeDef:
        """
        Update the specified lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client.update_lifecycle_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/#update_lifecycle_policy)
        """

    async def __aenter__(self) -> "ImagebuilderClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder.html#Imagebuilder.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_imagebuilder/client/)
        """
