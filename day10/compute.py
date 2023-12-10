#!/usr/bin/env python3
import math
from enum import Enum

class Side(Enum):
    LEFT = 1
    RIGHT = 2
    BOTH = 3
    NONE = 4

class Pipe:
    def __init__(self, value: str, pos: tuple[int,int], previous: tuple[int,int] | None = None):
        self.value = value
        self.pos = pos
        self.previous = previous
        self.next = None
        if previous is not None:
            if self.value == '-':
                if self.pos[0] < self.previous[0]:
                    self.next = (self.pos[0] - 1, self.pos[1])
                else:
                    self.next = (self.pos[0] + 1, self.pos[1])
            elif self.value == '|':
                if self.pos[1] < self.previous[1]:
                    self.next = (self.pos[0], self.pos[1] - 1)
                else:
                    self.next = (self.pos[0], self.pos[1] + 1)
            elif self.value == 'L':
                if self.pos[0] < self.previous[0]:
                    self.next = (self.pos[0], self.pos[1] - 1)
                else:
                    self.next = (self.pos[0] + 1, self.pos[1])
            elif self.value == 'J':
                if self.pos[0] > self.previous[0]:
                    self.next = (self.pos[0], self.pos[1] - 1)
                else:
                    self.next = (self.pos[0] - 1, self.pos[1])
            elif self.value == '7':
                if self.pos[0] > self.previous[0]:
                    self.next = (self.pos[0], self.pos[1] + 1)
                else:
                    self.next = (self.pos[0] - 1, self.pos[1])
            elif self.value == 'F':
                if self.pos[0] < self.previous[0]:
                    self.next = (self.pos[0], self.pos[1] + 1)
                else:
                    self.next = (self.pos[0] + 1, self.pos[1])

    def get_neighbours(self, side: Side, n_x: int, n_y: int) -> list[tuple[int,int]]:
        all_neighbours = get_neighbours(self.pos, n_x, n_y, check_validity = False)
        next_id = all_neighbours.index(self.next) # can be 1,3,5,7
        previous_id = all_neighbours.index(self.previous) # can be 1,3,5,7
        left_neighbours = []
        right_neighbours = []
        if side == Side.BOTH:
            return [neighbour for neighbour in all_neighbours if neighbour != self.next and neighbour != self.previous]

        if previous_id == 1: # enter left
            if next_id == 3:
                left_neighbours = [all_neighbours[2]]
                right_neighbours = [all_neighbours[0]] + all_neighbours[4:]
            elif next_id == 5:
                left_neighbours = all_neighbours[2:5]
                right_neighbours = [all_neighbours[0]] + all_neighbours[6:]
            elif next_id == 7:
                left_neighbours = all_neighbours[2:7]
                right_neighbours = [all_neighbours[0]]
            else:
                raise Exception('Invalid next_id: ' + str(next_id))
        elif previous_id == 3: # enter top
            if next_id == 1:
                left_neighbours = [all_neighbours[0]] + all_neighbours[4:]
                right_neighbours = [all_neighbours[2]]
            elif next_id == 5:
                left_neighbours = [all_neighbours[4]]
                right_neighbours = all_neighbours[:3] + all_neighbours[6:]
            elif next_id == 7:
                left_neighbours = all_neighbours[4:7]
                right_neighbours = all_neighbours[:3]
            else:
                raise Exception('Invalid next_id: ' + str(next_id))
        elif previous_id == 5: # enter right
            if next_id == 1:
                left_neighbours = all_neighbours[6:] + [all_neighbours[0]]
                right_neighbours = all_neighbours[2:5]
            elif next_id == 3:
                left_neighbours = all_neighbours[:3] + all_neighbours[5:]
                right_neighbours = [all_neighbours[4]]
            elif next_id == 7:
                left_neighbours = [all_neighbours[6]]
                right_neighbours = all_neighbours[:5]
            else:
                raise Exception('Invalid next_id: ' + str(next_id))
        elif previous_id == 7: # enter bottom
            if next_id == 1:
                left_neighbours = [all_neighbours[0]]
                right_neighbours = all_neighbours[2:7]
            elif next_id == 3:
                left_neighbours = all_neighbours[:3]
                right_neighbours = all_neighbours[4:7]
            elif next_id == 5:
                left_neighbours = all_neighbours[:5]
                right_neighbours = [all_neighbours[6]]
            else:
                raise Exception('Invalid next_id: ' + str(next_id))
        else:
            raise Exception('Invalid previous_id: ' + str(previous_id))

        if side == Side.LEFT:
            return left_neighbours
        elif side == Side.RIGHT:
            return right_neighbours
        else:
            raise Exception('Invalid side: ' + str(side))


def get_letter(pos: tuple[int,int], lines: list[str]) -> str:
    return lines[pos[1]][pos[0]]


def find_start(lines: list[str]) -> tuple[int,int]:
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == 'S':
                return (x,y)
    return (-1,-1)

