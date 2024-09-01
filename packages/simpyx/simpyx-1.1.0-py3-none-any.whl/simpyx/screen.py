# Copyright 2024 Josh Tompkin
# Licensed under the MIT license
"""Manipulate a file (usuaslly standard out) as a screen.

Will only work on terminals that respond to
[linux console escape sequences](https://www.man7.org/linux/man-pages/man4/console_codes.4.html).

Typical usage example:
```python
with Screen() as screen:
    screen.hide_cursor()
    screen.clear()
    screen.set_curor()
    screen.print_color("Hi, Mom!", 10, 100, 255)
```
"""

import sys
from shutil import get_terminal_size
from types import TracebackType
from typing import Optional, TextIO, Type

# pyright: strict


class Screen:
    """A file that can be manipulated as a screen through escape sequences."""

    def __init__(self, file: TextIO = sys.stdout) -> None:
        """Initializes Screen

        Args:
            file: (TextIO) Object to open and manipulate. (default sys.stdout)
        """
        self._file = file
        self.width, self.height = get_terminal_size()

    def update_size(self) -> None:
        self.width, self.height = get_terminal_size()

    def clear(self) -> None:
        """Write an escape sequence to clear the screen."""
        self._file.write("\x1b[2J")

    def hide_cursor(self) -> None:
        """Write an escape sequence to hide the cursor."""
        self._file.write("\x1b[?25l")

    def show_cursor(self) -> None:
        """Write an escape sequence to show the cursor."""
        self._file.write("\x1b[?25h")

    def set_cursor(self, x: int = 1, y: int = 1) -> None:
        """Write an escape sequence to set the cursor position.

        Args:
            x: (int) The 1 indexed x (column) position. (default 1)
            y: (int) The 1 indexed y (row) position. (default 1)
        """
        self._file.write(f"\x1b[{y};{x}H")

    def print_color(self, msg: str, r: int, g: int, b: int) -> None:
        """Print a message with RGB color to the screen.

        Args:
            msg: (str) Message to print.
            r: (int) Red color value, between 0 and 255.
            g: (int) Green color value, between 0 and 255.
            b: (int) Blue color value, between 0 and 255.
        """
        self._file.write(f"\x1b[38;2;{r};{g};{b}m{msg}")

    def print(self, msg: str) -> None:
        """Print a message to the screen.

        Args:
            msg: (str) Message to print.
        """
        self._file.write(msg)

    def flush(self) -> None:
        """Flush the file corresponding to the Screen."""
        self._file.flush()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        del exc_type, exc_value, exc_tb
        self.flush()
        self.show_cursor()
        self._file.close()
        return False
