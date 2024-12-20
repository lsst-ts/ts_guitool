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

import asyncio

import pytest
from lsst.ts.guitool import (
    ButtonStatus,
    get_config_dir,
    get_tol,
    read_yaml_file,
    run_command,
    update_boolean_indicator_status,
    update_button_color,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QRadioButton
from pytestqt.qtbot import QtBot


def command_normal(is_failed: bool) -> None:
    if is_failed:
        raise RuntimeError("Command is failed.")


async def command_coroutine(is_failed: bool) -> None:
    await asyncio.sleep(0.5)

    if is_failed:
        raise RuntimeError("Command is failed.")


def test_read_yaml_file_exception() -> None:
    with pytest.raises(IOError):
        read_yaml_file("no_this_yaml_file.yaml")


def test_read_yaml_file() -> None:
    yaml_file = get_config_dir("MTRotator/v2") / "default_gui.yaml"
    content = read_yaml_file(yaml_file)

    assert content["port"] == 5570


def test_get_config_dir() -> None:
    path = get_config_dir("MTRotator/v2")

    assert path.exists()
    assert path.name == "v2"


def test_get_tol() -> None:
    assert get_tol(1) == 0.1
    assert get_tol(2) == 0.01


@pytest.mark.asyncio
async def test_run_command(qtbot: QtBot) -> None:
    # Note that we need to add the "qtbot" here as the argument for the event
    # loop or GUI to run

    assert await run_command(command_normal, False) is True
    assert await run_command(command_normal, True, is_prompted=False) is False

    assert await run_command(command_coroutine, False) is True
    assert await run_command(command_coroutine, True, is_prompted=False) is False


def test_update_button_color() -> None:

    button = QRadioButton()

    colors = [Qt.gray, Qt.green, Qt.red, Qt.yellow]
    for status, color in zip(ButtonStatus, colors):
        update_button_color(button, QPalette.Base, status)

        assert button.palette().color(QPalette.Base) == color


def test_update_boolean_indicator_status() -> None:

    button = QRadioButton()

    # Error
    with pytest.raises(ValueError):
        update_boolean_indicator_status(button, False, is_fault=True, is_warning=True)

    # Not triggered
    update_boolean_indicator_status(button, False)
    assert button.palette().color(QPalette.Base) == Qt.gray

    update_boolean_indicator_status(button, False, is_default_error=True)
    assert button.palette().color(QPalette.Base) == Qt.red

    # Triggered
    update_boolean_indicator_status(button, True)
    assert button.palette().color(QPalette.Base) == Qt.green

    update_boolean_indicator_status(button, True, is_fault=True)
    assert button.palette().color(QPalette.Base) == Qt.red

    update_boolean_indicator_status(button, True, is_warning=True)
    assert button.palette().color(QPalette.Base) == Qt.yellow
