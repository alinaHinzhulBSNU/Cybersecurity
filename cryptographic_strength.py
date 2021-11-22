import math
import traceback
from prettytable import PrettyTable


# Get speed of brute force (FLOPS)
def get_flops(frequency, cores_number, threads_number, cpu_number):
    return frequency * cores_number * threads_number * cpu_number * 10**9


# Get brute force time (SECONDS)
def get_brute_force_time(l, v):
    return 2 ** l / v


# Get Moor brute force time (SECONDS)
def get_moor_brute_force_time(l, v):
    return 5 * math.log10((2 ** l * (10**(1/5) - 1)) / (2 * 10 ** (1 / 5) * v) + 1)


# Add units to time
def format_time(time_in_seconds):
    if time_in_seconds / (31.536 * 10**6) > 1:
        return str(round(time_in_seconds / (31.536 * 10**6), 1)) + " years"
    elif time_in_seconds / (60 * 60 * 24) > 1:
        return str(round(time_in_seconds / (60 * 60 * 24), 1)) + " days"
    elif time_in_seconds / (60 * 60) > 1:
        return str(round(time_in_seconds / (60 * 60), 1)) + " hours"
    elif time_in_seconds / 60 > 1:
        return str(round(time_in_seconds / 60, 1)) + " minutes"
    else:
        return str(round(time_in_seconds, 1)) + " seconds"


# Result
def print_result_table(l_list, v):
    th = ["Key length(bit)", "Time", "Moor time"]
    table = PrettyTable(th)
    for l in l_list:
        time = format_time(get_brute_force_time(l, v))
        moor_time = format_time(get_moor_brute_force_time(l, v))
        table.add_row([l, time, moor_time])
    print(table)


if __name__ == '__main__':
    try:
        # KEY LENGTH
        l_list = []
        n = int(input("Size of list for key length: "))
        for i in range(0, n):
            l = int(input())
            l_list.append(l)

        # FLOPS
        frequency = float(input("Input base frequency (in GHz): "))
        cores_number = float(input("Input cores number: "))
        threads_number = float(input("Input threads number: "))
        cpu_number = float(input("Input CPU number: "))
        v = get_flops(frequency, cores_number, threads_number, cpu_number)
        print("\nSpeed is " + str(round(v, 1)) + " FLOPS\n")

        # RESULT
        print_result_table(l_list, v)
    except Exception as e:
        print(traceback.format_exc())