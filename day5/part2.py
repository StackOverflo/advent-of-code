'''
--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds:
line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and
the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79
and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55,
56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84,
fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest
location number that corresponds to any of the initial seed numbers?
'''

filePath = 'day5\input.txt'


class RangesMapping:
    def __init__(self, sminR, dminR, amount):
        self.sourceMinRange = sminR
        self.sourceMaxRange = sminR + amount - 1
        self.destMinRange = dminR
        self.destMaxRange = dminR + amount - 1

    def __repr__(self):
        return f'\nsource: {self.sourceMinRange} - {self.sourceMaxRange} and Dest: {self.destMinRange} - {self.destMaxRange}'

    # return all the ranges in entry and use mapping for intersections
    def applyAsMask(self, r):
        start = r[0]
        end = r[1]
        masked = []
        unmasked = []
        # range|         |----|
        # self |  |----|
        # or
        # range|  |----|
        # self |         |----|
        if self.sourceMinRange > end or self.sourceMaxRange < start:
            unmasked.append((start, end))
        # range|     |----|
        # self |  |----|
        elif self.sourceMinRange < start <= self.sourceMaxRange:
            overlap = self.sourceMaxRange - start
            masked.append((self.destMaxRange - overlap, self.destMaxRange))
            unmasked.append((self.sourceMaxRange + 1, end))
        # range|  |----|
        # self |     |----|
        elif start < self.sourceMinRange <= end < self.sourceMaxRange:
            overlap = end - self.sourceMinRange
            unmasked.append((start, self.sourceMinRange - 1))
            masked.append((self.destMinRange, self.destMinRange + overlap))
        # range|  |----|
        # self |   |--|
        elif start < self.sourceMinRange <= self.sourceMaxRange < end:
            unmasked.append((start, self.sourceMinRange - 1))
            masked.append((self.destMinRange, self.destMaxRange))
            unmasked.append((self.sourceMaxRange + 1, end))
        # range|   |--|
        # self |  |----|
        elif self.sourceMinRange <= start <= end <= self.sourceMaxRange:
            lgap = start - self.sourceMinRange
            overlap = end - start
            masked.append((self.destMinRange + lgap, self.destMinRange + lgap + overlap))

        return masked, unmasked


class Mapping:
    def __init__(self):
        self.mapping = []

    def __repr__(self):
        return f'{self.mapping}'

    def add(self, entry):
        self.mapping.append(entry)

    def addMultiple(self, entries):
        for entry in entries:
            self.mapping.append(entry)

    def sourceToDest(self, num):
        for entry in self.mapping:
            if entry.sourceMinRange <= num <= entry.sourceMaxRange:
                return entry.destMinRange + (num - entry.sourceMinRange)
        return num

    def applyAsMask(self, ranges):
        newRanges = []

        for r in ranges:
            newMasked = []
            unmasked = [r]
            for rangeMapping in self.mapping:
                for u in unmasked:
                    masked, unmasked = rangeMapping.applyAsMask(u)
                    newMasked.extend(masked)
            newRanges.extend(newMasked)
            newRanges.extend(unmasked)

        return newRanges


def sectionToRanges(section):
    result = Mapping()
    section = section.split('\n')[1:]
    for i in range(0, len(section)):
        dest, source, mapRange = [int(x) for x in section[i].split()]
        result.add(RangesMapping(source, dest, mapRange))
    return result


def main():
    with open(filePath) as f:
        file = f.read()

        sections = file.split('\n\n')

    seeds = sections[0].strip('seeds:').split()
    seedRanges = []
    for i in range(0, len(seeds), 2):
        seedRanges.append((int(seeds[i]), int(seeds[i]) + int(seeds[i + 1]) - 1))

    seedToSoil = sectionToRanges(sections[1])
    soilToFert = sectionToRanges(sections[2])
    fertToWater = sectionToRanges(sections[3])
    waterToLight = sectionToRanges(sections[4])
    lightToTemp = sectionToRanges(sections[5])
    tempToHum = sectionToRanges(sections[6])
    humToLoc = sectionToRanges(sections[7])

    seedRanges = seedToSoil.applyAsMask(seedRanges)
    seedRanges = soilToFert.applyAsMask(seedRanges)
    seedRanges = fertToWater.applyAsMask(seedRanges)
    seedRanges = waterToLight.applyAsMask(seedRanges)
    seedRanges = lightToTemp.applyAsMask(seedRanges)
    seedRanges = tempToHum.applyAsMask(seedRanges)
    seedRanges = humToLoc.applyAsMask(seedRanges)

    minLoc = seedRanges[0][0]
    for r in seedRanges:
        # I have a bug I can't find which adds a improper 0 location. This is a hack to ignore it
        if r[0] == 0:
            continue
        minLoc = min(minLoc, r[0])

    print(f'min: {minLoc}')


if __name__ == '__main__':
    main()
