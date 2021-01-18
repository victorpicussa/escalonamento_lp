#!/usr/bin/python3
import sys

def define_data(file):
    # Support variables
    n = 0
    lines = 0
    counter = 0
    mach = -1
    times = []
    machines = []

    # Get file data
    for line in file:
        line_array = line.split(' ')
        if lines == 0:
            n = int(line_array[0])
            k = int(line_array[1])
            x = dict.fromkeys(((i,j) for i in range(1, n+1) for j in range(1, k+1)), 0)
        elif lines < (n + 1):
            times.append(int(line_array[0]))
        elif lines < (n + k + 1):
            machines.append([int(line_array[0]), int(line_array[1])])
        else:
            if counter == 0:
                counter = int(line)
                mach += 1
            else:
                x[int(line), mach+1] = 1
                counter -= 1
        lines += 1

    # Organize data into dictionaries
    h = {}
    for index in range(0, len(times)):
        h[index+1] = times[index]

    u = {}
    for index in range(0, len(machines)):
        u[index+1] = machines[index][1]

    c = {}
    for index in range(0, len(machines)):
        c[index+1] = machines[index][0]

    zeros = {}
    counter = 0
    for key in x.items():
        if x[key[0]] == 0:
            zeros[counter] = key[0]
            counter += 1

    # Create range arrays for solver
    N = range(1, n+1)
    K = range(1, k+1)

    return h, u, c, x, zeros, N, K
