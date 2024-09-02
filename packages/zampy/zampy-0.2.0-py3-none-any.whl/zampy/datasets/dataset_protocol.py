"""Outline of the dataset protocol."""

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Protocol
import numpy as np
import xarray as xr


FNAME_PROPERTIES = "properties.json"


@dataclass
class Variable:
    """zampy variable."""

    name: str
    unit: Any  # pint unit. typing has issues with pint 0.21
    desc: str | None = ""


@dataclass
class SpatialBounds:
    """zampy spatial bounds object."""

    north: float
    east: float
    south: float
    west: float

    def __post_init__(self) -> None:
        """Validate the initialized SpatialBounds class."""
        if self.south > self.north:
            raise ValueError(
                "Value of southern bound is greater than northern bound."
                "\nPlease check the spatial bounds input."
            )
        if self.west > self.east:
            raise ValueError(
                "Value of western bound is greater than eastern bound."
                "\nPlease check the spatial bounds input."
            )


@dataclass
class TimeBounds:
    """zampy time bounds object.

    Note: the bounds are closed on both sides.
    """

    start: np.datetime64
    end: np.datetime64

    def __post_init__(self) -> None:
        """Validate the initialized TimeBounds class."""
        if self.end < self.start:
            raise ValueError("Start time should be smaller than end time.")


class Dataset(Protocol):
    """Zampy Dataset.

    Methods:
        download: Download data from this dataset.
        ingest: Convert the raw data to a CF-compliant format.
        load: Load the data into an xarray Dataset.
    """

    name: str
    time_bounds: TimeBounds
    spatial_bounds: SpatialBounds
    crs: str
    license: str
    bib: str
    raw_variables: list[Variable]
    variable_names: list[str]
    variables: list[Variable]

    def __init__(self) -> None:
        """Init."""
        ...

    def download(
        self,
        download_dir: Path,
        time_bounds: TimeBounds,
        spatial_bounds: SpatialBounds,
        variable_names: list[str],
        overwrite: bool = False,
    ) -> bool:
        """Download the data.

        Args:
            download_dir: Path to the Zampy download directory.
            time_bounds: The start and end time of the data that should be loaded.
            spatial_bounds: The lat/lon bounding box for which the data should be
                loaded.
            variable_names: Which variables should be loaded.
            overwrite: Overwrite existing files instead of skipping them.

        Returns:
            Download success
        """
        ...

    def ingest(
        self,
        download_dir: Path,
        ingest_dir: Path,
        overwrite: bool = False,
    ) -> bool:
        """Convert the downloaded data to the CF-like Zampy convention.

        Args:
            download_dir: Path to the Zampy download directory.
            ingest_dir: Path to the Zampy ingest directory.
            overwrite: Overwrite existing files instead of skipping them.

        Returns:
            Ingest succes.
        """
        ...

    def load(
        self,
        ingest_dir: Path,
        time_bounds: TimeBounds,
        spatial_bounds: SpatialBounds,
        resolution: float,
        variable_names: list[str],
    ) -> xr.Dataset:
        """Get the dataset as an xarray Dataset.

        Args:
            ingest_dir: Path to the Zampy ingest directory.
            time_bounds: The start and end time of the data that should be loaded.
            spatial_bounds: The lat/lon bounding box for which the data should be
                loaded.
            resolution: The desired resolution of the loaded data. The ingested data
                will be regridded to match this resolution.

            variable_names: Which variables should be loaded.

        Returns:
            The desired data loaded as an xarray Dataset.
        """
        ...

    def convert(
        self,
        ingest_dir: Path,
        convention: str,
    ) -> bool:
        """Format variables to follow the desired convention.

        Args:
            ingest_dir: Path to the Zampy ingest directory.
            convention: Conventions for model forcing and outputs.

        Returns:
            The formatted data as an xarray Dataset.
        """
        ...


def write_properties_file(
    dataset_folder: Path,
    spatial_bounds: SpatialBounds,
    time_bounds: TimeBounds,
    variable_names: list[str],
) -> None:
    """Write the (serialized) spatial and time bounds to a json file.

    Args:
        dataset_folder: Path to the dataset folder (download/preprocessing).
        spatial_bounds: Spatial bounds of the data.
        time_bounds: Time bounds of the data.
        variable_names: The (standard) variable names of the data.
    """
    # Data to be written
    json_dict = {
        "start_time": str(time_bounds.start),
        "end_time": str(time_bounds.end),
        "north": spatial_bounds.north,
        "east": spatial_bounds.east,
        "south": spatial_bounds.south,
        "west": spatial_bounds.west,
        "variable_names": variable_names,
    }

    json_object = json.dumps(json_dict, indent=4)

    with (dataset_folder / FNAME_PROPERTIES).open(mode="w", encoding="utf-8") as file:
        file.write(json_object)


def read_properties_file(
    dataset_folder: Path,
) -> tuple[SpatialBounds, TimeBounds, list[str]]:
    """Load the serialized spatial and time bounds from the json file.

    Args:
        dataset_folder: Path to the dataset folder (download/preprocessing).

    Returns:
        Tuple[SpatialBounds, TimeBounds]: The spatial and time bounds of the data.
    """
    with (dataset_folder / FNAME_PROPERTIES).open(mode="r", encoding="utf-8") as file:
        json_dict = json.load(file)

    return (
        SpatialBounds(
            json_dict["north"],
            json_dict["east"],
            json_dict["south"],
            json_dict["west"],
        ),
        TimeBounds(start=json_dict["start_time"], end=json_dict["end_time"]),
        json_dict["variable_names"],
    )


def copy_properties_file(
    source_folder: Path,
    target_folder: Path,
) -> None:
    """Copy the properties file from one folder to another.

    To be used when, for example, the downloaded data has been ingested.

    Args:
        source_folder: Source folder containing the properties file.
        target_folder: Destination folder where the file should be copied to.
    """
    shutil.copy(source_folder / FNAME_PROPERTIES, target_folder / FNAME_PROPERTIES)
