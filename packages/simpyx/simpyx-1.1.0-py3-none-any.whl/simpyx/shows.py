# Copyright 2024 Josh Tompkin
# Licensed under the MIT license
"""Collection of programs to show off the simpyx library.

Typical usage example:
```python
with PixelDrawer(100) as pix_drawer:
    cycle(pix_drawer)
```
"""

from time import sleep

from . import pixels

# pyright: strict


def static(
    pixel_drawer: pixels.PixelDrawer, rgb: tuple[int, int, int], delay: float
) -> None:
    while True:
        pixel_drawer.fill(*rgb)
        pixel_drawer[3] = pixels.Pixel(100, 20, 255)
        pixel_drawer.show()
        sleep(delay)


def cycle(pixel_drawer: pixels.PixelDrawer, delay: float) -> None:
    delta = 255 / len(pixel_drawer)
    while True:
        pixel_drawer.redraw()
        for i, p in enumerate(pixel_drawer):
            p.set_rgb(round((i + 1) * delta), 0, 100)
            pixel_drawer.show()
            sleep(delay)
        pixel_drawer.fill(0, 0, 0)


def brightness(pixel_drawer: pixels.PixelDrawer, delay: float) -> None:
    delta = 1 / len(pixel_drawer)
    while True:
        pixel_drawer.redraw()
        pixel_drawer.fill(255, 0, 0)
        for i, p in enumerate(pixel_drawer):
            p.brightness = (i + 1) * delta
            pixel_drawer.show()
            sleep(delay)
