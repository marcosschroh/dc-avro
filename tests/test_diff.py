import os
from typing import Callable

import pytest
from rich.table import Table

from dc_avro._diff import (
    ADD_COLOR,
    DELETE_COLOR,
    TableDiff,
    context_diff,
    table_diff,
    unified_diff,
)


@pytest.mark.parametrize(
    "content_one, content_two, expected_rows",
    (
        (
            [],
            [],
            (),  # empty resources
        ),
        (
            ["First line", "Second line"],
            [],
            (
                [
                    TableDiff.build_text(
                        text="1 \x00-First line\x01", style={"color": DELETE_COLOR}
                    ),
                    TableDiff.build_text(text=" ", style={"color": ADD_COLOR}),
                ],
                [
                    TableDiff.build_text(
                        text="2 \x00-Second line\x01", style={"color": DELETE_COLOR}
                    ),
                    TableDiff.build_text(text=" ", style={"color": ADD_COLOR}),
                ],
            ),  # only source resource
        ),
        (
            [],
            ["First line", "Second line"],
            (
                [
                    TableDiff.build_text(text=" ", style={"color": DELETE_COLOR}),
                    TableDiff.build_text(
                        text="1 \x00+First line\x01", style={"color": ADD_COLOR}
                    ),
                ],
                [
                    TableDiff.build_text(text=" ", style={"color": DELETE_COLOR}),
                    TableDiff.build_text(
                        text="2 \x00+Second line\x01", style={"color": ADD_COLOR}
                    ),
                ],
            ),  # only target resource
        ),
        (
            ["First line", "Second line"],
            ["First line", "Second line"],
            (
                [
                    TableDiff.build_text(text="1 First line"),
                    TableDiff.build_text(text="1 First line"),
                ],  # noqa: E501
                [
                    TableDiff.build_text(text="2 Second line"),
                    TableDiff.build_text(text="2 Second line"),
                ],
            ),  # same resources
        ),
        (
            ["First line", "Second line"],
            ["First line", ""],
            (
                [
                    TableDiff.build_text(text="1 First line"),
                    TableDiff.build_text(text="1 First line"),
                ],
                [
                    TableDiff.build_text(
                        text="2 \x00-Second line\x01", style={"color": DELETE_COLOR}
                    ),
                    TableDiff.build_text(
                        text="2 \x00+ \x01", style={"color": ADD_COLOR}
                    ),
                ],
            ),  # different resources
        ),
        (
            ["First line", ""],
            ["First line", "Second line"],
            (
                [
                    TableDiff.build_text(text="1 First line"),
                    TableDiff.build_text(text="1 First line"),
                ],
                [
                    TableDiff.build_text(text="2 \x00- \x01"),
                    TableDiff.build_text(
                        text="2 \x00+Second line\x01", style={"color": ADD_COLOR}
                    ),
                ],
            ),  # different resources
        ),
        (
            ["First line", "Second line"],
            ["Not related", "No clue line"],
            (
                [
                    TableDiff.build_text(
                        text="1 \x00-First line\x01", style={"color": DELETE_COLOR}
                    ),
                    TableDiff.build_text(
                        text="1 \x00+Not related\x01", style={"color": ADD_COLOR}
                    ),
                ],
                [
                    TableDiff.build_text(
                        text="2 \x00-Second line\x01", style={"color": DELETE_COLOR}
                    ),
                    TableDiff.build_text(
                        text="2 \x00+No clue line\x01", style={"color": ADD_COLOR}
                    ),
                ],
            ),  # completely different resources
        ),
    ),
)
def test_table_diff(
    content_one: list[str],
    content_two: list[str],
    expected_rows: tuple[list[str]],
    create_table: Callable[..., Table],
) -> None:
    source_resource = "Resource A"
    target_resource = "Resource B"
    table = create_table(
        title="Schema Diff",
        source_name=source_resource,
        target_name=target_resource,
        rows=expected_rows,
    )

    result = table_diff(
        source_resource=content_one,
        target_resource=content_two,
        source_name=source_resource,
        target_name=target_resource,
    )

    assert result.row_count == len(expected_rows)
    assert result.columns == table.columns


