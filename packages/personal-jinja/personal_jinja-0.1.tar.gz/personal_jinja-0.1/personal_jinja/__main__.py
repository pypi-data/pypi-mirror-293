from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from jinja2 import Environment
import json
from pathlib import Path
import re
import sys
import time
from typing import (
    Any,
    Callable,
    cast,
    Mapping,
    Optional,
    Sequence,
    TextIO,
)


_OpenFile = Callable[[str], TextIO]


def _get_stdin(_: str) -> TextIO:
    return sys.stdin


def _get_stdout(_: str) -> TextIO:
    return sys.stdout


def _path_open(path: str) -> _OpenFile:
    return cast(_OpenFile, Path(path).open)


@dataclass
class Config:
    _open_source: _OpenFile
    _open_output: _OpenFile
    backup: Optional[Path]
    variables: Mapping[str, Any]

    def open_source(self) -> TextIO:
        return self._open_source("r")

    def open_output(self) -> TextIO:
        return self._open_output("w")

    @classmethod
    def from_args(cls, args: Sequence[str]) -> "Config":
        ns = _parse_args(args)
        source: _OpenFile
        output: _OpenFile
        backup: Optional[Path] = None

        if ns.file == "-":
            source = _get_stdin
            output = _get_stdout
        else:
            source = _path_open(ns.file)
            file_extended = (
                ns.file + time.strftime(ns.extension, time.localtime(time.time()))
            )
            if ns.reverse:
                output = _path_open(file_extended)
            else:
                output = source
                backup = Path(file_extended)

        if ns.output:
            if ns.output == "-":
                output = _get_stdout
            else:
                output = _path_open(ns.output)
            backup = None

        if ns.no_backup:
            backup = None

        variables = {}
        for definition in ns.variables:
            if "=" not in definition:
                raise ValueError(
                    " ".join([
                        f"Variable definition [{definition}] is illegal, as it is not",
                        "split by an = character.",
                    ])
                )
            name, value = definition.split("=", maxsplit=1)
            if not re.match(r"[a-zA-Z_][a-zA-Z0-9_]*$", name):
                raise ValueError(f"Variable name {name} is illegal.")
            variables[name] = json.loads(value)

        return Config(
            _open_source=source,
            _open_output=output,
            backup=backup,
            variables=variables,
        )


def _parse_args(args: Sequence[str]) -> Namespace:
    parser = ArgumentParser(
        description=" ".join([
            "Runs a file (or standard input) as a Jinja template, using the",
            "variable definitions provided at the command line. If a file is thus",
            "processed, it is rewritten with the result of rendering the template.",
        ])
    )
    parser.add_argument(
        "-f",
        "--file",
        default="-",
        help=" ".join([
            "File to render as a Jinja template.",
            "By default, or if the argument is `-', the template is read from",
            "standard input, and the rendered text is written to standard output."
        ])
    )
    parser.add_argument(
        "-x",
        "--extension",
        default=".%Y-%m-%d_%H.%M.%S",
        help=" ".join([
            "Extension appended to the name of the source file,",
            "where it is backed up ahead of the rendered template clobbering the",
            "source file. The strftime() templating %%-forms are substituted to",
            "form the final extension. Default value: .%%-%%m-%%d_%%H.%%M.%%S",
        ]),
    )
    parser.add_argument(
        "-o",
        "--output",
        help=" ".join([
            "Instead of clobbering the source file, the template is rendered",
            "to this file. If set to `-', template is rendered to standard output.",
            "The source file is not backed up, since it is not clobbered.",
        ])
    )
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        default=False,
        help=" ".join([
            "If this option is set, the opposite of the usual behaviour is",
            "realized: the template is rendered to a file named by appending an",
            "extension to the name of the source file. This only takes effect if a",
            "file is provided with option -f/--file, and if option -o/--output is",
            "not used. Note also that when using -r/--reverse, no backup of the",
            "source file is written, since it is never modified.",
        ])
    )
    parser.add_argument(
        "-n",
        "--no-backup",
        action="store_true",
        default=False,
        help=" ".join([
            "If this option is set and other settings are such that the source file",
            "would be backed up before it is clobbered by the template rendering,",
            "this backup step is skipped."
        ])
    )
    parser.add_argument(
        "variables",
        nargs="*",
        metavar="var=JSON",
        help=" ".join([
            "Definitions of JSON-valued `variables' that will be resolved during"
            "the rendering of the Jinja template. The variable names must satisfy"
            "Python identifier lexical rules, and the values must be valid JSON"
            "literals. In particular, string values must be double-quoted."
        ]),
    )
    return parser.parse_args(args)


def main():
    config = Config.from_args(sys.argv[1:])
    with config.open_source() as file_source:
        template = file_source.read()
    if config.backup:
        config.backup.write_bytes(template)

    output = Environment(
        block_start_string="<{",
        block_end_string="}>",
        variable_start_string="{{",
        variable_end_string="}}",
        line_statement_prefix=">>",
        comment_start_string="{#",
        comment_end_string="}",
        extensions=["jinja2.ext.do"]
    ).from_string(template).render(**config.variables)
    with config.open_output() as file_output:
        print(output, file=file_output)


if __name__ == '__main__':
    main()
