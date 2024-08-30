import dataclasses
import json
import re
import sys
from typing import Annotated, Any, Optional

import rich
import rich.theme
import typer

app = typer.Typer(add_completion=False)

CUSTOM_THEME = rich.theme.Theme(
    {
        "time": "bright_black",
        "prefix": "cyan",
        "debug": "blue",
        "trace": "blue",
        "info": "green",
        "warning": "yellow",
        "error": "red",
        "std": "white",
    }
)


@dataclasses.dataclass
class Line:
    time: str
    prefix: str | None
    level: str
    msg: str
    fields: dict[str, str]


def parse_line(line) -> Line:
    # Define the pattern to match key-value pairs
    pattern = re.compile(r'(\w+)=(\[.*?\]|".*?"|\S+)')

    # Find all matches in the line
    matches = pattern.findall(line)

    # Iterate over each match
    items = {(match[0] or match[2]): match[1] or match[3] for match in matches}

    time = items.pop("time")
    prefix = items.pop("prefix", None)
    level = items.pop("level")
    msg = items.pop("msg")

    return Line(time=time, prefix=prefix, level=level, msg=msg, fields=items)


def version_callback(value: bool):
    if value:
        print("Version 0.2.1")
        raise typer.Exit()


def parse_txt():
    console = rich.console.Console(theme=CUSTOM_THEME)
    for line in sys.stdin:
        try:
            parsed = parse_line(line)

            fields = (
                f"[{parsed.level}]{key}[/{parsed.level}]=[std]{value}[/std]"
                for key, value in parsed.fields.items()
            )

            msg = (
                f"[time][{parsed.time}][/time]  "
                f"[{parsed.level}]{parsed.level.upper()}[/{parsed.level}] "
                f"[prefix]{parsed.prefix}:[/prefix] "
                f"{parsed.msg} "
                f"{' '.join(fields)}"
            )

            console.print(msg)

        except Exception:
            # If exception, just print the line.
            print(line)


def parse_json():
    console = rich.console.Console(theme=CUSTOM_THEME)

    for line in sys.stdin:
        try:
            parsed: dict[str, Any] = json.loads(line)

            time: str = parsed.pop("time")
            time = time.replace("T", " ").replace("Z", "")
            level = parsed.pop("level")
            prefix = parsed.pop("prefix", None)
            msg = parsed.pop("msg")

            for key, value in parsed.items():
                if (
                    "duration" in key.lower()
                    or "time" in key.lower()
                    or "elapsed" in key.lower()
                ):
                    try:
                        parsed[key] = f"{int(value)/1_000_000_000:.6f}s"
                    except ValueError:
                        pass

            fields = (
                f"[{level}]{key}[/{level}]=[std]{value}[/std]"
                for key, value in parsed.items()
            )

            msg = (
                f"[time][{time}][/time]  "
                f"[{level}]{level.upper()}[/{level}] "
                f"[prefix]{prefix}:[/prefix] "
                f"{msg} "
                f"{' '.join(fields)}"
            )

            console.print(msg)
        except Exception:
            # If exception, just print the line.
            print(line)


@app.command()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", callback=version_callback, help="Show version info and exit."
        ),
    ] = None,
    json: Annotated[bool, typer.Option(help="Input as JSON.")] = False,
):
    (parse_json if json else parse_txt)()
