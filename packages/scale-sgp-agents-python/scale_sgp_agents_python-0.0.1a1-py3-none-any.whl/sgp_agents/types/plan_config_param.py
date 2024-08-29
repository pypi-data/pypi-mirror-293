# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "PlanConfigParam",
    "Plan",
    "PlanWorkflowItem",
    "PlanBranchConfig",
    "PlanBranchConfigConditionalWorkflow",
    "WorkflowsUnionMember1",
    "WorkflowsUnionMember1Config",
    "WorkflowsUnionMember1ConfigNodeConfig",
    "WorkflowsUnionMember1ConfigJinjaNodeConfig",
    "WorkflowsUnionMember1ConfigJinjaNodeConfigDataTransformations",
    "WorkflowsUnionMember1ConfigJinjaNodeConfigOutputTemplate",
    "WorkflowsUnionMember1ConfigChunkEvaluationNodeConfig",
    "WorkflowsUnionMember1ConfigRerankerNodeConfig",
    "WorkflowsUnionMember1ConfigRetrieverNodeConfig",
    "WorkflowsUnionMember1ConfigCitationNodeConfig",
    "WorkflowsUnionMember1ConfigCitationNodeConfigCitationContext",
    "WorkflowsUnionMember1ConfigSearchCitationNodeConfig",
    "WorkflowsUnionMember1ConfigDataTransformNodeConfig",
    "WorkflowsUnionMember1ConfigCreateMessagesNodeConfig",
    "WorkflowsUnionMember1ConfigCreateMessagesNodeConfigMessageConfig",
    "WorkflowsUnionMember1ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages",
    "WorkflowsUnionMember1ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages",
    "WorkflowsUnionMember1ConfigInsertMessagesConfig",
    "WorkflowsUnionMember1ConfigRemoveMessageConfig",
    "WorkflowsUnionMember1ConfigTokenizerChatTemplateConfig",
    "WorkflowsUnionMember1ConfigLlmEngineNodeConfig",
    "WorkflowsUnionMember1ConfigLlmEngineNodeConfigBatchSysKwargs",
    "WorkflowsUnionMember1ConfigResponseParserNodeConfig",
    "WorkflowsUnionMember1ConfigIngestorConfig",
    "WorkflowsUnionMember1ConfigProcessingNodeConfig",
    "WorkflowsUnionMember1ConfigProcessingNodeConfigFunctionSpecs",
    "WorkflowsUnionMember1ConfigSqlExecutorNodeConfig",
    "WorkflowsUnionMember1ConfigStaticNodeConfig",
    "WorkflowsUnionMember1ConfigGenerationNodeConfig",
    "Evaluation",
    "EvaluationConfig",
    "EvaluationConfigNodeConfig",
    "EvaluationConfigJinjaNodeConfig",
    "EvaluationConfigJinjaNodeConfigDataTransformations",
    "EvaluationConfigJinjaNodeConfigOutputTemplate",
    "EvaluationConfigChunkEvaluationNodeConfig",
    "EvaluationConfigRerankerNodeConfig",
    "EvaluationConfigRetrieverNodeConfig",
    "EvaluationConfigCitationNodeConfig",
    "EvaluationConfigCitationNodeConfigCitationContext",
    "EvaluationConfigSearchCitationNodeConfig",
    "EvaluationConfigDataTransformNodeConfig",
    "EvaluationConfigCreateMessagesNodeConfig",
    "EvaluationConfigCreateMessagesNodeConfigMessageConfig",
    "EvaluationConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages",
    "EvaluationConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages",
    "EvaluationConfigInsertMessagesConfig",
    "EvaluationConfigRemoveMessageConfig",
    "EvaluationConfigTokenizerChatTemplateConfig",
    "EvaluationConfigLlmEngineNodeConfig",
    "EvaluationConfigLlmEngineNodeConfigBatchSysKwargs",
    "EvaluationConfigResponseParserNodeConfig",
    "EvaluationConfigIngestorConfig",
    "EvaluationConfigProcessingNodeConfig",
    "EvaluationConfigProcessingNodeConfigFunctionSpecs",
    "EvaluationConfigSqlExecutorNodeConfig",
    "EvaluationConfigStaticNodeConfig",
    "EvaluationConfigGenerationNodeConfig",
]


