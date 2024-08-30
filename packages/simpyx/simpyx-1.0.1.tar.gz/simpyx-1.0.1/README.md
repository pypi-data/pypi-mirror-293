# simpyx

Simulate RGB pixel control in a terminal.

## Installation

Install with pip

```bash
pip install simpyx
```

## Modules

- `pixels`: Create and show RGB pixel arrays.
- `shows`: Collection of programs to show off the simpyx library.
- `screen`: Manipulate a file (usually standard out) as a screen.

## Usage

`pixels.PixelDrawer` object is the primary interface for displaying an array of
pixels.

Can index and iterate as a normal python array. Intended to work (kinda)
similarly to
[adafruit-circuitpython-neopixel](https://pypi.org/project/adafruit-circuitpython-neopixel).

```python
with pixels.PixelDrawer(100) as pix_drawer:
    for p in pix_drawer:
        p.set_rgb(255, 0, 100)
    pix_drawer[30] = pixels.Pixel(0, 0, 0)
    pix_drawer.show()
```

### Typical Python usage

```python
import time
from simpyx import pixels
with pixels.PixelDrawer(100) as pix:
    delta = 255 / len(pix)
    while True:
        for i, p in enumerate(pix):
            p.set_rgb(100, 0, round((i + i) * delta)
            pix.show()
            time.sleep(0.05)
        pix.fill(0, 0, 0)
        pix.show()
```

## License
Licensed under the MIT license. See LICENSE file.
