# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    
    # Initialize a new list for sequences made at each layer of recursion.
    sequences_list=[]
        
    # Tests for base case of a sequence of length 1.
    # Returns a list with the input string as its only entry.
    if len(sequence) == 1:
        sequences_list.append(sequence)
        return sequences_list
    
    # Recursive case: sequence of length > 1 (if sequence is an empty string, this will return an empty list).
    # Cycles through each letter in the sequence, creating a new string removing that letter.
    else:
        for index in range(len(sequence)):
            
            # Splits the string around the working letter, then concatenates. Does not matter if only 
            # first letter is removed. Will only remove first instance of that letter so duplicates
            # may change the order of sequences returned but this shouldn't affect the result.
            new_sequence = ''.join(sequence.split(sequence[index],1))

            # Makes a recursive call using the new shortened sequence, which returns a list of strings.
            for x in get_permutations(new_sequence):
                
                # The letter chosen from the original sequence is then added back at the beginning of the returned sequence.
                # Each letter + sequence is tested to make sure it is not a duplicate, then if it is not
                # it is added to the list created at the beginning of each level of recursion.
                if str(sequence[index] + x) not in sequences_list:
                    sequences_list.append(sequence[index] + x)
                    
    # The list created in the above loops is returned to the function caller. If this is a recursive
    # sub-loop, each entry will have the letter chosen in the for loop of the superior function added to it.
    return sequences_list

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    print()
    test_1 = 'a'
    print('Input:', test_1)
    print('Expected output:', ['a'])
    print('Actual output:', get_permutations(test_1))
    
    print()
    test_2 = 'abc'
    print('Input:', test_2)
    print('Expected output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual output:', get_permutations(test_2))
    
    print()
    test_3 = 'aba'
    print('Input:', test_3)
    print('Expected output:', ['aba', 'aab', 'baa'])
    print('Actual output:', get_permutations(test_3))
    
    print()
    test_4 = 'abcba'
    print('Input:', test_4)
    print('Expected number of outputs: 5!/4 = 30.')
    print('(Duplicate letters halve the number of unique outputs for each letter - there are two in this sequence.)')
    print('Actual number of outputs:', len(get_permutations(test_4)))

