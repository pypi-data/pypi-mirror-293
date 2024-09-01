import os
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase

import numpy as np
from hdmf.common import DynamicTable
from natsort import natsorted
from pynwb import NWBHDF5IO, NWBFile, TimeSeries
from pynwb.behavior import Position, SpatialSeries
from pynwb.file import Subject, TimeIntervals

from nwbinspector import (
    Importance,
    InspectorMessage,
    Severity,
    available_checks,
    inspect_all,
    inspect_nwbfile,
    inspect_nwbfile_object,
    load_config,
    register_check,
)
from nwbinspector.checks import (
    check_data_orientation,
    check_regular_timestamps,
    check_small_dataset_compression,
    check_subject_exists,
    check_timestamps_match_first_dimension,
)
from nwbinspector.testing import make_minimal_nwbfile
from nwbinspector.utils import FilePathType


def add_big_dataset_no_compression(nwbfile: NWBFile):
    time_series = TimeSeries(
        name="test_time_series_1", data=np.zeros(shape=int(1.1e9 / np.dtype("float").itemsize)), rate=1.0, unit=""
    )
    nwbfile.add_acquisition(time_series)


def add_regular_timestamps(nwbfile: NWBFile):
    regular_timestamps = np.arange(1.2, 11.2, 2)
    timestamps_length = len(regular_timestamps)
    time_series = TimeSeries(
        name="test_time_series_2",
        data=np.zeros(shape=(timestamps_length, timestamps_length - 1)),
        timestamps=regular_timestamps,
        unit="",
    )
    nwbfile.add_acquisition(time_series)


def add_flipped_data_orientation_to_acquisition(nwbfile: NWBFile):
    time_series = TimeSeries(name="my_spatial_series", data=np.zeros(shape=(2, 3)), unit="test_unit", rate=1.0)
    nwbfile.add_acquisition(time_series)


def add_flipped_data_orientation_to_processing(nwbfile: NWBFile):
    spatial_series = SpatialSeries(
        name="my_spatial_series", data=np.zeros(shape=(2, 3)), reference_frame="unknown", rate=1.0
    )
    module = nwbfile.create_processing_module(name="behavior", description="")
    module.add(Position(spatial_series=spatial_series))


def add_non_matching_timestamps_dimension(nwbfile: NWBFile):
    timestamps = [1.0, 2.1, 3.0]
    timestamps_length = len(timestamps)
    time_series = TimeSeries(
        name="test_time_series_3",
        data=np.zeros(shape=(timestamps_length + 1, timestamps_length)),
        timestamps=timestamps,
        unit="",
    )
    nwbfile.add_acquisition(time_series)


def add_simple_table(nwbfile: NWBFile):
    time_intervals = TimeIntervals(name="test_table", description="desc")
    time_intervals.add_row(start_time=2.0, stop_time=3.0)
    time_intervals.add_row(start_time=1.0, stop_time=2.0)
    nwbfile.add_acquisition(time_intervals)


class TestInspector(TestCase):
    """A common helper class for testing the NWBInspector."""

    def assertFileExists(self, path: FilePathType):
        path = Path(path)
        assert path.exists()

    def assertLogFileContentsEqual(
        self, test_file_path: FilePathType, true_file_path: FilePathType, skip_first_newlines: bool = False
    ):
        skip_first_n_lines = 0
        with open(file=test_file_path, mode="r") as test_file:
            test_file_lines = test_file.readlines()
        with open(file=true_file_path, mode="r") as true_file:
            true_file_lines = true_file.readlines()

        if skip_first_newlines:
            for line_number, test_line in enumerate(test_file_lines):
                if test_line != "\n":
                    skip_first_n_lines = line_number
                    break
        else:
            skip_first_n_lines = 0

        for line_number, test_line in enumerate(test_file_lines):
            if "Timestamp: " in test_line:
                # Transform the test file header to match ground true example
                test_file_lines[line_number] = "Timestamp: 2022-04-01 13:32:13.756390-04:00\n"
                test_file_lines[line_number + 1] = "Platform: Windows-10-10.0.19043-SP0\n"
                test_file_lines[line_number + 2] = "NWBInspector version: 0.3.6\n"
            if ".nwb" in test_line:
                # Transform temporary testing path and formatted to hardcoded fake path
                str_loc = test_line.find(".nwb")
                correction_str = test_line.replace(test_line[5 : str_loc - 8], "./")  # noqa: E203 (black)
                test_file_lines[line_number] = correction_str
        self.assertEqual(first=test_file_lines[skip_first_n_lines:-1], second=true_file_lines)


