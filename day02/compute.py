#!/usr/bin/env python3


class ColorCombo:
    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r, self.g, self.b = r, g, b

def get_color_combo_from_string(input: str):
    colorstrings = input.split(', ')
    output = ColorCombo()
    for colorstring in colorstrings:
        colorsplit = colorstring.split(' ')
        if colorsplit[1] == 'red':
            output.r = int(colorsplit[0])
        elif colorsplit[1] == 'green':
            output.g = int(colorsplit[0])
        elif colorsplit[1] == 'blue':
            output.b = int(colorsplit[0])
    return output

def get_largest_from_both(a: ColorCombo, b: ColorCombo):
    return ColorCombo(r=max(a.r, b.r), g=max(a.g, b.g), b=max(a.b, b.b))
    
def is_valid(valid_threshold: ColorCombo, min_required: ColorCombo):
    return min_required.r <= valid_threshold.r and min_required.g <= valid_threshold.g and min_required.b <= valid_threshold.b

def parse_line(line: str):
    line_split1 = line.strip('\n').strip('Game ').split(': ')
    game_id = int(line_split1[0])
    samples = [get_color_combo_from_string(samplestring) for samplestring in line_split1[1].split('; ')]
    return game_id, samples


def find_minimum_required_for_valid(samples: list):
    min_required = ColorCombo()
    for sample in samples:
        min_required = get_largest_from_both(min_required, sample)
    return min_required



def compute1(file_name: str):
    sum_of_ids = 0
    valid_threshold = ColorCombo(r=12, g=13, b=14)
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            game_id, samples = parse_line(line)
            min_required = find_minimum_required_for_valid(samples)
            if is_valid(valid_threshold, min_required):
                sum_of_ids += game_id

    return sum_of_ids


def compute2(file_name: str):
    sum_of_powers = 0
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            game_id, samples = parse_line(line)
            min_required = find_minimum_required_for_valid(samples)
            # print(min_required.r * min_required.g * min_required.b)
            sum_of_powers += min_required.r * min_required.g * min_required.b
    
    return sum_of_powers


if __name__ == '__main__':
    assert compute1('sample.txt') == 8
    print("Sample OK!")
    print("Full: " + str(compute1('full.txt')))

    assert compute2('sample.txt') == 2286
    print("Sample OK!")
    print("Full: " + str(compute2('full.txt')))