"""This module contains the setup_call function for Cohere tools."""

import inspect
from collections.abc import AsyncIterator, Awaitable, Callable, Coroutine, Iterator
from typing import Any, cast

from cohere import (
    AsyncClient,
    Client,
    NonStreamedChatResponse,
)
from cohere.types import ChatMessage

from ...base import BaseMessageParam, BaseTool, _utils
from ..call_kwargs import CohereCallKwargs
from ..call_params import CohereCallParams
from ..dynamic_config import CohereDynamicConfig
from ..tool import CohereTool
from ._convert_message_params import convert_message_params


def setup_call(
    *,
    model: str,
    client: Client | AsyncClient | None,
    fn: Callable[..., CohereDynamicConfig | Awaitable[CohereDynamicConfig]],
    fn_args: dict[str, Any],
    dynamic_config: CohereDynamicConfig,
    tools: list[type[BaseTool] | Callable] | None,
    json_mode: bool,
    call_params: CohereCallParams,
    extract: bool,
) -> tuple[
    Callable[..., NonStreamedChatResponse]
    | Callable[..., Awaitable[NonStreamedChatResponse]],
    str,
    list[ChatMessage],
    list[type[CohereTool]] | None,
    CohereCallKwargs,
]:
    prompt_template, messages, tool_types, call_kwargs = _utils.setup_call(
        fn, fn_args, dynamic_config, tools, CohereTool, call_params
    )
    call_kwargs = cast(CohereCallKwargs, call_kwargs)
    messages = cast(list[BaseMessageParam | ChatMessage], messages)
    messages = convert_message_params(messages)

    preamble = ""
    if "preamble" in call_kwargs and call_kwargs["preamble"] is not None:
        preamble = call_kwargs.pop("preamble", "") or ""
    if messages[0].role == "SYSTEM":  # type: ignore
        if preamble:
            preamble += "\n\n"
        preamble += messages.pop(0).message
    if preamble:
        call_kwargs["preamble"] = preamble
    if len(messages) > 1:
        call_kwargs["chat_history"] = messages[:-1]
    if json_mode:
        # Cannot mutate ChatMessage in place
        messages[-1] = ChatMessage(
            role=messages[-1].role,  # type: ignore
            message=messages[-1].message
            + _utils.json_mode_content(tool_types[0] if tool_types else None),
            tool_calls=messages[-1].tool_calls,
        )
        call_kwargs.pop("tools", None)
    elif extract:
        assert tool_types, "At least one tool must be provided for extraction."
    call_kwargs |= {
        "model": model,
        "message": messages[-1].message,
    }

    if client is None:
        client = AsyncClient() if inspect.iscoroutinefunction(fn) else Client()

    def create_or_stream(
        stream: bool,
        **kwargs: Any,  # noqa: ANN401
    ) -> (
        Iterator[Any]
        | AsyncIterator[Any]
        | NonStreamedChatResponse
        | Coroutine[Any, Any, NonStreamedChatResponse]
    ):
        if stream:
            return client.chat_stream(**kwargs)
        return client.chat(**kwargs)

    return create_or_stream, prompt_template, messages, tool_types, call_kwargs  # type: ignore
