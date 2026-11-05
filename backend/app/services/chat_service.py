from dataclasses import dataclass
from http.client import responses
from typing import Iterator

import anthropic

from app.core.config import settings

SYSTEM = 'You are a friendly customer support assistant. Answer briefly and clearly.'


class LLMError(Exception):
    '''The language model could not produce an answer.'''


@dataclass
class ChatResult:
    answer: str
    input_tokens: int
    output_tokens: int


class ChatService:
    def __init__(self, llm: anthropic.Anthropic):
        self.llm = llm

    def answer(self, message: str) -> ChatResult:
        try:
            response = self.llm.messages.create(
                model=settings.model,
                max_tokens=1024,
                system=SYSTEM,
                messages=[{'role': 'user', 'content': message}],
            )
        except anthropic.APIError as e:
            raise LLMError(str(e)) from e

        text = ''.join(b.text for b in response.content if b.type == 'text')
        return ChatResult(text, response.usage.input_tokens, response.usage.output_tokens)

    def stream_answer(self, message: str) -> Iterator[str]:
        with self.llm.messages.stream(
            model=settings.model,
            max_tokens=1024,
            system=SYSTEM,
            messages=[{'role': 'user', 'content': message}],
        ) as stream:
            yield from stream.text_stream
