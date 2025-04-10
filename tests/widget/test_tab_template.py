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

import pytest
from lsst.ts.guitool.widget import TabTemplate
from PySide6.QtWidgets import QScrollArea, QWidget
from pytestqt.qtbot import QtBot


@pytest.fixture
def widget(qtbot: QtBot) -> TabTemplate:
    widget = TabTemplate("Default")
    qtbot.addWidget(widget)

    return widget


def test_init(widget: TabTemplate) -> None:
    assert widget.windowTitle() == "Default"


def test_set_widget_scrollable(widget: TabTemplate) -> None:
    scroll_area = widget.set_widget_scrollable(QWidget(), False)
    assert type(scroll_area) is QScrollArea
    assert scroll_area.widgetResizable() is False

    scroll_area_resizable = widget.set_widget_scrollable(QWidget(), True)
    assert scroll_area_resizable.widgetResizable() is True


def test_create_and_start_timer(widget: TabTemplate) -> None:
    duration = 100
    timer = widget.create_and_start_timer(_callback_time_out, duration)

    assert timer.interval() == duration
    assert timer.isActive() is True


def _callback_time_out() -> None:
    pass


def test_check_duration_and_restart_timer(widget: TabTemplate) -> None:
    timer = widget.create_and_start_timer(_callback_time_out, 100)

    duration = 1000
    widget.check_duration_and_restart_timer(timer, duration)

    assert timer.interval() == duration
    assert timer.isActive() is True
