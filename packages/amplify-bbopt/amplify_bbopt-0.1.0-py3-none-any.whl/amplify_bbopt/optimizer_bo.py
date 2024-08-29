# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

import GPyOpt
import numpy as np

if TYPE_CHECKING:
    from .bb_func import BlackBoxFuncBase
    from .data_list import DataList

from .history import History
from .logger import logger
from .misc import exec_func_neat_stdout, header_obj, long_line, print_to_str
from .optimizer import OptimizerBase
from .solution_type import FlatSolution
from .variable import VariableBase, VariableListBase


class BayesianOptimizer(OptimizerBase):
    """Class for Bayesian optimizer implemented based on the GPyOpt library: https://gpyopt.readthedocs.io/en/."""

    def __init__(
        self,
        data: DataList,
        objective: BlackBoxFuncBase,
        optimizer_params: dict[str, Any] | None = None,
    ) -> None:
        """Initialize Bayesian optimizer.

        Args:
            data (DataList): Initial training dataset.
            objective (BlackBoxFuncBase): A black-box function class instance created with :obj:`blackbox` decorator.
            optimizer_params (dict[str, Any] | None, optional): Optimization parameters for Bayesian optimization. :obj:`BayesianOptimizer` automatically specifies `f`, `domain`, `X` and `Y` of these arguments. The users needs to specify other parameters. See: https://gpyopt.readthedocs.io/en/latest/GPyOpt.methods.html. When `optimizer_params` is set as `None`, the following default parameter set is considered: `{"model_type": "GP", "acquisition_type": "EI", "de_duplication": True, "maximize": False}`. Defaults to None.

        Raises:
            ValueError: If hard constraints are specified.
        """  # noqa: E501
        if optimizer_params is None:
            optimizer_params = {"model_type": "GP", "acquisition_type": "EI", "de_duplication": True, "maximize": False}

        if len(objective.constraints) > 0:
            raise ValueError(f"BayesianOptimizer does not consider hard constraints. {len(objective.constraints)=}")

        super().__init__(data, objective, 1.0)

        def obj_func(*args: list) -> float:
            inp = args[0][0]
            sol_dict = FlatSolution(self.objective.variables, inp).to_structured().to_solution_dict()
            return exec_func_neat_stdout(header_obj, self._objective._call_objective, logger(), **sol_dict)  # type: ignore # noqa: SLF001

        self._objective_func = obj_func

        self._domain: list[dict[str, Any]] = []

        def get_domain(v: VariableBase) -> dict:
            type_str = "discrete"
            domain: tuple | list | None = None
            if v.discrete_domain is not None:
                domain = v.discrete_domain
            if domain is None:
                type_str = "continuous"
                domain = v.bounds
            return {"name": v.name, "type": type_str, "domain": domain}

        for var in self.objective.variables.var_dict.values():
            if isinstance(var, VariableListBase):
                for v in var:
                    self._domain.append(get_domain(v))
            else:
                self._domain.append(get_domain(var))

        self._optimizer_params = optimizer_params

        self._elapsed_time: list[float] = [0.0] * len(self._data)

    @property
    def optimizer_params(self) -> dict:
        """Optimization parameters for the Bayesian optimizer."""
        return self._optimizer_params

    def optimize(self, num_cycles: int = 10) -> None:
        # https://nbviewer.org/github/SheffieldML/GPyOpt/blob/devel/manual/GPyOpt_external_objective_evaluation.ipynb
        """A function to execute black-box optmization with Bayesian optimization.

        Args:
            num_cycles (int, optional): A number of optimization iterations. Defaults to 10.
        """
        start = time.perf_counter()

        for self._i_cycle in range(num_cycles):
            logger().info(long_line)
            logger().info(f"#{self._i_cycle + 1}/{num_cycles} optimization cycle")

            self._x = np.array(self._data.x)
            self._y = np.array(self._data.y).reshape(-1, 1)

            self._bo = GPyOpt.methods.BayesianOptimization(
                f=self._objective_func,
                domain=self._domain,
                X=self._x,
                Y=self._y,
                **self._optimizer_params,
            )

            x_hat = self._bo.suggest_next_locations(ignored_X=self._x)
            y_hat = self._objective_func(x_hat)

            self._data.append((x_hat[0].tolist(), y_hat))
            self.set_best()

            logger().info(f"{y_hat=:.3e}, best objective={self.best_objective:.3e}")

            self._elapsed_time.append(time.perf_counter() - start)

    def fetch_history(self) -> History:
        """Return the optimization history.

        Returns:
            History: The optimization history.
        """
        return History(
            self._data,
            elapsed_time=self._elapsed_time,
            num_initial_data=self._num_initial_data,
        )

    def __str__(self) -> str:
        """Some human-readable information relevant to the optimizer.

        Returns:
            str: human-readable information of the optimizer.
        """
        variables = self._objective.variables
        ret = print_to_str(f"num variables: {len(variables)}")
        ret += print_to_str(f"num elemental variables: {variables.num_elemental_variables}")
        ret += print_to_str(f"parameters: {self._optimizer_params}")
        return ret
