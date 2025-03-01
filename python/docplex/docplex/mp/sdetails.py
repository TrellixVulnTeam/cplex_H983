# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2015, 2016
# --------------------------------------------------------------------------
from docplex.mp.compat23 import StringIO

from math import isnan

from six import PY2 as SIX_PY2


class SolveDetails(object):
    """
    The :class:`SolveDetails` class contains the details of a solve.

    This class should never be instantiated. You get an instance of this class from
    the model by calling the property :data:`docplex.mp.model.Model.solve_details`.
    """

    _unknown_label = "*unknown*"

    NOT_A_NUM = float('nan')

    _NO_GAP = NOT_A_NUM  # value used when no gap is available
    _NO_BEST_BOUND = NOT_A_NUM

    def __init__(self, time=0,
                 status_code=-1, status_string=None,
                 problem_type=None,
                 ncolumns=0, nonzeros=0,
                 miprelgap=None,
                 best_bound=None,
                 n_iterations=0,
                 n_nodes_processed=0):
        self._time = max(time, 0)
        self._solve_status_code = status_code
        self._solve_status = status_string or self._unknown_label
        self._problem_type = problem_type or self._unknown_label  # string
        self._ncolumns = ncolumns
        self._linear_nonzeros = nonzeros
        # --
        self._solution_method = -1
        # --
        self._miprelgap = self._NO_GAP if miprelgap is None else miprelgap
        self._best_bound = self._NO_BEST_BOUND if best_bound is None else best_bound
        # -- progress
        self._n_iterations = n_iterations
        self._n_nodes_processed = n_nodes_processed

        self._md5 = self._unknown_label

        self._quality_metrics = {}

    def as_worker_dict(self):
        # INTERNAL
        # Converts the solve details to a dictionary for python worker...
        # using "legacy' keys from drop-solve
        worker_dict = {"MODEL_DETAIL_TYPE": self._problem_type,
                       "MODEL_DETAIL_NONZEROS": self._linear_nonzeros
                       }
        if not isnan(self._miprelgap):
            worker_dict["PROGRESS_GAP"] = self._miprelgap
        if not isnan(self._best_bound):
            worker_dict['PROGRESS_BEST_OBJECTIVE'] = self._best_bound
        return worker_dict

    _problemtype_map = {0: "LP",
                        1: "MILP",
                        3: "fixed_MILP",
                        4: "nodeLP",
                        5: "QP",
                        7: "MIQP",
                        8: "fixed_MIQP",
                        9: "node_QP",
                        10: "QCP",
                        11: "MIQCP",
                        12: "node_QCP"}

    @staticmethod
    def _convert_problemtype(probtype, probtype_map=_problemtype_map, unknown_probtype="unknown"):
        try:
            iprobe_type = int(probtype)
            return probtype_map.get(iprobe_type, unknown_probtype)
        except ValueError:
            return unknown_probtype

    @staticmethod
    def to_plain_str(arg_s):
        if SIX_PY2:  # we are in py2: docloud returns unicode.
            try:
                return arg_s.encode()  # if unicode strings , come from cplex worker
            except AttributeError:
                return str(arg_s)
        else:
            return arg_s  # in py3 do nothing.

    # ---
    # list of fields to be retrived from the details
    # as tuples: (<detail_attribute_name>, <json_attribute_name>, <type_conversion_fn>, <default_value>)
    # exemple:
    # _time denotes solve time, a float value, default is 0, to be found in json["cplex.time"]
    # ---
    _json_fields = (("_time", "cplex.time", float, 0),
                    ("_solve_status_code", "cplex.status", int, -1),
                    ("_solve_status", "cplex.statusstring", lambda s: SolveDetails.to_plain_str(s), ""),
                    ("_problem_type", "cplex.problemtype", lambda p: SolveDetails._convert_problemtype(p), ""),
                    ("_ncolumns", "cplex.columns", int, 0),
                    ("_linear_nonzeros", "MODEL_DETAIL_NON_ZEROS", int, 0),
                    ("_miprelgap", "cplex.miprelgap", float, _NO_GAP),
                    ('_best_bound', 'PROGRESS_BEST_OBJECTIVE', float, _NO_BEST_BOUND),
                    ("_md5", "cplex.model.md5", str, ""),
                    ('_n_iterations', 'cplex.itcount', int, 0)
                    )

    @staticmethod
    def from_json(json_details, all_json_fields=_json_fields):
        if not json_details:
            return SolveDetails.make_dummy()

        # for k,v in json_details.iteritems():
        # print("{0}: {1!s}".format(k, v))
        # print("# -------------------------")
        details = SolveDetails()
        for attr_name, field_name, field_conv_fn, field_default in all_json_fields:
            field_val = json_details.get(field_name, field_default)
            if field_conv_fn is not None:
                field_val = field_conv_fn(field_val)  # conversion
            setattr(details, attr_name, field_val)

        return details

    @staticmethod
    def make_dummy():
        dummy_details = SolveDetails(status_string="dummy")
        return dummy_details

    @staticmethod
    def make_fake_details(time, feasible):
        if feasible:
            status_code = 1
            status = "OPTIMAL"
        else:
            status_code = 3
            status = "infeasible"
        details = SolveDetails(time=time,
                               status_code=status_code, status_string=status,
                               problem_type=None)
        return details

    @property
    def time(self):
        """ This property returns the solve time in seconds.

        """
        return self._time

    @property
    def status_code(self):
        return self._solve_status_code


    # status string
    # CPX_STAT_ABORT_DETTIME_LIM =  25
    # CPX_STAT_ABORT_DUAL_OBJ_LIM =  22
    # CPX_STAT_ABORT_IT_LIM =  10
    # CPX_STAT_ABORT_OBJ_LIM =  12
    # CPX_STAT_ABORT_PRIM_OBJ_LIM =  21
    # CPX_STAT_ABORT_TIME_LIM =  11
    # CPX_STAT_ABORT_USER =  13
    # CPX_STAT_CONFLICT_ABORT_CONTRADICTION =  32
    # CPX_STAT_CONFLICT_ABORT_DETTIME_LIM =  39
    # CPX_STAT_CONFLICT_ABORT_IT_LIM =  34
    # CPX_STAT_CONFLICT_ABORT_MEM_LIM =  37
    # CPX_STAT_CONFLICT_ABORT_NODE_LIM =  35
    # CPX_STAT_CONFLICT_ABORT_OBJ_LIM =  36
    # CPX_STAT_CONFLICT_ABORT_TIME_LIM =  33
    # CPX_STAT_CONFLICT_ABORT_USER =  38
    # CPX_STAT_CONFLICT_FEASIBLE =  30
    # CPX_STAT_CONFLICT_MINIMAL =  31
    # CPX_STAT_FEASIBLE =  23
    # CPX_STAT_FEASIBLE_RELAXED_INF =  16
    # CPX_STAT_FEASIBLE_RELAXED_QUAD =  18
    # CPX_STAT_FEASIBLE_RELAXED_SUM =  14
    # CPX_STAT_FIRSTORDER =  24
    # CPX_STAT_INFEASIBLE =  3
    # CPX_STAT_INForUNBD =  4
    # CPX_STAT_NUM_BEST =  6
    # CPX_STAT_OPTIMAL =  1
    # CPX_STAT_OPTIMAL_FACE_UNBOUNDED =  20
    # CPX_STAT_OPTIMAL_INFEAS =  5
    # CPX_STAT_OPTIMAL_RELAXED_INF =  17
    # CPX_STAT_OPTIMAL_RELAXED_QUAD =  19
    # CPX_STAT_OPTIMAL_RELAXED_SUM =  15
    # CPX_STAT_UNBOUNDED =  2

    @property
    def status(self):
        """ This property returns the solve status as a string.

        Example:
            * Returns "optimal" when the solution has been proven optimal.
            * Returns "feasible" for a feasible, but not optimal, solution.
            * Returns "MIP_time_limit_feasible" for a MIP solution obtained before a time limit.

        """
        return self._solve_status


    @property
    def problem_type(self):
        """  This property returns the problem type as a string.

        """
        return self._problem_type

    @property
    def columns(self):
        """  This property returns the number of columns.
        """
        return self._ncolumns

    @property
    def nb_linear_nonzeros(self):
        """ This property returns the number of linear non-zeros in the matrix solved.

        """
        return self._linear_nonzeros

    @property
    def mip_relative_gap(self):
        """ This property returns the MIP relative gap.

        Note:
            * This property returns NaN when the problem is not a MIP.
            * The gap is returned as a floating-point value, not as a percentage.
        """
        return self._miprelgap


    @property
    def best_bound(self):
        """ This property returns the MIP best bound at the end of the solve.

        Note:
            * This property returns NaN when the problem is not a MIP.
        """
        return self._best_bound

    @property
    def nb_iterations(self):
        """ This property returns the number of iterations at the end of the solve.

        Note:
            The nature of the iterations depend on the algorithm usd to solve the model.
        """
        return self._n_iterations

    @property
    def nb_nodes_processed(self):
        """ This property returns the number of nodes processed at the end of solve.

        """
        return self._n_nodes_processed

    def __repr__(self):
        return "docplex.mp.SolveDetails(time={0:g},status={1!r})" \
            .format(self._time, self._solve_status)

    def print_information(self):
        print("status  = {0}".format(self._solve_status))
        print("time    = {0:g} s.".format(self._time))
        print("problem = {0}".format(self._problem_type))
        print("columns = {0:d}".format(self._ncolumns))
        print("iterations={0:d}".format(self._n_iterations))
        # print("nonzeros= {0}".format(self._linear_nonzeros))
        if self._miprelgap >= 0:
            print("gap     = {0:g}%".format(100 * self._miprelgap))


    def to_string(self):
        oss = StringIO()
        oss.write("status  = {0}\n".format(self._solve_status))
        oss.write("time    = {0:g} s.\n".format(self._time))
        oss.write("problem = {0}\n".format(self._problem_type))
        if self._miprelgap >= 0:
            oss.write("gap     = {0:g}%\n".format(100.0 * self._miprelgap))
        return oss.getvalue()

    def __str__(self):
        return self.to_string()

    _limit_statuses = frozenset({104,  # solution limit
                                 107, 108  # time limit
                                 })

    def has_hit_limit(self):
        """
        Checks if the solve details indicate that the solve has hit a limit.

        Returns:
          Boolean: True if the solve details indicate that the solve has hit a limit.

        """
        return self._solve_status_code in self._limit_statuses


    @property
    def quality_metrics(self):
        return self._quality_metrics

