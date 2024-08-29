#!/usr/bin/env python3
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""Git utility functions to clone model repositories."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Repository:
    """Remote git repository.

    Attributes:
        cache_path: Path to clone the repository to in the local cache.
        commit: Commit ID or tag to checkout after cloning.
        url: URL to the remote git repository.
    """

    cache_path: str
    commit: str
    url: str


REPOSITORIES: Dict[str, Repository] = {
    "fourier_grx_descriptions": Repository(
        url="https://gitee.com/FourierIntelligence/wiki-grx-models.git",
        commit="5f9139bbf2d38256a77a4f272ee36c55fac05119",
        cache_path="fourier_grx_descriptions",
    )
}
