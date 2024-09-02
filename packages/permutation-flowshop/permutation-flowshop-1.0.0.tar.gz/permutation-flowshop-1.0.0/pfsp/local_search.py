import numpy as np

from pfsp.calculate_makespan import calculate_makespan
from pfsp.validations import validation_test

def local_search_swap_best_improvement(initial_solution, number_jobs, number_machines, constructive_makespan, time_matrix):

    validation_test(time_matrix, number_jobs, number_machines) #validation of time matrix

    solution = initial_solution
    best_local_search_makespan = constructive_makespan
    best = True
    while best == True:
        best = False
        for i in range(0, number_jobs-1):
            for j in range(i+1, number_jobs):
                swap = initial_solution[:]
                swap[i], swap[j] = swap[j],swap[i]

                #Best Improvement
                makespan = calculate_makespan(swap, number_jobs, number_machines, time_matrix)
                if makespan < best_local_search_makespan:
                    best_local_search_makespan = makespan
                    solution = swap.copy()
                    best = True

    return best_local_search_makespan, solution

def local_search_swap_first_improvement(initial_solution, number_jobs, number_machines, constructive_makespan, time_matrix):

    validation_test(time_matrix, number_jobs, number_machines) #validation of time matrix

    solution = initial_solution
    best_local_search_makespan = constructive_makespan
    best = True

    while best == True:
        for i in range(0, number_jobs-1):
            for j in range(i+1, number_jobs):
                swap = initial_solution[:]
                swap[i], swap[j] = swap[j],swap[i]

                #Best Improvement
                makespan = calculate_makespan(swap, number_jobs, number_machines, time_matrix)

                if makespan < best_local_search_makespan:
                    best_local_search_makespan = makespan
                    solution = swap.copy()
                    best = False
                    break

            if best == False:
                break

        #if not found best value needs break the iterations, otherwise stay in loop
        if best_local_search_makespan == constructive_makespan:
            break

        return best_local_search_makespan, solution