class TestInspectorAPI(TestInspector):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.tempdir = Path(mkdtemp())
        cls.checks = [
            check_small_dataset_compression,
            check_regular_timestamps,
            check_data_orientation,
            check_timestamps_match_first_dimension,
        ]
        num_nwbfiles = 4
        nwbfiles = list()
        for j in range(num_nwbfiles):
            nwbfiles.append(make_minimal_nwbfile())
        add_big_dataset_no_compression(nwbfiles[0])
        add_regular_timestamps(nwbfiles[0])
        add_flipped_data_orientation_to_processing(nwbfiles[0])
        add_non_matching_timestamps_dimension(nwbfiles[0])
        add_simple_table(nwbfiles[0])
        add_regular_timestamps(nwbfiles[1])
        # Third file to be left without violations
        add_non_matching_timestamps_dimension(nwbfiles[3])

        cls.nwbfile_paths = [str(cls.tempdir / f"testing{j}.nwb") for j in range(num_nwbfiles)]
        cls.nwbfile_paths[3] = str(cls.tempdir / f"._testing3.nwb")
        for nwbfile_path, nwbfile in zip(cls.nwbfile_paths, nwbfiles):
            with NWBHDF5IO(path=nwbfile_path, mode="w") as io:
                io.write(nwbfile)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.tempdir)

    def test_inspect_all(self):
        test_results = list(inspect_all(path=self.tempdir, select=[x.__name__ for x in self.checks]))
        true_results = [
            InspectorMessage(
                message="data is not compressed. Consider enabling compression when writing a dataset.",
                importance=Importance.BEST_PRACTICE_SUGGESTION,
                severity=Severity.LOW,
                check_function_name="check_small_dataset_compression",
                object_type="TimeSeries",
                object_name="test_time_series_1",
                location="/acquisition/test_time_series_1",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message=(
                    "TimeSeries appears to have a constant sampling rate. Consider specifying starting_time=1.2 "
                    "and rate=0.5 instead of timestamps."
                ),
                importance=Importance.BEST_PRACTICE_VIOLATION,
                severity=Severity.LOW,
                check_function_name="check_regular_timestamps",
                object_type="TimeSeries",
                object_name="test_time_series_2",
                location="/acquisition/test_time_series_2",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message=(
                    "Data may be in the wrong orientation. Time should be in the first dimension, and is usually "
                    "the longest dimension. Here, another dimension is longer."
                ),
                importance=Importance.CRITICAL,
                severity=Severity.LOW,
                check_function_name="check_data_orientation",
                object_type="SpatialSeries",
                object_name="my_spatial_series",
                location="/processing/behavior/Position/my_spatial_series",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message="The length of the first dimension of data (4) does not match the length of timestamps (3).",
                importance=Importance.CRITICAL,
                severity=Severity.LOW,
                check_function_name="check_timestamps_match_first_dimension",
                object_type="TimeSeries",
                object_name="test_time_series_3",
                location="/acquisition/test_time_series_3",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message=(
                    "TimeSeries appears to have a constant sampling rate. Consider specifying starting_time=1.2 "
                    "and rate=0.5 instead of timestamps."
                ),
                importance=Importance.BEST_PRACTICE_VIOLATION,
                severity=Severity.LOW,
                check_function_name="check_regular_timestamps",
                object_type="TimeSeries",
                object_name="test_time_series_2",
                location="/acquisition/test_time_series_2",
                file_path=self.nwbfile_paths[1],
            ),
        ]
        self.assertCountEqual(first=test_results, second=true_results)

        def test_inspect_all_parallel(self):
            test_results = list(
                inspect_all(path=Path(self.nwbfile_paths[0]).parent, select=[x.__name__ for x in self.checks], n_jobs=2)
            )
            true_results = [
                InspectorMessage(
                    message="data is not compressed. Consider enabling compression when writing a dataset.",
                    importance=Importance.BEST_PRACTICE_SUGGESTION,
                    severity=Severity.LOW,
                    check_function_name="check_small_dataset_compression",
                    object_type="TimeSeries",
                    object_name="test_time_series_1",
                    location="/acquisition/test_time_series_1",
                    file_path=self.nwbfile_paths[0],
                ),
                InspectorMessage(
                    message=(
                        "TimeSeries appears to have a constant sampling rate. Consider specifying starting_time=1.2 "
                        "and rate=0.5 instead of timestamps."
                    ),
                    importance=Importance.BEST_PRACTICE_VIOLATION,
                    severity=Severity.LOW,
                    check_function_name="check_regular_timestamps",
                    object_type="TimeSeries",
                    object_name="test_time_series_2",
                    location="/acquisition/test_time_series_2",
                    file_path=self.nwbfile_paths[0],
                ),
                InspectorMessage(
                    message=(
                        "Data may be in the wrong orientation. Time should be in the first dimension, and is usually "
                        "the longest dimension. Here, another dimension is longer."
                    ),
                    importance=Importance.CRITICAL,
                    severity=Severity.LOW,
                    check_function_name="check_data_orientation",
                    object_type="SpatialSeries",
                    object_name="my_spatial_series",
                    location="/processing/behavior/Position/my_spatial_series",
                    file_path=self.nwbfile_paths[0],
                ),
                InspectorMessage(
                    message=(
                        "The length of the first dimension of data (4) does not match the length of timestamps (3)."
                    ),
                    importance=Importance.CRITICAL,
                    severity=Severity.LOW,
                    check_function_name="check_timestamps_match_first_dimension",
                    object_type="TimeSeries",
                    object_name="test_time_series_3",
                    location="/acquisition/test_time_series_3",
                    file_path=self.nwbfile_paths[0],
                ),
                InspectorMessage(
                    message=(
                        "TimeSeries appears to have a constant sampling rate. Consider specifying starting_time=1.2 "
                        "and rate=0.5 instead of timestamps."
                    ),
                    importance=Importance.BEST_PRACTICE_VIOLATION,
                    severity=Severity.LOW,
                    check_function_name="check_regular_timestamps",
                    object_type="TimeSeries",
                    object_name="test_time_series_2",
                    location="/acquisition/test_time_series_2",
                    file_path=self.nwbfile_paths[1],
                ),
            ]
            self.assertCountEqual(first=test_results, second=true_results)

    def test_inspect_nwbfile(self):
        test_results = list(inspect_nwbfile(nwbfile_path=self.nwbfile_paths[0], checks=self.checks))
        true_results = [
            InspectorMessage(
                message="data is not compressed. Consider enabling compression when writing a dataset.",
                severity=Severity.LOW,
                importance=Importance.BEST_PRACTICE_SUGGESTION,
                check_function_name="check_small_dataset_compression",
                object_type="TimeSeries",
                object_name="test_time_series_1",
                location="/acquisition/test_time_series_1",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message=(
                    "TimeSeries appears to have a constant sampling rate. Consider specifying starting_time=1.2 and "
                    "rate=0.5 instead of timestamps."
                ),
                severity=Severity.LOW,
                importance=Importance.BEST_PRACTICE_VIOLATION,
                check_function_name="check_regular_timestamps",
                object_type="TimeSeries",
                object_name="test_time_series_2",
                location="/acquisition/test_time_series_2",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message=(
                    "Data may be in the wrong orientation. Time should be in the first dimension, and is usually the "
                    "longest dimension. Here, another dimension is longer."
                ),
                importance=Importance.CRITICAL,
                check_function_name="check_data_orientation",
                object_type="SpatialSeries",
                object_name="my_spatial_series",
                location="/processing/behavior/Position/my_spatial_series",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message="The length of the first dimension of data (4) does not match the length of timestamps (3).",
                importance=Importance.CRITICAL,
                check_function_name="check_timestamps_match_first_dimension",
                object_type="TimeSeries",
                object_name="test_time_series_3",
                location="/acquisition/test_time_series_3",
                file_path=self.nwbfile_paths[0],
            ),
        ]
        self.assertCountEqual(first=test_results, second=true_results)

    def test_inspect_nwbfile_importance_threshold_as_importance(self):
        test_results = list(
            inspect_nwbfile(
                nwbfile_path=self.nwbfile_paths[0], checks=self.checks, importance_threshold=Importance.CRITICAL
            )
        )
        true_results = [
            InspectorMessage(
                message=(
                    "Data may be in the wrong orientation. Time should be in the first dimension, and is "
                    "usually the longest dimension. Here, another dimension is longer."
                ),
                importance=Importance.CRITICAL,
                check_function_name="check_data_orientation",
                object_type="SpatialSeries",
                object_name="my_spatial_series",
                location="/processing/behavior/Position/my_spatial_series",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message="The length of the first dimension of data (4) does not match the length of timestamps (3).",
                importance=Importance.CRITICAL,
                check_function_name="check_timestamps_match_first_dimension",
                object_type="TimeSeries",
                object_name="test_time_series_3",
                location="/acquisition/test_time_series_3",
                file_path=self.nwbfile_paths[0],
            ),
        ]
        self.assertCountEqual(first=test_results, second=true_results)

    def test_inspect_nwbfile_importance_threshold_as_string(self):
        test_results = list(
            inspect_nwbfile(nwbfile_path=self.nwbfile_paths[0], checks=self.checks, importance_threshold="CRITICAL")
        )
        true_results = [
            InspectorMessage(
                message=(
                    "Data may be in the wrong orientation. Time should be in the first dimension, and is "
                    "usually the longest dimension. Here, another dimension is longer."
                ),
                importance=Importance.CRITICAL,
                check_function_name="check_data_orientation",
                object_type="SpatialSeries",
                object_name="my_spatial_series",
                location="/processing/behavior/Position/my_spatial_series",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message="The length of the first dimension of data (4) does not match the length of timestamps (3).",
                importance=Importance.CRITICAL,
                check_function_name="check_timestamps_match_first_dimension",
                object_type="TimeSeries",
                object_name="test_time_series_3",
                location="/acquisition/test_time_series_3",
                file_path=self.nwbfile_paths[0],
            ),
        ]
        self.assertCountEqual(first=test_results, second=true_results)

    def test_command_line_runs_cli_only(self):
        console_output_file = self.tempdir / "test_console_output.txt"
        os.system(
            f"nwbinspector {str(self.tempdir)} --overwrite --select check_timestamps_match_first_dimension,"
            "check_data_orientation,check_regular_timestamps,check_small_dataset_compression "
            "--modules random,math,datetime"
            f"> {console_output_file}"
        )
        self.assertLogFileContentsEqual(
            test_file_path=console_output_file,
            true_file_path=Path(__file__).parent / "true_nwbinspector_default_report.txt",
            skip_first_newlines=True,
        )

    def test_command_line_runs_cli_only_parallel(self):
        console_output_file = self.tempdir / "test_console_output_2.txt"
        os.system(
            f"nwbinspector {str(self.tempdir)} --n-jobs 2 --overwrite --select check_timestamps_match_first_dimension,"
            "check_data_orientation,check_regular_timestamps,check_small_dataset_compression"
            f"> {console_output_file}"
        )
        self.assertLogFileContentsEqual(
            test_file_path=console_output_file,
            true_file_path=Path(__file__).parent / "true_nwbinspector_default_report.txt",
            skip_first_newlines=True,
        )

    def test_command_line_saves_report(self):
        console_output_file = self.tempdir / "test_console_output_3.txt"
        os.system(
            f"nwbinspector {str(self.nwbfile_paths[0])} "
            f"--report-file-path {self.tempdir / 'test_nwbinspector_report_1.txt'}"
            f"> {console_output_file}"
        )
        self.assertFileExists(path=self.tempdir / "test_nwbinspector_report_1.txt")

    def test_command_line_organizes_levels(self):
        console_output_file = self.tempdir / "test_console_output_4.txt"
        os.system(
            f"nwbinspector {str(self.nwbfile_paths[0])} "
            f"--report-file-path {self.tempdir / 'test_nwbinspector_report_2.txt'} "
            "--levels importance,check_function_name,file_path"
            f"> {console_output_file}"
        )
        self.assertFileExists(path=self.tempdir / "test_nwbinspector_report_2.txt")

    def test_command_line_runs_saves_json(self):
        json_fpath = self.tempdir / "nwbinspector_results.json"
        os.system(f"nwbinspector {str(self.nwbfile_paths[0])} --json-file-path {json_fpath}")
        self.assertFileExists(path=json_fpath)

    def test_command_line_on_directory_matches_file(self):
        console_output_file = self.tempdir / "test_console_output_5.txt"
        os.system(
            f"nwbinspector {str(self.tempdir)} --overwrite --select check_timestamps_match_first_dimension,"
            "check_data_orientation,check_regular_timestamps,check_small_dataset_compression"
            f" --report-file-path {self.tempdir / 'test_nwbinspector_report_3.txt'}"
            f"> {console_output_file}"
        )
        self.assertLogFileContentsEqual(
            test_file_path=self.tempdir / "test_nwbinspector_report_3.txt",
            true_file_path=Path(__file__).parent / "true_nwbinspector_default_report.txt",
            skip_first_newlines=True,
        )

    def test_iterable_check_function(self):
        @register_check(importance=Importance.BEST_PRACTICE_VIOLATION, neurodata_type=DynamicTable)
        def iterable_check_function(table: DynamicTable):
            for col in table.columns:
                yield InspectorMessage(message=f"Column: {col.name}")

        test_results = list(inspect_nwbfile(nwbfile_path=self.nwbfile_paths[0], select=["iterable_check_function"]))
        true_results = [
            InspectorMessage(
                message="Column: start_time",
                importance=Importance.BEST_PRACTICE_VIOLATION,
                check_function_name="iterable_check_function",
                object_type="TimeIntervals",
                object_name="test_table",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message="Column: stop_time",
                importance=Importance.BEST_PRACTICE_VIOLATION,
                check_function_name="iterable_check_function",
                object_type="TimeIntervals",
                object_name="test_table",
                file_path=self.nwbfile_paths[0],
            ),
        ]
        self.assertCountEqual(first=test_results, second=true_results)

    def test_inspect_nwbfile_manual_iteration(self):
        generator = inspect_nwbfile(nwbfile_path=self.nwbfile_paths[0], checks=self.checks)
        message = next(generator)
        true_result = InspectorMessage(
            message="data is not compressed. Consider enabling compression when writing a dataset.",
            importance=Importance.BEST_PRACTICE_SUGGESTION,
            severity=Severity.LOW,
            check_function_name="check_small_dataset_compression",
            object_type="TimeSeries",
            object_name="test_time_series_1",
            location="/acquisition/test_time_series_1",
            file_path=self.nwbfile_paths[0],
        )
        self.assertEqual(message, true_result)

    def test_inspect_nwbfile_manual_iteration_stop(self):
        generator = inspect_nwbfile(nwbfile_path=self.nwbfile_paths[2], checks=self.checks)
        with self.assertRaises(expected_exception=StopIteration):
            next(generator)

    def test_inspect_nwbfile_dandi_config(self):
        config_checks = [check_subject_exists] + self.checks
        test_results = list(
            inspect_nwbfile(
                nwbfile_path=self.nwbfile_paths[0],
                checks=config_checks,
                config=load_config(filepath_or_keyword="dandi"),
            )
        )
        true_results = [
            InspectorMessage(
                message="Subject is missing.",
                importance=Importance.CRITICAL,  # Normally a BEST_PRACTICE_SUGGESTION
                check_function_name="check_subject_exists",
                object_type="NWBFile",
                object_name="root",
                location="/",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message=(
                    "Data may be in the wrong orientation. "
                    "Time should be in the first dimension, and is usually the longest dimension. "
                    "Here, another dimension is longer."
                ),
                importance=Importance.BEST_PRACTICE_VIOLATION,  # Normally CRITICAL, now a BEST_PRACTICE_VIOLATION
                check_function_name="check_data_orientation",
                object_type="SpatialSeries",
                object_name="my_spatial_series",
                location="/processing/behavior/Position/my_spatial_series",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message="data is not compressed. Consider enabling compression when writing a dataset.",
                importance=Importance.BEST_PRACTICE_SUGGESTION,
                check_function_name="check_small_dataset_compression",
                object_type="TimeSeries",
                object_name="test_time_series_1",
                location="/acquisition/test_time_series_1",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message=(
                    "TimeSeries appears to have a constant sampling rate. "
                    "Consider specifying starting_time=1.2 and rate=0.5 instead of timestamps."
                ),
                importance=Importance.BEST_PRACTICE_VIOLATION,
                check_function_name="check_regular_timestamps",
                object_type="TimeSeries",
                object_name="test_time_series_2",
                location="/acquisition/test_time_series_2",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message="The length of the first dimension of data (4) does not match the length of timestamps (3).",
                importance=Importance.CRITICAL,
                check_function_name="check_timestamps_match_first_dimension",
                object_type="TimeSeries",
                object_name="test_time_series_3",
                location="/acquisition/test_time_series_3",
                file_path=self.nwbfile_paths[0],
            ),
        ]
        self.assertCountEqual(first=test_results, second=true_results)


