from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from app import app, db
from app.models import *

from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('%s=%i' % (v, self.Value(v)), end=' ')
        print()

    def solution_count(self):
        return self.__solution_count


def SearchForAllSolutionsSampleSat():
    """Showcases calling the solver to search for all solutions."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    # num_vals = 3
    # x = model.NewIntVar(0, num_vals - 1, 'x')
    # y = model.NewIntVar(0, num_vals - 1, 'y')
    # z = model.NewIntVar(0, num_vals - 1, 'z')

    progs = Program.query.filter_by(progcode).all()

    for prog in progs:
        if prog.progcode == semstudent.studmajor:
                model.Add(prog.progcode != semstudent.studmajor)
                print('Prog: %s' % prog)



    # Create a solver and solve.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(progs)
    status = solver.SearchForAllSolutions(model, solution_printer)

    print('Status = %s' % solver.StatusName(status))
    print('Number of solutions found: %i' % solution_printer.solution_count())

SearchForAllSolutionsSampleSat()