def find_initial_direction(lines: list[str], start: tuple[int,int]) -> tuple[int,int]:
    n_x = len(lines[0])
    n_y = len(lines)
    if start[0] > 0:
        test_pos = (start[0] - 1, start[1])
        test_char = get_letter(test_pos, lines)
        if test_char == '-' or test_char == 'L' or test_char == 'F':
            return test_pos
    if start[0] < n_x - 1:
        test_pos = (start[0] + 1, start[1])
        test_char = get_letter(test_pos, lines)
        if test_char == '-' or test_char == 'J' or test_char == '7':
            return test_pos
    if start[1] > 0:
        test_pos = (start[0], start[1] - 1)
        test_char = get_letter(test_pos, lines)
        if test_char == '|' or test_char == 'F' or test_char == '7':
            return test_pos
    if start[1] < n_y - 1:
        test_pos = (start[0], start[1] + 1)
        test_char = get_letter(test_pos, lines)
        if test_char == '|' or test_char == 'L' or test_char == 'J':
            return test_pos
    return (-1,-1)
            

def compute1(file_name: str):
    with open(file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        loop_distance = 0
        start = find_start(lines)
        start_pipe = Pipe('S', start)
        start_pipe.next = find_initial_direction(lines, start)
        pipes = []
        pipes.append(start_pipe)
        # print('start: ', start)
        # print('start_direction: ', start_pipe.next)
        while (pipes[-1].next != start):
            # print('next: ', pipes[-1].next)
            # print('next_letter: ', get_letter(pipes[-1].next, lines))
            pipes.append(Pipe(get_letter(pipes[-1].next, lines), pipes[-1].next, pipes[-1].pos))
            loop_distance += 1
        
        pipes[0].previous = pipes[-1].pos

        print('loop_distance: ', loop_distance)
        max_dist = math.ceil(loop_distance / 2)
        print('max_dist: ', max_dist)
        return max_dist


def get_neighbours(pos: tuple[int,int], n_x: int, n_y: int, check_validity = True) -> list[tuple[int,int]]:
    neighbours = []
    if check_validity:
        if pos[0] > 0:
            if pos[1] < n_y - 1:
                neighbours.append((pos[0] - 1, pos[1] + 1)) # bottom left
            neighbours.append((pos[0] - 1, pos[1])) # left
            if pos[1] > 0:
                neighbours.append((pos[0] - 1, pos[1] - 1)) # top left
        if pos[1] > 0:
            neighbours.append((pos[0], pos[1] - 1)) # top
        if pos[0] < n_x - 1:
            if pos[1] > 0:
                neighbours.append((pos[0] + 1, pos[1] - 1)) # top right
            neighbours.append((pos[0] + 1, pos[1])) # right
            if pos[1] < n_y - 1:
                neighbours.append((pos[0] + 1, pos[1] + 1)) # bottom right
        if pos[1] < n_y - 1:
            neighbours.append((pos[0], pos[1] + 1)) # bottom
    else:
        neighbours.append((pos[0] - 1, pos[1] + 1)) # bottom left
        neighbours.append((pos[0] - 1, pos[1])) # left
        neighbours.append((pos[0] - 1, pos[1] - 1)) # top left
        neighbours.append((pos[0], pos[1] - 1)) # top
        neighbours.append((pos[0] + 1, pos[1] - 1)) # top right
        neighbours.append((pos[0] + 1, pos[1])) # right
        neighbours.append((pos[0] + 1, pos[1] + 1)) # bottom right
        neighbours.append((pos[0], pos[1] + 1)) # bottom
    return neighbours # clockwise from bottom left

class CleanedMap:
    def __init__(self, lines: list[str], loop: list[Pipe]):
        self.raw_lines = lines
        self.loop = loop
        self.n_x = len(lines[0])
        self.n_y = len(lines)
        self.cleaned_lines = [['.'] * self.n_x for _ in range(self.n_y)] 
        for pipe in loop:
            self.cleaned_lines[pipe.pos[1]][pipe.pos[0]] = pipe.value

        # self.mark_as_outside_from_edges()
        self.loop_outside_direction = Side.NONE
        self.loop_inside_direction = Side.NONE
        # self.find_loop_direction()
        # self.mark_from_loop()

    
    def find_loop_direction(self):
        for pipe in self.loop:
            for neighbour in pipe.get_neighbours(Side.LEFT, self.n_x, self.n_y):
                if self.cleaned_lines[neighbour[1]][neighbour[0]] == 'O':
                    self.loop_outside_direction = Side.LEFT
                    self.loop_inside_direction = Side.RIGHT
                    return
            for neighbour in pipe.get_neighbours(Side.RIGHT, self.n_x, self.n_y):
                if self.cleaned_lines[neighbour[1]][neighbour[0]] == 'O':
                    self.loop_outside_direction = Side.RIGHT
                    self.loop_inside_direction = Side.LEFT
                    return
        raise Exception('No loop direction found')
    

    def mark_from_loop(self):
        for pipe in self.loop:
            for neighbour in pipe.get_neighbours(self.loop_inside_direction, self.n_x, self.n_y):
                self.mark_if_not_pipe_or_already_marked(neighbour, False)
            for neighbour in pipe.get_neighbours(self.loop_outside_direction, self.n_x, self.n_y):
                self.mark_if_not_pipe_or_already_marked(neighbour, True)


    def mark_as_outside_from_edges(self):
        x_start = 0
        x_end = self.n_x - 1
        y_start = 0
        y_end = self.n_y - 1
        for y in range(0, self.n_y):
            if all([self.cleaned_lines[y][x] == '.' for x in range(self.n_x)]):
                self.cleaned_lines[y] = ['O'] * self.n_x
                y_start = y + 1
            else:
                break
        for y in range(self.n_y - 1, -1, -1):
            if all([self.cleaned_lines[y][x] == '.' for x in range(self.n_x)]):
                self.cleaned_lines[y] = ['O'] * self.n_x
                y_end = y - 1
            else:
                break

        for x in range(0, self.n_x):
            if all([self.cleaned_lines[y][x] == '.' for y in range(y_start, y_end + 1)]):
                for y in range(y_start, y_end + 1):
                    self.cleaned_lines[y][x] = 'O'
                x_start = x + 1
            else:
                break
        for x in range(self.n_x - 1, -1, -1):
            if all([self.cleaned_lines[y][x] == '.' for y in range(y_start, y_end + 1)]):
                for y in range(y_start, y_end + 1):
                    self.cleaned_lines[y][x] = 'O'
                x_end = x - 1
            else:
                break
        for x in range(self.n_x):
            self.mark_if_not_pipe_or_already_marked((x, y_start))
            self.mark_if_not_pipe_or_already_marked((x, y_end))
        for y in range(self.n_y):
            self.mark_if_not_pipe_or_already_marked((x_start, y))
            self.mark_if_not_pipe_or_already_marked((x_end, y))

    def mark_if_not_pipe_or_already_marked(self, pos: tuple[int,int], outside = True, depth = 0):
        if depth > 990:
            return
        if 0 <= pos[0] < self.n_x and 0 <= pos[1] < self.n_y and self.cleaned_lines[pos[1]][pos[0]] == '.':
            if outside:
                self.cleaned_lines[pos[1]][pos[0]] = 'O'
            else:
                self.cleaned_lines[pos[1]][pos[0]] = 'I'
            for neighbour in get_neighbours(pos, self.n_x, self.n_y):
                self.mark_if_not_pipe_or_already_marked(neighbour, outside, depth + 1)
            
    def get_unmarked_remaining(self) -> int:
        return self.get_char_remaining('.')
    
    def get_inside_remaining(self) -> int:
        return self.get_char_remaining('I')
    
    def get_char_remaining(self, char: str) -> int:
        output = 0
        for y in range(self.n_y):
            for x in range(self.n_x):
                if self.cleaned_lines[y][x] == char:
                    output += 1
        return output

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.cleaned_lines])

