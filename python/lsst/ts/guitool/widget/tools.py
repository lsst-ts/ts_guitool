# This file is part of ts_guitool.
#
# Developed for the Vera Rubin Observatory Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = ["connect_signal_to_future"]

import asyncio
import typing

from PySide6.QtCore import Signal


def connect_signal_to_future(signal: Signal, func: typing.Callable) -> asyncio.Future:
    """Connect the siganl to asyncio.Future() and execute the function.

    Parameters
    ----------
    signal : `PySide6.QtCore.Signal`
        Signal.
    func : `func`
        Function to execute.

    Returns
    -------
    future : `asyncio.Future`
        Future instance that represents an eventual result of an asynchronous
        operation.
    """

    future: asyncio.Future = asyncio.Future()
    signal.connect(lambda result: future.set_result(result))

    func()

    return future
