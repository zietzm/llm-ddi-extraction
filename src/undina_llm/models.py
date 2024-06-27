from typing import Literal

from sqlmodel import Column, Field, Relationship, SQLModel, String, UniqueConstraint


class SystemPrompt(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    prompt: str = Field(unique=True)


class Prompt(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    prompt: str = Field(unique=True)


class DrugLabel(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("set_id", "label_id", "spl_version", name="unique_drug_label"),
    )

    id: int | None = Field(default=None, primary_key=True)
    set_id: str
    label_id: str
    spl_version: str
    title: str
    AR: str | None = None
    WA: str | None = None
    PR: str | None = None
    IU: str | None = None
    CO: str | None = None
    DI: str | None = None
    WP: str | None = None
    SP: str | None = None
    DS: str | None = None
    BW: str | None = None
    OV: str | None = None
    MC: str | None = None
    MI: str | None = None


class Response(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    system_prompt_id: int | None = Field(default=None, foreign_key="systemprompt.id")
    system_prompt: SystemPrompt | None = Relationship()
    prompt_id: int | None = Field(default=None, foreign_key="prompt.id")
    prompt: Prompt | None = Relationship()
    drug_label_id: int | None = Field(default=None, foreign_key="druglabel.id")
    drug_label: DrugLabel | None = Relationship()
    section: Literal["DI", "CO"] = Field(sa_column=Column(String))
    model: str
    temperature: float
    response: str
