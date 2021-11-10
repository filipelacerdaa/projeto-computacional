import numpy as np

from constants import *


def solve_differential_system(f, y0: np.ndarray, params: dict) -> np.ndarray:
    """
    Middle point method to solve differential system y' = f(t,y)
    with condition y(a) = y0 and using n points to compute y.

    Args:
        f (function): describes the derivative of y with respect to t.
        y0 (numpy array): values of y in the initial condition – y(a).
        params (dict): parameters (a, b and n) of differential system.

    Returns:
        numpy array: tabulated values of y.
    """
    
    eqs = np.shape(y0)[0]
    
    y = np.zeros((params["n"] + 1, eqs))
    y[0] = y0
    
    t = params["a"]
    h = (params["b"] - params["a"]) / params["n"]
    
    for i in range(1, params["n"] + 1):
        partial_y = y[i-1] + 0.5 * h * f(t, y[i-1])
        t += 0.5 * h
        
        y[i] = y[i-1] + h * f(t, partial_y)
        t += 0.5 * h
    
    return y


def func(t: float, y: np.ndarray) -> np.ndarray:
    """
    Compute the y derivative with respect to t.

    Args:
        t (float): interest value of t – ti.
        y (numpy array): y vector in format [S, E, I, R] computed in t = ti.

    Returns:
        numpy array: derivative of y – dy/dt
    """
    
    return np.array(
        [
            -CONSTANT_1 * y[0] * y[2],
            CONSTANT_1 * y[0] * y[2] - CONSTANT_2 * y[1],
            CONSTANT_2 * y[1] - CONSTANT_3 * y[2],
            CONSTANT_3 * y[2]
        ]
    )


def seir_model() -> dict:
    """
    Uses SEIR model to predict SARS-COV-19 pandemic evolution in SP state.

    Returns:
        dict: data (t, S, E, I, R) to plot the pandemic analysis.
    """
    
    params = {
        "a": 0.0,
        "b": 498.0,
        "n": 498
    }
    
    y0 = np.array([1.0 - 1.0e-6, 1.0e-6, 0.0, 0.0])
    
    y = solve_differential_system(func, y0, params)
    t = np.linspace(params["a"], params["b"], params["n"] + 1)
    
    return {
        "t": t,
        "S": y[:,0],
        "E": y[:,1],
        "I": y[:,2],
        "R": y[:,3]
    }