class PlanWorkflowItem(TypedDict, total=False):
    workflow_name: Required[str]

    request_user_input: Literal["never", "maybe", "always"]
    """An enumeration."""

    workflow_inputs: Union[str, Dict[str, Union[str, Dict[str, Union[str, object]]]]]

    workflow_save_outputs: Dict[str, str]


class PlanBranchConfigConditionalWorkflow(TypedDict, total=False):
    condition: Required[Literal["if", "elif", "else"]]

    workflow_name: Required[str]

    condition_input_var: str

    operator: str

    reference_var: str

    request_user_input: Literal["never", "maybe", "always"]
    """An enumeration."""

    workflow_inputs: Union[str, Dict[str, Union[str, Dict[str, Union[str, object]]]]]

    workflow_nodes: List[str]

    workflow_save_outputs: Dict[str, str]


class PlanBranchConfig(TypedDict, total=False):
    branch: Required[str]

    conditional_workflows: Required[Iterable[PlanBranchConfigConditionalWorkflow]]

    merge_outputs: Dict[str, List[str]]

    request_user_input: Literal["never", "maybe", "always"]
    """An enumeration."""


Plan: TypeAlias = Union[PlanWorkflowItem, PlanBranchConfig]


class WorkflowsUnionMember1ConfigNodeConfig(TypedDict, total=False):
    node_metadata: List[str]

    num_workers: int


class WorkflowsUnionMember1ConfigJinjaNodeConfigDataTransformations(TypedDict, total=False):
    jinja_helper_functions: List[Union[str, object]]

    jinja_template_path: str

    jinja_template_str: str
    """Raw template to apply to the data.

    This should be a Jinja2 template string. Please note, the data will be mapped as
    'value' in the template. Default None corresponds to {{value}}. Should access
    property `jinja_template_str` or field `jinja_template_str_loaded` for the
    loaded template data
    """

    jinja_template_str_loaded: str
    """
    The original jinja_template_str field from the config might not contain the
    needed template, and we may need to load S3 data specified with
    `jinja_template_path`. This field caches the loaded template content, it is also
    accessed through property `jinja_template_str`.
    """


class WorkflowsUnionMember1ConfigJinjaNodeConfigOutputTemplate(TypedDict, total=False):
    jinja_helper_functions: List[Union[str, object]]

    jinja_template_path: str

    jinja_template_str: str
    """Raw template to apply to the data.

    This should be a Jinja2 template string. Please note, the data will be mapped as
    'value' in the template. Default None corresponds to {{value}}. Should access
    property `jinja_template_str` or field `jinja_template_str_loaded` for the
    loaded template data
    """

    jinja_template_str_loaded: str
    """
    The original jinja_template_str field from the config might not contain the
    needed template, and we may need to load S3 data specified with
    `jinja_template_path`. This field caches the loaded template content, it is also
    accessed through property `jinja_template_str`.
    """


class WorkflowsUnionMember1ConfigJinjaNodeConfig(TypedDict, total=False):
    data_transformations: Dict[str, WorkflowsUnionMember1ConfigJinjaNodeConfigDataTransformations]

    log_output: bool

    log_prefix: str

    node_metadata: List[str]

    num_workers: int

    output_template: WorkflowsUnionMember1ConfigJinjaNodeConfigOutputTemplate
    """
    Base model for a Jinja template. Guaranteed to store a string that can be read
    in to Template().
    """


class WorkflowsUnionMember1ConfigChunkEvaluationNodeConfig(TypedDict, total=False):
    top_k_thresholds: Required[Iterable[int]]

    fuzzy_match_threshold: float

    node_metadata: List[str]

    num_workers: int

    require_all: bool


class WorkflowsUnionMember1ConfigRerankerNodeConfig(TypedDict, total=False):
    num_to_return: Required[int]

    scorers: Required[Iterable[object]]

    node_metadata: List[str]

    num_workers: int

    score_threshold: float


class WorkflowsUnionMember1ConfigRetrieverNodeConfig(TypedDict, total=False):
    num_to_return: Required[int]

    exact_knn_search: bool

    knowledge_base_id: str

    knowledge_base_name: str

    metadata: Dict[str, str]

    node_metadata: List[str]

    num_workers: int


