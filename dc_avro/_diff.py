import difflib
from typing import Sequence

from rich.table import Table


class TableDiff:
    def __init__(
        self,
        title: str,
        source_name: str,
        target_name: str,
        only_deltas: bool = False,
    ) -> None:
        """
        Class to create a table with the differences between two resources.

        Args:
            title (str): Table title
            source_name (str): source name
            target_name (str): target name
            only_deltas (bool, optional): Whether to include only deltas.
                If set to True then only deltas are included rather than the
                whole resource in the diff result. Default to False.
        """
        self.table = Table(title=title, highlight=True)
        self.table.add_column(source_name, style="cyan")
        self.table.add_column(target_name, style="magenta")
        self.content: list[str] = []
        self.only_deltas = only_deltas
        self.line_number = 1

    def add_content(self, content: str) -> None:
        """
        If the line starts with a "-" character, it is added to the left column.
        If the line starts with a "+" character, it is added to the right column.
        If the line starts with a space character, it is added to both columns.
        If the line starts with a "?" character, it is ignored.

        Args:
            content (str): new content to be added to the table
        """
        if content.startswith("?"):
            # Ignore the line
            self.line_number += 1
            return
        elif content.startswith(" "):
            if self.only_deltas:
                self.line_number += 1
                return
            content = f"{self.line_number} {content}"
            self.add_row(source_colum=content, target_column=content)
        else:
            # add the content to check later
            self.content.append(content)

        if len(self.content) == 2:
            # here we are in the situation where we have a complete row
            # the combination can be: ("-", "+"), ("-", "-") or ("+", "+")
            content_one, content_two = self.content

            if content_one.startswith("-") and content_two.startswith("+"):
                self.add_row(
                    source_colum=f"{self.line_number} {content_one}",
                    target_column=f"{self.line_number} {content_two}",
                )
            elif content_one.startswith("-") and content_two.startswith("-"):
                self.add_row(
                    source_colum=f"{self.line_number} {content_one}",
                    target_column=f"{self.line_number}",
                )
                self.add_row(
                    source_colum=f"{self.line_number} {content_two}",
                    target_column=f"{self.line_number}",
                )
            else:
                self.add_row(
                    source_colum=f"{self.line_number}",
                    target_column=f"{self.line_number} {content_one}",
                )
                self.add_row(
                    source_colum=f"{self.line_number}",
                    target_column=f"{self.line_number} {content_two}",
                )

            self.content = []

    def add_row(self, *, source_colum: str, target_column: str) -> None:
        """
        Add new row to table.
        """
        self.table.add_row(source_colum, target_column)
        self.line_number += 1


def diff_resources(
    *,
    source_resource: Sequence[str],
    target_resource: Sequence[str],
    source_name: str,
    target_name: str,
    only_deltas: bool = False,
) -> Table:
    table_diff = TableDiff(
        title="Schema Diff",
        source_name=source_name,
        target_name=target_name,
        only_deltas=only_deltas,
    )
    diff = difflib.ndiff(source_resource, target_resource)

    for line in diff:
        table_diff.add_content(line.replace("\n", "").replace("\t", ""))
    return table_diff.table
