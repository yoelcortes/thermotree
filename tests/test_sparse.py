# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020-2023, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentVector/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
import pytest
import numpy as np
from thermosteam.base import SparseVector, SparseArray, sparse_vector, sparse_array
from numpy.testing import assert_allclose

def test_sparse_vector_creation():
    arr = np.array([1., 2., 0., 4.5])
    sv = sparse_vector(arr)
    assert (sv.to_array() == arr).all()
    assert repr(sv) == 'SparseVector([1. , 2. , 0. , 4.5])'
    assert str(sv) == '[1.  2.  0.  4.5]'
    
    arr = np.array([1., 2., 0., 4.5, 0., 0.])
    sv = sparse_vector(arr)
    assert (sv.to_array() == arr).all()
    assert repr(sv) == 'SparseVector([1. , 2. , 0. , 4.5, 0. , 0. ])'
    assert str(sv) == '[1.  2.  0.  4.5 0.  0. ]'
    
def test_sparse_array_creation():
    arr = np.array([[1., 2., 0., 4.5]])
    sa = sparse_array(arr)
    assert (sa.to_array() == arr).all()
    assert repr(sa) == 'SparseArray([[1. , 2. , 0. , 4.5]])'
    assert str(sa) == '[[1.  2.  0.  4.5]]'
    
    arr = np.array([[1., 2., 0., 4.5, 0., 0.]])
    sa = sparse_array(arr)
    assert (sa.to_array() == arr).all()
    assert repr(sa) == 'SparseArray([[1. , 2. , 0. , 4.5, 0. , 0. ]])'
    assert str(sa) == '[[1.  2.  0.  4.5 0.  0. ]]'

def test_sparse_vector_math():
    arr = np.array([1., 2., 0., 4.5])
    sv = sparse_vector(arr)
    assert (sv * 2).sparse_equal(2 * arr)
    assert (sv + sv).sparse_equal(2 * arr)
    assert (sv * 0).sparse_equal([])
    assert (sv - sv).sparse_equal([])
    assert (sv / sv).sparse_equal(np.array([1., 1., 0., 1.]))
    
    sv *= 0.
    assert sv.sparse_equal([0.])
    
    sv += arr
    assert sv.sparse_equal(arr)
    
    sv *= 2
    assert sv.sparse_equal(2. * arr)

    sv /= 2.
    assert sv.sparse_equal(arr)
    
    sv /= sv
    assert sv.sparse_equal(np.array([1., 1., 0., 1.]))
    
    sv[:] *= 0.
    assert sv.sparse_equal([0.])
    
    sv[:] += arr
    assert sv.sparse_equal(arr)
    
    sv[:] *= 2
    assert sv.sparse_equal(2. * arr)

    sv[:] /= 2.
    assert sv.sparse_equal(arr)
    
    sv[:] /= sv
    assert sv.sparse_equal(np.array([1., 1., 0., 1.]))
    sv[:] = 1
    assert (2. / sv).sparse_equal([2., 2., 2., 2.])
    assert ([2, 1, 0, 3] / sv).sparse_equal([2, 1, 0, 3])
    
    sv[:] = [0., 1]
    with pytest.raises(FloatingPointError):
        print(repr([2, 1, 0.1, 3] / sv))