class WorkflowsUnionMember1ConfigCitationNodeConfigCitationContext(TypedDict, total=False):
    generate_with_llm: bool

    metric: str

    min_similarity: float

    score: Literal["precision", "recall", "fmeasure"]


class WorkflowsUnionMember1ConfigCitationNodeConfig(TypedDict, total=False):
    citation_type: Required[Literal["rouge", "model_defined"]]

    citation_context: WorkflowsUnionMember1ConfigCitationNodeConfigCitationContext

    node_metadata: List[str]

    num_workers: int

    s3_path_override: str


class WorkflowsUnionMember1ConfigSearchCitationNodeConfig(TypedDict, total=False):
    end_search_regex: Required[str]

    search_regex: Required[str]

    node_metadata: List[str]

    num_workers: int


class WorkflowsUnionMember1ConfigDataTransformNodeConfig(TypedDict, total=False):
    action: Required[str]

    additional_inputs: object

    apply_to_dictlist_leaves: bool

    node_metadata: List[str]

    num_workers: int


class WorkflowsUnionMember1ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages(TypedDict, total=False):
    role_value_pairs: Required[Iterable[Dict[str, str]]]


class WorkflowsUnionMember1ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages(TypedDict, total=False):
    content: Required[str]

    role: Required[str]


WorkflowsUnionMember1ConfigCreateMessagesNodeConfigMessageConfig: TypeAlias = Union[
    WorkflowsUnionMember1ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages,
    WorkflowsUnionMember1ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages,
]


class WorkflowsUnionMember1ConfigCreateMessagesNodeConfig(TypedDict, total=False):
    message_configs: Required[Iterable[WorkflowsUnionMember1ConfigCreateMessagesNodeConfigMessageConfig]]

    node_metadata: List[str]

    num_workers: int


class WorkflowsUnionMember1ConfigInsertMessagesConfig(TypedDict, total=False):
    index: Required[int]

    node_metadata: List[str]

    num_workers: int


class WorkflowsUnionMember1ConfigRemoveMessageConfig(TypedDict, total=False):
    index: Required[int]

    node_metadata: List[str]

    num_workers: int


class WorkflowsUnionMember1ConfigTokenizerChatTemplateConfig(TypedDict, total=False):
    llm_model: Required[str]

    add_generation_prompt: bool

    kwargs: object

    max_length: int

    node_metadata: List[str]

    num_workers: int

    padding: bool

    truncation: bool


class WorkflowsUnionMember1ConfigLlmEngineNodeConfigBatchSysKwargs(TypedDict, total=False):
    checkpoint_path: str

    labels: Dict[str, str]

    num_shards: int

    seed: int


class WorkflowsUnionMember1ConfigLlmEngineNodeConfig(TypedDict, total=False):
    llm_model: Required[str]

    batch_run_mode: Literal["sync", "async"]

    batch_sys_kwargs: WorkflowsUnionMember1ConfigLlmEngineNodeConfigBatchSysKwargs

    frequency_penalty: float

    guided_choice: List[str]

    guided_json: object

    guided_regex: str

    include_stop_str_in_output: bool

    max_tokens: int

    node_metadata: List[str]

    num_workers: int

    presence_penalty: float

    stop_sequences: List[str]

    temperature: float

    timeout: int

    top_k: int

    top_p: float


class WorkflowsUnionMember1ConfigResponseParserNodeConfig(TypedDict, total=False):
    action: Required[str]

    node_metadata: List[str]

    num_workers: int

    reference_value: object


class WorkflowsUnionMember1ConfigIngestorConfig(TypedDict, total=False):
    node_metadata: List[str]

    num_workers: int


class WorkflowsUnionMember1ConfigProcessingNodeConfigFunctionSpecs(TypedDict, total=False):
    kwargs: Required[object]

    path: Required[str]


class WorkflowsUnionMember1ConfigProcessingNodeConfig(TypedDict, total=False):
    function_specs: Required[Dict[str, WorkflowsUnionMember1ConfigProcessingNodeConfigFunctionSpecs]]

    return_key: Required[str]

    node_metadata: List[str]

    num_workers: int


