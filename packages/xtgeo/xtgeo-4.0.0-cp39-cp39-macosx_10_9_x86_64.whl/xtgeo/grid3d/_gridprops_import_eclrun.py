from __future__ import annotations

import io
from copy import deepcopy
from typing import Generator, Literal

import resfo

import xtgeo
from xtgeo.common import null_logger
from xtgeo.common.constants import MAXKEYWORDS
from xtgeo.io._file import FileWrapper

from . import _grid3d_utils as utils
from ._find_gridprop_in_eclrun import (
    find_gridprop_from_init_file,
    find_gridprops_from_restart_file,
    valid_gridprop_lengths,
)
from ._gridprop_import_eclrun import decorate_name
from .grid_property import GridProperty

xtg = xtgeo.common.XTGeoDialog()

logger = null_logger(__name__)


def read_eclrun_properties(xtg_file: FileWrapper) -> Generator[str, None, None]:
    """Generates property names from Eclipse files.

    Args:
        xtg_file: The FileWrapper representing an Eclipse INIT or restart file.

    Returns:
        Names of properties within the Eclipse file.
    """
    is_stream = isinstance(xtg_file.file, (io.BytesIO, io.StringIO))
    try:
        if is_stream:
            mark = xtg_file.file.tell()
        ntotal = 0
        nactive = 0
        for item in resfo.lazy_read(xtg_file.file):
            keyword = item.read_keyword().strip()

            if keyword == "INTEHEAD":
                data = item.read_array()
                # nx * ny * nz
                ntotal = data[8] * data[9] * data[10]
                nactive = data[11]
                continue

            # Do some simple filtering of things that cannot be properties
            if item.read_length() in (ntotal, nactive) and item.read_type() in (
                b"INTE",
                b"REAL",
                b"DOUB",
            ):
                yield keyword
    finally:
        if is_stream:
            xtg_file.file.seek(mark)


def sanitize_date_list(
    dates: list[int] | list[str] | Literal["first", "all", "last"],
) -> list[int] | Literal["first", "all", "last"]:
    """
    Converts dateformats of the form 'YYYY-MM-DD', 'YYYYMMDD' or YYYYMMDD to
    list of integers of the form [YYYYMMDD] (ie. suitible for find_gridprops
    functions), but lets the special literals 'first' and 'last' remain
    unchanged.

    >>> sanitize_date_list('first')
    'first'
    >>> sanitize_date_list('last')
    'last'
    >>> sanitize_date_list('all')
    'all'
    >>> sanitize_date_list(['2020-01-01'])
    [20200101]
    >>> sanitize_date_list(['20200101'])
    [20200101]
    >>> sanitize_date_list([20200101])
    [20200101]
    """
    if dates in ("first", "last", "all"):
        return dates
    new_dates = []
    for date in dates:
        if isinstance(date, int):
            new_dates.append(date)
        else:
            try:
                if (
                    isinstance(date, str)
                    and len(date) == 10
                    and date[4] == "-"
                    and date[7] == "-"
                ):
                    date = date.replace("-", "")
                new_dates.append(int(date))
            except ValueError as err:
                raise ValueError(
                    "valid dates are either 'first'/'all'/'last', "
                    "list ints of the form YYYYMMDD or list of strings of "
                    f"'YYYY-MM-DD'/'YYYYMMDD' got {dates}"
                ) from err
    return new_dates


def import_ecl_init_gridproperties(
    pfile,
    names: list[str] | Literal["all"],
    grid,
    strict=True,
    maxkeys: int = MAXKEYWORDS,
) -> list[GridProperty]:
    """Imports list of properties from an init file.

    Note, the method does not determine whether a given keyword in the file
    is a grid property, only that it has the correct data type and length
    to be considered as a grid property.

    Args:
        pfile: Path to the ecl restart file
        names: List of names to fetch, can also be "all" to fetch all properties.
        grid: The grid used by the simulator to produce the restart file.
        strict: If strict=True, will raise error if key is not found.
        maxkeys: Maximum number of keywords allocated
    Returns:
        List of GridProperty objects fetched from the init file.
    """
    if not isinstance(pfile, FileWrapper):
        pfile = FileWrapper(pfile)

    if not grid:
        raise ValueError("Grid Geometry object is missing")

    if not names:
        raise ValueError("Name list cannot be empty (None)")

    # scan valid keywords
    kwlist = utils.scan_keywords(
        pfile,
        fformat="xecl",
        dataframe=True,
        dates=True,
        maxkeys=maxkeys,
    )

    validnames = []

    valid_lengths = valid_gridprop_lengths(grid)

    # get a list of valid property names
    for kw in list(kwlist.itertuples(index=False, name=None)):
        kwname, _, nlen, _, _ = kw
        if nlen in valid_lengths and kwname not in validnames:
            validnames.append(kwname)

    usenames = deepcopy(validnames) if names == "all" else list(names)

    for name in usenames:
        if name not in validnames:
            if strict:
                raise ValueError(
                    f"Requested keyword {name} is not in INIT file,"
                    f"valid entries are {validnames}, set strict=False to warn instead."
                )
            logger.warning(
                "Requested keyword %s is not in INIT file."
                "Entry will not be read, set strict=True to raise Error instead.",
                name,
            )

    results = find_gridprop_from_init_file(
        pfile.file,
        names=names,
        grid=grid,
    )
    properties_list = []
    for result in results:
        result["name"] = decorate_name(result["name"], grid.dualporo, fracture=False)
        properties_list.append(GridProperty(**result))

    return properties_list


