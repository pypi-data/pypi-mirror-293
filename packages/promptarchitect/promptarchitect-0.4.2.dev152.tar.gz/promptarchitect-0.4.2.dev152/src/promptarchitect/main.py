from typing import Annotated

import typer

from promptarchitect.validation import TestSession
from promptarchitect.validation.core import SessionConfiguration

app = typer.Typer(rich_markup_mode=True)


@app.command()
def main(
    prompts: Annotated[str, typer.Option()],
    output: Annotated[str, typer.Option()],
    templates: Annotated[str, typer.Option()] = None,
    report_path: Annotated[str, typer.Option()] = "dashboard",
    report_format: Annotated[str, typer.Option()] = "html",
    report_theme: Annotated[str, typer.Option()] = "blue",
):
    """
    Create engineered prompts for higher quality LLM completions.
    """

    configuration = SessionConfiguration(
        prompt_path=prompts,
        template_path=templates,
        report_format=report_format,
        output_path=output,
        report_path=report_path,
        report_theme=report_theme,
    )

    session = TestSession(configuration)

    if session.start():
        return 0
    else:
        return 1


if __name__ == "__main__":
    app()
