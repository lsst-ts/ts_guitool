# This file is part of ts_guitool.
#
# Developed for the LSST Telescope and Site Systems.
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

__all__ = ["ControlTabs"]

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout
from qasync import asyncSlot

from .tab_template import TabTemplate


class ControlTabs(object):
    """Control tables.

    Parameters
    ----------
    tabs : `list` [`TabTemplate`]
        List of the control tables.

    Attributes
    ----------
    layout : `PySide6.QtWidgets.QVBoxLayout`
        Layout.
    """

    def __init__(self, tabs: list[TabTemplate]) -> None:
        # List of the control tables
        self._tabs = tabs

        # Widget to have the list of control tables
        self._list_widget = self._create_list_widget()

        self.layout = self._set_layout()

    def _create_list_widget(self) -> QListWidget:
        """Create the list widget.

        Returns
        -------
        list_widget : `PySide6.QtWidgets.QListWidget`
            List widget.
        """

        list_widget = QListWidget()

        for tab in self._tabs:
            list_widget.addItem(tab.windowTitle())

        # Set the default selection
        list_widget.setCurrentRow(0)

        list_widget.setToolTip("Double click to open the table.")

        list_widget.itemDoubleClicked.connect(self._callback_show)

        return list_widget

    def _set_layout(self) -> QVBoxLayout:
        """Set the layout.

        Returns
        -------
        layout : `PySide6.QtWidgets.QVBoxLayout`
            Layout.
        """

        layout = QVBoxLayout()
        layout.addWidget(self._list_widget)

        return layout

    @asyncSlot()
    async def _callback_show(self, item: QListWidgetItem) -> None:
        """Callback function to show the selected table.

        Parameters
        ----------
        item : `PySide6.QtWidgets.QListWidgetItem`
            Current item.
        """

        control_tab = self._get_control_tab(item.text())

        if control_tab is not None:
            control_tab.show()

    def get_tab(self, name: str) -> tuple[QListWidgetItem | None, TabTemplate | None]:
        """Get the table.

        Parameters
        ----------
        name : `str`
            Name of the Table.

        Returns
        -------
        item : `PySide6.QtWidgets.QListWidgetItem` or None
            Table item object. None if nothing.
        control_tab : Child of `TabTemplate` or None
            Control table object. None if nothing.
        """

        try:
            item = self._list_widget.findItems(name, Qt.MatchExactly)[0]
            control_tab = self._get_control_tab(name)
            return item, control_tab

        except IndexError:
            return None, None

    def _get_control_tab(self, title: str) -> TabTemplate | None:
        """Get the control table.

        Parameters
        ----------
        title : `str`
            Title of the control table.

        Returns
        -------
        Child of `TabTemplate` or None
            Control table object. None if nothing.
        """
        for tab in self._tabs:
            if tab.windowTitle() == title:
                return tab

        return None