class TestDANDIConfig(TestInspector):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.tempdir = Path(mkdtemp())
        cls.checks = available_checks
        num_nwbfiles = 2
        nwbfiles = list()
        for j in range(num_nwbfiles):
            nwbfiles.append(make_minimal_nwbfile())
        add_big_dataset_no_compression(nwbfiles[0])
        add_regular_timestamps(nwbfiles[0])
        add_flipped_data_orientation_to_processing(nwbfiles[0])
        add_non_matching_timestamps_dimension(nwbfiles[0])
        add_simple_table(nwbfiles[0])
        add_flipped_data_orientation_to_acquisition(nwbfiles[1])

        cls.nwbfile_paths = [str(cls.tempdir / f"testing{j}.nwb") for j in range(num_nwbfiles)]
        for nwbfile_path, nwbfile in zip(cls.nwbfile_paths, nwbfiles):
            with NWBHDF5IO(path=nwbfile_path, mode="w") as io:
                io.write(nwbfile)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.tempdir)

    def test_inspect_nwbfile_dandi_config_critical_only_entire_registry(self):
        test_results = list(
            inspect_nwbfile(
                nwbfile_path=self.nwbfile_paths[0],
                checks=available_checks,
                config=load_config(filepath_or_keyword="dandi"),
                importance_threshold=Importance.CRITICAL,
            )
        )
        true_results = [
            InspectorMessage(
                message="Subject is missing.",
                importance=Importance.CRITICAL,  # Normally a BEST_PRACTICE_SUGGESTION
                check_function_name="check_subject_exists",
                object_type="NWBFile",
                object_name="root",
                location="/",
                file_path=self.nwbfile_paths[0],
            ),
            InspectorMessage(
                message="The length of the first dimension of data (4) does not match the length of timestamps (3).",
                importance=Importance.CRITICAL,
                check_function_name="check_timestamps_match_first_dimension",
                object_type="TimeSeries",
                object_name="test_time_series_3",
                location="/acquisition/test_time_series_3",
                file_path=self.nwbfile_paths[0],
            ),
        ]
        self.assertCountEqual(first=test_results, second=true_results)

    def test_inspect_nwbfile_dandi_config_violation_and_above_entire_registry(self):
        test_results = list(
            inspect_nwbfile(
                nwbfile_path=self.nwbfile_paths[1],
                checks=available_checks,
                config=load_config(filepath_or_keyword="dandi"),
                importance_threshold=Importance.BEST_PRACTICE_VIOLATION,
            )
        )
        true_results = [
            InspectorMessage(
                message="Subject is missing.",
                importance=Importance.CRITICAL,  # Normally a BEST_PRACTICE_SUGGESTION
                check_function_name="check_subject_exists",
                object_type="NWBFile",
                object_name="root",
                location="/",
                file_path=self.nwbfile_paths[1],
            ),
            InspectorMessage(
                message=(
                    "Data may be in the wrong orientation. Time should be in the first dimension, "
                    "and is usually the longest dimension. Here, another dimension is longer."
                ),
                importance=Importance.BEST_PRACTICE_VIOLATION,
                severity=Severity.LOW,
                check_function_name="check_data_orientation",
                object_type="TimeSeries",
                object_name="my_spatial_series",
                location="/acquisition/my_spatial_series",
                file_path=self.nwbfile_paths[1],
            ),
        ]
        self.assertCountEqual(first=test_results, second=true_results)

    def test_inspect_nwbfile_dandi_config_critical_only_entire_registry_cli(self):
        console_output_file_path = self.tempdir / "test_console_output.txt"

        os.system(
            f"nwbinspector {str(self.tempdir)} --overwrite --config dandi --threshold BEST_PRACTICE_VIOLATION"
            f"> {console_output_file_path}"
        )

        self.assertLogFileContentsEqual(
            test_file_path=console_output_file_path,
            true_file_path=Path(__file__).parent / "true_nwbinspector_report_with_dandi_config.txt",
            skip_first_newlines=True,
        )