@pytest.mark.parametrize("only_deltas, total_rows", ((True, 26), (False, 69)))
def test_table_diff_with_and_without_deltas(
    only_deltas: bool, total_rows: int, schema_dir: str
) -> None:
    source_name = os.path.join(schema_dir, "example.avsc")
    target_name = os.path.join(schema_dir, "example_v2.avsc")

    with open(source_name, mode="r") as source, open(target_name, mode="r") as target:
        source_resource = source.readlines()
        target_resource = target.readlines()

    result = table_diff(
        source_resource=source_resource,
        target_resource=target_resource,
        source_name=source_name,
        target_name=target_name,
        only_deltas=only_deltas,
    )

    assert result.row_count == total_rows


@pytest.mark.parametrize(
    "content_one, content_two, expected_result",
    (
        (
            [],
            [],
            "",  # empty resources
        ),
        (
            ["First line", "Second line"],
            [],
            (
                "*** Resource A\n--- Resource B\n***************\n*** 1,2 ****\n"
                "- First line- Second line--- 0 ----\n"
            ),  # only source resource
        ),
        (
            [],
            ["First line", "Second line"],
            (
                "*** Resource A\n--- Resource B\n***************\n*** 0 ****\n"
                "--- 1,2 ----\n+ First line+ Second line"
            ),  # only target resource
        ),
        (
            ["First line", "Second line"],
            ["First line", "Second line"],
            "",  # same resources
        ),
        (
            ["First line", "Second line"],
            ["First line", ""],
            (
                "*** Resource A\n--- Resource B\n***************\n*** 1,2 ****\n  "
                "First line! Second line--- 1,2 ----\n  First line! "
            ),  # different resources
        ),
        (
            ["First line", ""],
            ["First line", "Second line"],
            (
                "*** Resource A\n--- Resource B\n***************\n*** 1,2 ****\n  "
                "First line! --- 1,2 ----\n  First line! Second line"
            ),  # different resources
        ),
        (
            ["First line", "Second line"],
            ["Not related", "No clue line"],
            (
                "*** Resource A\n--- Resource B\n***************\n*** 1,2 ****\n! "
                "First line! Second line--- 1,2 ----\n! Not related! No clue line"
            ),  # completely different resources
        ),
    ),
)
def test_context_diff(
    content_one: list[str],
    content_two: list[str],
    expected_result: str,
) -> None:
    source_resource = "Resource A"
    target_resource = "Resource B"

    assert expected_result == context_diff(
        source_resource=content_one,
        target_resource=content_two,
        source_name=source_resource,
        target_name=target_resource,
    )


@pytest.mark.parametrize(
    "content_one, content_two, expected_result",
    (
        (
            [],
            [],
            "",  # empty resources
        ),
        (
            ["First line", "Second line"],
            [],
            "--- Resource A\n+++ Resource B\n@@ -1,2 +0,0 @@\n-First line-Second line",
            # only source resource
        ),
        (
            [],
            ["First line", "Second line"],
            "--- Resource A\n+++ Resource B\n@@ -0,0 +1,2 @@\n+First line+Second line",
            # only target resource
        ),
        (
            ["First line", "Second line"],
            ["First line", "Second line"],
            "",  # same resources
        ),
        (
            ["First line", "Second line"],
            ["First line", ""],
            "--- Resource A\n+++ Resource B\n@@ -1,2 +1,2 @@\n First line-Second line+",
            # different resources
        ),
        (
            ["First line", ""],
            ["First line", "Second line"],
            "--- Resource A\n+++ Resource B\n@@ -1,2 +1,2 @@\n First line-+Second line",
            # different resources
        ),
        (
            ["First line", "Second line"],
            ["Not related", "No clue line"],
            (
                "--- Resource A\n+++ Resource B\n@@ -1,2 +1,2 @@\n-First line-Second "
                "line+Not related+No clue line"
            ),
            # completely different resources
        ),
    ),
)
def test_unified_diff(
    content_one: list[str],
    content_two: list[str],
    expected_result: str,
) -> None:
    source_resource = "Resource A"
    target_resource = "Resource B"

    assert expected_result == unified_diff(
        source_resource=content_one,
        target_resource=content_two,
        source_name=source_resource,
        target_name=target_resource,
    )
