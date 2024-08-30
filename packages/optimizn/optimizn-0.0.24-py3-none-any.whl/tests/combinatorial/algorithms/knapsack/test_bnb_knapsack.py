# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import numpy as np
from optimizn.combinatorial.algorithms.knapsack.bnb_knapsack\
    import KnapsackParams, ZeroOneKnapsackProblem
from tests.combinatorial.algorithms.check_sol_utils import check_bnb_sol,\
    check_sol, check_sol_vs_init_sol
from optimizn.combinatorial.branch_and_bound import BnBSelectionStrategy


def test_bnb_zeroone_knapsack():
    TEST_CASES = [
        # test case: (weights, values, capacity, initial solution, optimal
        # solution)
        (np.array([1, 25, 12, 12]), np.array([1, 24, 12, 12]), 25,
         [1, 0, 1, 1]),
        (np.array([10, 10, 15, 1]), np.array([20, 12, 54, 21]), 25,
         [0, 0, 1, 1]),
        (np.array([1, 3, 2, 5, 4]), np.array([10, 35, 20, 25, 5]), 4,
         [1, 1, 0, 0, 0])
    ]
    for bnb_selection_strategy in BnBSelectionStrategy:
        for weights, values, capacity, opt_sol in TEST_CASES:
            for bnb_type in [0, 1]:
                params = KnapsackParams(values, weights, capacity)
                kp = ZeroOneKnapsackProblem(params, bnb_selection_strategy)
                kp.solve(1000, 100, 120, bnb_type)

                # check final solution
                check_bnb_sol(kp, bnb_type, params)
                check_sol_vs_init_sol(kp.best_cost, kp.init_cost)

                # check final solution optimality
                check_sol(kp.best_solution, [opt_sol])