class WorkflowsUnionMember1ConfigSqlExecutorNodeConfig(TypedDict, total=False):
    connector_kwargs: Required[Dict[str, str]]

    connector_type: Literal["snowflake"]

    log_queries: bool

    node_metadata: List[str]

    num_workers: int

    return_type: Literal["df", "dicts", "markdown", "json", "str"]

    schema_remapping_file: str

    secrets: List[str]


class WorkflowsUnionMember1ConfigStaticNodeConfig(TypedDict, total=False):
    from_file: Union[Iterable[object], str, object]

    node_metadata: List[str]

    num_workers: int

    value: object


class WorkflowsUnionMember1ConfigGenerationNodeConfig(TypedDict, total=False):
    llm_model: str

    llm_model_deployment: str

    llm_model_instance: str

    max_tokens: int

    node_metadata: List[str]

    num_workers: int

    stop_sequences: List[str]

    strip_whitespace: bool

    temperature: float

    tool_name: str


WorkflowsUnionMember1Config: TypeAlias = Union[
    WorkflowsUnionMember1ConfigNodeConfig,
    WorkflowsUnionMember1ConfigJinjaNodeConfig,
    WorkflowsUnionMember1ConfigChunkEvaluationNodeConfig,
    WorkflowsUnionMember1ConfigRerankerNodeConfig,
    WorkflowsUnionMember1ConfigRetrieverNodeConfig,
    WorkflowsUnionMember1ConfigCitationNodeConfig,
    WorkflowsUnionMember1ConfigSearchCitationNodeConfig,
    WorkflowsUnionMember1ConfigDataTransformNodeConfig,
    WorkflowsUnionMember1ConfigCreateMessagesNodeConfig,
    WorkflowsUnionMember1ConfigInsertMessagesConfig,
    WorkflowsUnionMember1ConfigRemoveMessageConfig,
    WorkflowsUnionMember1ConfigTokenizerChatTemplateConfig,
    WorkflowsUnionMember1ConfigLlmEngineNodeConfig,
    WorkflowsUnionMember1ConfigResponseParserNodeConfig,
    WorkflowsUnionMember1ConfigIngestorConfig,
    WorkflowsUnionMember1ConfigProcessingNodeConfig,
    WorkflowsUnionMember1ConfigSqlExecutorNodeConfig,
    WorkflowsUnionMember1ConfigStaticNodeConfig,
    WorkflowsUnionMember1ConfigGenerationNodeConfig,
]


class WorkflowsUnionMember1(TypedDict, total=False):
    config: Required[WorkflowsUnionMember1Config]
    """A data model describing parameters for back-citation using ROUGE similarity.

    metric is the ROUGE metric to use (e.g. rouge1, rouge2, rougeLsum) score is one
    of "precision", "recall", "fmeasure"

    NOTE (john): copied directly from generation.py in order to subclass from
    NodeConfig.
    """

    name: Required[str]

    type: Required[str]

    inputs: Dict[str, Union[str, Dict[str, Union[str, object]]]]


class EvaluationConfigNodeConfig(TypedDict, total=False):
    node_metadata: List[str]

    num_workers: int


class EvaluationConfigJinjaNodeConfigDataTransformations(TypedDict, total=False):
    jinja_helper_functions: List[Union[str, object]]

    jinja_template_path: str

    jinja_template_str: str
    """Raw template to apply to the data.

    This should be a Jinja2 template string. Please note, the data will be mapped as
    'value' in the template. Default None corresponds to {{value}}. Should access
    property `jinja_template_str` or field `jinja_template_str_loaded` for the
    loaded template data
    """

    jinja_template_str_loaded: str
    """
    The original jinja_template_str field from the config might not contain the
    needed template, and we may need to load S3 data specified with
    `jinja_template_path`. This field caches the loaded template content, it is also
    accessed through property `jinja_template_str`.
    """


