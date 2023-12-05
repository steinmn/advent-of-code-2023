#!/usr/bin/env python3
import re

def parse_line(line: str):
    split1 = line.split(': ')
    card_id = int(split1[0])
    split2 = split1[1].split(' | ')
    winning = [int(x) for x in split2[0].split(' ')]
    yours = [int(x) for x in split2[1].split(' ')]
    return card_id, winning, yours

def get_points(winning: list, yours: list):
    points = 0
    for number in winning:
        if number in yours:
            if points == 0:
                points = 1
            else:
                points *= 2
    return points

def get_n_winners(winning: list, yours: list):
    points = 0
    for number in winning:
        if number in yours:
            points += 1
    return points

def compute1(file_name: str):
    sum_of_points = 0
    with open(file_name, 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip('\n').lstrip('Card ') for line in lines]
        lines = [re.sub('  ', ' ', line) for line in lines]
        for line in lines:
            card_id, winning, yours = parse_line(line)
            points = get_points(winning, yours)
            sum_of_points += points
        

    print(sum_of_points)
    return sum_of_points


def compute2(file_name: str):
    sum_of_cards = 0
    with open(file_name, 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip('\n').lstrip('Card ') for line in lines]
        lines = [re.sub('  ', ' ', line) for line in lines]
        number_of_cards = [1 for line in lines]
        for line_index in range(len(lines)-1):
            card_id, winning, yours = parse_line(lines[line_index])
            winners = get_n_winners(winning, yours)
            for i in range(min(winners, len(lines) - line_index - 1)):
                number_of_cards[line_index + i + 1] += number_of_cards[line_index]
        sum_of_cards = sum(number_of_cards)
        
    
    print(sum_of_cards)
    return sum_of_cards


if __name__ == '__main__':
    assert compute1('sample.txt') == 13
    print("Sample OK!")
    print("Full: " + str(compute1('full.txt')))

    assert compute2('sample.txt') == 30
    print("Sample OK!")
    print("Full: " + str(compute2('full.txt')))