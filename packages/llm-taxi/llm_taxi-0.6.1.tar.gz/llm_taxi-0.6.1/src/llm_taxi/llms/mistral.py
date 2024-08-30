from collections.abc import AsyncGenerator
from typing import ClassVar

from mistralai.models.chat_completion import ChatMessage

from llm_taxi.clients.mistral import Mistral as MistralClient
from llm_taxi.conversation import Message
from llm_taxi.llms.base import LLM
from llm_taxi.llms.openai import streaming_response
from llm_taxi.types import NOT_SUPPORTED, NotSupportedOr, SupportedParams


class Mistral(MistralClient, LLM):
    param_mapping: ClassVar[dict[SupportedParams, NotSupportedOr[str]]] = {
        "temperature": "temperature",
        "max_tokens": "max_tokens",
        "top_k": NOT_SUPPORTED,
        "top_p": "top_p",
        "stop": NOT_SUPPORTED,
        "seed": "random_seed",
        "frequency_penalty": NOT_SUPPORTED,
        "presence_penalty": NOT_SUPPORTED,
        "response_format": "response_format",
        "tools": "tools",
        "tool_choice": "tool_choice",
    }

    def _convert_messages(self, messages: list[Message]) -> list[ChatMessage]:
        return [ChatMessage(role=x.role.value, content=x.content) for x in messages]

    async def streaming_response(
        self,
        messages: list[Message],
        **kwargs,
    ) -> AsyncGenerator:
        response = self.client.chat_stream(
            messages=self._convert_messages(messages),
            **self._get_call_kwargs(**kwargs),
        )

        return streaming_response(response)

    async def response(self, messages: list[Message], **kwargs) -> str:
        response = await self.client.chat(
            messages=self._convert_messages(messages),
            **self._get_call_kwargs(**kwargs),
        )

        content = response.choices[0].message.content
        if isinstance(content, list):
            return "".join(content)

        return content