class EvaluationConfigJinjaNodeConfigOutputTemplate(TypedDict, total=False):
    jinja_helper_functions: List[Union[str, object]]

    jinja_template_path: str

    jinja_template_str: str
    """Raw template to apply to the data.

    This should be a Jinja2 template string. Please note, the data will be mapped as
    'value' in the template. Default None corresponds to {{value}}. Should access
    property `jinja_template_str` or field `jinja_template_str_loaded` for the
    loaded template data
    """

    jinja_template_str_loaded: str
    """
    The original jinja_template_str field from the config might not contain the
    needed template, and we may need to load S3 data specified with
    `jinja_template_path`. This field caches the loaded template content, it is also
    accessed through property `jinja_template_str`.
    """


class EvaluationConfigJinjaNodeConfig(TypedDict, total=False):
    data_transformations: Dict[str, EvaluationConfigJinjaNodeConfigDataTransformations]

    log_output: bool

    log_prefix: str

    node_metadata: List[str]

    num_workers: int

    output_template: EvaluationConfigJinjaNodeConfigOutputTemplate
    """
    Base model for a Jinja template. Guaranteed to store a string that can be read
    in to Template().
    """


class EvaluationConfigChunkEvaluationNodeConfig(TypedDict, total=False):
    top_k_thresholds: Required[Iterable[int]]

    fuzzy_match_threshold: float

    node_metadata: List[str]

    num_workers: int

    require_all: bool


class EvaluationConfigRerankerNodeConfig(TypedDict, total=False):
    num_to_return: Required[int]

    scorers: Required[Iterable[object]]

    node_metadata: List[str]

    num_workers: int

    score_threshold: float


class EvaluationConfigRetrieverNodeConfig(TypedDict, total=False):
    num_to_return: Required[int]

    exact_knn_search: bool

    knowledge_base_id: str

    knowledge_base_name: str

    metadata: Dict[str, str]

    node_metadata: List[str]

    num_workers: int


class EvaluationConfigCitationNodeConfigCitationContext(TypedDict, total=False):
    generate_with_llm: bool

    metric: str

    min_similarity: float

    score: Literal["precision", "recall", "fmeasure"]


class EvaluationConfigCitationNodeConfig(TypedDict, total=False):
    citation_type: Required[Literal["rouge", "model_defined"]]

    citation_context: EvaluationConfigCitationNodeConfigCitationContext

    node_metadata: List[str]

    num_workers: int

    s3_path_override: str


class EvaluationConfigSearchCitationNodeConfig(TypedDict, total=False):
    end_search_regex: Required[str]

    search_regex: Required[str]

    node_metadata: List[str]

    num_workers: int


class EvaluationConfigDataTransformNodeConfig(TypedDict, total=False):
    action: Required[str]

    additional_inputs: object

    apply_to_dictlist_leaves: bool

    node_metadata: List[str]

    num_workers: int


class EvaluationConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages(TypedDict, total=False):
    role_value_pairs: Required[Iterable[Dict[str, str]]]


class EvaluationConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages(TypedDict, total=False):
    content: Required[str]

    role: Required[str]


EvaluationConfigCreateMessagesNodeConfigMessageConfig: TypeAlias = Union[
    EvaluationConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages,
    EvaluationConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages,
]


class EvaluationConfigCreateMessagesNodeConfig(TypedDict, total=False):
    message_configs: Required[Iterable[EvaluationConfigCreateMessagesNodeConfigMessageConfig]]

    node_metadata: List[str]

    num_workers: int


class EvaluationConfigInsertMessagesConfig(TypedDict, total=False):
    index: Required[int]

    node_metadata: List[str]

    num_workers: int


class EvaluationConfigRemoveMessageConfig(TypedDict, total=False):
    index: Required[int]

    node_metadata: List[str]

    num_workers: int


class EvaluationConfigTokenizerChatTemplateConfig(TypedDict, total=False):
    llm_model: Required[str]

    add_generation_prompt: bool

    kwargs: object

    max_length: int

    node_metadata: List[str]

    num_workers: int

    padding: bool

    truncation: bool


class EvaluationConfigLlmEngineNodeConfigBatchSysKwargs(TypedDict, total=False):
    checkpoint_path: str

    labels: Dict[str, str]

    num_shards: int

    seed: int


