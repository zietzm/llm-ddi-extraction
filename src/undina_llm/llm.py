from typing import Literal

from openai import OpenAI

from undina_llm.models import DrugLabel, Prompt, Response, SystemPrompt


def query(
    client: OpenAI,
    system_prompt: SystemPrompt,
    prompt: Prompt,
    drug_label: DrugLabel,
    section: Literal["DI", "CO"],
    model: str,
    temperature: float,
    seed: int,
) -> Response:
    """Query the LLM with the given prompts and drug label."""
    section_str = getattr(drug_label, section)
    raw_response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt.prompt},
            {"role": "user", "content": prompt.prompt.format(section_str)},
        ],
        model=model,
        temperature=temperature,
        seed=seed,
    )
    result_str = raw_response.choices[0].message.content
    assert isinstance(result_str, str)

    return Response(
        system_prompt=system_prompt,
        prompt=prompt,
        drug_label=drug_label,
        section=section,
        model=model,
        temperature=temperature,
        response=result_str,
    )