class TestCheckUniqueIdentifiersPass(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.tempdir = Path(mkdtemp())
        num_nwbfiles = 3
        unique_id_nwbfiles = list()
        for j in range(num_nwbfiles):
            unique_id_nwbfiles.append(make_minimal_nwbfile())

        cls.unique_id_nwbfile_paths = [str(cls.tempdir / f"unique_id_testing{j}.nwb") for j in range(num_nwbfiles)]
        for nwbfile_path, nwbfile in zip(cls.unique_id_nwbfile_paths, unique_id_nwbfiles):
            with NWBHDF5IO(path=nwbfile_path, mode="w") as io:
                io.write(nwbfile)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.tempdir)

    def test_check_unique_identifiers_pass(self):
        assert list(inspect_all(path=self.tempdir, select=["check_data_orientation"])) == []


class TestCheckUniqueIdentifiersFail(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.tempdir = Path(mkdtemp())
        num_nwbfiles = 3
        non_unique_id_nwbfiles = list()
        for j in range(num_nwbfiles):
            non_unique_id_nwbfiles.append(
                NWBFile(
                    session_description="",
                    identifier="not a unique identifier!",
                    session_start_time=datetime.now().astimezone(),
                )
            )

        cls.non_unique_id_nwbfile_paths = [
            str(cls.tempdir / f"non_unique_id_testing{j}.nwb") for j in range(num_nwbfiles)
        ]
        for nwbfile_path, nwbfile in zip(cls.non_unique_id_nwbfile_paths, non_unique_id_nwbfiles):
            with NWBHDF5IO(path=nwbfile_path, mode="w") as io:
                io.write(nwbfile)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.tempdir)

    def test_check_unique_identifiers_fail(self):
        assert list(inspect_all(path=self.tempdir, select=["check_data_orientation"])) == [
            InspectorMessage(
                message=(
                    "The identifier 'not a unique identifier!' is used across the .nwb files: "
                    f"{natsorted([Path(x).name for x in self.non_unique_id_nwbfile_paths])}. "
                    "The identifier of any NWBFile should be a completely unique value - "
                    "we recommend using uuid4 to achieve this."
                ),
                importance=Importance.CRITICAL,
                check_function_name="check_unique_identifiers",
                object_type="NWBFile",
                object_name="root",
                location="/",
                file_path=str(self.tempdir),
            )
        ]


def test_dandi_config_in_vitro_injection():
    """Test that a subject_id starting with 'protein' excludes meaningless CRITICAL-elevated subject checks."""
    nwbfile = make_minimal_nwbfile()
    nwbfile.subject = Subject(
        subject_id="proteinCaMPARI3", description="A detailed description about the in vitro setup."
    )
    config = load_config(filepath_or_keyword="dandi")
    importance_threshold = "CRITICAL"
    messages = list(
        inspect_nwbfile_object(nwbfile_object=nwbfile, config=config, importance_threshold=importance_threshold)
    )
    assert messages == []


def test_dandi_config_in_vitro_injection():
    """Test the safe subject ID retrieval of the in vitro injection."""
    nwbfile = make_minimal_nwbfile()
    nwbfile.subject = Subject(subject_id=None, description="A detailed description about the in vitro setup.")
    config = load_config(filepath_or_keyword="dandi")
    messages = list(inspect_nwbfile_object(nwbfile_object=nwbfile, config=config))
    assert len(messages) != 0
