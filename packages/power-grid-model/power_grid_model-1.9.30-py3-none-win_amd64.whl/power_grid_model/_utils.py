# SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
#
# SPDX-License-Identifier: MPL-2.0

"""
This file contains helper functions for library-internal use only.

Disclaimer!

We do not officially support this functionality and may remove features in this library at any given time!
"""

from copy import deepcopy
from typing import Optional, cast

import numpy as np

from power_grid_model.core.data_handling import OutputType, process_output_component_types
from power_grid_model.core.dataset_definitions import ComponentType
from power_grid_model.data_types import (
    BatchComponentData,
    BatchDataset,
    BatchList,
    Dataset,
    DenseBatchArray,
    PythonDataset,
    SingleArray,
    SingleComponentData,
    SingleDataset,
    SinglePythonDataset,
    SparseBatchData,
)
from power_grid_model.typing import ComponentAttributeMapping


def is_nan(data) -> bool:
    """
    Determine if the data point is valid
    Args:
        data: a single scaler or numpy array

    Returns:
        True if all the data points are invalid
        False otherwise
    """
    nan_func = {
        np.dtype("f8"): lambda x: np.all(np.isnan(x)),
        np.dtype("i4"): lambda x: np.all(x == np.iinfo("i4").min),
        np.dtype("i1"): lambda x: np.all(x == np.iinfo("i1").min),
    }
    return bool(nan_func[data.dtype](data))


def convert_batch_dataset_to_batch_list(batch_data: BatchDataset) -> BatchList:
    """
    Convert batch datasets to a list of individual batches

    Args:
        batch_data: a batch dataset for power-grid-model

    Returns:
        A list of individual batches
    """

    # If the batch data is empty, return an empty list
    if len(batch_data) == 0:
        return []

    n_batches = get_and_verify_batch_sizes(batch_data=batch_data)

    # Initialize an empty list with dictionaries
    # Note that [{}] * n_batches would result in n copies of the same dict.
    list_data: BatchList = [{} for _ in range(n_batches)]

    # While the number of batches must be the same for each component, the structure (2d numpy array or indptr/data)
    # doesn't have to be. Therefore, we'll check the structure for each component and copy the data accordingly.
    for component, data in batch_data.items():
        if isinstance(data, np.ndarray):
            component_batches = split_numpy_array_in_batches(data, component)
        elif isinstance(data, dict):
            component_batches = split_sparse_batches_in_batches(data, component)
        else:
            raise TypeError(
                f"Invalid data type {type(data).__name__} in batch data for '{component}' "
                "(should be a Numpy structured array or a python dictionary)."
            )
        for i, batch in enumerate(component_batches):
            if batch.size > 0:
                list_data[i][component] = batch
    return list_data


def get_and_verify_batch_sizes(batch_data: BatchDataset) -> int:
    """
    Determine the number of batches for each component and verify that each component has the same number of batches

    Args:
        batch_data: a batch dataset for power-grid-model

    Returns:
        The number of batches
    """

    n_batch_size = 0
    checked_components: list[ComponentType] = []
    for component, data in batch_data.items():
        n_component_batch_size = get_batch_size(data)
        if checked_components and n_component_batch_size != n_batch_size:
            if len(checked_components) == 1:
                checked_components_str = f"'{checked_components.pop()}'"
            else:
                str_checked_components = [str(component) for component in checked_components]
                checked_components_str = "/".join(sorted(str_checked_components))
            raise ValueError(
                f"Inconsistent number of batches in batch data. "
                f"Component '{component}' contains {n_component_batch_size} batches, "
                f"while {checked_components_str} contained {n_batch_size} batches."
            )
        n_batch_size = n_component_batch_size
        checked_components.append(component)
    return n_batch_size


