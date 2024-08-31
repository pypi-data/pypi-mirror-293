import msvcrt
import os
import sys
from ctypes import c_ulong, pointer, windll
from ctypes.wintypes import DWORD, HANDLE
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import TYPE_CHECKING, Callable, List, Optional, TypeVar

from typing_extensions import ParamSpec

from latch_cli.click_utils import AnsiCodes

from . import common
from .win32_types import (
    INPUT_RECORD,
    KEY_EVENT_RECORD,
    MOUSE_EVENT_RECORD,
    STD_INPUT_HANDLE,
    EventTypes,
)

# assert sys.platform == "win32"

P = ParamSpec("P")
T = TypeVar("T")


def raw_input(f: Callable[P, T]) -> Callable[P, T]:
    # ayush: got most of this from
    # https://github.com/prompt-toolkit/python-prompt-toolkit/blob/669541123c9a72da1fda662cbd0a18ffe9e6d113/src/prompt_toolkit/input/win32.py
    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:

        original_mode = DWORD()
        handle = HANDLE(windll.kernel32.GetStdHandle(STD_INPUT_HANDLE))
        windll.kernel32.GetConsoleMode(handle, pointer(original_mode))

        enable_echo_input = 0x0004
        enable_line_input = 0x0002
        enable_processed_input = 0x0001

        windll.kernel32.SetConsoleMode(
            handle,
            original_mode.value
            & ~(enable_echo_input | enable_line_input | enable_processed_input),
        )

        try:
            return f(*args, **kwargs)
        finally:
            windll.kernel32.SetConsoleMode(handle, original_mode)

    return wrapper


class Special(Enum):
    left = "left"
    right = "right"
    up = "up"
    down = "down"
    enter = "enter"
    ctrlc = "ctrlc"
    ctrld = "ctrld"


@dataclass
class KeyInput:
    special: Optional[Special]
    value: str


# ignoring most things except for arrow keys / enter
def get_key_input() -> Optional[KeyInput]:
    # ayush:
    # https://github.com/prompt-toolkit/python-prompt-toolkit/blob/669541123c9a72da1fda662cbd0a18ffe9e6d113/src/prompt_toolkit/input/win32.py#L127
    handle: HANDLE
    if sys.stdin.isatty():
        handle = HANDLE(windll.kernel32.GetStdHandle(STD_INPUT_HANDLE))
    else:
        _fdcon = os.open("CONIN$", os.O_RDWR | os.O_BINARY)
        handle = HANDLE(msvcrt.get_osfhandle(_fdcon))

    max_count = 2048  # Max events to read at the same time.

    read = DWORD(0)
    arrtype = INPUT_RECORD * max_count
    input_records = arrtype()

    windll.kernel32.ReadConsoleInputW(
        handle, pointer(input_records), max_count, pointer(read)
    )

    for i in range(read.value):
        ir = input_records[i]

        if ir.EventType not in EventTypes:
            continue

        ev = getattr(ir.Event, EventTypes[ir.EventType])

        if not (isinstance(ev, KEY_EVENT_RECORD) and ev.KeyDown):
            continue

        u_char = ev.uChar.UnicodeChar

        special: Optional[Special] = None
        if u_char == "\x00":  # special keys, e.g. arrow keys
            if ev.VirtualKeyCode == 37:
                special = Special.left
            elif ev.VirtualKeyCode == 38:
                special = Special.up
            elif ev.VirtualKeyCode == 39:
                special = Special.right
            elif ev.VirtualKeyCode == 40:
                special = Special.down
        elif u_char == "\x0d":
            special = Special.enter
        elif u_char == "\x03":
            special = Special.ctrlc
        elif u_char == "\x04":
            special = Special.ctrld

        return KeyInput(special, u_char)


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
            k = get_key_input()
            if k is None:
                continue

            if k.special == Special.enter:
                return options[curr_selected]["value"]
            elif k.special == Special.up:  # Up Arrow
                curr_selected = max(curr_selected - 1, 0)
                if curr_selected - start_index < max_per_page // 2 and start_index > 0:
                    start_index -= 1
            elif k.special == Special.down:  # Down Arrow
                curr_selected = min(curr_selected + 1, len(options) - 1)
                if (
                    curr_selected - start_index > max_per_page // 2
                    and start_index < len(options) - max_per_page
                ):
                    start_index += 1
            elif k.special in {Special.ctrlc, Special.ctrld} or k.value in {"q", "Q"}:
                return
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
