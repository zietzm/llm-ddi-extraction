from sqlmodel import Session, SQLModel, create_engine, select

from undina_llm.models import DrugLabel, Prompt, Response, SystemPrompt


class SessionManager:
    def __init__(self, db_string: str):
        self.engine = create_engine(db_string)
        SQLModel.metadata.create_all(self.engine)

    def get_prompt(self, prompt: str) -> Prompt:
        with Session(self.engine) as session:
            return session.exec(select(Prompt).where(Prompt.prompt == prompt)).one()

    def get_system_prompt(self, system_prompt: str) -> SystemPrompt:
        with Session(self.engine) as session:
            return session.exec(
                select(SystemPrompt).where(SystemPrompt.prompt == system_prompt)
            ).one()

    def get_drug_label(self, drug_label: DrugLabel) -> DrugLabel:
        with Session(self.engine) as session:
            return session.exec(
                select(DrugLabel).where(
                    (DrugLabel.set_id == drug_label.set_id)
                    & (DrugLabel.label_id == drug_label.label_id)
                    & (DrugLabel.spl_version == drug_label.spl_version)
                )
            ).one()

    def get_response(self, response: Response) -> Response | None:
        with Session(self.engine) as session:
            return session.exec(
                select(Response).where(
                    (Response.prompt == response.prompt)
                    & (Response.drug_label == response.drug_label)
                    & (Response.system_prompt == response.system_prompt)
                )
            ).one_or_none()

    def register_prompt(self, prompt: str) -> Prompt:
        prompt_obj = Prompt(prompt=prompt)
        with Session(self.engine) as session:
            session.add(prompt_obj)
            session.commit()
            session.refresh(prompt_obj)
            return prompt_obj

    def register_system_prompt(self, system_prompt: str) -> SystemPrompt:
        system_prompt_obj = SystemPrompt(prompt=system_prompt)
        with Session(self.engine) as session:
            session.add(system_prompt_obj)
            session.commit()
            session.refresh(system_prompt_obj)
            return system_prompt_obj

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

    def register_response(self, response: Response) -> None:
        with Session(self.engine, expire_on_commit=False) as session:
            session.add(response)
            session.commit()