# cplex.miprelgap: 0
# cplex.quality.int.CPX_MAX_QCSLACK: -1
# MODEL_DETAIL_CONSTRAINTS: 78
# cplex.quality.int.CPX_MAX_SCALED_PRIMAL_RESIDUAL: 66
# cplex.quality.double.CPX_SUM_QCSLACK: 0
# cplex.semiintegers: 0
# cplex.solution.type: 3
# cplex.statusstring: integer optimal solution
# cplex.status: 101
# cplex.quality.double.CPX_SUM_PRIMAL_RESIDUAL: 2.10942374678779742680490016937255859375E-15
# cplex.quality.int.CPX_MAX_INDSLACK_INFEAS: -1
# cplex.numquad: 0
# cplex.quality.double.CPX_MAX_QCSLACK_INFEAS: 0
# cplex.quality.int.CPX_MAX_SLACK: 3
# cplex.quality.double.CPX_MAX_SCALED_X: 5.99999999999999911182158029987476766109466552734375
# cplex.quality.int.CPX_MAX_QCPRIMAL_RESIDUAL: -1
# cplex.quality.double.CPX_SUM_SCALED_SLACK: 10.608333333333337833437326480634510517120361328125
# MODEL_DETAIL_CONTINUOUS_VARS: 26
# cplex.nodes.processed: 0
# cplex.quality.double.CPX_MAX_SCALED_PRIMAL_INFEAS: 1.1102230246251565404236316680908203125E-15
# cplex.model.md5: B019A9CEBA436F0A65EAD04B9378517E
# MODEL_DETAIL_TYPE: MILP
# cplex.quality.double.CPX_MAX_PRIMAL_RESIDUAL: 4.44089209850062616169452667236328125E-16
# PROGRESS_CURRENT_OBJECTIVE: 144.266750000000001818989403545856475830078125
# cplex.quality.double.CPX_MAX_X: 5.99999999999999911182158029987476766109466552734375
# cplex.infeasible: false
# MODEL_DETAIL_NON_ZEROS: 189
# MODEL_DETAIL_BOOLEAN_VARS: 40
# MODEL_DETAIL_LINEAR_CONSTRAINTS: 78
# cplex.quality.double.CPX_SUM_SCALED_PRIMAL_RESIDUAL: 2.10942374678779742680490016937255859375E-15
# cplex.qpnonzeros: 0
# cplex.quality.int.CPX_MAX_PRIMAL_INFEAS: -62
# MODEL_DETAIL_INTEGER_VARS: 0
# cplex.quality.double.CPX_MAX_INDSLACK_INFEAS: 0
# cplex.quality.double.CPX_SUM_PRIMAL_INFEAS: 4.55191440096314181573688983917236328125E-15
# cplex.quality.double.CPX_SUM_SCALED_PRIMAL_INFEAS: 4.55191440096314181573688983917236328125E-15
# cplex.solution.dfeas: true
# cplex.quality.int.CPX_MAX_SCALED_PRIMAL_INFEAS: -62
# cplex.quality.double.CPX_MAX_QCSLACK: 0
# cplex.quality.double.CPX_SUM_X: 85.18333333333333712289459072053432464599609375
# cplex.quality.double.CPX_MAX_QCPRIMAL_RESIDUAL: 0
# cplex.quality.double.CPX_MAX_SLACK: 1.875
# cplex.indicatorconstraints: 0
# cplex.nodes.left: 0
# cplex.quality.double.CPX_SUM_QCPRIMAL_RESIDUAL: 0
# cplex.quality.double.CPX_MAX_SCALED_PRIMAL_RESIDUAL: 4.44089209850062616169452667236328125E-16
# PROGRESS_GAP: 4.930898076512417
# cplex.quality.double.CPX_SUM_QCSLACK_INFEAS: 0
# cplex.quality.int.CPX_MAX_QCSLACK_INFEAS: -1
# cplex.quality.double.CPX_SUM_INDSLACK_INFEAS: 0
# cplex.quality.double.CPX_MAX_PRIMAL_INFEAS: 1.1102230246251565404236316680908203125E-15
# cplex.quality.double.CPX_SUM_SCALED_X: 85.18333333333333712289459072053432464599609375
# cplex.quality.int.CPX_MAX_X: 1
# cplex.objective.sense: -1
# cplex.quality.int.CPX_MAX_PRIMAL_RESIDUAL: 66
# cplex.quality.double.CPX_MAX_INT_INFEAS: 7.7715611723760957829654216766357421875E-16
# cplex.solution.method: 12
# cplex.parameters.md5: B08B4BE748EC31D8D31294F0EBE7F26D
# cplex.time: 0.03053903579711914
# cplex.quality.int.CPX_MAX_SCALED_X: 1
# cplex.quality.double.CPX_SUM_INT_INFEAS: 1.5543122344752191565930843353271484375E-15
# cplex.columns: 66
# cplex.sosconstraints: 0
# cplex.mipitcount: 5
# cplex.quality.int.CPX_MAX_INT_INFEAS: 14
# cplex.problemtype: 1
# cplex.quality.double.CPX_MAX_SCALED_SLACK: 1.875
# cplex.solution.pfeas: true
# cplex.semicontinuous: 0
# cplex.quality.double.CPX_SUM_SLACK: 10.608333333333337833437326480634510517120361328125
# MODEL_DETAIL_QUADRATIC_CONSTRAINTS: 0
# cplex.mipabsgap: 0
# cplex.quality.int.CPX_MAX_SCALED_SLACK: 3
# cplex.dettime: 0.2523078918457031
# PROGRESS_BEST_OBJECTIVE: 144.266750000000001818989403545856475830078125
