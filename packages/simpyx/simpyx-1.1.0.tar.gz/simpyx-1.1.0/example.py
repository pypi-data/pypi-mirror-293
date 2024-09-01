#!/usr/bin/env python3
# Copyright 2024 Josh Tompkin
# Licensed under the MIT license

import argparse

from simpyx import shows, pixels


def _positive_int(s: str) -> int:
    if (arg := int(s)) < 1:
        raise argparse.ArgumentTypeError("must be an integer greater than 0")
    return arg


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Example script to demonstrate simulating neopixels using simpyx.",
    )
    parser.add_argument(
        "-n",
        type=_positive_int,
        metavar="int",
        default=100,
        help="Specify the number of pixels to simulate. (default 100)",
    )
    parser.add_argument(
        "-s",
        metavar="str",
        default="■ ",
        help='Specify the string to represent each pixel on the screen. (default "■ ")',
    )
    args = parser.parse_args(argv)
    try:
        with pixels.PixelDrawer(args.n, args.s) as pixel_drawer:
            shows.cycle(pixel_drawer, 0.03)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
