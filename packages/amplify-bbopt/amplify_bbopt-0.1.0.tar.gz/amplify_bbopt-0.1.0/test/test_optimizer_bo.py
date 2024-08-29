# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
from typing import Annotated

import pytest
from amplify_bbopt import BayesianOptimizer, BinaryVariableList, DataList, DatasetGenerator, blackbox, logger


@blackbox
def objective_func_1(
    x: Annotated[list[bool], BinaryVariableList(length=3)],
):
    return sum(x)


assert logger.handler is not None
logger.handler.setLevel(logging.ERROR)


@pytest.fixture
def bo_optimizer(objective_func=objective_func_1):
    data = DatasetGenerator(objective=objective_func, seed=0).generate(num_samples=3)
    assert isinstance(data, DataList)
    return BayesianOptimizer(data, objective_func)


def test_bo_optimizer(bo_optimizer):
    assert bo_optimizer.i_cycle == 0

    assert bo_optimizer.num_initial_data == 3
    bo_optimizer.data.append(([True, False, True], 2))
    bo_optimizer.num_initial_data = 4

    with pytest.raises(ValueError) as _:
        # elapse_time does not have the same length as optimizer._data.
        _ = bo_optimizer.fetch_history()

    bo_optimizer._elapsed_time.append(0)  # noqa: SLF001
    history = bo_optimizer.fetch_history()
    print(history.history_df)

    assert len(history.history_df) == 4
    assert history.num_initial_data == 4

    bo_optimizer.optimize(num_cycles=1)

    assert "x" in bo_optimizer.best_solution
