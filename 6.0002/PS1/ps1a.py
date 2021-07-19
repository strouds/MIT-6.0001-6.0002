###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

COWS_FILE = 'ps1_cow_data.txt'
COWS_FILE_2 = 'ps1_cow_data_2.txt'

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    
    cows_file = open(filename, 'r')
    cows = {}
    for line in cows_file:
        cow, weight = line.strip('\n').split(',')   # removes line break, splits name and weight
        cows[cow] = int(weight)
    cows_file.close()
    return cows
    

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    cows = cows.copy()
    trips_list = []
    
    # loop trips until cows empty
    while len(cows) > 0:
        weight_left = limit
        trip = []
        
        # loops cow selection cycle until no weight left
        while True: #weight_left > 0:
            cowtemp = ('',0)
            
            # loops through cows and saves the fattest one that fits
            for cow in cows:
                if cowtemp[1] < cows.get(cow) and cows.get(cow) <= weight_left:
                    cowtemp = (cow,cows.get(cow))
                    
            # checks that a cow has been chosen and takes it, or breaks loop
            if cowtemp[1] > 0:
                trip.append(cowtemp[0])
                cows.pop(cowtemp[0])
                weight_left -= cowtemp[1]
            else:
                break
            
        trips_list.append(trip)
    return(trips_list)

# print(greedy_cow_transport({'maggie':3,'jennie':8,'harold':6}))
print(len(greedy_cow_transport(load_cows(COWS_FILE))))
# print(greedy_cow_transport(load_cows(COWS_FILE_2)))

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows = cows.copy()
    
    # makes a list of len(cows) for comparison
    best_list = []
    for cow in cows:
        best_list.append(cow)
    
    #use get_partitions to generate all possible sets
    for partition in get_partitions(cows.keys()):
        trips_good = []
        #analyze each trip to make sure they pass the weight test
        for trip in partition:
            weight = 0
            
            for cow in trip:
                weight += cows[cow]
            if weight <= limit:
                trips_good.append(True)
            else:
                trips_good.append(False)
        # compares the partitions with all good trips and if it is shorter than best_list,
        #   updates best_list
        if all(trips_good) and len(partition) < len(best_list):
            best_list = partition
    return best_list
                

# brute_force_cow_transport({'maggie':3,'jennie':8,'harold':6})
print(len(brute_force_cow_transport(load_cows(COWS_FILE))))
# print(brute_force_cow_transport(load_cows(COWS_FILE_2)))
                          
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    greedy_start = time.perf_counter()
    greedy = greedy_cow_transport(load_cows(COWS_FILE))
    greedy_stop = time.perf_counter()
    # print('Trips needed for greedy algorithm:', len(greedy))
    # print('Time needed for greedy algorithm:', greedy_stop - greedy_start, 'seconds.')
    
    brute_start = time.perf_counter()
    brute_force = brute_force_cow_transport(load_cows(COWS_FILE))
    brute_stop = time.perf_counter()
    # print('\nTrips needed for brute force solution:', len(brute_force))
    # print('Time needed for brute force solution:', brute_stop - brute_start, 'seconds.')
    
    print('\nGreedy is', int((brute_stop - brute_start)/(greedy_stop - greedy_start)), 'times faster than brute force.')
    return int((brute_stop - brute_start)/(greedy_stop - greedy_start))

# numTests = 25
# total = 0
# for i in range(numTests):
#     total += compare_cow_transport_algorithms()
# print(total/numTests)