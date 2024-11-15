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
    "PORT_MINIMUM",
    "PORT_MAXIMUM",
    "TIMEOUT_MINIMUM",
    "LOG_LEVEL_MINIMUM",
    "LOG_LEVEL_MAXIMUM",
    "REFRESH_FREQUENCY_MINIMUM",
    "REFRESH_FREQUENCY_MAXIMUM",
    "POINT_SIZE_MINIMUM",
    "POINT_SIZE_MAXIMUM",
]


PORT_MINIMUM = 1
PORT_MAXIMUM = 65535

# In second
TIMEOUT_MINIMUM = 1

LOG_LEVEL_MINIMUM = 10
LOG_LEVEL_MAXIMUM = 50

# In Hz
REFRESH_FREQUENCY_MINIMUM = 1
REFRESH_FREQUENCY_MAXIMUM = 20

POINT_SIZE_MINIMUM = 9
POINT_SIZE_MAXIMUM = 14
