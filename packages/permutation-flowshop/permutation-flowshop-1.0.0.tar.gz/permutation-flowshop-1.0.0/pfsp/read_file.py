

def read_file(file):
    with open(file, 'r') as file:
        first_line = file.readline().split()
        number_jobs, number_machines = map(int, first_line[:2])
        time_matrix_mean = [list(map(int, linha.split())) for linha in file]

    return number_jobs, number_machines, time_matrix_mean