def test_sparse_array_math():
    arr = np.array([[1., 2., 0., 4.5], [0., 0., 1., 1.5]])
    sa = sparse_array(arr)
    assert (sa * 2).sparse_equal(2. * arr)
    assert (sa + sa).sparse_equal(2. * arr)
    assert (sa * 0).sparse_equal([[0.], [0.]])
    assert (sa - sa).sparse_equal([[0.], [0.]])
    assert (sa / sa).sparse_equal(np.array([[1., 1., 0., 1.], [0., 0., 1., 1.]]))
    
    sa *= 0.
    assert sa.sparse_equal([[0.], [0.]])
    
    sa += arr
    assert sa.sparse_equal(arr)
    
    sa -= arr
    assert sa.sparse_equal([[0.], [0.]])
    
    sa += arr
    assert sa.sparse_equal(arr)
    
    sa *= 2
    assert sa.sparse_equal(2. * arr)

    sa /= 2.
    assert sa.sparse_equal(arr)
    
    sa /= sa
    assert sa.sparse_equal(np.array([[1., 1., 0., 1.], [0., 0., 1., 1.]]))
    
    sa[:] *= 0.
    assert sa.sparse_equal([[0.], [0.]])
    
    sa[:] += arr
    assert sa.sparse_equal(arr)
    
    sa[:] -= arr
    assert sa.sparse_equal([[0.], [0.]])
    
    sa[:] += arr
    assert sa.sparse_equal(arr)
    
    sa[:] *= 2
    assert sa.sparse_equal(2. * arr)

    sa[:] /= 2.
    assert sa.sparse_equal(arr)
    
    sa[:] /= sa
    assert sa.sparse_equal(np.array([[1., 1., 0., 1.], [0., 0., 1., 1.]]))
    
def test_sparse_vector_indexing():
    arr = np.array([1., 2., 0., 4.5])
    sv = sparse_vector(arr)
    assert sv.size == 4 # Size is not strict
    old_dct = sv.dct.copy()
    sv[20] = 0.
    assert sv.dct == old_dct
    sv[5] = 3.
    assert sv.sparse_equal(np.array([1., 2., 0., 4.5, 0., 3.]))
    sv[[1, 3]] = [0., 0.]
    assert sv.sparse_equal(np.array([1., 0., 0., 0., 0., 3.]))
    assert (sv[[0, 1, 5]] == np.array([1., 0., 3.])).all()
    assert sv[0] == 1.
    assert sv[4] == 0.
    assert sv[5] == 3.
    assert sv[10] == 0.
    sv[[0, 1, 5]] = 1.
    assert sv.sparse_equal(np.array([1., 1., 0., 0., 0., 1.]))
    sv[:] = 2.
    assert sv.size == 4
    assert sv.sparse_equal([2., 2., 2., 2.])
    sv[(1,)] = 3
    assert sv[(1,)] == sv[1] == 3
    assert (sv[([1, 2],)] == np.array([3, 2])).all()
    assert (sv[[1, 2]] == np.array([3, 2])).all()
    
    with pytest.raises(IndexError):
        sv[(1, 2)]
    with pytest.raises(IndexError):
        sv[(1, 2)] = 0.
    with pytest.raises(IndexError):
        sv[(1,)] = [0., 1]
    with pytest.raises(IndexError):
        sv[1] = [0., 1]

