"""Canonicalize and solve a system of equations."""

import numpy as np

import common_types as ct


def canonicalize(eqs: list[ct.Equation]) -> ct.CanonicalEquationSystem:
    variable_names = set()
    for eq in eqs:
        for side in (eq.left_side, eq.right_side):
            for term in side.terms:
                if term.variable_name:
                    variable_names.add(term.variable_name)
    variable_names = sorted(variable_names)
    var_coefficients = np.zeros((len(eqs), len(variable_names)), dtype=int)
    free_coefficients = np.zeros((len(eqs), 1), dtype=int)
    for n_eq, eq in enumerate(eqs):
        for multiplier, side in [(1, eq.left_side), (-1, eq.right_side)]:
            for term in side.terms:
                if term.variable_name:
                    variable_idx = variable_names.index(term.variable_name)
                    var_coefficients[n_eq, variable_idx] += multiplier * term.coefficient
                else:
                    free_coefficients[n_eq] += -multiplier * term.coefficient
    return ct.CanonicalEquationSystem(
        var_names=variable_names,
        var_coefficients=var_coefficients,
        free_coefficients=free_coefficients
    )

