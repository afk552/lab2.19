#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import *
import click


@click.command()
@click.option("--pth", default=Path.cwd(), help="Директория", type=str)
@click.option("--level", default=-1, help="Уровень вложенности", type=int)
@click.option(
    "--option",
    default="1",
    help=(
        "1 - Показать файлы, папки и подпапки, "
        "2 - Показать папки и подпапки, "
        "3 - Показать только папки."
    ),
    type=int,
)
def tree(pth, level, option):
    print(f"{pth}")
    match option:
        case 1:
            contents = Path(pth).rglob("*")
        case 2:
            contents = Path(pth).glob("**")
        case 3:
            contents = Path(pth).glob("*/")
        case _:
            contents = []

    for path in contents:
        depth = len(path.relative_to(pth).parts)
        if depth <= level or level == -1:
            spacer = "-" * depth
            print(f">{spacer}{path.name}")


if __name__ == "__main__":
    tree()
