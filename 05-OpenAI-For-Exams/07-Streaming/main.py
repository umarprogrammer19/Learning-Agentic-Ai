import asyncio
from dataclasses import dataclass
from typing import Callable
from agents import Agent, Runner, function_tool, RunContextWrapper, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent


@dataclass
class UserContext:
    username: str
    email: str | None = None
