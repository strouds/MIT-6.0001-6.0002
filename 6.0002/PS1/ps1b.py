###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================
import random, time
# Problem 1
def easy_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    egg_weights = list(egg_weights)
    if egg_weights == []:
        return 0
    
    numLargest = target_weight // egg_weights[-1]
    largest_weight = egg_weights[-1] * numLargest
    if largest_weight <= target_weight:
        total = numLargest + easy_make_weight(egg_weights[:-1], target_weight - largest_weight)
    return total

def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # egg_weights = sorted(egg_weights, reverse=True)
    return decision_tree(egg_weights, target_weight, memo)[0]
    

def decision_tree(egg_weights, target_weight, memo):
    """
    Works through decision tree of eggs choices
    Takes egg_weights, target_weight, and memo from dp_make_weight
    Returns a tuple of (eggs, weight_remaining) which allows actually enough information to do this problem properly
    """
    # try 
    # print(egg_weights)
    if (tuple(egg_weights), target_weight) in memo:
        result = memo[(tuple(egg_weights), target_weight)]
        # print(egg_weights, target_weight, 'in memo')
    if egg_weights == () or target_weight == 0:
        result = (0, target_weight)
        # print(result)
    elif egg_weights[0] > target_weight:
        result = (0, target_weight)
        # print(result, egg_weights)
    elif egg_weights[0] == target_weight:
        result = (target_weight // egg_weights[0], 0)
        # print(result, egg_weights)
    else:
        result = (target_weight // egg_weights[0], target_weight % egg_weights[0])
        # print(result, egg_weights[0])
        results_list = []
        for num_eggs in range(target_weight // egg_weights[0] + 1):
            weight_remaining = target_weight - num_eggs * egg_weights[0]
            # print(num_eggs, egg_weights, weight_remaining)
            num_larger_eggs, weight_remaining = decision_tree(egg_weights[1:], weight_remaining, memo)
            # print(num_eggs, num_larger_eggs, egg_weights, weight_remaining)
            if weight_remaining == 0:
                results_list.append((num_larger_eggs + num_eggs, weight_remaining))
                # print(num_eggs, num_larger_eggs, egg_weights, weight_remaining)
                # print('results list,',results_list[-1])
        for tup in results_list:
            # print('tup=',tup)
            if tup[0] < result[0]:
                result = tup
        # print('result bottom of for', result)
                
    memo[egg_weights, target_weight] = result
    return result

def decision_tree_no_memo(egg_weights, target_weight, memo):
    """
    Works through decision tree of eggs choices
    Takes egg_weights, target_weight, and memo from dp_make_weight
    Returns a tuple of (eggs, weight_remaining) which allows actually enough information to do this problem properly
    """
    # try 
    # print(egg_weights)
    if (tuple(egg_weights), target_weight) in memo:
        result = memo[(tuple(egg_weights), target_weight)]
    if egg_weights == () or target_weight == 0:
        result = (0, target_weight)
        # print(result)
    elif egg_weights[0] > target_weight:
        result = (0, target_weight)
        # print(result)
    elif egg_weights[0] == target_weight:
        result = (target_weight // egg_weights[0], 0)
        # print(result)
    else:
        result = (target_weight // egg_weights[0], target_weight % egg_weights[0])
        results_list = []
        for num_eggs in range(target_weight // egg_weights[0] + 1):
            weight_remaining = target_weight - num_eggs * egg_weights[0]
            # print(num_eggs, egg_weights, weight_remaining)
            num_larger_eggs, weight_remaining = decision_tree(egg_weights[1:], weight_remaining, memo)
            # print(num_eggs, num_larger_eggs, egg_weights, weight_remaining)
            if weight_remaining == 0:
                results_list.append((num_larger_eggs + num_eggs, weight_remaining))
                # print(num_eggs, num_larger_eggs, egg_weights, weight_remaining)
                # print('results list,',results_list[-1])
        for tup in results_list:
            # print('tup=',tup)
            if tup[0] < result[0]:
                result = tup
        # print('result bottom of for', result)
                
    # memo[egg_weights, target_weight] = result
    return result
    

# # EXAMPLE TESTING CODE, feel free to add more if you'd like
# if __name__ == '__main__':
#     egg_weights = (1, 5, 10, 25)
#     n = 99
#     print("Egg weights = (1, 5, 10, 25)")
#     print("n = 99")
#     print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
#     print("Actual output:", dp_make_weight(egg_weights, n))
#     print()

# this part stolen from dorond on github
def buildRandomEggTuple(numItems, maxWeight):
    egg_weights = []
    for i in range(numItems):
        egg_weights.append(random.randint(1, maxWeight))
    return tuple(sorted(egg_weights))

def test_memo_time():
    egg_weights = buildRandomEggTuple(25, 90)
    n = 99
    
    print('Running decision_tree with no memoization')
    start_no_memo = time.perf_counter()
    decision_tree_no_memo(egg_weights, n, memo={})
    stop_no_memo = time.perf_counter()
    time_no_memo = stop_no_memo - start_no_memo
    print(time_no_memo, 'with no memoization')
    
    print('Running decision tree with memoization')
    start_memo = time.perf_counter()
    decision_tree(egg_weights, n, memo={})
    stop_memo = time.perf_counter()
    time_memo = stop_memo - start_memo
    print(time_memo, 'with memoization')
    
    return time_no_memo, time_memo
    

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    # egg_weights = (1, 5, 10, 25)
    # n = 99
    # print("Egg weights = (1, 5, 10, 25)")
    # print("n = 9")
    # print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    # print()
    # egg_weights = (1, 5, 10, 20)
    # n = 99
    # print("Egg weights = (1, 5, 10, 20)")
    # print("n = 99")
    # print("Expected ouput: 10 (4 * 20 + 1 * 10 + 1 * 5 + 4 * 1 = 99)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    # print()
    # egg_weights = buildRandomEggTuple(50, 90)
    # n = 99
    # print("Egg weights =", egg_weights)
    # print("n = 99")
    # #print("Expected ouput: 10 (4 * 20 + 1 * 10 + 1 * 5 + 4 * 1 = 99)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    # print()
    no_memo_sum = 0
    memo_sum = 0
    for i in range(10):
        no_memo, memo = test_memo_time()
        no_memo_sum += no_memo
        memo_sum += memo
    memo_ratio = no_memo_sum / memo_sum
    print('Using a memo makes this algorithm', round((memo_ratio - 1) * 100, 2), 'percent faster')