def get_batch_size(batch_data: BatchComponentData) -> int:
    """
    Determine the number of batches and verify the data structure while we're at it.

    Args:
        batch_data: a batch array for power-grid-model

    Returns:
        The number of batches
    """
    if isinstance(batch_data, np.ndarray):
        # We expect the batch data to be a 2d numpy array of n_batches x n_objects. If it is a 1d numpy array instead,
        # we assume that it is a single batch.
        if batch_data.ndim == 1:
            return 1
        return batch_data.shape[0]

    if isinstance(batch_data, dict):
        # If the batch data is a dictionary, we assume that it is an indptr/data structure (otherwise it is an
        # invalid dictionary). There is always one indptr more than there are batches.
        if "indptr" not in batch_data:
            raise ValueError("Invalid batch data format, expected 'indptr' and 'data' entries")
        indptr = batch_data["indptr"]
        if isinstance(indptr, np.ndarray):
            return indptr.size - 1

    # If the batch data is not a numpy array and not a dictionary, it is invalid
    raise ValueError(
        "Invalid batch data format, expected a 2-d numpy array or a dictionary with an 'indptr' and 'data' entry"
    )


def split_numpy_array_in_batches(data: DenseBatchArray | SingleArray, component: ComponentType) -> list[np.ndarray]:
    """
    Split a single dense numpy array into one or more batches

    Args:
        data: A 1D or 2D Numpy structured array. A 1D array is a single table / batch, a 2D array is a batch per table.
        component: The name of the component to which the data belongs, only used for errors.

    Returns:
        A list with a single numpy structured array per batch

    """
    if not isinstance(data, np.ndarray):
        raise TypeError(
            f"Invalid data type {type(data).__name__} in batch data for '{component}' "
            "(should be a 1D/2D Numpy structured array)."
        )
    if data.ndim == 1:
        return [data]
    if data.ndim == 2:
        return [data[i, :] for i in range(data.shape[0])]
    raise TypeError(
        f"Invalid data dimension {data.ndim} in batch data for '{component}' "
        "(should be a 1D/2D Numpy structured array)."
    )


def split_sparse_batches_in_batches(batch_data: SparseBatchData, component: ComponentType) -> list[SingleComponentData]:
    """
    Split a single numpy array representing, a compressed sparse structure, into one or more batches

    Args:
        batch_data: Sparse batch data
        component: The name of the component to which the data belongs, only used for errors.

    Returns:
        A list with a single numpy structured array per batch
    """

    for key in ["indptr", "data"]:
        if key not in batch_data:
            raise KeyError(
                f"Missing '{key}' in sparse batch data for '{component}' "
                "(expected a python dictionary containing two keys: 'indptr' and 'data')."
            )

    data = batch_data["data"]
    indptr = batch_data["indptr"]

    def _split_buffer(buffer: np.ndarray, scenario: int) -> SingleArray:
        if not isinstance(buffer, np.ndarray) or buffer.ndim != 1:
            raise TypeError(
                f"Invalid data type {type(buffer).__name__} in sparse batch data for '{component}' "
                "(should be a 1D Numpy structured array (i.e. a single 'table'))."
            )

        if not isinstance(indptr, np.ndarray) or indptr.ndim != 1 or not np.issubdtype(indptr.dtype, np.integer):
            raise TypeError(
                f"Invalid indptr data type {type(indptr).__name__} in batch data for '{component}' "
                "(should be a 1D Numpy array (i.e. a single 'list'), "
                "containing indices (i.e. integers))."
            )

        if indptr[0] != 0 or indptr[-1] != len(buffer) or indptr[scenario] > indptr[scenario + 1]:
            raise TypeError(
                f"Invalid indptr in batch data for '{component}' "
                f"(should start with 0, end with the number of objects ({len(buffer)}) "
                "and be monotonic increasing)."
            )

        return buffer[indptr[scenario] : indptr[scenario + 1]]

    def _get_scenario(scenario: int) -> SingleComponentData:
        if isinstance(data, dict):
            # return {attribute: _split_buffer(attribute_data, scenario) for attribute, attribute_data in data.items()}
            raise NotImplementedError()  # TODO(mgovers): uncomment when columnar data support is added
        return _split_buffer(data, scenario)

    return [_get_scenario(i) for i in range(len(indptr) - 1)]


