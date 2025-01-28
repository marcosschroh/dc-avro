import difflib
from dataclasses import dataclass
from enum import Enum
from typing import Dict, NamedTuple, Optional, Sequence

from rich.style import Style
from rich.table import Table
from rich.text import Text

DELETE_COLOR = "red"
ADD_COLOR = "green"


class DiffTypes(str, Enum):
    TABLE = "table"
    CONTEXT = "context"
    UNIFIED = "unified"


@dataclass
class Content:
    line_number: int
    sequence: str

    @property
    def diff_format(self) -> str:
        return f"{self.line_number} {self.sequence}".replace("\t", "").replace("\n", "")


class DiffLine(NamedTuple):
    content_one: Content
    content_two: Content
    has_diff: bool


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
        self.table.add_column(source_name)
        self.table.add_column(target_name)
        self.only_deltas = only_deltas

    def add_content(self, diff_line: DiffLine) -> None:
        """
        If diff_line has differences, add a new row to the table with
        the differences styles, othewrise add a new row without sytles
        """

        if diff_line.has_diff:
            self.add_row(
                source_colum=self.build_text(
                    text=diff_line.content_one.diff_format,
                    style={"color": DELETE_COLOR},
                ),
                target_column=self.build_text(
                    text=diff_line.content_two.diff_format,
                    style={"color": ADD_COLOR},
                ),
            )
        else:
            self.add_row(
                source_colum=self.build_text(
                    text=diff_line.content_one.diff_format,
                ),
                target_column=self.build_text(
                    text=diff_line.content_two.diff_format,
                ),
            )

    @staticmethod
    def build_text(text: str, style: Optional[Dict[str, str]] = None) -> Text:
        style = style or {}
        return Text(text=text, style=Style(**style))  # type: ignore

    def add_row(
        self, *, source_colum: Text, target_column: Text, style: Optional[str] = None
    ) -> None:
        """
        Add new row to table.
        """
        self.table.add_row(source_colum, target_column, style=style)


def unified_diff(
    *,
    source_resource: Sequence[str],
    target_resource: Sequence[str],
    source_name: str,
    target_name: str,
    only_deltas: bool = False,
    num_lines: int = 5,
) -> str:
    if only_deltas and num_lines >= 0:
        context_lines = num_lines
    else:
        # make sure to show all the diff
        context_lines = 10000000

    diff = difflib.unified_diff(
        source_resource,
        target_resource,
        fromfile=source_name,
        tofile=target_name,
        n=context_lines,
    )

    return "".join(diff)


def context_diff(
    *,
    source_resource: Sequence[str],
    target_resource: Sequence[str],
    source_name: str,
    target_name: str,
    only_deltas: bool = False,
    num_lines: int = 5,
) -> str:
    if only_deltas and num_lines >= 0:
        context_lines = num_lines
    else:
        # make sure to show all the diff
        context_lines = 10000000

    diff = difflib.context_diff(
        source_resource,
        target_resource,
        fromfile=source_name,
        tofile=target_name,
        n=context_lines,
    )

    return "".join(diff)


def table_diff(
    *,
    source_resource: Sequence[str],
    target_resource: Sequence[str],
    source_name: str,
    target_name: str,
    only_deltas: bool = False,
    num_lines: int = 5,
) -> Table:
    table_diff = TableDiff(
        title="Schema Diff",
        source_name=source_name,
        target_name=target_name,
    )

    if only_deltas and num_lines >= 0:
        context_lines = num_lines
    else:
        context_lines = None

    diff = difflib._mdiff(source_resource, target_resource, context=context_lines)  # type: ignore

    for line in diff:
        if None not in line:
            content_one, content_two, has_diff = line
            diff_line = DiffLine(
                content_one=Content(content_one[0], sequence=content_one[1]),
                content_two=Content(content_two[0], sequence=content_two[1]),
                has_diff=has_diff,
            )
            table_diff.add_content(diff_line=diff_line)
    return table_diff.table
