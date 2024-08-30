"""Tests for the algorithm class."""
import pytest

import algpy.dataset
import algpy.algorithm
from sklearn.cluster import KMeans
import numpy as np
from typing import List


# We will use this KMeans implementation throughout the tests.
def kmeans_impl(data: algpy.dataset.PointCloudDataset, k=10):
    sklearn_km = KMeans(n_clusters=k)
    sklearn_km.fit(data.data)
    return sklearn_km.labels_


def no_dataset_impl(n=10):
    return n ** 3


def test_algorithm():
    # Test the algorithm class as it is intended to be used.
    kmeans_algorithm = algpy.algorithm.Algorithm('kmeans',
                                                 kmeans_impl,
                                                 return_type=np.ndarray,
                                                 dataset_class=algpy.dataset.PointCloudDataset,
                                                 parameter_names=['k'])

    test_data = algpy.dataset.TwoMoonsDataset()
    _ = kmeans_algorithm.run(test_data, {'k': 8})


def test_bad_return_type():
    # Specify the wrong return type
    kmeans_algorithm = algpy.algorithm.Algorithm('kmeans',
                                                 kmeans_impl,
                                                 return_type=List,
                                                 dataset_class=algpy.dataset.PointCloudDataset,
                                                 parameter_names=['k'])

    test_data = algpy.dataset.TwoMoonsDataset()

    with pytest.raises(TypeError, match='return_type'):
        _ = kmeans_algorithm.run(test_data, {'k': 8})


def test_bad_parameter_names():
    # Specify the wrong parameter names
    kmeans_algorithm = algpy.algorithm.Algorithm('kmeans',
                                                 kmeans_impl,
                                                 return_type=np.ndarray,
                                                 dataset_class=algpy.dataset.PointCloudDataset,
                                                 parameter_names=['m'])

    test_data = algpy.dataset.TwoMoonsDataset()

    with pytest.raises(ValueError, match='parameter'):
        _ = kmeans_algorithm.run(test_data, {'k': 8})


def test_unspecified_parameter():
    # Test the algorithm class as it is intended to be used.
    kmeans_algorithm = algpy.algorithm.Algorithm('kmeans',
                                                 kmeans_impl,
                                                 return_type=np.ndarray,
                                                 dataset_class=algpy.dataset.PointCloudDataset,
                                                 parameter_names=['k'])

    # Not fully specifying the parameter is permitted when running.
    test_data = algpy.dataset.TwoMoonsDataset()
    _ = kmeans_algorithm.run(test_data, {})


def test_no_dataset():
    cube_algorithm = algpy.algorithm.Algorithm('power',
                                               no_dataset_impl,
                                               return_type=int,
                                               parameter_names=['n'])

    _ = cube_algorithm.run(algpy.dataset.NoDataset(), {'n': 20})


def test_wrong_dataset():
    cube_algorithm = algpy.algorithm.Algorithm('power',
                                               no_dataset_impl,
                                               return_type=int,
                                               parameter_names=['n'])

    with pytest.raises(TypeError, match='dataset'):
        _ = cube_algorithm.run(algpy.dataset.TwoMoonsDataset(), {'n': 20})
