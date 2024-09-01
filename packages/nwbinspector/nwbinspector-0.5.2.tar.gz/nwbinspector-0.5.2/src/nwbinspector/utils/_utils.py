"""Commonly reused logic for evaluating conditions; must not have external dependencies."""

import json
import os
import re
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from time import sleep
from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union

import h5py
import numpy as np
from hdmf.backends.hdf5.h5_utils import H5Dataset
from numpy.typing import ArrayLike
from packaging import version

# TODO: deprecated these in favor of explicit typing
PathType = TypeVar("PathType", str, Path)  # For types that can be either files or folders
FilePathType = TypeVar("FilePathType", str, Path)
OptionalListOfStrings = Optional[List[str]]

dict_regex = r"({.+:.+})"  # TODO: remove this from global scope
MAX_CACHE_ITEMS = 1000  # lru_cache default is 128 calls of matching input/output, but might need more to get use here


@lru_cache(maxsize=MAX_CACHE_ITEMS)
def _cache_data_retrieval_command(
    data: h5py.Dataset, reduced_selection: Tuple[Tuple[Optional[int], Optional[int], Optional[int]]]
) -> np.ndarray:
    """LRU caching for _cache_data_selection cannot be applied to list inputs; this expects the tuple or Dataset."""
    selection = tuple([slice(*reduced_slice) for reduced_slice in reduced_selection])  # reconstitute the slices
    return data[selection]


def cache_data_selection(data: Union[h5py.Dataset, ArrayLike], selection: Union[slice, Tuple[slice]]) -> np.ndarray:
    """Extract the selection lazily from the data object for efficient caching (most beneficial during streaming)."""
    if isinstance(data, np.memmap):  # np.memmap objects are not hashable - simply return the selection lazily
        return data[selection]
    if not (
        isinstance(data, h5py.Dataset) or isinstance(data, H5Dataset)
    ):  # No need to attempt to cache if data is already in-memory
        # Cast as numpy array for efficient fancy indexing
        # Note that this technically copies the entire data, so could use more than 2x RAM for that object
        return np.array(data)[selection]

    # Slices aren't hashable, but their reduced representation is
    if isinstance(selection, slice):  # A single slice
        reduced_selection = tuple([selection.__reduce__()[1]])
    else:  # Iterable of slices
        reduced_selection = tuple([selection_slice.__reduce__()[1] for selection_slice in selection])
    return _cache_data_retrieval_command(data=data, reduced_selection=reduced_selection)


def format_byte_size(byte_size: int, units: str = "SI"):
    """
    Format a number representing a total number of bytes into a convenient unit.

    Parameters
    ----------
    byte_size : int
        Total number of bytes to format.
    units : str, optional
        Convention for orders of magnitude to apply.
        May be either SI (orders of 1000) or binary (in memory, orders of 1024).
        The default is SI.
    """
    num = byte_size
    prefixes = ["", "K", "M", "G", "T", "P", "E", "Z"]
    if units == "SI":
        order = 1000.0
        suffix = "B"
    elif units == "binary":
        order = 1024.0
        suffix = "iB"
    else:
        raise ValueError("'units' argument must be either 'SI' (for orders of 1000) or 'binary' (for orders of 1024).")
    for prefix in prefixes:
        if abs(num) < order:
            return f"{num:3.2f}{prefix}{suffix}"
        num /= order
    return f"{num:.2f}Y{suffix}"


def is_regular_series(series: np.ndarray, tolerance_decimals: int = 9):
    """General purpose function for checking if the difference between all consecutive points in a series are equal."""
    uniq_diff_ts = np.unique(np.diff(series).round(decimals=tolerance_decimals))
    return len(uniq_diff_ts) == 1


def is_ascending_series(series: Union[h5py.Dataset, ArrayLike], nelems: Optional[int] = None):
    """General purpose function for determining if a series is monotonic increasing."""
    if isinstance(series, h5py.Dataset):
        data = cache_data_selection(data=series, selection=slice(nelems))
    else:
        data = series[:nelems]

    # Remove NaN values from the series
    data = np.array(data)
    valid_data = data[~np.isnan(data)]

    # Compute the differences between consecutive elements
    differences = np.diff(valid_data)

    return np.all(differences >= 0)


def is_dict_in_string(string: str):
    """
    Determine if the string value contains an encoded Python dictionary.

    Can also be the direct results of string casting a dictionary, *e.g.*, ``str(dict(a=1))``.
    """
    return any(re.findall(pattern=dict_regex, string=string))


