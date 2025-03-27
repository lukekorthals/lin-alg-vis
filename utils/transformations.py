import numpy as np
from scipy.linalg import logm, expm
from settings.settings import WIDTH, HEIGHT, UNIT

def center_to_topleft(v: np.ndarray | list | tuple) -> np.ndarray:
    """Converts vector coordinates from center to top-left origin."""
    assert type(v) in [np.ndarray, list, tuple], "v must be a numpy array, list or tuple."
    return np.array(v) * UNIT * np.array((1, -1)) + np.array((WIDTH/2, HEIGHT/2))

def topleft_to_center(v: np.ndarray | list | tuple) -> np.ndarray:
    """Converts vector coordinates from top-left to center origin."""
    assert type(v) in [np.ndarray, list, tuple], "v must be a numpy array, list or tuple."
    return (np.array(v) - np.array((WIDTH/2, HEIGHT/2))) * np.array((1, -1)) / UNIT

# Tests
assert np.all(center_to_topleft(((0, 1), (1, 1), (0, 0))) == np.array(((400, 320), (480, 320), (400, 400)))), "Test for center_to_topleft failed"


def apply_transformation(v: np.ndarray | list | tuple, m: np.ndarray | list | tuple) -> np.ndarray:
    """Applies a transformation matrix to a vector."""
    assert type(v) in [np.ndarray, list, tuple], "v must be a numpy array, list or tuple."
    assert type(m) in [np.ndarray, list, tuple], "m must be a numpy array, list or tuple."
    m = np.array(m)
    v = np.array(v)
    if len(v.shape) == 1:
        return np.matmul(m, v)
    else:
        return np.matmul(m, v.T).T

# Tests
assert np.all(apply_transformation((0, 1), ((1, 0), (0, 2))) == np.array((0, 2))), "1. test for apply_transformation failed"
assert np.all(apply_transformation(((0, 1), (1, 0)), ((1, 0), (0, 2))) == np.array(((0, 2), (1, 0)))), "2. test for apply_transformation failed"


def get_matrices_for_smooth_transformation(m: np.ndarray | list | tuple, 
                                           steps: int = 100, 
                                           identity: np.ndarray | list | tuple = np.eye(2)) -> np:
    """Returns a list of transformation matrices to smoothly transform from the identity matrix to `m`."""
    assert type(m) in [np.ndarray, list, tuple], "m must be a numpy array, list or tuple."
    assert type(identity) in [np.ndarray, list, tuple], "identity must be a numpy array, list or tuple."
    m = np.array(m)
    identity_m = np.array(identity)
    transformations = np.linspace(identity_m, m, steps)
    return transformations


