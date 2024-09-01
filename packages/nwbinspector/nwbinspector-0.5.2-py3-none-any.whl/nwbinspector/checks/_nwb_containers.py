"""Check functions that can apply to any object inside an NWBContainer."""

import os

import h5py
from pynwb import NWBContainer

from .._registration import Importance, InspectorMessage, Severity, register_check


@register_check(importance=Importance.BEST_PRACTICE_VIOLATION, neurodata_type=NWBContainer)
def check_large_dataset_compression(nwb_container: NWBContainer, gb_lower_bound: float = 20.0):
    """
    If the data in the Container object is a 'large' h5py.Dataset, check if it has compression enabled.

    Will only return an inspector warning if the size of the h5py.Dataset is larger than the
    gb_lower_bound (default of 20 GB).

    Best Practice: :ref:`best_practice_compression`
    """
    for field in getattr(nwb_container, "fields", dict()).values():
        if not isinstance(field, h5py.Dataset):
            continue
        if field.compression is None and field.size * field.dtype.itemsize > gb_lower_bound * 1e9:
            return InspectorMessage(
                severity=Severity.HIGH,
                message=f"{os.path.split(field.name)[1]} is a large uncompressed dataset! Please enable compression.",
            )


@register_check(importance=Importance.BEST_PRACTICE_SUGGESTION, neurodata_type=NWBContainer)
def check_small_dataset_compression(
    nwb_container: NWBContainer,
    gb_severity_threshold: float = 10.0,
    mb_lower_bound: float = 50.0,
    gb_upper_bound: float = 20.0,  # 20 GB upper bound to prevent double-raise
):
    """
    If the data in the Container object is a h5py.Dataset, check if it has compression enabled.

    Will only return an inspector warning if the size of the h5py.Dataset is larger than mb_lower_bound (default 50 MB)
    and smaller than gb_upper_bound (default of 20 GB).

    Best Practice: :ref:`best_practice_compression`
    """
    for field in getattr(nwb_container, "fields", dict()).values():
        if not isinstance(field, h5py.Dataset):
            continue
        if (
            field.compression is None
            and mb_lower_bound * 1e6 < field.size * field.dtype.itemsize < gb_upper_bound * 1e9
        ):
            if field.size * field.dtype.itemsize > gb_severity_threshold * 1e9:
                severity = Severity.HIGH
            else:
                severity = Severity.LOW
            return InspectorMessage(
                severity=severity,
                message=(
                    f"{os.path.split(field.name)[1]} is not compressed. Consider enabling compression when writing a "
                    "dataset."
                ),
            )


@register_check(importance=Importance.BEST_PRACTICE_SUGGESTION, neurodata_type=NWBContainer)
def check_empty_string_for_optional_attribute(nwb_container: NWBContainer):
    """
    Check if any NWBContainer has optional fields that are written as an empty string.

    These values should just be omitted instead.

    Parameters
    ----------
    nwb_container: NWBContainer

    Best Practice: :ref:`best_practice_placeholders`
    """
    docval_args = type(nwb_container).__init__.__docval__["args"]
    optional_attrs = [
        arg["name"] for arg in docval_args if arg["type"] is str and "default" in arg and arg["default"] is None
    ]
    fields = [attr for attr in optional_attrs if getattr(nwb_container, attr) == ""]
    for field in fields:
        yield InspectorMessage(
            message=f'The attribute "{field}" is optional and you have supplied an empty string. Improve my omitting '
            "this attribute (in MatNWB or PyNWB) or entering as None (in PyNWB)"
        )