def import_ecl_restart_gridproperties(
    pfile,
    names: list[str] | Literal["all"],
    dates: list[int] | list[str] | Literal["all", "last", "first"],
    grid,
    strict: tuple[bool, bool],
    namestyle: Literal[0, 1],
    maxkeys: int = MAXKEYWORDS,
) -> list[GridProperty]:
    """Imports list of gridproperties from a restart file.

    Note, the method does not determine whether a given keyword in the file
    is a grid property, only that it has the correct data type and length
    to be considered as a grid property.

    Args:
        pfile: Path to the ecl restart file
        names: List of names to fetch, can also be "all" to fetch all properties.
        dates: List of xtgeo style dates (e.g. int(19990101) or "YYYYMMDD"),
            also Also accepts "YYYY-MM-DD".  "all", "last" and "first" can be
            given for all, last or first date(s) in the file. Dates=None means
            look for properties in the init file.
        grid: The grid used by the simulator to produce the restart file.
        strict: strict (False, False) means that if keyname,
            optionally with date is not found is will just warn and continue to
            next. If (True, True) it will warn but TRY to import anyway, which
            in turn may raise a KeywordNotError or DateNotFoundError.  The
            (True, False) will be strict on keywords, but sloppy on dates,
            meaning that missing dates will be skipped. However, if all dates
            are missing an exception will be raised
        namestyle : 0 (default) for style SWAT_20110223,
            1 for SWAT--2011_02_23 (applies to restart only)
        maxkeys: Maximum number of keywords allocated
    Returns:
        List of GridProperty objects fetched from the restart file.
    """

    strictkeycomb, strictdate = strict
    if not grid:
        raise ValueError("Grid Geometry object is missing")

    if not names:
        raise ValueError("Name list cannot be empty (None)")

    dates = sanitize_date_list(dates)

    # scan valid keywords with dates
    kwlist = utils.scan_keywords(
        pfile,
        fformat="xecl",
        dataframe=True,
        dates=True,
        maxkeys=maxkeys,
    )

    validnamedatepairs, validdates = _process_valid_namesdates(kwlist, grid)

    # allow sloppy dates, i.e. remove invalid date entries
    if isinstance(dates, list) and strictdate is False:
        dates = _process_sloppydates(dates, validdates)

    usenamedatepairs = []
    if names == "all" and dates == "all":
        usenamedatepairs = deepcopy(validnamedatepairs)
        usedates = dates
    else:
        if names == "all" and dates != "all":
            usenames = [namedate[0] for namedate in validnamedatepairs]
            usedates = dates
        elif names != "all" and dates == "all":
            usedates = [namedate[1] for namedate in validnamedatepairs]
            usenames = names
        else:
            usedates = dates
            usenames = names

        for name in usenames:
            for date in usedates:
                usenamedatepairs.append((name, date))

    # Do the actual import
    for namedate in usenamedatepairs:
        name, date = namedate

        if name not in ("SGAS", "SOIL", "SWAT") and namedate not in validnamedatepairs:
            # saturation keywords are a mess in Eclipse and friends; check later
            if strictkeycomb:
                raise ValueError(
                    f"Keyword data combo {name} {date} is not in RESTART file."
                    f"Possible entries are: {validnamedatepairs}"
                )
            logger.warning(
                "Keyword data combo %s %s is not in RESTART file."
                "Possible entries are: %s"
                "Value will not be imported",
                name,
                date,
                validnamedatepairs,
            )

    results = find_gridprops_from_restart_file(pfile.file, names, dates, grid=grid)
    properties_list = []
    for result in results:
        if namestyle == 1:
            sdate = str(result["date"])
            result["name"] += "--" + sdate[0:4] + "_" + sdate[4:6] + "_" + sdate[6:8]
        else:
            result["name"] = decorate_name(
                result["name"], grid.dualporo, fracture=False, date=result["date"]
            )

        properties_list.append(GridProperty(**result))

    return properties_list


def _process_valid_namesdates(kwlist, grid):
    """Return lists with valid pairs, dates scanned from RESTART"""
    validnamedatepairs = []
    validdates = []
    valid_lengths = valid_gridprop_lengths(grid)
    for kw in list(kwlist.itertuples(index=False, name=None)):
        kwname, kwtyp, nlen, _, date = kw
        if (
            kwtyp != "CHAR"
            and nlen in valid_lengths
            and (kwname, date) not in validnamedatepairs
        ):
            validnamedatepairs.append((kwname, date))
        if kwtyp != "CHAR" and nlen in valid_lengths and date not in validdates:
            validdates.append(date)

    return validnamedatepairs, validdates


def _process_sloppydates(dates, validdates):
    """Allow "sloppy dates", which removes invalid dates from the list"""

    usedates = []
    skipdates = []
    for date in dates:
        if date not in validdates:
            skipdates.append(date)
        else:
            usedates.append(date)
    if not usedates:
        msg = f"No valid dates given (dates: {dates} vs {validdates})"
        xtg.error(msg)
        raise ValueError(msg)

    if skipdates:
        msg = f"Some dates not found: {skipdates}; will continue with dates: {usedates}"
        xtg.warn(msg)

    return usedates
