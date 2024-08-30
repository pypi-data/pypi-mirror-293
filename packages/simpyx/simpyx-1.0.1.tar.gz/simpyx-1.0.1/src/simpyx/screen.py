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
from types import TracebackType
from typing import Optional, TextIO, Type

# pyright: strict


class Screen:
    """A file that can be manipulated as a screen through escape sequences."""

    def __init__(self, file: TextIO = sys.stdout) -> None:
        """Initializes Screen

        Args:
            file: Object to open and manipulate.
        """
        self._file = file

    def clear(self):
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
            x: The 1 indexed x (column) position.
            y: The 1 indexed y (row) position
        """
        self._file.write(f"\x1b[{y};{x}H")

    def print_color(self, msg: str, r: int, g: int, b: int) -> None:
        """Print a message with RGB color to the screen.

        Args:
            msg: Message to print.
            r: Red color value, between 0 and 255.
            g: Green color value, between 0 and 255.
            b: Blue color value, between 0 and 255.
        """
        self._file.write(f"\x1b[38;2;{r};{g};{b}m{msg}")

    def print(self, msg: str) -> None:
        """Print a message to the screen.

        Args:
            msg: Message to print.
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
        self.flush()
        self.show_cursor()
        self._file.close()
        return False
