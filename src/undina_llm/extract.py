from typing import Literal

from sqlmodel import Session, SQLModel, create_engine, select

from undina_llm.models import DrugLabel, Prompt, Response, SystemPrompt

SQLITE_FILE = "sqlite:///undina_llm.db"


class SessionManager:
    def __init__(self):
        self.engine = create_engine(SQLITE_FILE)
        SQLModel.metadata.create_all(self.engine)

    def get_prompt(self, prompt: str) -> Prompt:
        with Session(self.engine) as session:
            return session.exec(select(Prompt).where(Prompt.prompt == prompt)).one()

    def register_prompt(self, prompt: str) -> Prompt:
        prompt_obj = Prompt(prompt=prompt)
        with Session(self.engine) as session:
            session.add(prompt_obj)
            session.commit()
            session.refresh(prompt_obj)
            return prompt_obj

    def get_system_prompt(self, system_prompt: str) -> SystemPrompt:
        with Session(self.engine) as session:
            return session.exec(
                select(SystemPrompt).where(SystemPrompt.prompt == system_prompt)
            ).one()

    def register_system_prompt(self, system_prompt: str) -> SystemPrompt:
        system_prompt_obj = SystemPrompt(prompt=system_prompt)
        with Session(self.engine) as session:
            session.add(system_prompt_obj)
            session.commit()
            session.refresh(system_prompt_obj)
            return system_prompt_obj

    def get_drug_label(self, drug_label: DrugLabel) -> DrugLabel:
        with Session(self.engine) as session:
            return session.exec(
                select(DrugLabel).where(
                    (DrugLabel.set_id == drug_label.set_id)
                    & (DrugLabel.label_id == drug_label.label_id)
                    & (DrugLabel.spl_version == drug_label.spl_version)
                )
            ).one()

    def register_drug_label(self, drug_label: DrugLabel) -> DrugLabel:
        with Session(self.engine) as session:
            session.add(drug_label)
            session.commit()
            session.refresh(drug_label)
            return drug_label

    def register_drug_labels(self, drug_labels: list[DrugLabel]) -> list[DrugLabel]:
        with Session(self.engine) as session:
            for drug_label in drug_labels:
                session.add(drug_label)
            session.commit()
            for drug_label in drug_labels:
                session.refresh(drug_label)
            return drug_labels

    def register_response(
        self,
        system_prompt: SystemPrompt,
        prompt: Prompt,
        drug_label: DrugLabel,
        section: Literal["DI", "CO"],
        model: str,
        temperature: float,
        response: str,
    ) -> None:
        with Session(self.engine) as session:
            response_obj = Response(
                system_prompt=system_prompt,
                prompt=prompt,
                drug_label=drug_label,
                section=section,
                model=model,
                temperature=temperature,
                response=response,
            )
            session.add(response_obj)
            session.commit()
