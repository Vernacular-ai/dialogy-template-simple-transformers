"""
This module contains utilities for creating a default data directory.
A data directory for this template contains the following structure:

```
data
|-- <version>
    |-- classification
    |   |-- datasets
    |   |-- metrics
    |   +-- models
    +-- ner
        |-- datasets
        |-- metrics
        +-- models
```

Given a valid semver, the code here helps creating
and hence maintaining the uniformity of the directory structure here.
"""
import os
import shutil

import semver

from slu import constants as const


def create_data_directory(version: str, force: bool = False) -> None:
    """
    Create subdirectories.

    1. This function will check if `version` is a valid semver.
    2. Create a directory that contains a structure if it doesn't already exist.
        Unless `force=True`.

    Args:
        version (str): Semver for the dataset, model and metrics.
        force (bool, optional): Flag to overwrite existing directory. Defaults to False.
    """
    # This will raise an exception for invalid semver. So we don't have to catch it.
    semver.VersionInfo.parse(version)

    base_module_path = os.path.join(const.DATA, version)
    depth_level_1 = [const.CLASSIFICATION, const.NER]
    depth_level_2 = [const.DATASETS, const.METRICS, const.MODELS]

    for subdir in depth_level_1:
        for childdir in depth_level_2:
            # `exist_ok=False` is the default argument, it raises OSError if the path already exists.
            os.makedirs(
                os.path.join(base_module_path, subdir, childdir), exist_ok=force
            )


def copy_data_directory(copy_from: str, copy_to: str, force: bool = False) -> None:
    """
    Copy subdirectory.

    1. This function will check `copy_from` and `copy_to` are valid semver.
    2. This function will check `copy_to` doesn't already exist.
    3. Unless force = True, this function will not overwrite existing directory.

    Args:
        copy_from (str): semver -> Source directory.
        copy_to (str): semver -> Destination directory.
        force (bool, optional): Flag to overwrite existing directory. Defaults to False.
    """
    # This will raise an exception for invalid semver. So we don't have to catch it.
    semver.VersionInfo.parse(copy_from)
    semver.VersionInfo.parse(copy_to)

    source = os.path.join(const.DATA, copy_from)
    destination = os.path.join(const.DATA, copy_to)
    shutil.copytree(source, destination, dirs_exist_ok=force)
