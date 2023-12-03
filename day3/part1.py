'''
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source,
but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone!
The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If
you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers
and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part
number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58
(middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine
schematic?

The schematic part total is 527369
'''

import re

filePath = 'day3\input.txt'


def isSymbol(row, col, schematic):
    if row < 0 or row >= len(schematic) or col < 0 or col >= len(schematic[0]):
        return False
    return not schematic[row][col].isnumeric() and schematic[row][col] != '.'


def hasAdjacentForSymbol(row, col, schematic):
    return (isSymbol(row + 1, col, schematic) or
            isSymbol(row + 1, col - 1, schematic) or
            isSymbol(row + 1, col + 1, schematic) or
            isSymbol(row - 1, col, schematic) or
            isSymbol(row - 1, col - 1, schematic) or
            isSymbol(row - 1, col + 1, schematic) or
            isSymbol(row, col - 1, schematic) or
            isSymbol(row, col + 1, schematic))


def main():
    with open(filePath) as f:
        lines = f.readlines()
        schematic = [[char for char in line.rstrip('\n')] for line in lines]

    result = 0
    for rowIndex, row in enumerate(schematic):
        i = 0
        while i < len(row):
            if row[i].isnumeric():
                numEnd = i + 1
                num = int(row[i])
                while numEnd < len(row) and row[numEnd].isnumeric():
                    num = num * 10 + int(row[numEnd])
                    numEnd += 1

                for digitIndex in range(i, numEnd):
                    if hasAdjacentForSymbol(rowIndex, digitIndex, schematic):
                        result += num
                        break

                i = numEnd - 1
            i += 1

    print(f'The schematic part total is {result}')


if __name__ == '__main__':
    main()
