# Copyright 2024 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Data models for `slurmdbd.conf` configuration file."""

from .model import BaseModel, format_key, generate_descriptors
from .option import SlurmdbdConfigOptionSet


class SlurmdbdConfig(BaseModel):
    """`slurmdbd.conf` data model."""

    def __init__(self, **kwargs):
        super().__init__(SlurmdbdConfigOptionSet, **kwargs)


for opt in SlurmdbdConfigOptionSet.keys():
    setattr(SlurmdbdConfig, format_key(opt), property(*generate_descriptors(opt)))
