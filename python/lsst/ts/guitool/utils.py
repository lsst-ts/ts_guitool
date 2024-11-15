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

__all__ = [
    "is_coroutine",
    "set_button",
    "create_grid_layout_buttons",
    "create_label",
    "create_group_box",
    "create_table",
    "get_tol",
    "prompt_dialog_critical",
    "prompt_dialog_warning",
    "run_command",
    "get_button_action",
    "get_checked_buttons",
    "base_frame_run_application",
]

import asyncio
import os
import sys
import typing
from functools import partial

import qasync
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QPalette
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QTableWidget,
    QToolBar,
)

from .widget import QMessageBoxAsync


def is_coroutine(function: typing.Any) -> bool:
    """Input function is a coroution or not.

    Parameters
    ----------
    function : `func`, `coroutine`, `asyncio.Task`, or `asyncio.Future`
        Function.

    Returns
    -------
    `bool`
        True if the function is a corountine. Otherwise, False.
    """
    return asyncio.iscoroutine(function) or asyncio.iscoroutinefunction(function)


def set_button(
    name: str,
    callback: typing.Callable | None,
    *args: typing.Any,
    is_checkable: bool = False,
    is_indicator: bool = False,
    is_adjust_size: bool = False,
    tool_tip: str | None = None,
) -> QPushButton:
    """Set the button.

    Parameters
    ----------
    name : `str`
        Button name.
    callback : `func` or None
        Callback function object to use in future partial calls. Put None
        if you do not want to have the callback function connected.
    *args : `args`
        Tuple of callback arguments to future partial calls. This is only
        meaningful if the callback is not None.
    is_checkable : `bool`, optional
        The button is checkable or not. (the default is False)
    is_indicator : `bool`, optional
        The button is indicator or not. Put the callback to be None if the
        value is True. (the default is False)
    is_adjust_size : `bool`, optional
        Adjust the size of button or not. (the default is False)
    tool_tip : `str` or None, optional
        Tool tip. If None, there will be no tip. (the default is None)

    Returns
    -------
    button : `PySide6.QtWidgets.QPushButton`
        button.
    """

    button = QPushButton(name)
    if is_checkable:
        button.setCheckable(is_checkable)

    if callback is not None:
        button.clicked.connect(partial(callback, *args))

    if is_indicator:
        button.setEnabled(False)
        button.setAutoFillBackground(True)

        palette = button.palette()
        palette.setColor(QPalette.ButtonText, Qt.black)

        button.setPalette(palette)

    if is_adjust_size:
        button.adjustSize()

    if tool_tip is not None:
        button.setToolTip(tool_tip)

    return button


def create_grid_layout_buttons(
    buttons: dict[str, QPushButton] | list[QPushButton], num_column: int
) -> QGridLayout:
    """Create the grid layout of buttons.

    Parameters
    ----------
    buttons : `dict` or `list`
        Buttons to put on the grid layout.
    num_column : `int`
        Number of column on the grid layput.

    Returns
    -------
    layout : `PySide6.QtWidgets.QGridLayout`
        Grid layout of buttons.
    """

    # Use the list in the following
    if isinstance(buttons, dict):
        items = list(buttons.values())
    else:
        items = buttons

    # Add the item to the layout
    layout = QGridLayout()

    column = 0
    row = 0
    for item in items:
        layout.addWidget(item, row, column)

        column += 1
        if column >= num_column:
            column = 0
            row += 1

    return layout


def create_label(
    name: str = "",
    tool_tip: str = "",
    point_size: int | None = None,
    is_bold: bool = False,
) -> QLabel:
    """Create the label.

    Parameters
    ----------
    name : `str`, optional
        Label name. (the default is "")
    tool_tip : `str`, optional
        Tool tip. (the default is "")
    point_size : `int` or None, optional
        Point size of label. The value should be greater than 0. Put None if
        use the system default. (the default is None)
    is_bold : `bool`
        Is the bold format or not. (the default is False)

    Returns
    -------
    label : `PySide6.QtWidgets.QLabel`
        label.
    """
    label = QLabel(name)

    # Set the tool tip
    if tool_tip != "":
        label.setToolTip(tool_tip)

    # Set the specific font
    font = label.font()

    if point_size is not None:
        font.setPointSize(point_size)

    if is_bold:
        font.setBold(True)

    label.setFont(font)

    return label


def create_group_box(name: str, layout: QtWidgets) -> QGroupBox:
    """Create the group box.

    Parameters
    ----------
    name : `str`
        Name of the group box.
    layout : Layout in `PySide6.QtWidgets`
        Layout.

    Returns
    -------
    group_box : `PySide6.QtWidgets.QGroupBox`
        Group box.
    """

    group_box = QGroupBox(name)
    group_box.setLayout(layout)

    return group_box


def create_table(
    header_text: list[str], is_disabled_selection: bool = False
) -> QTableWidget:
    """Create the table.

    Parameters
    ----------
    header_text : `list`
        Text of the header.
    is_disabled_selection : `bool`, optional
        The selection is disabled or not. (the default is False)

    Returns
    -------
    table : `PySide6.QtWidgets.QTableWidget`
        Table.
    """

    table = QTableWidget()

    table.setColumnCount(len(header_text))
    table.setHorizontalHeaderLabels(header_text)

    if is_disabled_selection:
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setFocusPolicy(Qt.NoFocus)
        table.setSelectionMode(QTableWidget.NoSelection)

    return table