def convert_dataset_to_python_dataset(data: Dataset) -> PythonDataset:
    """
    Convert internal numpy arrays to native python data
      If an attribute is not available (NaN value), it will not be exported.

    Args:
        data: A single or batch dataset for power-grid-model
    Returns:
        A python dict for single dataset
        A python list for batch dataset
    """

    # Check if the dataset is a single dataset or batch dataset
    # It is batch dataset if it is 2D array or a indptr/data structure
    is_batch: Optional[bool] = None
    for component, array in data.items():
        is_dense_batch = isinstance(array, np.ndarray) and array.ndim == 2
        is_sparse_batch = isinstance(array, dict) and "indptr" in array and "data" in array
        if is_batch is not None and is_batch != (is_dense_batch or is_sparse_batch):
            raise ValueError(
                f"Mixed {'' if is_batch else 'non-'}batch data "
                f"with {'non-' if is_batch else ''}batch data ({component})."
            )
        is_batch = is_dense_batch or is_sparse_batch

    # If it is a batch, convert the batch data to a list of batches, then convert each batch individually.
    if is_batch:
        # We have established that this is batch data, so let's tell the type checker that this is a BatchDataset
        data = cast(BatchDataset, data)
        list_data = convert_batch_dataset_to_batch_list(data)
        return [convert_single_dataset_to_python_single_dataset(data=x) for x in list_data]

    # We have established that this is not batch data, so let's tell the type checker that this is a BatchDataset
    data = cast(SingleDataset, data)
    return convert_single_dataset_to_python_single_dataset(data=data)


def convert_single_dataset_to_python_single_dataset(data: SingleDataset) -> SinglePythonDataset:
    """
    Convert internal numpy arrays to native python data
    If an attribute is not available (NaN value), it will not be exported.

    Args:
        data: A single dataset for power-grid-model

    Returns:
        A python dict for single dataset
    """

    # This should be a single data set
    for component, array in data.items():
        if not isinstance(array, np.ndarray) or array.ndim != 1:
            raise ValueError("Invalid data format")

    # Convert each numpy array to a list of objects, which contains only the non-NaN attributes:
    # For example: {"node": [{"id": 0, ...}, {"id": 1, ...}], "line": [{"id": 2, ...}]}
    return {
        component: [
            {attribute: obj[attribute].tolist() for attribute in objects.dtype.names if not is_nan(obj[attribute])}
            for obj in objects
        ]
        for component, objects in data.items()
    }


def copy_output_to_columnar_dataset(
    output_data: Dataset,
    output_component_types: ComponentAttributeMapping,
    output_type: OutputType,
    available_components: list[ComponentType],
) -> Dataset:
    """Temporary function to copy row based dataset to a column based dataset as per output_component_types.
    The purpose of this function is to mimic columnar data without any memory footprint benefits.

    Args:
        data (Dataset):
        component_types (_ComponentAttributeMappingDict):

    Returns:
        Dataset: converted to
    Args:
        output_data (Dataset): dataset to convert
        output_component_types (ComponentAttributeMapping): desired component and attribute mapping
        output_type (OutputType): output type sym or asym
        available_components (list[ComponentType]): available components in model

    Returns:
        Dataset: converted dataset
    """
    processed_output_types = process_output_component_types(output_type, output_component_types, available_components)

    result_data = {}
    for comp_name, attrs in processed_output_types.items():
        if comp_name not in output_data:
            continue
        if attrs is None:
            result_data[comp_name] = output_data[comp_name]
        elif isinstance(attrs, (list, set)) and len(attrs) == 0:
            result_data[comp_name] = {}
        else:
            result_data[comp_name] = {attr: deepcopy(output_data[comp_name][attr]) for attr in attrs}
    return result_data