class EvaluationConfigLlmEngineNodeConfig(TypedDict, total=False):
    llm_model: Required[str]

    batch_run_mode: Literal["sync", "async"]

    batch_sys_kwargs: EvaluationConfigLlmEngineNodeConfigBatchSysKwargs

    frequency_penalty: float

    guided_choice: List[str]

    guided_json: object

    guided_regex: str

    include_stop_str_in_output: bool

    max_tokens: int

    node_metadata: List[str]

    num_workers: int

    presence_penalty: float

    stop_sequences: List[str]

    temperature: float

    timeout: int

    top_k: int

    top_p: float


class EvaluationConfigResponseParserNodeConfig(TypedDict, total=False):
    action: Required[str]

    node_metadata: List[str]

    num_workers: int

    reference_value: object


class EvaluationConfigIngestorConfig(TypedDict, total=False):
    node_metadata: List[str]

    num_workers: int


class EvaluationConfigProcessingNodeConfigFunctionSpecs(TypedDict, total=False):
    kwargs: Required[object]

    path: Required[str]


class EvaluationConfigProcessingNodeConfig(TypedDict, total=False):
    function_specs: Required[Dict[str, EvaluationConfigProcessingNodeConfigFunctionSpecs]]

    return_key: Required[str]

    node_metadata: List[str]

    num_workers: int


class EvaluationConfigSqlExecutorNodeConfig(TypedDict, total=False):
    connector_kwargs: Required[Dict[str, str]]

    connector_type: Literal["snowflake"]

    log_queries: bool

    node_metadata: List[str]

    num_workers: int

    return_type: Literal["df", "dicts", "markdown", "json", "str"]

    schema_remapping_file: str

    secrets: List[str]


class EvaluationConfigStaticNodeConfig(TypedDict, total=False):
    from_file: Union[Iterable[object], str, object]

    node_metadata: List[str]

    num_workers: int

    value: object


class EvaluationConfigGenerationNodeConfig(TypedDict, total=False):
    llm_model: str

    llm_model_deployment: str

    llm_model_instance: str

    max_tokens: int

    node_metadata: List[str]

    num_workers: int

    stop_sequences: List[str]

    strip_whitespace: bool

    temperature: float

    tool_name: str


EvaluationConfig: TypeAlias = Union[
    EvaluationConfigNodeConfig,
    EvaluationConfigJinjaNodeConfig,
    EvaluationConfigChunkEvaluationNodeConfig,
    EvaluationConfigRerankerNodeConfig,
    EvaluationConfigRetrieverNodeConfig,
    EvaluationConfigCitationNodeConfig,
    EvaluationConfigSearchCitationNodeConfig,
    EvaluationConfigDataTransformNodeConfig,
    EvaluationConfigCreateMessagesNodeConfig,
    EvaluationConfigInsertMessagesConfig,
    EvaluationConfigRemoveMessageConfig,
    EvaluationConfigTokenizerChatTemplateConfig,
    EvaluationConfigLlmEngineNodeConfig,
    EvaluationConfigResponseParserNodeConfig,
    EvaluationConfigIngestorConfig,
    EvaluationConfigProcessingNodeConfig,
    EvaluationConfigSqlExecutorNodeConfig,
    EvaluationConfigStaticNodeConfig,
    EvaluationConfigGenerationNodeConfig,
]


class Evaluation(TypedDict, total=False):
    config: Required[EvaluationConfig]
    """A data model describing parameters for back-citation using ROUGE similarity.

    metric is the ROUGE metric to use (e.g. rouge1, rouge2, rougeLsum) score is one
    of "precision", "recall", "fmeasure"

    NOTE (john): copied directly from generation.py in order to subclass from
    NodeConfig.
    """

    name: Required[str]

    type: Required[str]

    inputs: Dict[str, Union[str, Dict[str, Union[str, object]]]]


class PlanConfigParam(TypedDict, total=False):
    plan: Required[Iterable[Plan]]

    workflows: Required[Dict[str, Union[str, Iterable[WorkflowsUnionMember1]]]]

    id: str

    account_id: str

    concurrency_default: bool

    datasets: Iterable[object]

    egp_api_key_override: str

    evaluations: Iterable[Evaluation]

    final_output_nodes: List[str]

    nodes_to_log: Union[str, List[str]]

    num_workers: int

    streaming_nodes: List[str]
