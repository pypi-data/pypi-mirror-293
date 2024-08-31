from enum import Enum


class AppEnv(str, Enum):
    DEV = "dev"
    TEST = "test"
    STAG = "stag"
    PROD = "prod"


class ModelNameLLM(str, Enum):
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20240620"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    GPT_4 = "gpt-4o"
    GPT_3 = "gpt-3.5-turbo"


class TaskType(str, Enum):
    # Coder
    FRONTEND = "FRONTEND"
    SVC_IMPL = "SVC_IMPL"
    UNIT_TEST = "UNIT_TEST"
    INTERFACE = "INTERFACE"
    DATA_MODEL = "DATA_MODEL"

    # CTO
    SCOPED_TASK = "SCOPED_TASK"
    REQUIREMENT = "REQUIREMENT"
    ARCHITECTURE = "ARCHITECTURE"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    PROTOTYPE = "PROTOTYPE"

    # CEO
    ROADMAP = "ROADMAP"
    OKR = "OKR"

    # COO
    COMPLIANCE = "COMPLIANCE"

    # General
    DOCUMENTATION = "DOCUMENTATION"

    # Special
    UNDEFINED = "UNDEFINED"
