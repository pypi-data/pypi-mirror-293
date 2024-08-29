"""
Type annotations for sagemaker service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker.client import SageMakerClient
    from types_aiobotocore_sagemaker.paginator import (
        ListActionsPaginator,
        ListAlgorithmsPaginator,
        ListAliasesPaginator,
        ListAppImageConfigsPaginator,
        ListAppsPaginator,
        ListArtifactsPaginator,
        ListAssociationsPaginator,
        ListAutoMLJobsPaginator,
        ListCandidatesForAutoMLJobPaginator,
        ListClusterNodesPaginator,
        ListClustersPaginator,
        ListCodeRepositoriesPaginator,
        ListCompilationJobsPaginator,
        ListContextsPaginator,
        ListDataQualityJobDefinitionsPaginator,
        ListDeviceFleetsPaginator,
        ListDevicesPaginator,
        ListDomainsPaginator,
        ListEdgeDeploymentPlansPaginator,
        ListEdgePackagingJobsPaginator,
        ListEndpointConfigsPaginator,
        ListEndpointsPaginator,
        ListExperimentsPaginator,
        ListFeatureGroupsPaginator,
        ListFlowDefinitionsPaginator,
        ListHumanTaskUisPaginator,
        ListHyperParameterTuningJobsPaginator,
        ListImageVersionsPaginator,
        ListImagesPaginator,
        ListInferenceComponentsPaginator,
        ListInferenceExperimentsPaginator,
        ListInferenceRecommendationsJobStepsPaginator,
        ListInferenceRecommendationsJobsPaginator,
        ListLabelingJobsPaginator,
        ListLabelingJobsForWorkteamPaginator,
        ListLineageGroupsPaginator,
        ListMlflowTrackingServersPaginator,
        ListModelBiasJobDefinitionsPaginator,
        ListModelCardExportJobsPaginator,
        ListModelCardVersionsPaginator,
        ListModelCardsPaginator,
        ListModelExplainabilityJobDefinitionsPaginator,
        ListModelMetadataPaginator,
        ListModelPackageGroupsPaginator,
        ListModelPackagesPaginator,
        ListModelQualityJobDefinitionsPaginator,
        ListModelsPaginator,
        ListMonitoringAlertHistoryPaginator,
        ListMonitoringAlertsPaginator,
        ListMonitoringExecutionsPaginator,
        ListMonitoringSchedulesPaginator,
        ListNotebookInstanceLifecycleConfigsPaginator,
        ListNotebookInstancesPaginator,
        ListOptimizationJobsPaginator,
        ListPipelineExecutionStepsPaginator,
        ListPipelineExecutionsPaginator,
        ListPipelineParametersForExecutionPaginator,
        ListPipelinesPaginator,
        ListProcessingJobsPaginator,
        ListResourceCatalogsPaginator,
        ListSpacesPaginator,
        ListStageDevicesPaginator,
        ListStudioLifecycleConfigsPaginator,
        ListSubscribedWorkteamsPaginator,
        ListTagsPaginator,
        ListTrainingJobsPaginator,
        ListTrainingJobsForHyperParameterTuningJobPaginator,
        ListTransformJobsPaginator,
        ListTrialComponentsPaginator,
        ListTrialsPaginator,
        ListUserProfilesPaginator,
        ListWorkforcesPaginator,
        ListWorkteamsPaginator,
        SearchPaginator,
    )

    session = get_session()
    with session.create_client("sagemaker") as client:
        client: SageMakerClient

        list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
        list_algorithms_paginator: ListAlgorithmsPaginator = client.get_paginator("list_algorithms")
        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_app_image_configs_paginator: ListAppImageConfigsPaginator = client.get_paginator("list_app_image_configs")
        list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
        list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
        list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
        list_auto_ml_jobs_paginator: ListAutoMLJobsPaginator = client.get_paginator("list_auto_ml_jobs")
        list_candidates_for_auto_ml_job_paginator: ListCandidatesForAutoMLJobPaginator = client.get_paginator("list_candidates_for_auto_ml_job")
        list_cluster_nodes_paginator: ListClusterNodesPaginator = client.get_paginator("list_cluster_nodes")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_code_repositories_paginator: ListCodeRepositoriesPaginator = client.get_paginator("list_code_repositories")
        list_compilation_jobs_paginator: ListCompilationJobsPaginator = client.get_paginator("list_compilation_jobs")
        list_contexts_paginator: ListContextsPaginator = client.get_paginator("list_contexts")
        list_data_quality_job_definitions_paginator: ListDataQualityJobDefinitionsPaginator = client.get_paginator("list_data_quality_job_definitions")
        list_device_fleets_paginator: ListDeviceFleetsPaginator = client.get_paginator("list_device_fleets")
        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_edge_deployment_plans_paginator: ListEdgeDeploymentPlansPaginator = client.get_paginator("list_edge_deployment_plans")
        list_edge_packaging_jobs_paginator: ListEdgePackagingJobsPaginator = client.get_paginator("list_edge_packaging_jobs")
        list_endpoint_configs_paginator: ListEndpointConfigsPaginator = client.get_paginator("list_endpoint_configs")
        list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
        list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
        list_feature_groups_paginator: ListFeatureGroupsPaginator = client.get_paginator("list_feature_groups")
        list_flow_definitions_paginator: ListFlowDefinitionsPaginator = client.get_paginator("list_flow_definitions")
        list_human_task_uis_paginator: ListHumanTaskUisPaginator = client.get_paginator("list_human_task_uis")
        list_hyper_parameter_tuning_jobs_paginator: ListHyperParameterTuningJobsPaginator = client.get_paginator("list_hyper_parameter_tuning_jobs")
        list_image_versions_paginator: ListImageVersionsPaginator = client.get_paginator("list_image_versions")
        list_images_paginator: ListImagesPaginator = client.get_paginator("list_images")
        list_inference_components_paginator: ListInferenceComponentsPaginator = client.get_paginator("list_inference_components")
        list_inference_experiments_paginator: ListInferenceExperimentsPaginator = client.get_paginator("list_inference_experiments")
        list_inference_recommendations_job_steps_paginator: ListInferenceRecommendationsJobStepsPaginator = client.get_paginator("list_inference_recommendations_job_steps")
        list_inference_recommendations_jobs_paginator: ListInferenceRecommendationsJobsPaginator = client.get_paginator("list_inference_recommendations_jobs")
        list_labeling_jobs_paginator: ListLabelingJobsPaginator = client.get_paginator("list_labeling_jobs")
        list_labeling_jobs_for_workteam_paginator: ListLabelingJobsForWorkteamPaginator = client.get_paginator("list_labeling_jobs_for_workteam")
        list_lineage_groups_paginator: ListLineageGroupsPaginator = client.get_paginator("list_lineage_groups")
        list_mlflow_tracking_servers_paginator: ListMlflowTrackingServersPaginator = client.get_paginator("list_mlflow_tracking_servers")
        list_model_bias_job_definitions_paginator: ListModelBiasJobDefinitionsPaginator = client.get_paginator("list_model_bias_job_definitions")
        list_model_card_export_jobs_paginator: ListModelCardExportJobsPaginator = client.get_paginator("list_model_card_export_jobs")
        list_model_card_versions_paginator: ListModelCardVersionsPaginator = client.get_paginator("list_model_card_versions")
        list_model_cards_paginator: ListModelCardsPaginator = client.get_paginator("list_model_cards")
        list_model_explainability_job_definitions_paginator: ListModelExplainabilityJobDefinitionsPaginator = client.get_paginator("list_model_explainability_job_definitions")
        list_model_metadata_paginator: ListModelMetadataPaginator = client.get_paginator("list_model_metadata")
        list_model_package_groups_paginator: ListModelPackageGroupsPaginator = client.get_paginator("list_model_package_groups")
        list_model_packages_paginator: ListModelPackagesPaginator = client.get_paginator("list_model_packages")
        list_model_quality_job_definitions_paginator: ListModelQualityJobDefinitionsPaginator = client.get_paginator("list_model_quality_job_definitions")
        list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
        list_monitoring_alert_history_paginator: ListMonitoringAlertHistoryPaginator = client.get_paginator("list_monitoring_alert_history")
        list_monitoring_alerts_paginator: ListMonitoringAlertsPaginator = client.get_paginator("list_monitoring_alerts")
        list_monitoring_executions_paginator: ListMonitoringExecutionsPaginator = client.get_paginator("list_monitoring_executions")
        list_monitoring_schedules_paginator: ListMonitoringSchedulesPaginator = client.get_paginator("list_monitoring_schedules")
        list_notebook_instance_lifecycle_configs_paginator: ListNotebookInstanceLifecycleConfigsPaginator = client.get_paginator("list_notebook_instance_lifecycle_configs")
        list_notebook_instances_paginator: ListNotebookInstancesPaginator = client.get_paginator("list_notebook_instances")
        list_optimization_jobs_paginator: ListOptimizationJobsPaginator = client.get_paginator("list_optimization_jobs")
        list_pipeline_execution_steps_paginator: ListPipelineExecutionStepsPaginator = client.get_paginator("list_pipeline_execution_steps")
        list_pipeline_executions_paginator: ListPipelineExecutionsPaginator = client.get_paginator("list_pipeline_executions")
        list_pipeline_parameters_for_execution_paginator: ListPipelineParametersForExecutionPaginator = client.get_paginator("list_pipeline_parameters_for_execution")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        list_processing_jobs_paginator: ListProcessingJobsPaginator = client.get_paginator("list_processing_jobs")
        list_resource_catalogs_paginator: ListResourceCatalogsPaginator = client.get_paginator("list_resource_catalogs")
        list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
        list_stage_devices_paginator: ListStageDevicesPaginator = client.get_paginator("list_stage_devices")
        list_studio_lifecycle_configs_paginator: ListStudioLifecycleConfigsPaginator = client.get_paginator("list_studio_lifecycle_configs")
        list_subscribed_workteams_paginator: ListSubscribedWorkteamsPaginator = client.get_paginator("list_subscribed_workteams")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
        list_training_jobs_paginator: ListTrainingJobsPaginator = client.get_paginator("list_training_jobs")
        list_training_jobs_for_hyper_parameter_tuning_job_paginator: ListTrainingJobsForHyperParameterTuningJobPaginator = client.get_paginator("list_training_jobs_for_hyper_parameter_tuning_job")
        list_transform_jobs_paginator: ListTransformJobsPaginator = client.get_paginator("list_transform_jobs")
        list_trial_components_paginator: ListTrialComponentsPaginator = client.get_paginator("list_trial_components")
        list_trials_paginator: ListTrialsPaginator = client.get_paginator("list_trials")
        list_user_profiles_paginator: ListUserProfilesPaginator = client.get_paginator("list_user_profiles")
        list_workforces_paginator: ListWorkforcesPaginator = client.get_paginator("list_workforces")
        list_workteams_paginator: ListWorkteamsPaginator = client.get_paginator("list_workteams")
        search_paginator: SearchPaginator = client.get_paginator("search")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    AlgorithmSortByType,
    AppImageConfigSortKeyType,
    AssociationEdgeTypeType,
    AutoMLJobStatusType,
    AutoMLSortByType,
    AutoMLSortOrderType,
    CandidateSortByType,
    CandidateStatusType,
    ClusterSortByType,
    CodeRepositorySortByType,
    CodeRepositorySortOrderType,
    CompilationJobStatusType,
    CrossAccountFilterOptionType,
    EdgePackagingJobStatusType,
    EndpointConfigSortKeyType,
    EndpointSortKeyType,
    EndpointStatusType,
    ExecutionStatusType,
    FeatureGroupSortByType,
    FeatureGroupSortOrderType,
    FeatureGroupStatusType,
    HyperParameterTuningJobSortByOptionsType,
    HyperParameterTuningJobStatusType,
    ImageSortByType,
    ImageSortOrderType,
    ImageVersionSortByType,
    ImageVersionSortOrderType,
    InferenceComponentSortKeyType,
    InferenceComponentStatusType,
    InferenceExperimentStatusType,
    LabelingJobStatusType,
    ListCompilationJobsSortByType,
    ListDeviceFleetsSortByType,
    ListEdgeDeploymentPlansSortByType,
    ListEdgePackagingJobsSortByType,
    ListInferenceRecommendationsJobsSortByType,
    ListOptimizationJobsSortByType,
    ListWorkforcesSortByOptionsType,
    ListWorkteamsSortByOptionsType,
    ModelApprovalStatusType,
    ModelCardExportJobSortByType,
    ModelCardExportJobSortOrderType,
    ModelCardExportJobStatusType,
    ModelCardSortByType,
    ModelCardSortOrderType,
    ModelCardStatusType,
    ModelPackageGroupSortByType,
    ModelPackageSortByType,
    ModelPackageTypeType,
    ModelSortKeyType,
    MonitoringAlertHistorySortKeyType,
    MonitoringAlertStatusType,
    MonitoringExecutionSortKeyType,
    MonitoringJobDefinitionSortKeyType,
    MonitoringScheduleSortKeyType,
    MonitoringTypeType,
    NotebookInstanceLifecycleConfigSortKeyType,
    NotebookInstanceLifecycleConfigSortOrderType,
    NotebookInstanceSortKeyType,
    NotebookInstanceSortOrderType,
    NotebookInstanceStatusType,
    OfflineStoreStatusValueType,
    OptimizationJobStatusType,
    OrderKeyType,
    ProcessingJobStatusType,
    RecommendationJobStatusType,
    ResourceCatalogSortOrderType,
    ResourceTypeType,
    ScheduleStatusType,
    SearchSortOrderType,
    SortActionsByType,
    SortAssociationsByType,
    SortByType,
    SortContextsByType,
    SortExperimentsByType,
    SortInferenceExperimentsByType,
    SortLineageGroupsByType,
    SortOrderType,
    SortPipelineExecutionsByType,
    SortPipelinesByType,
    SortTrackingServerByType,
    SortTrialComponentsByType,
    SortTrialsByType,
    SpaceSortKeyType,
    StudioLifecycleConfigAppTypeType,
    StudioLifecycleConfigSortKeyType,
    TrackingServerStatusType,
    TrainingJobSortByOptionsType,
    TrainingJobStatusType,
    TransformJobStatusType,
    UserProfileSortKeyType,
    WarmPoolResourceStatusType,
)
from .type_defs import (
    ListActionsResponseTypeDef,
    ListAlgorithmsOutputTypeDef,
    ListAliasesResponseTypeDef,
    ListAppImageConfigsResponseTypeDef,
    ListAppsResponseTypeDef,
    ListArtifactsResponseTypeDef,
    ListAssociationsResponseTypeDef,
    ListAutoMLJobsResponseTypeDef,
    ListCandidatesForAutoMLJobResponseTypeDef,
    ListClusterNodesResponseTypeDef,
    ListClustersResponseTypeDef,
    ListCodeRepositoriesOutputTypeDef,
    ListCompilationJobsResponseTypeDef,
    ListContextsResponseTypeDef,
    ListDataQualityJobDefinitionsResponseTypeDef,
    ListDeviceFleetsResponseTypeDef,
    ListDevicesResponseTypeDef,
    ListDomainsResponseTypeDef,
    ListEdgeDeploymentPlansResponseTypeDef,
    ListEdgePackagingJobsResponseTypeDef,
    ListEndpointConfigsOutputTypeDef,
    ListEndpointsOutputTypeDef,
    ListExperimentsResponseTypeDef,
    ListFeatureGroupsResponseTypeDef,
    ListFlowDefinitionsResponseTypeDef,
    ListHumanTaskUisResponseTypeDef,
    ListHyperParameterTuningJobsResponseTypeDef,
    ListImagesResponseTypeDef,
    ListImageVersionsResponseTypeDef,
    ListInferenceComponentsOutputTypeDef,
    ListInferenceExperimentsResponseTypeDef,
    ListInferenceRecommendationsJobsResponseTypeDef,
    ListInferenceRecommendationsJobStepsResponseTypeDef,
    ListLabelingJobsForWorkteamResponseTypeDef,
    ListLabelingJobsResponseTypeDef,
    ListLineageGroupsResponseTypeDef,
    ListMlflowTrackingServersResponseTypeDef,
    ListModelBiasJobDefinitionsResponseTypeDef,
    ListModelCardExportJobsResponseTypeDef,
    ListModelCardsResponseTypeDef,
    ListModelCardVersionsResponseTypeDef,
    ListModelExplainabilityJobDefinitionsResponseTypeDef,
    ListModelMetadataResponseTypeDef,
    ListModelPackageGroupsOutputTypeDef,
    ListModelPackagesOutputTypeDef,
    ListModelQualityJobDefinitionsResponseTypeDef,
    ListModelsOutputTypeDef,
    ListMonitoringAlertHistoryResponseTypeDef,
    ListMonitoringAlertsResponseTypeDef,
    ListMonitoringExecutionsResponseTypeDef,
    ListMonitoringSchedulesResponseTypeDef,
    ListNotebookInstanceLifecycleConfigsOutputTypeDef,
    ListNotebookInstancesOutputTypeDef,
    ListOptimizationJobsResponseTypeDef,
    ListPipelineExecutionsResponseTypeDef,
    ListPipelineExecutionStepsResponseTypeDef,
    ListPipelineParametersForExecutionResponseTypeDef,
    ListPipelinesResponseTypeDef,
    ListProcessingJobsResponseTypeDef,
    ListResourceCatalogsResponseTypeDef,
    ListSpacesResponseTypeDef,
    ListStageDevicesResponseTypeDef,
    ListStudioLifecycleConfigsResponseTypeDef,
    ListSubscribedWorkteamsResponseTypeDef,
    ListTagsOutputTypeDef,
    ListTrainingJobsForHyperParameterTuningJobResponseTypeDef,
    ListTrainingJobsResponseTypeDef,
    ListTransformJobsResponseTypeDef,
    ListTrialComponentsResponseTypeDef,
    ListTrialsResponseTypeDef,
    ListUserProfilesResponseTypeDef,
    ListWorkforcesResponseTypeDef,
    ListWorkteamsResponseTypeDef,
    ModelMetadataSearchExpressionTypeDef,
    PaginatorConfigTypeDef,
    SearchExpressionTypeDef,
    SearchResponseTypeDef,
    TimestampTypeDef,
    VisibilityConditionsTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ListActionsPaginator",
    "ListAlgorithmsPaginator",
    "ListAliasesPaginator",
    "ListAppImageConfigsPaginator",
    "ListAppsPaginator",
    "ListArtifactsPaginator",
    "ListAssociationsPaginator",
    "ListAutoMLJobsPaginator",
    "ListCandidatesForAutoMLJobPaginator",
    "ListClusterNodesPaginator",
    "ListClustersPaginator",
    "ListCodeRepositoriesPaginator",
    "ListCompilationJobsPaginator",
    "ListContextsPaginator",
    "ListDataQualityJobDefinitionsPaginator",
    "ListDeviceFleetsPaginator",
    "ListDevicesPaginator",
    "ListDomainsPaginator",
    "ListEdgeDeploymentPlansPaginator",
    "ListEdgePackagingJobsPaginator",
    "ListEndpointConfigsPaginator",
    "ListEndpointsPaginator",
    "ListExperimentsPaginator",
    "ListFeatureGroupsPaginator",
    "ListFlowDefinitionsPaginator",
    "ListHumanTaskUisPaginator",
    "ListHyperParameterTuningJobsPaginator",
    "ListImageVersionsPaginator",
    "ListImagesPaginator",
    "ListInferenceComponentsPaginator",
    "ListInferenceExperimentsPaginator",
    "ListInferenceRecommendationsJobStepsPaginator",
    "ListInferenceRecommendationsJobsPaginator",
    "ListLabelingJobsPaginator",
    "ListLabelingJobsForWorkteamPaginator",
    "ListLineageGroupsPaginator",
    "ListMlflowTrackingServersPaginator",
    "ListModelBiasJobDefinitionsPaginator",
    "ListModelCardExportJobsPaginator",
    "ListModelCardVersionsPaginator",
    "ListModelCardsPaginator",
    "ListModelExplainabilityJobDefinitionsPaginator",
    "ListModelMetadataPaginator",
    "ListModelPackageGroupsPaginator",
    "ListModelPackagesPaginator",
    "ListModelQualityJobDefinitionsPaginator",
    "ListModelsPaginator",
    "ListMonitoringAlertHistoryPaginator",
    "ListMonitoringAlertsPaginator",
    "ListMonitoringExecutionsPaginator",
    "ListMonitoringSchedulesPaginator",
    "ListNotebookInstanceLifecycleConfigsPaginator",
    "ListNotebookInstancesPaginator",
    "ListOptimizationJobsPaginator",
    "ListPipelineExecutionStepsPaginator",
    "ListPipelineExecutionsPaginator",
    "ListPipelineParametersForExecutionPaginator",
    "ListPipelinesPaginator",
    "ListProcessingJobsPaginator",
    "ListResourceCatalogsPaginator",
    "ListSpacesPaginator",
    "ListStageDevicesPaginator",
    "ListStudioLifecycleConfigsPaginator",
    "ListSubscribedWorkteamsPaginator",
    "ListTagsPaginator",
    "ListTrainingJobsPaginator",
    "ListTrainingJobsForHyperParameterTuningJobPaginator",
    "ListTransformJobsPaginator",
    "ListTrialComponentsPaginator",
    "ListTrialsPaginator",
    "ListUserProfilesPaginator",
    "ListWorkforcesPaginator",
    "ListWorkteamsPaginator",
    "SearchPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listactionspaginator)
    """

    def paginate(
        self,
        *,
        SourceUri: str = ...,
        ActionType: str = ...,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: SortActionsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listactionspaginator)
        """


class ListAlgorithmsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAlgorithms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listalgorithmspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        SortBy: AlgorithmSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListAlgorithmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAlgorithms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listalgorithmspaginator)
        """


class ListAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listaliasespaginator)
    """

    def paginate(
        self,
        *,
        ImageName: str,
        Alias: str = ...,
        Version: int = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listaliasespaginator)
        """


class ListAppImageConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAppImageConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappimageconfigspaginator)
    """

    def paginate(
        self,
        *,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        ModifiedTimeBefore: TimestampTypeDef = ...,
        ModifiedTimeAfter: TimestampTypeDef = ...,
        SortBy: AppImageConfigSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListAppImageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAppImageConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappimageconfigspaginator)
        """


class ListAppsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListApps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappspaginator)
    """

    def paginate(
        self,
        *,
        SortOrder: SortOrderType = ...,
        SortBy: Literal["CreationTime"] = ...,
        DomainIdEquals: str = ...,
        UserProfileNameEquals: str = ...,
        SpaceNameEquals: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListApps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappspaginator)
        """


class ListArtifactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListArtifacts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listartifactspaginator)
    """

    def paginate(
        self,
        *,
        SourceUri: str = ...,
        ArtifactType: str = ...,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: Literal["CreationTime"] = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListArtifactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListArtifacts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listartifactspaginator)
        """


class ListAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listassociationspaginator)
    """

    def paginate(
        self,
        *,
        SourceArn: str = ...,
        DestinationArn: str = ...,
        SourceType: str = ...,
        DestinationType: str = ...,
        AssociationType: AssociationEdgeTypeType = ...,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: SortAssociationsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listassociationspaginator)
        """


class ListAutoMLJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAutoMLJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listautomljobspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        StatusEquals: AutoMLJobStatusType = ...,
        SortOrder: AutoMLSortOrderType = ...,
        SortBy: AutoMLSortByType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListAutoMLJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListAutoMLJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listautomljobspaginator)
        """


class ListCandidatesForAutoMLJobPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCandidatesForAutoMLJob)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcandidatesforautomljobpaginator)
    """

    def paginate(
        self,
        *,
        AutoMLJobName: str,
        StatusEquals: CandidateStatusType = ...,
        CandidateNameEquals: str = ...,
        SortOrder: AutoMLSortOrderType = ...,
        SortBy: CandidateSortByType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListCandidatesForAutoMLJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCandidatesForAutoMLJob.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcandidatesforautomljobpaginator)
        """


class ListClusterNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListClusterNodes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusternodespaginator)
    """

    def paginate(
        self,
        *,
        ClusterName: str,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        InstanceGroupNameContains: str = ...,
        SortBy: ClusterSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListClusterNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListClusterNodes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusternodespaginator)
        """


class ListClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusterspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        SortBy: ClusterSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusterspaginator)
        """


class ListCodeRepositoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCodeRepositories)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcoderepositoriespaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        SortBy: CodeRepositorySortByType = ...,
        SortOrder: CodeRepositorySortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListCodeRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCodeRepositories.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcoderepositoriespaginator)
        """


class ListCompilationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCompilationJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcompilationjobspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        StatusEquals: CompilationJobStatusType = ...,
        SortBy: ListCompilationJobsSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListCompilationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListCompilationJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcompilationjobspaginator)
        """


class ListContextsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListContexts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcontextspaginator)
    """

    def paginate(
        self,
        *,
        SourceUri: str = ...,
        ContextType: str = ...,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: SortContextsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListContextsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListContexts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcontextspaginator)
        """


class ListDataQualityJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDataQualityJobDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
    """

    def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringJobDefinitionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListDataQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDataQualityJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
        """


class ListDeviceFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDeviceFleets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicefleetspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        SortBy: ListDeviceFleetsSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListDeviceFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDeviceFleets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicefleetspaginator)
        """


class ListDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicespaginator)
    """

    def paginate(
        self,
        *,
        LatestHeartbeatAfter: TimestampTypeDef = ...,
        ModelName: str = ...,
        DeviceFleetName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicespaginator)
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdomainspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdomainspaginator)
        """


class ListEdgeDeploymentPlansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEdgeDeploymentPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgedeploymentplanspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        DeviceFleetNameContains: str = ...,
        SortBy: ListEdgeDeploymentPlansSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListEdgeDeploymentPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEdgeDeploymentPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgedeploymentplanspaginator)
        """


class ListEdgePackagingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEdgePackagingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgepackagingjobspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        ModelNameContains: str = ...,
        StatusEquals: EdgePackagingJobStatusType = ...,
        SortBy: ListEdgePackagingJobsSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListEdgePackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEdgePackagingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgepackagingjobspaginator)
        """


class ListEndpointConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEndpointConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointconfigspaginator)
    """

    def paginate(
        self,
        *,
        SortBy: EndpointConfigSortKeyType = ...,
        SortOrder: OrderKeyType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListEndpointConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEndpointConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointconfigspaginator)
        """


class ListEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointspaginator)
    """

    def paginate(
        self,
        *,
        SortBy: EndpointSortKeyType = ...,
        SortOrder: OrderKeyType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        StatusEquals: EndpointStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointspaginator)
        """


class ListExperimentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListExperiments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listexperimentspaginator)
    """

    def paginate(
        self,
        *,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: SortExperimentsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListExperiments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listexperimentspaginator)
        """


class ListFeatureGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListFeatureGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listfeaturegroupspaginator)
    """

    def paginate(
        self,
        *,
        NameContains: str = ...,
        FeatureGroupStatusEquals: FeatureGroupStatusType = ...,
        OfflineStoreStatusEquals: OfflineStoreStatusValueType = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        SortOrder: FeatureGroupSortOrderType = ...,
        SortBy: FeatureGroupSortByType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListFeatureGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListFeatureGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listfeaturegroupspaginator)
        """


class ListFlowDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListFlowDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listflowdefinitionspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListFlowDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListFlowDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listflowdefinitionspaginator)
        """


class ListHumanTaskUisPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListHumanTaskUis)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhumantaskuispaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListHumanTaskUisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListHumanTaskUis.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhumantaskuispaginator)
        """


class ListHyperParameterTuningJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListHyperParameterTuningJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhyperparametertuningjobspaginator)
    """

    def paginate(
        self,
        *,
        SortBy: HyperParameterTuningJobSortByOptionsType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        StatusEquals: HyperParameterTuningJobStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListHyperParameterTuningJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListHyperParameterTuningJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhyperparametertuningjobspaginator)
        """


class ListImageVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListImageVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimageversionspaginator)
    """

    def paginate(
        self,
        *,
        ImageName: str,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        SortBy: ImageVersionSortByType = ...,
        SortOrder: ImageVersionSortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListImageVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListImageVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimageversionspaginator)
        """


class ListImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListImages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimagespaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        SortBy: ImageSortByType = ...,
        SortOrder: ImageSortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListImages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimagespaginator)
        """


class ListInferenceComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencecomponentspaginator)
    """

    def paginate(
        self,
        *,
        SortBy: InferenceComponentSortKeyType = ...,
        SortOrder: OrderKeyType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        StatusEquals: InferenceComponentStatusType = ...,
        EndpointNameEquals: str = ...,
        VariantNameEquals: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListInferenceComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencecomponentspaginator)
        """


class ListInferenceExperimentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceExperiments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferenceexperimentspaginator)
    """

    def paginate(
        self,
        *,
        NameContains: str = ...,
        Type: Literal["ShadowMode"] = ...,
        StatusEquals: InferenceExperimentStatusType = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        SortBy: SortInferenceExperimentsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListInferenceExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceExperiments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferenceexperimentspaginator)
        """


class ListInferenceRecommendationsJobStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
    """

    def paginate(
        self,
        *,
        JobName: str,
        Status: RecommendationJobStatusType = ...,
        StepType: Literal["BENCHMARK"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListInferenceRecommendationsJobStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
        """


class ListInferenceRecommendationsJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceRecommendationsJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        StatusEquals: RecommendationJobStatusType = ...,
        SortBy: ListInferenceRecommendationsJobsSortByType = ...,
        SortOrder: SortOrderType = ...,
        ModelNameEquals: str = ...,
        ModelPackageVersionArnEquals: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListInferenceRecommendationsJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListInferenceRecommendationsJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
        """


class ListLabelingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLabelingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        SortBy: SortByType = ...,
        SortOrder: SortOrderType = ...,
        StatusEquals: LabelingJobStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListLabelingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLabelingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobspaginator)
        """


class ListLabelingJobsForWorkteamPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLabelingJobsForWorkteam)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
    """

    def paginate(
        self,
        *,
        WorkteamArn: str,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        JobReferenceCodeContains: str = ...,
        SortBy: Literal["CreationTime"] = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListLabelingJobsForWorkteamResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLabelingJobsForWorkteam.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
        """


class ListLineageGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLineageGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlineagegroupspaginator)
    """

    def paginate(
        self,
        *,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: SortLineageGroupsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListLineageGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListLineageGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlineagegroupspaginator)
        """


class ListMlflowTrackingServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMlflowTrackingServers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmlflowtrackingserverspaginator)
    """

    def paginate(
        self,
        *,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        TrackingServerStatus: TrackingServerStatusType = ...,
        MlflowVersion: str = ...,
        SortBy: SortTrackingServerByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListMlflowTrackingServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMlflowTrackingServers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmlflowtrackingserverspaginator)
        """


class ListModelBiasJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelBiasJobDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
    """

    def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringJobDefinitionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelBiasJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelBiasJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
        """


class ListModelCardExportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelCardExportJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardexportjobspaginator)
    """

    def paginate(
        self,
        *,
        ModelCardName: str,
        ModelCardVersion: int = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        ModelCardExportJobNameContains: str = ...,
        StatusEquals: ModelCardExportJobStatusType = ...,
        SortBy: ModelCardExportJobSortByType = ...,
        SortOrder: ModelCardExportJobSortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelCardExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelCardExportJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardexportjobspaginator)
        """


class ListModelCardVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelCardVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardversionspaginator)
    """

    def paginate(
        self,
        *,
        ModelCardName: str,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        ModelCardStatus: ModelCardStatusType = ...,
        SortBy: Literal["Version"] = ...,
        SortOrder: ModelCardSortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelCardVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelCardVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardversionspaginator)
        """


class ListModelCardsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelCards)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        ModelCardStatus: ModelCardStatusType = ...,
        SortBy: ModelCardSortByType = ...,
        SortOrder: ModelCardSortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelCardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelCards.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardspaginator)
        """


class ListModelExplainabilityJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
    """

    def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringJobDefinitionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelExplainabilityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
        """


class ListModelMetadataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelMetadata)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelmetadatapaginator)
    """

    def paginate(
        self,
        *,
        SearchExpression: ModelMetadataSearchExpressionTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelMetadata.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelmetadatapaginator)
        """


class ListModelPackageGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelPackageGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagegroupspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        SortBy: ModelPackageGroupSortByType = ...,
        SortOrder: SortOrderType = ...,
        CrossAccountFilterOption: CrossAccountFilterOptionType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelPackageGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelPackageGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagegroupspaginator)
        """


class ListModelPackagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelPackages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagespaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        ModelApprovalStatus: ModelApprovalStatusType = ...,
        ModelPackageGroupName: str = ...,
        ModelPackageType: ModelPackageTypeType = ...,
        SortBy: ModelPackageSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelPackages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagespaginator)
        """


class ListModelQualityJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelQualityJobDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
    """

    def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringJobDefinitionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModelQualityJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
        """


class ListModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelspaginator)
    """

    def paginate(
        self,
        *,
        SortBy: ModelSortKeyType = ...,
        SortOrder: OrderKeyType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListModels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelspaginator)
        """


class ListMonitoringAlertHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringAlertHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalerthistorypaginator)
    """

    def paginate(
        self,
        *,
        MonitoringScheduleName: str = ...,
        MonitoringAlertName: str = ...,
        SortBy: MonitoringAlertHistorySortKeyType = ...,
        SortOrder: SortOrderType = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        StatusEquals: MonitoringAlertStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListMonitoringAlertHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringAlertHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalerthistorypaginator)
        """


class ListMonitoringAlertsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringAlerts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalertspaginator)
    """

    def paginate(
        self, *, MonitoringScheduleName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListMonitoringAlertsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringAlerts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalertspaginator)
        """


class ListMonitoringExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringexecutionspaginator)
    """

    def paginate(
        self,
        *,
        MonitoringScheduleName: str = ...,
        EndpointName: str = ...,
        SortBy: MonitoringExecutionSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        ScheduledTimeBefore: TimestampTypeDef = ...,
        ScheduledTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        StatusEquals: ExecutionStatusType = ...,
        MonitoringJobDefinitionName: str = ...,
        MonitoringTypeEquals: MonitoringTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListMonitoringExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringexecutionspaginator)
        """


class ListMonitoringSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringSchedules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringschedulespaginator)
    """

    def paginate(
        self,
        *,
        EndpointName: str = ...,
        SortBy: MonitoringScheduleSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        StatusEquals: ScheduleStatusType = ...,
        MonitoringJobDefinitionName: str = ...,
        MonitoringTypeEquals: MonitoringTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListMonitoringSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListMonitoringSchedules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringschedulespaginator)
        """


class ListNotebookInstanceLifecycleConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
    """

    def paginate(
        self,
        *,
        SortBy: NotebookInstanceLifecycleConfigSortKeyType = ...,
        SortOrder: NotebookInstanceLifecycleConfigSortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListNotebookInstanceLifecycleConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
        """


class ListNotebookInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListNotebookInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancespaginator)
    """

    def paginate(
        self,
        *,
        SortBy: NotebookInstanceSortKeyType = ...,
        SortOrder: NotebookInstanceSortOrderType = ...,
        NameContains: str = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        StatusEquals: NotebookInstanceStatusType = ...,
        NotebookInstanceLifecycleConfigNameContains: str = ...,
        DefaultCodeRepositoryContains: str = ...,
        AdditionalCodeRepositoryEquals: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListNotebookInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListNotebookInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancespaginator)
        """


class ListOptimizationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListOptimizationJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listoptimizationjobspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        OptimizationContains: str = ...,
        NameContains: str = ...,
        StatusEquals: OptimizationJobStatusType = ...,
        SortBy: ListOptimizationJobsSortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListOptimizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListOptimizationJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listoptimizationjobspaginator)
        """


class ListPipelineExecutionStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineExecutionSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionstepspaginator)
    """

    def paginate(
        self,
        *,
        PipelineExecutionArn: str = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListPipelineExecutionStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineExecutionSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionstepspaginator)
        """


class ListPipelineExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionspaginator)
    """

    def paginate(
        self,
        *,
        PipelineName: str,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: SortPipelineExecutionsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListPipelineExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionspaginator)
        """


class ListPipelineParametersForExecutionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineParametersForExecution)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
    """

    def paginate(
        self, *, PipelineExecutionArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListPipelineParametersForExecutionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelineParametersForExecution.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
        """


class ListPipelinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelines)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelinespaginator)
    """

    def paginate(
        self,
        *,
        PipelineNamePrefix: str = ...,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: SortPipelinesByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelinespaginator)
        """


class ListProcessingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListProcessingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listprocessingjobspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        StatusEquals: ProcessingJobStatusType = ...,
        SortBy: SortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListProcessingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListProcessingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listprocessingjobspaginator)
        """


class ListResourceCatalogsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListResourceCatalogs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listresourcecatalogspaginator)
    """

    def paginate(
        self,
        *,
        NameContains: str = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        SortOrder: ResourceCatalogSortOrderType = ...,
        SortBy: Literal["CreationTime"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListResourceCatalogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListResourceCatalogs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listresourcecatalogspaginator)
        """


class ListSpacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListSpaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listspacespaginator)
    """

    def paginate(
        self,
        *,
        SortOrder: SortOrderType = ...,
        SortBy: SpaceSortKeyType = ...,
        DomainIdEquals: str = ...,
        SpaceNameContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListSpacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListSpaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listspacespaginator)
        """


class ListStageDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListStageDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststagedevicespaginator)
    """

    def paginate(
        self,
        *,
        EdgeDeploymentPlanName: str,
        StageName: str,
        ExcludeDevicesDeployedInOtherStage: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListStageDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListStageDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststagedevicespaginator)
        """


class ListStudioLifecycleConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListStudioLifecycleConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
    """

    def paginate(
        self,
        *,
        NameContains: str = ...,
        AppTypeEquals: StudioLifecycleConfigAppTypeType = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        CreationTimeAfter: TimestampTypeDef = ...,
        ModifiedTimeBefore: TimestampTypeDef = ...,
        ModifiedTimeAfter: TimestampTypeDef = ...,
        SortBy: StudioLifecycleConfigSortKeyType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListStudioLifecycleConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListStudioLifecycleConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
        """


class ListSubscribedWorkteamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListSubscribedWorkteams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listsubscribedworkteamspaginator)
    """

    def paginate(
        self, *, NameContains: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListSubscribedWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListSubscribedWorkteams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listsubscribedworkteamspaginator)
        """


class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtagspaginator)
    """

    def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListTagsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtagspaginator)
        """


class ListTrainingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrainingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        StatusEquals: TrainingJobStatusType = ...,
        SortBy: SortByType = ...,
        SortOrder: SortOrderType = ...,
        WarmPoolStatusEquals: WarmPoolResourceStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListTrainingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrainingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobspaginator)
        """


class ListTrainingJobsForHyperParameterTuningJobPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
    """

    def paginate(
        self,
        *,
        HyperParameterTuningJobName: str,
        StatusEquals: TrainingJobStatusType = ...,
        SortBy: TrainingJobSortByOptionsType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListTrainingJobsForHyperParameterTuningJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
        """


class ListTransformJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTransformJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtransformjobspaginator)
    """

    def paginate(
        self,
        *,
        CreationTimeAfter: TimestampTypeDef = ...,
        CreationTimeBefore: TimestampTypeDef = ...,
        LastModifiedTimeAfter: TimestampTypeDef = ...,
        LastModifiedTimeBefore: TimestampTypeDef = ...,
        NameContains: str = ...,
        StatusEquals: TransformJobStatusType = ...,
        SortBy: SortByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListTransformJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTransformJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtransformjobspaginator)
        """


class ListTrialComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrialComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialcomponentspaginator)
    """

    def paginate(
        self,
        *,
        ExperimentName: str = ...,
        TrialName: str = ...,
        SourceArn: str = ...,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: SortTrialComponentsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListTrialComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrialComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialcomponentspaginator)
        """


class ListTrialsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrials)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialspaginator)
    """

    def paginate(
        self,
        *,
        ExperimentName: str = ...,
        TrialComponentName: str = ...,
        CreatedAfter: TimestampTypeDef = ...,
        CreatedBefore: TimestampTypeDef = ...,
        SortBy: SortTrialsByType = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListTrialsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListTrials.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialspaginator)
        """


class ListUserProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListUserProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listuserprofilespaginator)
    """

    def paginate(
        self,
        *,
        SortOrder: SortOrderType = ...,
        SortBy: UserProfileSortKeyType = ...,
        DomainIdEquals: str = ...,
        UserProfileNameContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListUserProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListUserProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listuserprofilespaginator)
        """


class ListWorkforcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListWorkforces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkforcespaginator)
    """

    def paginate(
        self,
        *,
        SortBy: ListWorkforcesSortByOptionsType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListWorkforcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListWorkforces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkforcespaginator)
        """


class ListWorkteamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListWorkteams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkteamspaginator)
    """

    def paginate(
        self,
        *,
        SortBy: ListWorkteamsSortByOptionsType = ...,
        SortOrder: SortOrderType = ...,
        NameContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListWorkteams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkteamspaginator)
        """


class SearchPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.Search)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#searchpaginator)
    """

    def paginate(
        self,
        *,
        Resource: ResourceTypeType,
        SearchExpression: SearchExpressionTypeDef = ...,
        SortBy: str = ...,
        SortOrder: SearchSortOrderType = ...,
        CrossAccountFilterOption: CrossAccountFilterOptionType = ...,
        VisibilityConditions: Sequence[VisibilityConditionsTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[SearchResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.Search.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#searchpaginator)
        """
