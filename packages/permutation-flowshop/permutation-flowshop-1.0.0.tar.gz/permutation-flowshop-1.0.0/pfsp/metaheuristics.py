import numpy as np
import pandas as pd
import random as rd
import time

from pfsp.local_search import local_search_swap_best_improvement, local_search_swap_first_improvement
from pfsp.earliest_time_makespan_calculate import earliest_time_makespan_calculate, earliest_time
from pfsp.calculate_makespan import calculate_makespan
from pfsp.validations import validation_test

def multistart(number_jobs, number_machines, time_matrix, starts, ls, logs):
    best_makespan = np.inf
    best_sequence = []
    elapsed_time = 0
    iterations = 0
    local_search = None
    completion_time_matrix = np.zeros((number_machines, number_jobs), dtype=np.float64)

    validation_test(time_matrix, number_jobs, number_machines)

    if ls == 'swapbi':
        local_search = local_search_swap_best_improvement
        print("\nUsing Swap operator with Best Improvent Strategy...\n")

    elif ls == 'swapfi':
        local_search = local_search_swap_first_improvement
        print("\nUsing Swap operator with First Improvent Strategy...\n")

    else:
        local_search = False

    initial_time = time.time()

    while iterations < starts:

        initial_solution = np.random.permutation(number_jobs).tolist()

        # calculating constructive makespan
        constructive_makespan = calculate_makespan(initial_solution, number_jobs, number_machines, time_matrix)
        # Executing local search
        local_search_makespan, local_search_sequence = local_search(initial_solution, number_jobs, number_machines, constructive_makespan, time_matrix)

        # Updating best solution found
        if local_search_makespan < best_makespan:
            best_makespan = local_search_makespan
            best_sequence = local_search_sequence
            if logs == True:
                # print("Contructive Solution: ", initial_solution)
                print(f"Iteration: {iterations}. \nContructive Makespan = {constructive_makespan}; Local Search Makespan = {local_search_makespan};")
                print("Current Best Sequence: ", best_sequence)
            else:
                pass

        iterations += 1

    end_time = time.time()
    elapsed_time = round(end_time - initial_time, 4)

    print("\nBest Sequence Found: ", best_sequence)
    print("Best Makespan Found: ", best_makespan)
    print("Number of iterations performed: ", iterations)
    print(f"Best solution found in {elapsed_time} (seconds)")

    earliest_completion_time, makespan = earliest_time_makespan_calculate(best_sequence, time_matrix, number_machines, number_jobs)

    # Collect completion times in the matrix
    for j in range(number_machines):
        for index, job in enumerate(best_sequence):
            machine = j
            end_time = earliest_completion_time[j][index] + time_matrix[j][job]
            completion_time_matrix[machine][index] = end_time
    print("\n===== Completion Time matrix ======")
    print(completion_time_matrix)
    print()


    return best_sequence, best_makespan, iterations, elapsed_time, completion_time_matrix
