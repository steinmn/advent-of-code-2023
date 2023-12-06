#!/usr/bin/env python3
import re

def load_file(file_name: str, concat: bool = False):
    with open(file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        if concat:
            duration = int(re.sub(' ', '',lines[0].lstrip('Time: ')))
            distance = int(re.sub(' ', '',lines[1].lstrip('Distance: ')))
            return duration, distance
        else:
            durations = [int(t) for t in lines[0].lstrip('Time: ').split(' ')]
            distances = [int(d) for d in lines[1].lstrip('Distance: ').split(' ')]
            return durations, distances
    

def distance_from_press_duration(press_duration: int, available_duration: int):
    return (available_duration - press_duration) * press_duration


def find_longest_distance(available_duration: int):
    press_duration = 0
    distance = 0
    return press_duration, distance

def find_shortest_press_above_distance(available_duration: int, min_distance: int):
    press_duration = 0
    return press_duration

def find_longest_press_above_distance(available_duration: int, min_distance: int):
    press_duration = 0
    return press_duration

def find_winning_press_durations(available_duration: int, min_distance: int):
    first_index, max_dist, last_index = 0, 0, 0
    found_max = False
    for i in range(1, available_duration):
        dist = distance_from_press_duration(i, available_duration)
        if dist > min_distance:
            if first_index == 0:
                first_index = i
            if dist > max_dist:
                max_dist = dist
            elif not found_max:
                found_max = True
        elif found_max:
            last_index = i - 1
            return first_index, last_index
        
    return -1, -1

def binary_search(available_duration: int, min_distance: int, start: int, end: int, descending = False):
    if start == end:
        return start - 1 if descending else start
    else:
        mid = (start + end) // 2
        dist = distance_from_press_duration(mid, available_duration)
        if descending:
            if dist > min_distance:
                return binary_search(available_duration, min_distance, mid + 1, end, descending)
            else:
                return binary_search(available_duration, min_distance, start, mid, descending)
        else:
            if dist > min_distance:
                return binary_search(available_duration, min_distance, start, mid)
            else:
                return binary_search(available_duration, min_distance, mid + 1, end)

def find_winning_press_durations2(available_duration: int, min_distance: int):
    split_index = available_duration // 2
    first_index = binary_search(available_duration, min_distance, 1, split_index)
    last_index = binary_search(available_duration, min_distance, split_index + 1, available_duration - 1, True)
    print(first_index, last_index)
    return first_index, last_index


def compute1(file_name: str):
    durations, distances = load_file(file_name)
    product = 1
    for i in range(len(durations)):
        first_index, last_index = find_winning_press_durations(durations[i], distances[i])
        product *= (last_index - first_index + 1)

    print('product: ', product)
    return product

def compute2(file_name: str):
    duration, distance = load_file(file_name, True)
    
    first_index, last_index = find_winning_press_durations2(duration, distance)
    product = (last_index - first_index + 1)

    print('product: ', product)
    return product




if __name__ == '__main__':
    assert compute1('sample.txt') == 288
    print("Sample OK!")
    print("Full: " + str(compute1('full.txt')))

    assert compute2('sample.txt') == 71503
    print("Sample OK!")
    print("Full: " + str(compute2('full.txt')))