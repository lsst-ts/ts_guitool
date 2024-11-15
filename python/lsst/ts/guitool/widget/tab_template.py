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

__all__ = ["TabTemplate"]

import types
import typing

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDockWidget, QLayout, QScrollArea, QWidget


class TabTemplate(QDockWidget):
    """Table template.

    Parameters
    ----------
    title : `str`
        Table's title.
    """

    def __init__(self, title: str) -> None:
        super().__init__()

        self.setWindowTitle(title)
        self.setWidget(QWidget())

        # Turn off the docker widget specific features
        # Because the code reuse in this project is mainly based on the
        # composition instead of inheritance in QT logic, these dock widget
        # features bring more troubles than the benifits.
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)

    def set_widget_and_layout(self, is_scrollable: bool = False) -> None:
        """Set the widget and layout.

        Parameters
        ----------
        is_scrollable : `bool`, optional
            Is is_scrollable or not. (the default is False)
        """

        widget = self.widget()
        widget.setLayout(self.create_layout())

        # Resize the dock to have a similar size of layout
        self.resize(widget.sizeHint())

        if is_scrollable:
            self.setWidget(self.set_widget_scrollable(widget, True))

    def create_layout(self) -> QLayout:
        """Create the layout.

        Returns
        -------
        layout : `PySide6.QtWidgets.QLayout`
            Layout.

        Raises
        ------
        `NotImplementedError`
            If the child class does not implement this function.
        """
        raise NotImplementedError("Child class should implemented this.")

    def set_widget_scrollable(self, widget: QWidget, is_resizable: bool) -> QScrollArea:
        """Set the widget to be scrollable.

        Parameters
        ----------
        widget : `PySide6.QtWidgets.QWidget`
            Widget.
        is_resizable : `bool`
            Is resizable or not.

        Returns
        -------
        scroll_area : `PySide6.QtWidgets.QScrollArea`
            Scrollable area.
        """

        scroll_area = QScrollArea()
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(is_resizable)

        return scroll_area

    def create_and_start_timer(
        self, callback_time_out: typing.Callable, duration: int
    ) -> QTimer:
        """Create and start the timer.

        Parameters
        ----------
        callback_time_out : `func`
            Callback function to handle the timeout. You may want to let the
            "callback_time_out" call the
            self.check_duration_and_restart_timer() to monitor the duration and
            restart the timer when the duration is changed.
        duration : `int`
            Duration to do the refresh in milliseconds.

        Returns
        -------
        timer : `PySide6.QtCore.QTimer`
            Timer.
        """

        timer = QTimer(self)
        timer.timeout.connect(callback_time_out)
        timer.start(duration)

        return timer

    def check_duration_and_restart_timer(self, timer: QTimer, duration: int) -> None:
        """Check the duration and restart the timer if the duration has been
        updated.

        Parameters
        ----------
        timer : `PySide6.QtCore.QTimer`
            Timer.
        duration : `int`
            Duration to do the refresh in milliseconds.
        """

        if timer.interval() != duration:
            timer.start(duration)

    async def __aenter__(self) -> QDockWidget:
        """This is an overridden function to support the asynchronous context
        manager."""
        return self

    async def __aexit__(
        self,
        type: typing.Type[BaseException] | None,
        value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        """This is an overridden function to support the asynchronous context
        manager.

        Raises
        ------
        `NotImplementedError`
            If the child class does not implement this function.
        """
        raise NotImplementedError("Child class should implemented this.")