def is_string_json_loadable(string: str):
    """
    Determine if the serialized dictionary is a JSON object.

    Rather than constructing a complicated regex pattern, a simple try/except of the json.load should suffice.
    """
    try:
        json.loads(string)
        return True
    except json.JSONDecodeError:
        return False


def is_module_installed(module_name: str):
    """
    Check if the given module is installed on the system.

    Used for lazy imports.
    """
    try:
        import_module(name=module_name)
        return True
    except ModuleNotFoundError:
        return False


def get_package_version(name: str) -> version.Version:
    """
    Retrieve the version of a package regardless of if it has a __version__ attribute set.

    Parameters
    ----------
    name : str
        Name of package.

    Returns
    -------
    version : Version
        The package version as an object from packaging.version.Version, which allows comparison to other versions.
    """
    try:
        from importlib.metadata import version as importlib_version

        package_version = importlib_version(name)
    except ModuleNotFoundError:  # Remove the except clause when minimal supported version becomes 3.8
        from pkg_resources import get_distribution

        package_version = get_distribution(name).version
    return version.parse(package_version)


def robust_s3_read(
    command: Callable, max_retries: int = 10, command_args: Optional[list] = None, command_kwargs: Optional[Dict] = None
):
    """Attempt the command (usually acting on an S3 IO) up to the number of max_retries using exponential backoff."""
    command_args = command_args or []
    command_kwargs = command_kwargs or dict()
    for retry in range(max_retries):
        try:
            return command(*command_args, **command_kwargs)
        except Exception as exc:
            if "curl" in str(exc):  # 'cannot curl request' can show up in potentially many different return error types
                sleep(0.1 * 2**retry)
            else:
                raise exc
    raise TimeoutError(f"Unable to complete the command ({command.__name__}) after {max_retries} attempts!")


def calculate_number_of_cpu(requested_cpu: int = 1) -> int:
    """
    Calculate the number CPUs to use with respect to negative slicing and check against maximal available resources.

    Parameters
    ----------
    requested_cpu : int, optional
        The desired number of CPUs to use.

        The default is 1.
    """
    total_cpu = os.cpu_count()
    assert requested_cpu <= total_cpu, f"Requested more CPUs ({requested_cpu}) than are available ({total_cpu})!"
    assert requested_cpu >= -(
        total_cpu - 1
    ), f"Requested fewer CPUs ({requested_cpu}) than are available ({total_cpu})!"
    if requested_cpu > 0:
        return requested_cpu
    else:
        return total_cpu + requested_cpu


def get_data_shape(data, strict_no_data_load=False):
    """
    modified from hdmf.utils.get_data_shape to return shape instead of maxshape
    Helper function used to determine the shape of the given array.

    In order to determine the shape of nested tuples, lists, and sets, this function
    recursively inspects elements along the dimensions, assuming that the data has a regular,
    rectangular shape. In the case of out-of-core iterators, this means that the first item
    along each dimension would potentially be loaded into memory. Set strict_no_data_load=True
    to enforce that this does not happen, at the cost that we may not be able to determine
    the shape of the array.

    :param data: Array for which we should determine the shape.
    :type data: List, numpy.ndarray, DataChunkIterator, any object that support __len__ or .shape.
    :param strict_no_data_load: If True and data is an out-of-core iterator, None may be returned. If False (default),
                                the first element of data may be loaded into memory.
    :return: Tuple of ints indicating the size of known dimensions. Dimensions for which the size is unknown
             will be set to None.
    """

    def __get_shape_helper(local_data):
        shape = list()
        if hasattr(local_data, "__len__"):
            shape.append(len(local_data))
            if len(local_data):
                el = next(iter(local_data))
                if not isinstance(el, (str, bytes)):
                    shape.extend(__get_shape_helper(el))
        return tuple(shape)

    if hasattr(data, "shape") and data.shape is not None:
        return data.shape
    if isinstance(data, dict):
        return
    if hasattr(data, "__len__") and not isinstance(data, (str, bytes)):
        if not strict_no_data_load or isinstance(data, (list, tuple, set)):
            return __get_shape_helper(data)


def strtobool(val: str) -> bool:
    """
    Convert a string representation of truth to True or False.

    True values are 'y', 'yes', 't', 'true', 'on', and '1';
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if 'val' is anything else.
    """
    if not isinstance(val, str):
        raise TypeError(f"Invalid type of {val!r} - must be str for `strtobool`")
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truth value {val!r}")
