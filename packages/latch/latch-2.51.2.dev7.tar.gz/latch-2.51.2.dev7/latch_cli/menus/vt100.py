import os
import sys
import termios
import tty
from functools import wraps
from typing import Callable, List, Optional, TypeVar

from typing_extensions import ParamSpec

from latch_cli.click_utils import AnsiCodes

from . import common

P = ParamSpec("P")
T = TypeVar("T")


def raw_input(f: Callable[P, T]) -> Callable[P, T]:
    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        old_settings = termios.tcgetattr(sys.stdin.fileno())
        tty.setraw(sys.stdin.fileno())

        try:
            return f(*args, **kwargs)
        finally:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, old_settings)

    return wrapper


def read_next_byte() -> bytes:
    b = sys.stdin.buffer.read(1)
    if b in (
        b"\x03",  # CTRL C
        b"\x04",  # CTRL D
        b"q",
        b"Q",
    ):
        raise KeyboardInterrupt
    return b


def read_bytes(num_bytes: int) -> bytes:
    if num_bytes < 0:
        raise ValueError(f"cannot read {num_bytes} bytes")
    result = b""
    for _ in range(num_bytes):
        result += read_next_byte()
    return result


@raw_input
def select_tui(
    title: str, options: List[common.SelectOption[T]], clear_terminal: bool = True
) -> Optional[T]:
    """
    Renders a terminal UI that allows users to select one of the options
    listed in `options`

    Args:
        title: The title of the selection window.
        options: A list of names for each of the options.
        clear_terminal: Whether or not to clear the entire terminal window
            before displaying - default False
    """

    if len(options) == 0:
        raise ValueError("No options given")

    def render(
        curr_selected: int,
        start_index: int = 0,
        max_per_page: int = 10,
        indent: str = "    ",
    ) -> int:
        if curr_selected < 0 or curr_selected >= len(options):
            curr_selected = 0

        print(title)
        common.line_down(2)

        num_lines_rendered = 4  # 4 "extra" lines for header + footer

        for i in range(start_index, start_index + max_per_page):
            if i >= len(options):
                break
            name = options[i]["display_name"]
            if i == curr_selected:
                color = AnsiCodes.color
                bold = AnsiCodes.bold
                reset = AnsiCodes.full_reset

                prefix = indent[:-2] + "> "

                print(f"{color}{bold}{prefix}{name}{reset}\x1b[1E")
            else:
                print(f"{indent}{name}\x1b[1E")
            num_lines_rendered += 1

        common.line_down(1)

        control_str = "[ARROW-KEYS] Navigate\t[ENTER] Select\t[Q] Quit"
        print(control_str)
        common.line_up(num_lines_rendered - 1)

        common.show()

        return num_lines_rendered

    curr_selected = 0
    start_index = 0
    _, term_height = os.get_terminal_size()
    common.remove_cursor()

    max_per_page = min(len(options), term_height - 4)

    if clear_terminal:
        common.clear_screen()
        common.move_cursor((0, 0))
    else:
        print("\n" * (max_per_page + 3))
        common.move_cursor_up(max_per_page + 4)

    num_lines_rendered = render(
        curr_selected,
        start_index=start_index,
        max_per_page=max_per_page,
    )

    try:
        while True:
            b = read_bytes(1)
            if b == b"\r":
                return options[curr_selected]["value"]
            elif b == b"\x1b":
                b = read_bytes(2)
                if b == b"[A":  # Up Arrow
                    curr_selected = max(curr_selected - 1, 0)
                    if (
                        curr_selected - start_index < max_per_page // 2
                        and start_index > 0
                    ):
                        start_index -= 1
                elif b == b"[B":  # Down Arrow
                    curr_selected = min(curr_selected + 1, len(options) - 1)
                    if (
                        curr_selected - start_index > max_per_page // 2
                        and start_index < len(options) - max_per_page
                    ):
                        start_index += 1
                else:
                    continue
            common.clear(num_lines_rendered)
            num_lines_rendered = render(
                curr_selected,
                start_index=start_index,
                max_per_page=max_per_page,
            )
    except KeyboardInterrupt:
        ...
    finally:
        common.clear(num_lines_rendered)
        common.reveal_cursor()
        common.show()
