import numpy as np
import sys

def validation_test(time_matrix, number_jobs, number_machines):

    for row in time_matrix:
        for element in row:
            if element < 0:
                print("Error! Your time array has one or more negative elements!")
                sys.exit()

            elif number_jobs != len(row) or number_machines != len(time_matrix):
                print(f"Error! Dimensions mismatch! Expected Matrix with ({number_machines} machines, {number_jobs} jobs), but got ({len(time_matrix)} machines, {len(row)} jobs).")
                sys.exit()

            else:
                pass
