# Copyright 2024 Josh Tompkin
# Licensed under the MIT license
"""Create and show RGB pixel arrays.

Typical usage example:
```python
    with PixelDrawer(60) as pix:
        pix.fill(Pixel(100, 0, 255))
        pix[4] = Pixel(255, 255, 255)
        pix.show()
```
"""

from types import TracebackType
from typing import Generator, Optional, Type

from .screen import Screen

# pyright: strict


class Pixel:
    """Represents a single Pixel with RGB color and brightness.

    Attributes:
        changed: (bool) Indicates whether or not the Pixel has been modified
            since last showing. Should be set to `False` manually when shown.
    """

    def __init__(self, r: int, g: int, b: int, brightness: float = 1) -> None:
        """Initializes Pixel.

        Args:
            r: (int) Red color value, between 0 and 255.
            g: (int) Green color value, between 0 and 255.
            b: (int) Blue color value, between 0 and 255.
            brightness: (float) Pixel brightness as a proportion, between 0 and
                1. (default 1)
        """
        self._r, self._g, self._b = (r, g, b)
        self._brightness: float = brightness
        self.changed = True

    @property
    def brightness(self) -> float:
        """Pixel brightness as a proportion."""
        return self._brightness

    @brightness.setter
    def brightness(self, f: float) -> None:
        self.changed = True
        self._brightness = f
        assert (
            self.brightness >= 0
        ), "brightnesss must be greater than or equal to zero"

    def get_rgb(self) -> tuple[int, int, int]:
        """Get the RGB representation of the pixel.

        Returns:
            (tuple[int, int, int]) RGB values of the pixel.
        """
        return (
            round(self._r * self.brightness),
            round(self._g * self.brightness),
            round(self._b * self.brightness),
        )

    def set_rgb(self, r: int, g: int, b: int) -> None:
        """set_rgb sets the RGB values of the Pixel.

        Args:
            r: (int) Red color value, between 0 and 255.
            g: (int) Green color value, between 0 and 255.
            b: (int) Blue color value, between 0 and 255.
        """
        self._r, self._g, self._b = (r, g, b)
        self.changed = True

    def __repr__(self) -> str:
        return f"Color({self._r}, {self._g}, {self._b})"

    def __str__(self) -> str:
        return str((self._r, self._g, self._b))


class PixelDrawer:
    """PixelDrawer contains methods to draw a Pixel array to the Screen.

    The Pixel array may be accessed by indexing the PixelDrawer object.
    PixelDrawer should be opened in a context manager to ensure the Screen is
    closed properly.
    """

    def __init__(
        self,
        n: int,
        pixel_str: str = "■ ",
        header: str = "[ ",
        footer: str = " ]",
        screen: Optional[Screen] = None,
    ) -> None:
        """Initializes PixelDrawer.

        Args:
            n: (int) Number of Pixels in the array.
            pixel_str: (str) Representation of each Pixel. Will get funky if
                more than 1 character. (default "■")
            header: (str) This will be drawn before the Pixel array.
                (default "[ ")
            footer: (str) This will be drawn after the Pixel array.
                (default "]")
            screen: (Screen | None) Object to draw Pixels onto.
                (default `None`)
        """
        self._pix_str = pixel_str
        self._header = header
        self._footer = footer
        self._pixel_array = [Pixel(0, 0, 0) for _ in range(n)]

        if screen is None:
            screen = Screen().__enter__()
        self._screen = screen
        self._screen.hide_cursor()
        self.width = 0
        self.redraw()

    @property
    def pix_str(self) -> str:
        """Representation of each Pixel in the array."""
        return self._pix_str

    @pix_str.setter
    def pix_str(self, s: str) -> None:
        self._pix_str = s
        self.redraw()

    @property
    def header(self) -> str:
        """Prints before the Pixel array."""
        return self._header

    @header.setter
    def header(self, s: str) -> None:
        self._header = s
        self.redraw()

    @property
    def footer(self) -> str:
        """Prints after the Pixel array."""
        return self._footer

    @footer.setter
    def footer(self, s: str) -> None:
        self._footer = s
        self.redraw()

    def redraw(self) -> None:
        """Clear the screen, update its size, and print the header and footer"""
        self._screen.clear()
        self._screen.update_size()
        self._screen.set_cursor()
        self._screen.print_color(self._header, 220, 220, 220)
        self.width = self._screen.width - len(self._pix_str) + 1
        x = len(self) * len(self._pix_str) + len(self._header)
        self._screen.set_cursor(x % self.width + 1, x // self.width + 1)
        self._screen.print(self.footer)

    def fill(self, r: int, g: int, b: int, brightness: float = 1) -> None:
        """Set every Pixel in the array.

        Args:
            r: (int) Red color value, between 0 and 255.
            g: (int) Green color value, between 0 and 255.
            b: (int) Blue color value, between 0 and 255.
            brightness: (float) Pixel brightness as a proportion, between 0 and
                1.
        """
        for p in self._pixel_array:
            p.set_rgb(r, g, b)
            p.brightness = brightness

    def show(self) -> None:
        """Print the Pixel array to the Screen."""
        for i, p in enumerate(self._pixel_array):
            if p.changed:
                x = i * len(self._pix_str) + len(self._header)
                self._screen.set_cursor(x % self.width + 1, x // self.width + 1)
                self._screen.print_color(self._pix_str, *p.get_rgb())
                p.changed = False
        self._screen.flush()

    def __getitem__(self, i: int) -> Pixel:
        return self._pixel_array[i]

    def __setitem__(self, i: int, pixel: Pixel) -> None:
        self._pixel_array[i] = pixel

    def __iter__(self) -> Generator[Pixel, None, None]:
        i = 0
        while i < len(self._pixel_array):
            yield self._pixel_array[i]
            i += 1

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        return self._screen.__exit__(exc_type, exc_value, exc_tb)

    def __len__(self) -> int:
        return len(self._pixel_array)

    def __repr__(self) -> str:
        return f"Pixels({len(self)}, {self._pix_str} ,{self._header}, {self._footer})"

    def __str__(self) -> str:
        return str(self._pixel_array)
