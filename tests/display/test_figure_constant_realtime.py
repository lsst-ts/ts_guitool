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
from lsst.ts.guitool.display import FigureConstant
from pytestqt.qtbot import QtBot


@pytest.fixture
def widget(qtbot: QtBot) -> FigureConstant:
    widget = FigureConstant(
        2,
        5,
        10,
        "title_x",
        "title_y",
        "title_figure",
        ["text_legend_1", "text_legend_2"],
        num_lines=2,
        is_realtime=True,
    )
    qtbot.addWidget(widget)

    return widget


def test_update_data_exception(widget: FigureConstant) -> None:
    data = range(0, 11)

    with pytest.raises(RuntimeError):
        widget.update_data(data, data)


def test_append_data(widget: FigureConstant) -> None:
    # Check the update of y-axis
    widget.append_data(-20, idx=0)

    assert widget.get_series(0).count() == 1
    assert widget.axis_y.min() == -22.0
    assert widget.axis_y.max() == 2.0

    assert widget._counter_realtime == 1

    widget.append_data(20, idx=1)

    assert widget.get_series(1).count() == 1
    assert widget.axis_y.min() == -24.0
    assert widget.axis_y.max() == 24.0

    # Check the y-axis will be adjusted
    for counter in range(25):
        widget.append_data(24, idx=0)

    assert widget._counter_realtime == 7
    assert widget.axis_y.min() == 19.6
    assert widget.axis_y.max() == 24.4


def test_append_point(widget: FigureConstant) -> None:
    # No point yet
    points = widget.get_points(0)
    widget._append_point(points, 1)

    assert len(points) == 1
    assert points[0].x() == 0
    assert points[0].y() == 1

    # Add more points
    for idx in range(1, widget._num_points):
        widget._append_point(points, idx + 1)

        assert len(points) == (idx + 1)
        assert points[-1].x() == idx
        assert points[-1].y() == (idx + 1)

    # Points are full
    widget._append_point(points, 999)

    assert len(points) == widget._num_points

    assert points[-1].x() == widget._num_points
    assert points[-1].y() == 999