def get_tol(num_digit_after_decimal: int) -> float:
    """Get the tolerance.

    Parameters
    ----------
    num_digit_after_decimal : `int`
        Number of digits after the decimal. This should be greater than 0.

    Returns
    -------
    `float`
        Tolerance.
    """

    return 10 ** -int(num_digit_after_decimal)


async def __prompt_dialog(
    title: str, description: str, icon: int, is_prompted: bool = True
) -> None:
    """Shows a warning dialog.

    The user must react to this dialog. The rest of the GUI is blocked until
    the dialog is dismissed.

    Parameters
    ----------
    title : `str`
        Title of the dialog.
    description : `str`
        Description message to be shown in the dialog.
    icon : `int`
        QMessageBox icon id (Warning, Critical, etc.) to be shown with the
        message.
    is_prompted : `bool`, optional
        When False, dialog will not be executed. That is used for tests, which
        shall not be the case when used in the real GUI. (the default is True)
    """

    dialog = QMessageBoxAsync()
    dialog.setIcon(icon)
    dialog.setWindowTitle(title)
    dialog.setText(description)

    # Block the user to interact with other running widgets
    dialog.setModal(True)

    if is_prompted:
        await dialog.show()


async def prompt_dialog_critical(
    title: str, description: str, is_prompted: bool = True
) -> None:
    """Shows a critical dialog.

    The user must react to this dialog. The rest of the GUI is blocked until
    the dialog is dismissed.

    Parameters
    ----------
    title : `str`
        Title of the dialog.
    description : `str`
        Description message to be shown in the dialog.
    is_prompted : `bool`, optional
        When False, dialog will not be executed. That is used for tests, which
        shall not be the case when used in the real GUI. (the default is True)
    """
    await __prompt_dialog(title, description, QMessageBoxAsync.Critical, is_prompted)


async def prompt_dialog_warning(
    title: str, description: str, is_prompted: bool = True
) -> None:
    """Shows a warning dialog.

    The user must react to this dialog. The rest of the GUI is blocked until
    the dialog is dismissed.

    Parameters
    ----------
    title : `str`
        Title of the dialog.
    description : `str`
        Description message to be shown in the dialog.
    is_prompted : `bool`, optional
        When False, dialog will not be executed. That is used for tests, which
        shall not be the case when used in the real GUI. (the default is True)
    """
    await __prompt_dialog(title, description, QMessageBoxAsync.Warning, is_prompted)


async def run_command(
    command: typing.Callable | typing.Coroutine,
    *args: typing.Any,
    is_prompted: bool = True,
    **kwargs: dict[str, typing.Any],
) -> bool:
    """Run the command, which can be a normal function or a coroutine.

    If the command fails and is_prompted is True, a dialog to warn the users
    will appear/pop up.

    Parameters
    ----------
    command : `func` or `coroutine`
        Command to execute.
    *args : `args`
        Arguments of the command.
    is_prompted : `bool`, optional
        When False, dialog will not be executed. That is used for tests, which
        shall not be the case when used in the real GUI. (the default is True)
    **kwargs : `dict`, optional
        Additional keyword arguments to run the command.

    Returns
    -------
    `bool`
        True if the command succeeds. Otherwise, False.
    """

    try:
        if is_coroutine(command):
            await command(*args, **kwargs)  # type: ignore[operator]
        else:
            command(*args, **kwargs)  # type: ignore[operator]
    except Exception as error:
        await prompt_dialog_warning(
            f"{command.__name__}()", str(error), is_prompted=is_prompted
        )

        return False

    return True


def get_button_action(tool_bar: QToolBar, name: str) -> QAction:
    """Get the button widget of action in tool bar.

    Parameters
    ----------
    tool_bar : `PySide6.QtWidgets.QToolBar`
        Tool bar.
    name : `str`
        Action name.

    Returns
    -------
    `PySide6.QtWidgets.QAction` or None
        Button widget of the action. None if does not exist.
    """

    actions = tool_bar.actions()
    for action in actions:
        if action.text() == name:
            return tool_bar.widgetForAction(action)

    return None


def get_checked_buttons(buttons: list[QPushButton]) -> list[int]:
    """Get the checked buttons.

    Parameters
    ----------
    buttons : `list`
        Buttons.

    Returns
    -------
    `list`
        Indexes of the checked buttons.
    """

    return [idx for idx, button in enumerate(buttons) if button.isChecked()]


def base_frame_run_application(main: typing.Coroutine) -> None:
    """Base frame to run the application.

    Parameters
    ----------
    main : `asyncio.coroutine`
        Main application. This function should have an input argument to accept
        the command line arguments as a list.
    """

    if "QT_API" not in os.environ:
        os.environ.setdefault("QT_API", "PySide6")
        print("qasync: QT_API not set, defaulting to PySide6.")

    # Workaround the Python 3.11 issue in 'qasync' module based on:
    # https://github.com/CabbageDevelopment/qasync/issues/68
    if (sys.version_info.major == 3) and (sys.version_info.minor >= 11):
        with qasync._set_event_loop_policy(qasync.DefaultQEventLoopPolicy()):
            runner = asyncio.runners.Runner()

            try:
                runner.run(main(sys.argv))  # type: ignore[operator]

            except asyncio.exceptions.CancelledError:
                sys.exit(0)

            finally:
                runner.close()
    else:
        try:
            qasync.run(main(sys.argv))  # type: ignore[operator]
        except asyncio.exceptions.CancelledError:
            sys.exit(0)
