from pydantic import BaseModel, Field
from typing import Optional


class MathHomeworkOutput(BaseModel):
    is_math_homework: bool = Field(
        ..., description="Whether the query appears to be math homework"
    )
    reasoning: str = Field(
        ..., description="Explanation of why this is or isn't math homework"
    )


class CodeAssignmentOutput(BaseModel):
    is_code_assignment: bool = Field(
        ..., description="Whether the query appears to be a coding assignment"
    )
    reasoning: str = Field(
        ..., description="Explanation of why this is or isn't a coding assignment"
    )


class EssayWritingOutput(BaseModel):
    is_essay_request: bool = Field(
        ..., description="Whether the query appears to be asking for an essay"
    )
    reasoning: str = Field(
        ..., description="Explanation of why this is or isn't an essay request"
    )
    subject: Optional[str] = Field(
        None, description="The subject of the essay if applicable"
    )
