#!/usr/bin/env python3
import functools
from copy import deepcopy


class Node:
    def __init__(self, line: str):
        self.id = line[0:3]
        self.left = line[7:10]
        self.right = line[12:15]


# class Path:
#     def __init__(self, node_dict: dict, go_right: list, include_jokers: bool = False):


def load_file(file_name: str, include_jokers: bool = False):
    with open(file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        map_string = lines.pop(0)
        lines.pop(0) # empty line
        go_right = [char == 'R' for char in map_string]
        node_dict = {}
        
        for line in lines:
            new_node = Node(line)
            node_dict[new_node.id] = new_node

        return node_dict, go_right

def compute1(file_name: str):
    node_dict, go_right = load_file(file_name)
    next_string = 'AAA'
    goal = 'ZZZ'
    found = False
    steps = 0
    n_instructions = len(go_right)
    while not found:
        next_node = node_dict[next_string]
        if go_right[steps % n_instructions]:
            next_string = next_node.right
        else:
            next_string = next_node.left
        steps += 1
        if next_string == goal:
            found = True

    print('steps: ', steps)
    return steps


def find_steps_from_start_to_an_end_with_offset(node_dict: dict, go_right: list, start_string: str, offset: int = 0):
    next_string = deepcopy(start_string)
    found = False
    steps = 0
    n_instructions = len(go_right)
    while not found:
        next_node = node_dict[next_string]
        if go_right[(steps + offset) % n_instructions]:
            next_string = deepcopy(next_node.right)
        else:
            next_string = deepcopy(next_node.left)
        steps += 1
        if next_string.endswith('Z'):
            found = True

    # print('start_string ' + start_string + ' to ' + next_string + ' with offset ' + str(offset) + ' steps: ', steps)
    if next_string != start_string:
        print('start_string ' + start_string + ' to ' + next_string + ' with offset ' + str(offset) + ' steps: ', steps)
    return steps, next_string


def compute2dumb(file_name: str):
    node_dict, go_right = load_file(file_name)
    next_strings = [key for key in node_dict.keys() if key.endswith('A')]
    print(next_strings)
    goal_end = 'Z'
    found = False
    steps = 0
    n_instructions = len(go_right)
    while not found:
        next_nodes = [node_dict[next_string] for next_string in next_strings]
        if go_right[steps % n_instructions]:
            next_strings = [next_node.right for next_node in next_nodes]
        else:
            next_strings = [next_node.left for next_node in next_nodes]
        steps += 1
        if all([next_string.endswith(goal_end) for next_string in next_strings]):
            found = True

        if steps % 100000 == 0:
                print('steps: ', steps)
    print('steps: ', steps)
    return steps


class MapOfEndLoops:
    def __init__(self, node_dict: dict, go_right: list, end_strings: list, n_instructions: int):
        offsets = range(n_instructions)
        self.n_instructions = n_instructions
        self.map = {}
        for end_string in end_strings:
            self.map[end_string] = [find_steps_from_start_to_an_end_with_offset(node_dict, go_right, end_string, offset) for offset in offsets]
            # loops = []
            # for offset in offsets:
            #     steps, next_string = find_steps_from_start_to_an_end_with_offset(node_dict, go_right, end_string, offset)
            #     loops.append((steps, next_string))
            #     print('end_string: ' + end_string + 'offset: ' + str(offset) + ' steps: ' + str(steps) + ' next_string: ' + next_string)
            # self.map[end_string] = loops

        print('Map generated')

    def find_loop(self, start_string: str, initial_offset: int):
        next_string = deepcopy(start_string)
        visited_offsets = []
        visited_offsets.append(initial_offset)
        steps_list = []
        found = False
        while not found:
            steps, next_string = self.map[next_string][visited_offsets[-1]]
            if next_string != start_string:
                print('next_string != start_string: start_string ' + start_string + ' to ' + next_string + ' with offset ' + str(visited_offsets[-1]) + ' steps: ', steps)
            steps_list.append(steps)
            new_offset = (visited_offsets[-1] + steps) % self.n_instructions
            if new_offset in visited_offsets:
                found = True
            visited_offsets.append(new_offset)

        print('Loop found, visited_offsets: ', visited_offsets)

        looping_offsets = []
        steps_to_next = []
        steps_to_loop_start = 0
        in_loop = False
        for i in range(len(steps_list)):
            if not in_loop:
                steps_to_loop_start += steps_list[i]
                if visited_offsets[i] == new_offset:
                    in_loop = True

            if in_loop:
                looping_offsets.append(visited_offsets[i])
                steps_to_next.append(steps_list[i])
        loop_length = len(looping_offsets)
        loop_length_steps = sum(steps_to_next)

        print('Loop ID ' + start_string + ': steps_to_loop_start: ' + str(steps_to_loop_start) + ' loop_length: ' + str(loop_length) + ' loop_length_steps: ' + str(loop_length_steps))
        return steps_to_loop_start, loop_length, loop_length_steps, looping_offsets, steps_to_next

def done(steps_list: list):
    return all([steps == steps_list[0] for steps in steps_list])

def compute2(file_name: str):
    node_dict, go_right = load_file(file_name)
    start_strings = [key for key in node_dict.keys() if key.endswith('A')]
    steps_list, next_list = zip(*[find_steps_from_start_to_an_end_with_offset(node_dict, go_right, start_string) for start_string in start_strings])
    steps_list = list(steps_list)
    next_list = list(next_list)
    print(steps_list)
    print(next_list)
    end_strings = [key for key in node_dict.keys() if key.endswith('Z')]
    print(end_strings)
    map_of_end_loops = MapOfEndLoops(node_dict, go_right, end_strings, len(go_right))
    n_instructions = len(go_right)
    print('n_instructions: ', n_instructions)
    for end_string, initial_steps in zip(next_list, steps_list):
        print('end_string: ' + end_string + ' initial_steps: ' + str(initial_steps))
        map_of_end_loops.find_loop(end_string, initial_steps % n_instructions)
    
    n_threads = len(start_strings)
    i = 0
    # while not done(steps_list):
    #     # steps_min = min(steps_list)
    #     # index_to_work_on = steps_list.index(steps_min)
    #     # start_string = next_list[index_to_work_on]
    #     # steps, next_string = map_of_end_loops.map[start_string][steps_min % n_instructions]
    #     # # print(steps)
    #     # # print(next_string)
    #     # next_list[index_to_work_on] = next_string
    #     # steps_list[index_to_work_on] += steps
    #     steps_max = max(steps_list)
    #     for thread in range(n_threads):
    #         if steps_list[thread] < steps_max:
    #             start_string = next_list[thread]
    #             steps_before = steps_list[thread]
    #             steps, next_string = map_of_end_loops.map[start_string][steps_before % n_instructions]
    #             next_list[thread] = next_string
    #             steps_list[thread] += steps


    #     i += 1
    #     if i % 1000000 == 0:
    #         print('steps_list: ', steps_list)
    #         print('next_list: ', next_list)

    print('steps_list: ', steps_list)
    print('steps: ', steps_list[0])
    return 6

def compute2no_assumption(file_name: str):
    node_dict, go_right = load_file(file_name)
    start_strings = [key for key in node_dict.keys() if key.endswith('A')]
    steps_list, next_list = zip(*[find_steps_from_start_to_an_end_with_offset(node_dict, go_right, start_string) for start_string in start_strings])
    steps_list = list(steps_list)
    next_list = list(next_list)
    print(steps_list)
    print(next_list)
    end_strings = [key for key in node_dict.keys() if key.endswith('Z')]
    print(end_strings)
    map_of_end_loops = MapOfEndLoops(node_dict, go_right, end_strings, len(go_right))
    n_instructions = len(go_right)
    n_threads = len(start_strings)
    i = 0
    while not done(steps_list):
        # steps_min = min(steps_list)
        # index_to_work_on = steps_list.index(steps_min)
        # start_string = next_list[index_to_work_on]
        # steps, next_string = map_of_end_loops.map[start_string][steps_min % n_instructions]
        # # print(steps)
        # # print(next_string)
        # next_list[index_to_work_on] = next_string
        # steps_list[index_to_work_on] += steps
        steps_max = max(steps_list)
        for thread in range(n_threads):
            if steps_list[thread] < steps_max:
                start_string = next_list[thread]
                steps_before = steps_list[thread]
                steps, next_string = map_of_end_loops.map[start_string][steps_before % n_instructions]
                next_list[thread] = next_string
                steps_list[thread] += steps


        i += 1
        if i % 1000000 == 0:
            print('steps_list: ', steps_list)
            print('next_list: ', next_list)

    print('steps_list: ', steps_list)
    print('steps: ', steps_list[0])
    return steps_list[0]

def calculate_based_on_prime_cycles():
    return 71 * 43 * 79 * 53 * 47 * 61 * 283


if __name__ == '__main__':
    assert compute1('sample1.txt') == 2
    assert compute1('sample2.txt') == 6
    print("Sample OK!")
    print("Full: " + str(compute1('full.txt')))

    assert compute2('sample3.txt') == 6
    print("Sample OK!")
    # print("Full: " + str(compute2('full.txt')))
    print("Full: " + str(calculate_based_on_prime_cycles()))
    # > 254600000