def test_sparse_array_indexing():
    arr = np.array([[1., 2., 0., 4.5], [0., 0., 1., 1.5]])
    sa = sparse_array(arr)
    
    old_rows = [i.copy() for i in sa.rows]
    sa[0, 20] = 0.
    assert (sa == old_rows).all()
    sa[0, 5] = 3.
    assert sa[0].sparse_equal(np.array([1., 2., 0., 4.5, 0., 3.]))
    assert sa.sparse_equal(
        np.array([[1., 2., 0., 4.5, 0., 3.],
                  [0., 0., 1., 1.5, 0,  0.]])
    )
    assert sa[[0, 1]].sparse_equal(sa)
    sa[0, [0, 1]] = [0., 0.]
    assert sa[0].sparse_equal(np.array([0. , 0. , 0. , 4.5, 0. , 3. ]))
    assert (sa[0, [0, 1, 5]] == np.array([0., 0., 3.])).all()
    assert sa[0, 0] == 0.
    assert sa[0, 4] == 0.
    assert sa[0, 5] == 3.
    assert sa[0, 10] == 0.
    sa[1] = 0
    assert sa[1].sparse_equal([])
    assert sa[0].sparse_equal(np.array([0. , 0. , 0. , 4.5, 0. , 3. ]))
    sa[:, 1] = 2
    assert sa.sparse_equal(
        np.array([[0., 2., 0., 4.5, 0., 3.],
                  [0., 2., 0., 0. , 0,  0.]])
    )
    sa[:, [1, 2]] = 1.
    assert sa.sparse_equal(
        np.array([[0., 1., 1., 4.5, 0., 3.],
                  [0., 1., 1., 0. , 0,  0.]])
    )
    sa[:] = 0
    assert sa.sparse_equal([])
    
    arr = np.array([1., 2., 0., 4.5])
    sv = sparse_vector(arr)
    sa[0, :] = sv
    assert sa[0, :].sparse_equal(arr)
    sa[0, :] = 0.
    assert sa[0, :].sparse_equal([])
    sa[[0, 1], :] = sv
    assert sa.sparse_equal(
        [[1., 2., 0., 4.5],
         [1., 2., 0., 4.5]]
    )
    sa[[0, 1], :] = [0, 1, 0]
    assert sa.sparse_equal(
        [[0, 1],
         [0, 1]]
    )
    sa[[0, 1], :] = [[0, 1], [1, 0]]
    assert sa.sparse_equal(
        [[0, 1],
         [1, 0]]
    )
    sa[:] = 0
    sa[:, [1, 3]] = [[0, 1],
                     [1, 0]]
    assert sa.sparse_equal(
        [[0, 0, 0, 1],
         [0, 1, 0, 0]]
    )
    sa[:] = 2.
    assert sa.sparse_equal(
        [[2., 2., 2., 2.],
         [2., 2., 2., 2.]]
    )
    sa[[0, 1], :] = 3.
    assert sa.sparse_equal(
        [[3., 3., 3., 3.],
         [3., 3., 3., 3.]]
    )
    with pytest.raises(IndexError):
        sa[[[0, 1], [2, 3]]] = 2
    
    sa[[0, 1], [2, 3]] = 2
    assert (sa[[0, 1], [2, 3]] == np.array([2., 2.])).all()
    assert sa.sparse_equal(
        [[3., 3., 2., 3.],
         [3., 3., 3., 2.]]
    )

    sa_not_a_view = sa[:, [1, 2]]
    with pytest.raises(ValueError):
        sa_not_a_view[:] = 20
    
    assert (sa_not_a_view ==
        [[3., 2.],
         [3., 3.]]
    ).all()

def test_sparse_array_boolean_indexing():
    arr = np.array([[1., 0.], [0., 1.]])
    sa = sparse_array(arr)
    assert (sa[sa == 0] == arr[arr == 0]).all()
    sa[sa == 0] = 1.
    arr[arr == 0] = 1.
    assert (sa == arr).all()
    sa[sa == 1] = [0., 1, 1, 0.]
    arr[arr == 1] = [0., 1, 1, 0.]
    assert (sa == arr).all()

def test_sparse_vector_boolean_indexing():
    arr = np.array([1., 0., 0., 1.])
    sv = sparse_vector(arr)
    assert (sv[sv == 0] == arr[arr == 0]).all()
    sv[sv == 0] = 1.
    arr[arr == 0] = 1.
    assert (sv == arr).all()
    sv[sv == 1] = [0., 1, 1, 0.]
    arr[arr == 1] = [0., 1, 1, 0.]
    assert (sv == arr).all()

def test_sparse_vector_special_methods():
    arr = np.array([1., 2., 0., 4.5])
    sv = sparse_vector(arr)
    assert (sv.to_flat_array() == np.array([1., 2., 0., 4.5])).all()
    sv.from_flat_array(np.array([1., 2., 0., 2]))
    assert (sv.to_flat_array() == np.array([1., 2., 0., 2])).all()
    
    arr = np.array([[1., 2., 0., 4.5], [1., 2., 0., 4.5]])
    sa = sparse_array(arr)
    
    assert (sa.to_flat_array() == np.array([1., 2., 0., 4.5, 1., 2., 0., 4.5])).all()
    sa.from_flat_array(np.array([1., 2., 0., 2, 1., 2., 0., 2]))
    assert (sa == np.array([[1., 2., 0., 2], [1., 2., 0., 2]])).all()