def compute2(file_name: str):
    with open(file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        loop_distance = 0
        start = find_start(lines)
        start_pipe = Pipe('S', start)
        start_pipe.next = find_initial_direction(lines, start)
        pipes = []
        pipes.append(start_pipe)
        print('start: ', start)
        print('start_direction: ', start_pipe.next)
        while (pipes[-1].next != start):
            # print('next: ', pipes[-1].next)
            # print('next_letter: ', get_letter(pipes[-1].next, lines))
            pipes.append(Pipe(get_letter(pipes[-1].next, lines), pipes[-1].next, pipes[-1].pos))
            loop_distance += 1
        
        pipes[0].previous = pipes[-1].pos

        cleaned_map = CleanedMap(lines, pipes)
        print('\ncleaned_map:')
        print(cleaned_map)
        cleaned_map.mark_as_outside_from_edges()
        print('\ncleaned_map with partial outside:')
        print(cleaned_map)
        cleaned_map.find_loop_direction()
        cleaned_map.mark_from_loop()
        print('\ncleaned_map with inside and outside:')
        print(cleaned_map)
        get_unmarked_remaining = cleaned_map.get_unmarked_remaining()
        print('unmarked_left: ', get_unmarked_remaining)

        get_inside_remaining = cleaned_map.get_inside_remaining()
        print('inside_left: ', get_inside_remaining)

        # print('loop_distance: ', loop_distance)
        # max_dist = math.ceil(loop_distance / 2)
        # print('max_dist: ', max_dist)
        return get_inside_remaining


if __name__ == '__main__':
    assert compute1('sample1.txt') == 4
    assert compute1('sample2.txt') == 8
    print("Sample OK!")
    print("Full: " + str(compute1('full.txt')))

    print(get_neighbours((1,1), 3, 3))

    assert compute2('sample3.txt') == 4
    assert compute2('sample4.txt') == 8
    assert compute2('sample5.txt') == 10
    print("Sample OK!")
    print("Full: " + str(compute2('full.txt')))