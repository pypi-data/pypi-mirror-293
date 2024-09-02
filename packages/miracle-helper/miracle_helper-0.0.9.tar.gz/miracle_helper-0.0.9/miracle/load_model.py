import os

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def get_anthropic_model(
    model_name="haiku",
    temperature=0.1,
    max_tokens=4096,
    max_retries=3
) -> ChatAnthropic:
    """Load the Anthropic model easily. You can freely revise it to make it easier to use."""
    if model_name == 'sonnet':
        model = "claude-3-5-sonnet-20240620"
    elif model_name == 'haiku':
        model = "claude-3-haiku-20240307"
    else:
        model = "claude-3-opus-20240229"

    llm = ChatAnthropic(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
        timeout=None,
        max_retries=max_retries,
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
    )
    return llm


def get_openai_model(
    model_name="chatgpt-4o-latest",
    temperature=0.1,
    max_tokens=4096,
    max_retries=3
) -> ChatOpenAI:
    if model_name == 'gpt-4o-2024-05-13':
        model = "gpt-4o-2024-05-13"
    elif model_name == 'gpt-4o-2024-08-06':
        model = 'gpt-4o-2024-08-06'
    elif model_name == 'chatgpt-4o-latest':
        model = 'chatgpt-4o-latest'
    else:
        model = "gpt-4-turbo-2024-04-09"

    llm = ChatOpenAI(
        model_name=model,
        temperature=temperature,
        max_tokens=max_tokens,
        max_retries=max_retries,
        openai_api_key=os.getenv('OPENAI_API_KEY'),
    )
    return llm


def get_openai_embedding_model(model_name="small") -> OpenAIEmbeddings:
    """Load the OpenAI embedding model easily. You can freely revise it to make it easier to use."""
    if model_name == 'small':
        model = "text-embedding-3-small"
    else:
        model = "text-embedding-3-large"
    embedding = OpenAIEmbeddings(
        model=model,
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    return embedding
