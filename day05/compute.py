#!/usr/bin/env python3
import time


class Mapping:
    def __init__(self, line: str):
        linesplit = line.split(' ')
        self.dest_range_start = int(linesplit[0])
        self.source_range_start = int(linesplit[1])
        self.range_length = int(linesplit[2])
    
    def __str__(self):
        return str(self.dest_range_start) + ' ' + str(self.source_range_start) + ' ' + str(self.range_length)
    
    def source_in_range(self, source: int):
        return self.source_range_start <= source < self.source_range_start + self.range_length
    
    def dest_in_range(self, dest: int):
        return self.dest_range_start <= dest < self.dest_range_start + self.range_length
    
    def map_source_to_dest(self, source: int):
        return self.dest_range_start + source - self.source_range_start
    
    def map_dest_to_source(self, dest: int):
        return self.source_range_start + dest - self.dest_range_start


class Almanac:
    def __init__(self):
        self.seed2soilMappings = []
        self.soil2fertilizerMappings = []
        self.fertilizer2waterMappings = []
        self.water2lightMappings = []
        self.light2temperatureMappings = []
        self.temperature2humidityMappings = []
        self.humidity2locationMappings = []

    def seed2soil(self, seed: int):
        return convert_source_to_dest(seed, self.seed2soilMappings)
    
    def soil2fertilizer(self, soil: int):
        return convert_source_to_dest(soil, self.soil2fertilizerMappings)
    
    def fertilizer2water(self, fertilizer: int):
        return convert_source_to_dest(fertilizer, self.fertilizer2waterMappings)
    
    def water2light(self, water: int):
        return convert_source_to_dest(water, self.water2lightMappings)
    
    def light2temperature(self, light: int):
        return convert_source_to_dest(light, self.light2temperatureMappings)
    
    def temperature2humidity(self, temperature: int):
        return convert_source_to_dest(temperature, self.temperature2humidityMappings)
    
    def humidity2location(self, humidity: int):
        return convert_source_to_dest(humidity, self.humidity2locationMappings)
    
    def seed2location(self, seed: int):
        soil = self.seed2soil(seed)
        fertilizer = self.soil2fertilizer(soil)
        water = self.fertilizer2water(fertilizer)
        light = self.water2light(water)
        temperature = self.light2temperature(light)
        humidity = self.temperature2humidity(temperature)
        location = self.humidity2location(humidity)
        return location
    
    def location2seed(self, location: int):
        humidity = convert_dest_to_source(location, self.humidity2locationMappings)
        temperature = convert_dest_to_source(humidity, self.temperature2humidityMappings)
        light = convert_dest_to_source(temperature, self.light2temperatureMappings)
        water = convert_dest_to_source(light, self.water2lightMappings)
        fertilizer = convert_dest_to_source(water, self.fertilizer2waterMappings)
        soil = convert_dest_to_source(fertilizer, self.soil2fertilizerMappings)
        seed = convert_dest_to_source(soil, self.seed2soilMappings)
        return seed
    
    def print_almanac_lengths(self):
        print('seed2soilMappings: ' + str(len(self.seed2soilMappings)))
        print('soil2fertilizerMappings: ' + str(len(self.soil2fertilizerMappings)))
        print('fertilizer2waterMappings: ' + str(len(self.fertilizer2waterMappings)))
        print('water2lightMappings: ' + str(len(self.water2lightMappings)))
        print('light2temperatureMappings: ' + str(len(self.light2temperatureMappings)))
        print('temperature2humidityMappings: ' + str(len(self.temperature2humidityMappings)))
        print('humidity2locationMappings: ' + str(len(self.humidity2locationMappings)))

def convert_source_to_dest(source: int, mappings: list[Mapping]):
    for mapping in mappings:
        if mapping.source_in_range(source):
            return mapping.map_source_to_dest(source)
    return source

def convert_dest_to_source(dest: int, mappings: list[Mapping]):
    for mapping in mappings:
        if mapping.dest_in_range(dest):
            return mapping.map_dest_to_source(dest)
    return dest


class SeedRanges:
    def __init__(self, starts: list[int], range_lengths: list[int]):
        self.starts = starts
        self.range_lengths = range_lengths
        self.n = len(starts)

    def in_range(self, seed: int):
        for i in range(self.n):
            if self.starts[i] <= seed < self.starts[i] + self.range_lengths[i]:
                return True
        return False

def get_seeds_and_almanac(file_name: str):
    seeds = []
    almanac = Almanac()
    
    with open(file_name, 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip('\n').lstrip('Card ') for line in lines]
        stage = 0
        
        for line in lines:
            if not line:
                continue

            if line.startswith('seeds: '):
                seeds = [int(x) for x in line.lstrip('seeds: ').split(' ')]
                continue
            
            if line.startswith('seed-to'):
                stage = 1
                continue

            if line.startswith('soil-to'):
                stage = 2
                continue

            if line.startswith('fertilizer-to'):
                stage = 3
                continue

            if line.startswith('water-to'):
                stage = 4
                continue

            if line.startswith('light-to'):
                stage = 5
                continue

            if line.startswith('temperature-to'):
                stage = 6
                continue

            if line.startswith('humidity-to'):
                stage = 7
                continue

            if stage == 1:
                almanac.seed2soilMappings.append(Mapping(line))
            elif stage == 2:
                almanac.soil2fertilizerMappings.append(Mapping(line))
            elif stage == 3:
                almanac.fertilizer2waterMappings.append(Mapping(line))
            elif stage == 4:
                almanac.water2lightMappings.append(Mapping(line))
            elif stage == 5:
                almanac.light2temperatureMappings.append(Mapping(line))
            elif stage == 6:
                almanac.temperature2humidityMappings.append(Mapping(line))
            elif stage == 7:
                almanac.humidity2locationMappings.append(Mapping(line))
    
    return seeds, almanac

def compute1(file_name: str):
    seeds, almanac = get_seeds_and_almanac(file_name)
    print('min location')
    locations = [almanac.seed2location(seed) for seed in seeds]
    print(min(locations))

    return min(locations)

def compute2(file_name: str):
    start_time = time.time()
    seeds, almanac = get_seeds_and_almanac(file_name)
    seedstart = []
    seedrange_length = []
    for i in range(len(seeds)):
        if i % 2 == 0:
            seedstart.append(seeds[i])
        else:
            seedrange_length.append(seeds[i])

    print('seedstart: ', seedstart)
    print('seedrange: ', seedrange_length)
    print('n_seeds = ', sum(seedrange_length))

    init_locations = [almanac.seed2location(seed) for seed in seedstart]
    print('init_locations min: ', min(init_locations))
    min_init_location = min(init_locations)

    seedranges = SeedRanges(seedstart, seedrange_length)


    for location in range(0, min_init_location + 1):
        seed = almanac.location2seed(location)
        if seedranges.in_range(seed):
            print('location: ', location, ' seed: ', seed)
            print('Computation duration: ', time.time() - start_time)
            return location
        # print('i: ', i, ' location: ', location)




if __name__ == '__main__':
    # assert compute1('sample.txt') == 35
    # print("Sample OK!")
    # print("Full: " + str(compute1('full.txt')))

    assert compute2('sample.txt') == 46
    print("Sample OK!")
    print("Full: " + str(compute2('full.txt')))
    # N seeds 1 785 709 269
    # init_locations min:  869 299 388