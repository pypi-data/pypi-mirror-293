from __future__ import annotations

import enum
from pathlib import Path
from typing import TypeAlias

import numpy as np
from numpy.typing import NDArray

_PKG_NAME: str = Path(__file__).parent.stem

VERSION = "2024.739127.0"

__version__ = VERSION

DATA_DIR: Path = Path.home() / _PKG_NAME
"""
Defines a subdirectory named for this package in the user's home path.

If the subdirectory doesn't exist, it is created on package invocation.
"""
if not DATA_DIR.is_dir():
    DATA_DIR.mkdir(parents=False)

np.set_printoptions(precision=18)


ArrayINT = NDArray[np.intp]
ArrayFloat = NDArray[np.half | np.single | np.double]


ArrayBoolean: TypeAlias = NDArray[np.bool_]

ArrayDouble: TypeAlias = NDArray[np.double]
ArrayBIGINT: TypeAlias = NDArray[np.int64]

DEFAULT_REC_RATE = 0.85


@enum.unique
class RECForm(enum.StrEnum):
    """Recapture rate - derivation methods."""

    INOUT = "inside-out"
    OUTIN = "outside-in"
    FIXED = "proportional"


@enum.unique
class UPPAggrSelector(enum.StrEnum):
    """
    Aggregator selection for GUPPI and diversion ratio

    """

    AVG = "average"
    CPA = "cross-product-share weighted average"
    CPD = "cross-product-share weighted distance"
    CPG = "cross-product-share weighted geometric mean"
    DIS = "symmetrically-weighted distance"
    GMN = "geometric mean"
    MAX = "max"
    MIN = "min"
    OSA = "own-share weighted average"
    OSD = "own-share weighted distance"
    OSG = "own-share weighted geometric mean"
