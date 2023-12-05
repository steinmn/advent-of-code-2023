#!/usr/bin/env python3


def extract_part_numbers_from_line(line: str, previous_line: str, next_line: str):
    parts = []
    indeces_of_parts = []
    lengths_of_parts = []
    current_part = ''
    part_is_valid = False
    symbol_in_previous_column = False
    for i in range(0, len(line)):
        if line[i].isdigit():
            if not current_part and symbol_in_previous_column:
                # first digit, check previous column
                part_is_valid = True
            current_part += line[i]
        elif current_part:
            # end of part add more check
            if part_is_valid or line[i] != '.' or next_line[i] != '.' or previous_line[i] != '.':
                parts.append(int(current_part))
                indeces_of_parts.append(i - len(current_part))
                lengths_of_parts.append(len(current_part))
            current_part = ''
            part_is_valid = False

        if (not line[i].isdigit() and line[i] != '.') or (not next_line[i].isdigit() and next_line[i] != '.') or (not previous_line[i].isdigit() and previous_line[i] != '.'):
            symbol_in_previous_column = True
            if current_part:
                part_is_valid = True
        else:
            symbol_in_previous_column = False

    if current_part and part_is_valid:
        parts.append(int(current_part))
        indeces_of_parts.append(len(line) - len(current_part))
        lengths_of_parts.append(len(current_part))

    return parts, indeces_of_parts, lengths_of_parts

def compute1(file_name: str):
    sum_of_parts = 0
    with open(file_name, 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines]
        line_length = len(lines[0])
        padding_line = '.' * line_length
        lines.insert(0, padding_line)
        lines.append(padding_line)
        for line_index in range(1, len(lines) - 1):
            parts, ind, lens = extract_part_numbers_from_line(lines[line_index], lines[line_index - 1], lines[line_index + 1])
            # print(parts)
            sum_of_parts += sum(parts)

    print(sum_of_parts)
    return sum_of_parts


def get_gear_indeces(line: str):
    gear_indeces = []
    for i in range(0, len(line)):
        if line[i] == '*':
            gear_indeces.append(i)
    return gear_indeces


def is_part_adjacent_to_gear(part_index: int, part_length: int, gear_index: int):
    if gear_index - part_length <= part_index and gear_index + 1 >= part_index:
        return True
    return False


def get_adjacent_parts(parts: list, indeces: list, lengths: list, gear_index: int):
    adjacent_parts = []
    for i in range(0, len(parts)):
        if is_part_adjacent_to_gear(indeces[i], lengths[i], gear_index):
            adjacent_parts.append(parts[i])
    return adjacent_parts


def compute2(file_name: str):
    sum_of_powers = 0
    with open(file_name, 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines]
        line_length = len(lines[0])
        padding_line = '.' * line_length
        lines.insert(0, padding_line)
        lines.append(padding_line)
        list_of_parts = []
        list_of_indeces = []
        list_of_lengths = []
        for line_index in range(1, len(lines) - 1):
            parts, indeces, lengths = extract_part_numbers_from_line(lines[line_index], lines[line_index - 1], lines[line_index + 1])
            list_of_parts.append(parts)
            list_of_indeces.append(indeces)
            list_of_lengths.append(lengths)
        
        for line_index in range(1, len(lines) - 1):
            gear_candidates = get_gear_indeces(lines[line_index])
            for gear_candidate in gear_candidates:
                adjacent_parts = get_adjacent_parts(list_of_parts[line_index - 2], list_of_indeces[line_index - 2], list_of_lengths[line_index - 2], gear_candidate)
                adjacent_parts += get_adjacent_parts(list_of_parts[line_index - 1], list_of_indeces[line_index - 1], list_of_lengths[line_index - 1], gear_candidate)
                adjacent_parts += get_adjacent_parts(list_of_parts[line_index], list_of_indeces[line_index], list_of_lengths[line_index], gear_candidate)
                # print(adjacent_parts)
                if len(adjacent_parts) == 2:
                    # print(adjacent_parts[0] * adjacent_parts[1])
                    sum_of_powers += adjacent_parts[0] * adjacent_parts[1]
    
    print(sum_of_powers)
    return sum_of_powers


if __name__ == '__main__':
    assert compute1('sample.txt') == 4361
    print("Sample OK!")
    print("Full: " + str(compute1('full.txt')))

    assert compute2('sample.txt') == 467835
    print("Sample OK!")
    print("Full: " + str(compute2('full.txt')))