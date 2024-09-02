"""
Checks for updates in GitHub.
"""

# Copyright (C) 2023, Jacob Sánchez Pérez

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import requests
from pathlib import Path
from typing import Optional
from packaging import version
from importlib.metadata import version, PackageNotFoundError


def is_inside_container() -> bool:
    return Path('/.flatpak-info').exists()

def check_for_updates() -> Optional[str]:
    """Checks if there is a newer release than the current on Github."""
    # Get version
    try:
        __version__ = version("blackboard_sync")
    except PackageNotFoundError:
        return None

    url = 'https://api.github.com/repos/sanjacob/BlackboardSync/releases/latest'
    response = requests.get(url, timeout=2000)
    if response.status_code == 200:
        json_response = response.json()
        tag = json_response['tag_name']
        tag = tag[1:] if tag[0] == 'v' else tag
        if version.parse(tag) > version.parse(__version__):
            return 'container' if is_inside_container() else json_response['html_url']

    return None


