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
    "PaginatedApplicationTestCaseOutputWithViews",
    "Item",
    "ItemApplicationTestCaseGenerationOutputResponseWithViews",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteraction",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpan",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsMetricScore",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadata",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadataUsage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViews",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutput",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfFlexibleIoChunk",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationExtraInfo",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteraction",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpan",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsMetricScore",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadata",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadataUsage",
]


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpan(BaseModel):
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
                ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk
            ],
            List[
                ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2
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
                ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk
            ],
            List[
                ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2
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
                    ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk
                ],
                List[
                    ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2
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


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteraction(BaseModel):
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

    trace_spans: Optional[List[ItemApplicationTestCaseGenerationOutputResponseWithViewsInteractionTraceSpan]] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadataUsage(BaseModel):
    completion_tokens: Optional[int] = None

    cost: Optional[float] = None

    model: Optional[Literal["gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125", "gpt-4o-2024-05-13"]] = None
    """An enumeration."""

    prompt_tokens: Optional[int] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadata(BaseModel):
    logging: Optional[object] = None

    reasoning: Optional[str] = None

    time_elapsed_s: Optional[int] = None

    usage: Optional[List[ItemApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadataUsage]] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViewsMetricScore(BaseModel):
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

    llm_metadata: Optional[ItemApplicationTestCaseGenerationOutputResponseWithViewsMetricScoreLlmMetadata] = None

    score: Optional[float] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViews(BaseModel):
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

    interaction: Optional[ItemApplicationTestCaseGenerationOutputResponseWithViewsInteraction] = None

    metric_scores: Optional[List[ItemApplicationTestCaseGenerationOutputResponseWithViewsMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["GENERATION"]] = None

    test_case_version: Optional[TestCase] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]

ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutput(BaseModel):
    generation_output: Union[
        str,
        float,
        List[ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfFlexibleIoChunk],
        List[ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2],
        List[object],
        Dict[
            str,
            Union[
                str,
                float,
                List[
                    ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                List[
                    ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                List[object],
                object,
            ],
        ],
        object,
    ]

    generation_extra_info: Optional[ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationExtraInfo] = (
        None
    )


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpan(BaseModel):
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
                ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfFlexibleIoChunk
            ],
            List[
                ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationInputArrayOfChatMessageV2
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
                ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfFlexibleIoChunk
            ],
            List[
                ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationOutputArrayOfChatMessageV2
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
                    ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfFlexibleIoChunk
                ],
                List[
                    ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpanOperationExpectedArrayOfChatMessageV2
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


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteraction(BaseModel):
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

    trace_spans: Optional[List[ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteractionTraceSpan]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadataUsage(BaseModel):
    completion_tokens: Optional[int] = None

    cost: Optional[float] = None

    model: Optional[Literal["gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125", "gpt-4o-2024-05-13"]] = None
    """An enumeration."""

    prompt_tokens: Optional[int] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadata(BaseModel):
    logging: Optional[object] = None

    reasoning: Optional[str] = None

    time_elapsed_s: Optional[int] = None

    usage: Optional[List[ItemApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadataUsage]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsMetricScore(BaseModel):
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

    llm_metadata: Optional[ItemApplicationTestCaseFlexibleOutputResponseWithViewsMetricScoreLlmMetadata] = None

    score: Optional[float] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ItemApplicationTestCaseFlexibleOutputResponseWithViewsOutput

    test_case_id: str

    application_interaction_id: Optional[str] = None

    interaction: Optional[ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteraction] = None

    metric_scores: Optional[List[ItemApplicationTestCaseFlexibleOutputResponseWithViewsMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["FLEXIBLE"]] = None

    test_case_version: Optional[TestCase] = None


Item: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseGenerationOutputResponseWithViews, ItemApplicationTestCaseFlexibleOutputResponseWithViews
    ],
    PropertyInfo(discriminator="schema_type"),
]


class PaginatedApplicationTestCaseOutputWithViews(BaseModel):
    current_page: int
    """The current page number."""

    items: List[Item]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""
