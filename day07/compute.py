#!/usr/bin/env python3
import functools


class CamelHand:
    def __init__(self, string: str, id: int, jokers: bool = False):
        if len(string) != 5:
            print('Invalid hand: ' + string)
            raise ValueError
        self.string = string
        self.cards = []
        self.id = id
        self.grade = 0 # grades 5-ofa-kind=6, 4-of-a-kind=5, full house=4, 3-of-a-kind=3, 2-pair=2, 1-pair=1, high card = 0
        self.map_of_cards = [0] * 15
        for char in string:
            if char.isdigit() and char != '0' and char != '1':
                digit = int(char)
                self.cards.append(digit)
                self.map_of_cards[digit] += 1
            elif char == 'A':
                self.cards.append(14)
                self.map_of_cards[14] += 1
            elif char == 'K':
                self.cards.append(13)
                self.map_of_cards[13] += 1
            elif char == 'Q':
                self.cards.append(12)
                self.map_of_cards[12] += 1
            elif char == 'J':
                if jokers:
                    self.cards.append(1)
                    self.map_of_cards[1] += 1
                else:
                    self.cards.append(11)
                    self.map_of_cards[11] += 1
            elif char == 'T':
                self.cards.append(10)
                self.map_of_cards[10] += 1
            else:
                print('Invalid character in hand: ' + char)
                raise ValueError
        max_same = max(self.map_of_cards[2:15]) + self.map_of_cards[1]
        if max_same == 5:
            self.grade = 6
        elif max_same == 4:
            self.grade = 5
        elif max_same == 3:
            if self.map_of_cards[1] == 0: # no jokers
                if 2 in self.map_of_cards[2:15]:
                    self.grade = 4
                else:
                    self.grade = 3
            elif self.map_of_cards[1] == 1: # 1 joker
                if self.map_of_cards[2:15].count(2) == 2:
                    self.grade = 4
                else:
                    self.grade = 3
            else:
                self.grade = 3 # 2 jokers
        elif max_same == 2:
            if self.map_of_cards[1] == 0:
                if self.map_of_cards[2:15].count(2) == 2:
                    self.grade = 2
                else:
                    self.grade = 1
            else: # 1 joker
                self.grade = 1

    def __str__(self):
        return self.string + ' grade=' + str(self.grade)
    
    def __gt__(self, other: 'CamelHand'):
        if self.grade > other.grade:
            return True
        elif self.grade < other.grade:
            return False
        else:
            for i in range(5):
                if self.cards[i] > other.cards[i]:
                    return True
                elif self.cards[i] < other.cards[i]:
                    return False
            return False
        
    def __lt__(self, other: 'CamelHand'):
        if self.grade < other.grade:
            return True
        elif self.grade > other.grade:
            return False
        else:
            for i in range(5):
                if self.cards[i] < other.cards[i]:
                    return True
                elif self.cards[i] > other.cards[i]:
                    return False
            return False


def compare_hands(hand1: CamelHand, hand2: CamelHand):
    if hand1 > hand2:
        return 1
    elif hand1 < hand2:
        return -1
    else:
        return 0


def load_file(file_name: str, include_jokers: bool = False):
    with open(file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        hands = []
        bids = []
        
        i = 0
        for line in lines:
            linesplit = line.split(' ')
            hands.append(CamelHand(linesplit[0], i, include_jokers))
            bids.append(int(linesplit[1]))
            i += 1

        return hands, bids


def compute1(file_name: str):
    hands, bids = load_file(file_name)
    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare_hands))
    
    sum_winnings = 0
    for i in range(len(sorted_hands)):
        sum_winnings += bids[sorted_hands[i].id] * (i + 1)

    print('winnings: ', sum_winnings)
    return sum_winnings

def compute2(file_name: str):
    hands, bids = load_file(file_name, include_jokers=True)
    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare_hands))
    
    sum_winnings = 0
    for i in range(len(sorted_hands)):
        sum_winnings += bids[sorted_hands[i].id] * (i + 1)

    print('winnings: ', sum_winnings)
    return sum_winnings




if __name__ == '__main__':
    assert compute1('sample.txt') == 6440
    print("Sample OK!")
    print("Full: " + str(compute1('full.txt')))

    assert compute2('sample.txt') == 5905
    print("Sample OK!")
    print("Full: " + str(compute2('full.txt')))