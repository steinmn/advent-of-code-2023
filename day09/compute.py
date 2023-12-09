#!/usr/bin/env python3

def load_file(file_name: str):
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
    

def predict_next_value(values: list):
    if all([value == 0 for value in values]):
        return 0
    
    diffs = [values[i] - values[i - 1] for i in range(1, len(values))]
    next_diff = predict_next_value(diffs)
    return values[-1] + next_diff


def predict_previous_value(values: list):
    if all([value == 0 for value in values]):
        return 0
    
    diffs = [values[i] - values[i - 1] for i in range(1, len(values))]
    previous_diff = predict_previous_value(diffs)
    return values[0] - previous_diff


def compute1(file_name: str):
    with open(file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        sum_values = 0
        for line in lines:
            values = line.split(' ')
            values = [int(value) for value in values]
            sum_values += predict_next_value(values)


    print('sum values: ', sum_values)
    return sum_values

def compute2(file_name: str):
    with open(file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        sum_values = 0
        for line in lines:
            values = line.split(' ')
            values = [int(value) for value in values]
            sum_values += predict_previous_value(values)


    print('sum values: ', sum_values)
    return sum_values




if __name__ == '__main__':
    assert compute1('sample.txt') == 114
    print("Sample OK!")
    print("Full: " + str(compute1('full.txt')))

    assert compute2('sample.txt') == 2
    print("Sample OK!")
    print("Full: " + str(compute2('full.txt')))