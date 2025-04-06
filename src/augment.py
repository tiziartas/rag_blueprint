"""
This script is used to handle chat interactions using the ChainLit library and a query engine from the RAG (Retrieval-Augmented Generation) model.
To make it work vector storage should be filled with the embeddings of the documents.
To run the script execute the following command from the root directory of the project:

> python src/chat.py
"""

import chainlit as cl
from chainlit.cli import run_chainlit

from augmentation.bootstrap.initializer import AugmentationInitializer
from augmentation.chainlit.service import (
    ChainlitService,
    ChainlitServiceFactory,
)
from augmentation.chainlit.utils import ChainlitUtils
from augmentation.components.query_engines.registry import QueryEngineRegistry


@cl.cache
def get_cached_initializer() -> AugmentationInitializer:
    return AugmentationInitializer()


@cl.data_layer
def get_data_layer() -> ChainlitService:
    """Initialize application-level components.

    This runs once when the Chainlit app starts.
    """
    configuration = get_cached_initializer().get_configuration()
    return ChainlitServiceFactory.create(configuration.augmentation)


@cl.on_chat_start
async def start():
    """Initialize chat session with query engine.

    Sets up session-specific query engine and displays welcome message.
    """
    configuration = get_cached_initializer().get_configuration()
    query_engine = QueryEngineRegistry.get(
        configuration.augmentation.query_engine.name
    ).create(configuration)
    query_engine.set_session_id(cl.user_session.get("id"))
    cl.user_session.set("query_engine", query_engine)
    await ChainlitUtils.get_welcome_message().send()


@cl.on_message
async def main(user_message: cl.Message):
    """Process user messages and generate responses.

    Args:
        user_message: Message received from user

    Note:
        Streams tokens for real-time response generation
        Adds source references to responses
    """
    query_engine = cl.user_session.get("query_engine")
    assistant_message = cl.Message(content="", author="Assistant")
    response = await cl.make_async(query_engine.query)(
        user_message.content, assistant_message.parent_id
    )
    for token in response.response_gen:
        await assistant_message.stream_token(token)
    ChainlitUtils.add_references(assistant_message, response)
    await assistant_message.send()


if __name__ == "__main__":
    run_chainlit(__file__)
