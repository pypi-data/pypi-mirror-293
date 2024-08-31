# -*- coding: utf-8 -*-

# Copyright (c) 2017 - 2024 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package containing utility modules and functions.
"""

import semver

from PyQt6.QtCore import QByteArray, QCoreApplication

###############################################################################
## Functions for converting QSetting return types to valid types.
###############################################################################


def toBool(value):
    """
    Function to convert a value to bool.

    @param value value to be converted
    @type str
    @return converted data
    @rtype bool
    """
    if (isinstance(value, str) and value.lower() in ["true", "1", "yes"]) or (
        isinstance(value, bytes) and value.lower() in [b"true", b"1", b"yes"]
    ):
        return True
    elif (isinstance(value, str) and value.lower() in ["false", "0", "no"]) or (
        isinstance(value, bytes) and value.lower() in [b"false", b"0", b"no"]
    ):
        return False
    else:
        return bool(value)


def toList(value):
    """
    Function to convert a value to a list.

    @param value value to be converted
    @type None, list or Any
    @return converted data
    @rtype list
    """
    if value is None:
        return []
    elif not isinstance(value, list):
        return [value]
    else:
        return value


def toByteArray(value):
    """
    Function to convert a value to a byte array.

    @param value value to be converted
    @type QByteArray or None
    @return converted data
    @rtype QByteArray
    """
    if value is None:
        return QByteArray()
    else:
        return value


def toDict(value):
    """
    Function to convert a value to a dictionary.

    @param value value to be converted
    @type dict or None
    @return converted data
    @rtype dict
    """
    if value is None:
        return {}
    else:
        return value


###############################################################################
## Functions for version handling.
###############################################################################


def versionIsValid(version):
    """
    Function to check, if the given version string is valid.

    @param version version string
    @type str
    @return flag indicating validity
    @rtype bool
    """
    try:
        return semver.VersionInfo.is_valid(version)
    except AttributeError:
        return semver.VersionInfo.isvalid(version)


def versionToTuple(version):
    """
    Function to convert a version string into a tuple.

    Note: A version string consists of non-negative decimals separated by "."
    optionally followed by a suffix. Suffix is everything after the last
    decimal.

    @param version version string
    @type str
    @return version named tuple containing the version parts
    @rtype semver.VersionInfo
    """
    while version and not version[0].isdecimal():
        # sanitize version string (get rid of leading non-decimal characters)
        version = version[1:]

    while len(version.split(".")) < 3:
        # ensure the version string contains at least three parts
        version += ".0"

    if versionIsValid(version):
        return semver.VersionInfo.parse(version)
    else:
        return semver.VersionInfo(0, 0, 0)


###############################################################################
## Functions for extended string handling.
###############################################################################


def strGroup(txt, sep, groupLen=4):
    """
    Function to group a string into sub-strings separated by a
    separator.

    @param txt text to be grouped
    @type str
    @param sep separator string
    @type str
    @param groupLen length of each group
    @type int
    @return result string
    @rtype str
    """
    groups = []

    while len(txt) // groupLen != 0:
        groups.insert(0, txt[-groupLen:])
        txt = txt[:-groupLen]
    if len(txt) > 0:
        groups.insert(0, txt)
    return sep.join(groups)


def strToQByteArray(txt):
    """
    Function to convert a Python string into a QByteArray.

    @param txt Python string to be converted
    @type str, bytes, bytearray
    @return converted QByteArray
    @rtype QByteArray
    """
    if isinstance(txt, str):
        txt = txt.encode("utf-8")

    return QByteArray(txt)


def dataString(size, loc=None):
    """
    Function to generate a formatted size string.

    @param size size to be formatted
    @type int
    @param loc locale to be used for localized size strings (defaults to None)
    @type QLocale (optional)
    @return formatted data string
    @rtype str
    """
    if loc is None:
        if size < 1024:
            return QCoreApplication.translate("EricUtilities", "{0:4d} Bytes").format(
                size
            )
        elif size < 1024 * 1024:
            size /= 1024
            return QCoreApplication.translate("EricUtilities", "{0:4.2f} KiB").format(
                size
            )
        elif size < 1024 * 1024 * 1024:
            size /= 1024 * 1024
            return QCoreApplication.translate("EricUtilities", "{0:4.2f} MiB").format(
                size
            )
        elif size < 1024 * 1024 * 1024 * 1024:
            size /= 1024 * 1024 * 1024
            return QCoreApplication.translate("EricUtilities", "{0:4.2f} GiB").format(
                size
            )
        else:
            size /= 1024 * 1024 * 1024 * 1024
            return QCoreApplication.translate("EricUtilities", "{0:4.2f} TiB").format(
                size
            )
    else:
        if not isinstance(size, float):
            size = float(size)

        if size < 1024:
            return QCoreApplication.translate("EricUtilities", "{0} Bytes").format(
                loc.toString(size)
            )
        elif size < 1024 * 1024:
            size /= 1024
            return QCoreApplication.translate("EricUtilities", "{0} KiB").format(
                loc.toString(size, "f", 2)
            )
        elif size < 1024 * 1024 * 1024:
            size /= 1024 * 1024
            return QCoreApplication.translate("EricUtilities", "{0} MiB").format(
                loc.toString(size, "f", 2)
            )
        elif size < 1024 * 1024 * 1024 * 1024:
            size /= 1024 * 1024 * 1024
            return QCoreApplication.translate("EricUtilities", "{0} GiB").format(
                loc.toString(size, "f", 2)
            )
        else:
            size /= 1024 * 1024 * 1024 * 1024
            return QCoreApplication.translate("EricUtilities", "{0} TiB").format(
                loc.toString(size, "f", 2)
            )