def test_sparse_array_special_methods():
    arr = np.array([[1., 2., 0., 4.5], [0., 0., 1., 1.5]])
    sa = sparse_array(arr)
    assert (sa.to_flat_array() == np.array([1., 2., 0., 4.5, 0., 0., 1., 1.5])).all()
    sa.from_flat_array(np.array([1., 2., 0., 0, 0., 0., 1., 2]))
    assert (sa.to_flat_array() == np.array([1., 2., 0., 0, 0., 0., 1., 2])).all()

def test_sparse_vector_methods_vs_numpy():
    arrays = [
        np.array([1., 2., 0., 4.5]),
        np.zeros(3),
        np.ones(3),
    ]
    for arr in arrays:
        sv = sparse_vector(arr)
        for method in ('min', 'max', 'argmin', 'argmax', 'mean', 'sum', 'any', 'all'):
            sv_method = getattr(sv, method)
            arr_method = getattr(arr, method)
            for axis in (0, None, 1):
                for keepdims in (False, True):
                    if axis == 1:
                        with pytest.raises(ValueError):
                            np.asarray(sv_method(axis=axis, keepdims=keepdims))
                        with pytest.raises(ValueError): # For good measure
                            arr_method(axis=axis, keepdims=keepdims)
                        continue
                    sv_result = np.asarray(sv_method(axis=axis, keepdims=keepdims))
                    arr_result = arr_method(axis=axis, keepdims=keepdims)
                    assert sv_result.shape == arr_result.shape, f"wrong shape in SparseVector.{method} with axis {axis} and keepdims {keepdims}"
                    assert (sv_result == arr_result).all(), f"wrong value in SparseVector.{method} with axis {axis} and keepdims {keepdims}"

def test_sparse_array_methods_vs_numpy():
    arrays = [
        np.array([[1., 2., 0., 4.5], [0., 0., 1., 1.5]]),
        np.zeros([2, 3]),
        np.ones([2, 3]),
    ]
    for arr in arrays:
        sa = sparse_array(arr)
        for method in ('min', 'max', 'argmin', 'argmax', 'mean', 'sum', 'any', 'all'):
            sa_method = getattr(sa, method)
            arr_method = getattr(arr, method)
            for axis in (0, 1, None, 2):
                for keepdims in (False, True):
                    if axis == 2:
                        with pytest.raises(ValueError):
                            np.asarray(sa_method(axis=axis, keepdims=keepdims))
                        with pytest.raises(ValueError): # For good measure
                            arr_method(axis=axis, keepdims=keepdims)
                        continue
                    sa_result = np.asarray(sa_method(axis=axis, keepdims=keepdims))
                    arr_result = arr_method(axis=axis, keepdims=keepdims)
                    assert sa_result.shape == arr_result.shape, f"wrong shape in SparseArray.{method} with axis {axis} and keepdims {keepdims}"
                    assert (sa_result == arr_result).all(), f"wrong value in SparseArray.{method} with axis {axis} and keepdims {keepdims}"


if __name__ == '__main__':
    test_sparse_vector_creation()
    test_sparse_array_creation()
    test_sparse_vector_math()
    test_sparse_array_math()
    test_sparse_vector_indexing()
    test_sparse_array_indexing()
    test_sparse_vector_boolean_indexing()
    test_sparse_array_boolean_indexing()
    test_sparse_vector_special_methods()
    test_sparse_array_special_methods()
    test_sparse_vector_methods_vs_numpy()
    test_sparse_array_methods_vs_numpy()