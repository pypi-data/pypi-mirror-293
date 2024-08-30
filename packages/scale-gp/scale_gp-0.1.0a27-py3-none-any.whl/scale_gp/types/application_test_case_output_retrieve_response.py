# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .evaluation_datasets.test_case import TestCase
from .shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from .shared.result_schema_generation import ResultSchemaGeneration
from .shared.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "ApplicationTestCaseOutputRetrieveResponse",
    "ApplicationTestCaseGenerationOutputResponseWithViews",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteraction",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpan",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseGenerationOutputResponseWithViewsMetricScore",
    "ApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadata",
    "ApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadataUsage",
    "ApplicationTestCaseFlexibleOutputResponseWithViews",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutput",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfFlexibleIoChunk",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationExtraInfo",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteraction",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpan",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsMetricScore",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadata",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadataUsage",
]


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpan(BaseModel):
    id: str
    """Identifies the application step"""

    application_interaction_id: str
    """The id of the application insight this step belongs to"""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    node_id: str
    """The id of the node in the application_variant config that emitted this insight"""

    operation_input: Dict[
        str,
        Union[
            str,
            float,
            List[
                ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk
            ],
            List[
                ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2
            ],
            List[object],
            object,
        ],
    ]
    """The JSON representation of the input that this step received."""

    operation_output: Dict[
        str,
        Union[
            str,
            float,
            List[
                ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk
            ],
            List[
                ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2
            ],
            List[object],
            object,
        ],
    ]
    """The JSON representation of the output that this step emitted."""

    operation_status: Literal["SUCCESS", "ERROR"]
    """An enumeration."""

    operation_type: Literal[
        "TEXT_INPUT",
        "TEXT_OUTPUT",
        "COMPLETION",
        "KB_RETRIEVAL",
        "RERANKING",
        "EXTERNAL_ENDPOINT",
        "PROMPT_ENGINEERING",
        "DOCUMENT_INPUT",
        "MAP_REDUCE",
        "DOCUMENT_SEARCH",
        "DOCUMENT_PROMPT",
        "CUSTOM",
        "INPUT_GUARDRAIL",
        "OUTPUT_GUARDRAIL",
    ]
    """An enumeration."""

    start_timestamp: datetime
    """The start time of the step"""

    operation_expected: Optional[
        Dict[
            str,
            Union[
                str,
                float,
                List[
                    ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk
                ],
                List[
                    ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2
                ],
                List[object],
                object,
            ],
        ]
    ] = None
    """The JSON representation of the expected output for this step"""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """


class ApplicationTestCaseGenerationOutputResponseWithViewsInteraction(BaseModel):
    id: str

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: object

    operation_status: Literal["SUCCESS", "ERROR"]
    """An enumeration."""

    output: object

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT"]] = None
    """An enumeration."""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    trace_spans: Optional[List[ApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpan]] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadataUsage(BaseModel):
    completion_tokens: Optional[int] = None

    cost: Optional[float] = None

    model: Optional[Literal["gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125", "gpt-4o-2024-05-13"]] = None
    """An enumeration."""

    prompt_tokens: Optional[int] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadata(BaseModel):
    logging: Optional[object] = None

    reasoning: Optional[str] = None

    time_elapsed_s: Optional[int] = None

    usage: Optional[List[ApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadataUsage]] = None


class ApplicationTestCaseGenerationOutputResponseWithViewsMetricScore(BaseModel):
    category: Literal["accuracy", "quality", "retrieval", "trust-and-safety"]
    """An enumeration."""

    metric_type: Literal[
        "answer-correctness",
        "answer-relevance",
        "faithfulness",
        "context-recall",
        "coherence",
        "grammar",
        "moderation",
        "safety",
        "safety-bias-and-stereotyping",
        "safety-opinions-disputed-topics",
        "safety-unethical-harmful-activities",
        "safety-copyright-violations",
        "safety-harmful-content",
        "safety-privacy-violations",
    ]

    llm_metadata: Optional[ApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadata] = None

    score: Optional[float] = None


class ApplicationTestCaseGenerationOutputResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ResultSchemaGeneration

    test_case_id: str

    application_interaction_id: Optional[str] = None

    interaction: Optional[ApplicationTestCaseGenerationOutputResponseWithViewsInteraction] = None

    metric_scores: Optional[List[ApplicationTestCaseGenerationOutputResponseWithViewsMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["GENERATION"]] = None

    test_case_version: Optional[TestCase] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]

ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutput(BaseModel):
    generation_output: Union[
        str,
        float,
        List[ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfFlexibleIoChunk],
        List[ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2],
        List[object],
        Dict[
            str,
            Union[
                str,
                float,
                List[
                    ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                List[
                    ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                List[object],
                object,
            ],
        ],
        object,
    ]

    generation_extra_info: Optional[ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationExtraInfo] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpan(BaseModel):
    id: str
    """Identifies the application step"""

    application_interaction_id: str
    """The id of the application insight this step belongs to"""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    node_id: str
    """The id of the node in the application_variant config that emitted this insight"""

    operation_input: Dict[
        str,
        Union[
            str,
            float,
            List[
                ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk
            ],
            List[
                ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2
            ],
            List[object],
            object,
        ],
    ]
    """The JSON representation of the input that this step received."""

    operation_output: Dict[
        str,
        Union[
            str,
            float,
            List[
                ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk
            ],
            List[
                ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2
            ],
            List[object],
            object,
        ],
    ]
    """The JSON representation of the output that this step emitted."""

    operation_status: Literal["SUCCESS", "ERROR"]
    """An enumeration."""

    operation_type: Literal[
        "TEXT_INPUT",
        "TEXT_OUTPUT",
        "COMPLETION",
        "KB_RETRIEVAL",
        "RERANKING",
        "EXTERNAL_ENDPOINT",
        "PROMPT_ENGINEERING",
        "DOCUMENT_INPUT",
        "MAP_REDUCE",
        "DOCUMENT_SEARCH",
        "DOCUMENT_PROMPT",
        "CUSTOM",
        "INPUT_GUARDRAIL",
        "OUTPUT_GUARDRAIL",
    ]
    """An enumeration."""

    start_timestamp: datetime
    """The start time of the step"""

    operation_expected: Optional[
        Dict[
            str,
            Union[
                str,
                float,
                List[
                    ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk
                ],
                List[
                    ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2
                ],
                List[object],
                object,
            ],
        ]
    ] = None
    """The JSON representation of the expected output for this step"""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteraction(BaseModel):
    id: str

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: object

    operation_status: Literal["SUCCESS", "ERROR"]
    """An enumeration."""

    output: object

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT"]] = None
    """An enumeration."""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    trace_spans: Optional[List[ApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpan]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadataUsage(BaseModel):
    completion_tokens: Optional[int] = None

    cost: Optional[float] = None

    model: Optional[Literal["gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125", "gpt-4o-2024-05-13"]] = None
    """An enumeration."""

    prompt_tokens: Optional[int] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadata(BaseModel):
    logging: Optional[object] = None

    reasoning: Optional[str] = None

    time_elapsed_s: Optional[int] = None

    usage: Optional[List[ApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadataUsage]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsMetricScore(BaseModel):
    category: Literal["accuracy", "quality", "retrieval", "trust-and-safety"]
    """An enumeration."""

    metric_type: Literal[
        "answer-correctness",
        "answer-relevance",
        "faithfulness",
        "context-recall",
        "coherence",
        "grammar",
        "moderation",
        "safety",
        "safety-bias-and-stereotyping",
        "safety-opinions-disputed-topics",
        "safety-unethical-harmful-activities",
        "safety-copyright-violations",
        "safety-harmful-content",
        "safety-privacy-violations",
    ]

    llm_metadata: Optional[ApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadata] = None

    score: Optional[float] = None


class ApplicationTestCaseFlexibleOutputResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ApplicationTestCaseFlexibleOutputResponseWithViewsOutput

    test_case_id: str

    application_interaction_id: Optional[str] = None

    interaction: Optional[ApplicationTestCaseFlexibleOutputResponseWithViewsInteraction] = None

    metric_scores: Optional[List[ApplicationTestCaseFlexibleOutputResponseWithViewsMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["FLEXIBLE"]] = None

    test_case_version: Optional[TestCase] = None


ApplicationTestCaseOutputRetrieveResponse: TypeAlias = Annotated[
    Union[ApplicationTestCaseGenerationOutputResponseWithViews, ApplicationTestCaseFlexibleOutputResponseWithViews],
    PropertyInfo(discriminator="schema_type"),
]
