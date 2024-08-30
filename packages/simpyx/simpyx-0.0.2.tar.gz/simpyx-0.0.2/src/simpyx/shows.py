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

DELAY = 0.05


def static(pix: pixels.PixelDrawer) -> None:
    pix.fill(0, 255, 0)
    pix[3] = pixels.Pixel(100, 20, 255)
    pix.show()
    input()


def cycle(pix: pixels.PixelDrawer) -> None:
    delta = 255 / len(pix)
    while True:
        for i, p in enumerate(pix):
            p.set_rgb(round((i + 1) * delta), 0, 100)
            pix.show()
            sleep(DELAY)
        pix.fill(0, 0, 0)
        pix.show()


def brightness(pix: pixels.PixelDrawer) -> None:
    delta = 1 / len(pix)
    while True:
        pix.fill(255, 0, 0)
        pix.show()
        for i, p in enumerate(pix):
            p.brightness = (i + 1) * delta
            pix.show()
            sleep(DELAY)
