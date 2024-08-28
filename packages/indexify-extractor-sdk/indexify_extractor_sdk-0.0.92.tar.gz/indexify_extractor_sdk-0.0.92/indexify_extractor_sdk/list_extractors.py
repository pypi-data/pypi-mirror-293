from typing import Optional

from rich import print
from rich.console import Console
from rich.table import Table

from .utils import ExtractorIndex


def list_extractors(extractor_type: Optional[str] = None):
    extractors_index = ExtractorIndex()

    table = Table(title="[bold]Extractor List[/bold]", title_justify="left")

    print(
        "[bold yellow]Download Extractor:[/bold yellow] [red] indexify-extractor download <extractor_name>[/]"
    )
    print(
        "[bold yellow]Run Specific Extractor:[/bold yellow] [red] indexify-extractor join-server <module_name>[/]"
    )
    print(
        "[bold yellow]Run All Downloaded Extractors:[/bold yellow] [red] indexify-extractor join-server [/]"
    )

    table.add_column("Type", style="magenta")
    table.add_column("Name", style="orange3")

    for extractor in extractors_index.all_metadata().values():
        if extractor_type and extractor_type != extractor.get("type"):
            continue

        table.add_row(extractor.get("type"), extractor.get("name"))

    console = Console()
    console.print(table)
