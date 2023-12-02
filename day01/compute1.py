#!/usr/bin/env python3
import re

def compute1():
    sum_of_numbers = 0
    # with open('sample.txt', 'r') as f:
    with open('full.txt', 'r') as f:
        lines = f.readlines()
        # print(lines)
        for line in lines:
            numline = re.sub(r'\D', '', line)
            # print(numline)
            number = int(numline[0] + numline[-1])
            print(number)
            sum_of_numbers += number

    print('\n\n\nSum of numbers: ')
    print(sum_of_numbers)

def check_for_number(line, start: bool):
    if start and line[0].isdigit():
        return line[0]

    if not start and line[-1].isdigit():
        return line[-1]

    number_strings = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    for i in range(len(number_strings)):
        if (start and line.startswith(number_strings[i])) or (not start and line.endswith(number_strings[i])):
            return str(i)
    return ''

def find_numbers(line):
    line = line.lower()
    first = ''
    second = ''
    for i in range(len(line)):
        if not first:
            first = check_for_number(line[i:-1], True)

        if not second:
            second = check_for_number(line[0:-1-i], False)

        if first and second:
            break

    return first + second


def compute2():
    sum_of_numbers = 0
    # with open('sample2.txt', 'r') as f:
    with open('full.txt', 'r') as f:
        lines = f.readlines()
        # print(lines)
        for line in lines:
            number = int(find_numbers(line))
            print(number)
            sum_of_numbers += number

    print('\n\n\nSum of numbers: ')
    print(sum_of_numbers)


if __name__ == '__main__':
    # compute1()
    compute2()