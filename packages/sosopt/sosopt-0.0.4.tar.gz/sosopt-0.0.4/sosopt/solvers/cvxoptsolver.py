import math
import cvxopt
import numpy as np

from dataclassabc import dataclassabc

from polymat.typing import ArrayRepr

from sosopt.solvers.solveargs import SolveArgs
from sosopt.solvers.solverdata import SolverData
from sosopt.solvers.solvermixin import SolverMixin


@dataclassabc(frozen=True)
class CVXOptSolverResult(SolverData):
    x: np.ndarray
    y: np.ndarray
    s: np.ndarray
    z: np.ndarray
    status: str
    gap: float
    relative_gap: float
    primal_objective: float
    dual_objective: float
    primal_infeasibility: float
    dual_infeasibility: float
    primal_slack: float
    dual_slack: float
    iterations: int

    @property
    def solution(self) -> np.ndarray:
        return self.x
    
    @property
    def cost(self) -> float:
        return self.primal_objective


class CVXOPTSolver(SolverMixin):
    def solve(self, info: SolveArgs):
        def get_dim_s(array: ArrayRepr) -> int:
            dim = np.sqrt(array.n_eq)
            assert math.isclose(int(dim), dim), f'{dim=}'
            return int(dim)

        dim_l = sum(d.n_eq for d in info.l_data)
        dim_q = list(d.n_eq for d in info.q_data)
        dim_s = list(get_dim_s(d) for d in info.s_data)

        constraints = info.l_data + info.q_data + info.s_data

        q = info.lin_cost[1].T
        h = np.vstack(tuple(c[0] for c in constraints))
        G = np.vstack(tuple(-c[1] for c in constraints))

        if info.quad_cost is None:
            return_val = cvxopt.solvers.conelp(
                c=cvxopt.matrix(q),
                G=cvxopt.matrix(G), 
                h=cvxopt.matrix(h),
                dims={'l': dim_l, 'q': dim_q, 's': dim_s},
            )

        else:
            P = info.quad_cost[1].T @ info.quad_cost[1]

            return_val = cvxopt.solvers.coneqp(
                P=cvxopt.matrix(P), 
                q=cvxopt.matrix(q.reshape(-1, 1)),
                G=cvxopt.matrix(G), 
                h=cvxopt.matrix(h),
                dims={'l': dim_l, 'q': dim_q, 's': dim_s},
            )

        solver_result = CVXOptSolverResult(
            x=np.array(return_val['x']).reshape(-1),
            y=np.array(return_val['y']).reshape(-1),
            s=np.array(return_val['s']).reshape(-1),
            z=np.array(return_val['z']).reshape(-1),
            status=return_val['status'],
            gap=return_val['gap'],
            relative_gap=return_val['relative gap'],
            primal_objective=return_val['primal objective'],
            dual_objective=return_val['dual objective'],
            primal_infeasibility=return_val['primal infeasibility'],
            dual_infeasibility=return_val['dual infeasibility'],
            primal_slack=return_val['primal slack'],
            dual_slack=return_val['dual slack'],
            iterations=return_val['iterations'],
        )

        return solver_result