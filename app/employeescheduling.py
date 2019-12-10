from __future__ import print_function
from ortools.sat.python import cp_model



class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_nurses, num_days, num_shifts, bool_res, progs, prog_and_gpa, gpas, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._bool_res = bool_res
        self._progs = progs
        self._prog_and_gpa = prog_and_gpa
        self._gpas = gpas
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            # for d in range(self._num_days):
            #     print('Day %i' % d)
            #     for n in range(self._num_nurses):
            #         is_working = False
            #         for s in range(self._num_shifts):
            #             if self.Value(self._shifts[(n, d, s)]):
            #                 is_working = True
            #                 print('  Nurse %i works shift %i' % (n, s))
            #         if not is_working:
            #             print('  Nurse {} does not work'.format(n))
            # print()

            for p in self._progs:
                for g in gpas:
                    if self.Value(self._bool_res[(p)]) and self.Value(self._prog_and_gpa[(p,g)]):
                        print('This program: {} is recommended'.format(p))
                    else:
                    # print('This program: {} is NOT recommended'.format(p))
                        pass
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count




def main():
    # Data.
    num_nurses = 4
    num_shifts = 3
    num_days = 3
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d,
                                                                          s))
    # print('Shifts: ')
    # for s in shifts:
    #     print('{}'.format(s))

    # print('{}'.format(shifts))

    bool_res = {}
    prog_and_gpa = {}

    progs = ['BSCS', 'BSIT', 'BSMATH', 'BSSTAT']
    gpas = [1.0,1.5,1.75,2.0,2.5,2.75,3.0]
    intgpas = len(gpas)
    
    
    for p in progs:
        bool_res[(p)] = model.NewBoolVar('%s' % (p))
        for gpa in range(intgpas):
            print('{} : {}'.format(p,gpa))
            prog_and_gpa[(p, gpa)] = model.NewBoolVar('prog%s_gpa%d' % (p,gpa))

    print(prog_and_gpa)

    for p in progs:
        if (p != 'BSIT'):
            model.Add(bool_res[(p)] == 1)
        else:
            model.Add(bool_res[(p)] == 0)

        for g in gpas:
            if (p == 'BSCS') and (g < 2.0):
                model.Add(sum(prog_and_gpa[(p, g)]) == 1)
            else: 
                model.Add(sum(prog_and_gpa[(p, g)]) == 0)


    # Each shift is assigned to exactly one nurse in the schedule period.
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) == 1)

    # Each nurse works at most one shift per day.
    for n in all_nurses:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # min_shifts_per_nurse is the largest integer such that every nurse
    # can be assigned at least that many shifts. If the number of nurses doesn't
    # divide the total number of shifts over the schedule period,
    # some nurses have to work one more shift, for a total of
    # min_shifts_per_nurse + 1.
    min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
    max_shifts_per_nurse = min_shifts_per_nurse + 1
    for n in all_nurses:
        num_shifts_worked = sum(
            shifts[(n, d, s)] for d in all_days for s in all_shifts)
        model.Add(min_shifts_per_nurse <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_nurse)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first five solutions.
    a_few_solutions = range(5)
    solution_printer = NursesPartialSolutionPrinter(
        shifts, num_nurses, num_days, num_shifts, bool_res, progs, prog_and_gpa, gpas, a_few_solutions)
    solver.SearchForAllSolutions(model, solution_printer)

    # Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main()