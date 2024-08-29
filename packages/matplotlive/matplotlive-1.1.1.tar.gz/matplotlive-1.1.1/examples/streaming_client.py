#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Stream sine waves from streaming_server.py to a live plot."""

import socket

try:
    import msgpack
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "This example needs msgpack: `conda install msgpack-python` "
        "or `pip install msgpack`"
    )

try:
    from loop_rate_limiters import RateLimiter
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "This example needs loop rate limiters: "
        "`[conda|pip] install loop-rate-limiters`"
    )

from matplotlive import LivePlot

OMEGA = 20.0  # Hz
TIMESTEP = 1e-2  # seconds
DURATION = 5.0  # duration of this example, in seconds


def prepare_plot():
    """Prepare a live plot to stream to."""
    plot = LivePlot(
        timestep=TIMESTEP,
        duration=1.0,
        ylim=(-1.5, 1.5),
        ylim_right=(-3.5, 3.5),
    )
    plot.add_left("sine", "b-")
    plot.left_axis.set_ylabel(r"$\sin(\omega t)$", color="b")
    plot.left_axis.tick_params(axis="y", labelcolor="b")
    plot.add_right("cosine", "g-")
    plot.right_axis.set_ylabel(r"$3 \cos(\omega t)$", color="g")
    plot.right_axis.tick_params(axis="y", labelcolor="g")
    plot.redraw()
    return plot


def main():
    """Main function of this example."""
    unpacker = msgpack.Unpacker(raw=False)
    rate = RateLimiter(frequency=1.0 / TIMESTEP)
    plot = prepare_plot()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect(("localhost", 4747))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(
            "Did you run `streaming_server.py` first?"
        )
    for i in range(int(DURATION / TIMESTEP)):
        server.send("get".encode("utf-8"))
        data = server.recv(4096)
        if not data:
            break
        unpacker.feed(data)
        for unpacked in unpacker:
            for key, value in unpacked.items():
                plot.send(key, value)
        plot.update()
        rate.sleep()
    server.close()


if __name__ == "__main__":
    main()
