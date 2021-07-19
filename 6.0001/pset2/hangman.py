# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    char_counter = 0
    for char_word in secret_word:
        for char_guess in letters_guessed:
            if char_guess == char_word:
                char_counter += 1
    if char_counter >= len(secret_word):
        return True
    else:
        return False
            


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''
    for char_word in secret_word:
        miss_counter = 0
        for char_guess in letters_guessed:
            if char_guess == char_word:
                guessed_word += char_guess + ' '
            else:
                miss_counter += 1
            if miss_counter == len(letters_guessed):
                guessed_word += '_ '
    if guessed_word == '':
        guessed_word += '_ ' * len(secret_word)
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    not_guessed = ''
    for char in string.ascii_lowercase:
        if char not in letters_guessed:
            not_guessed += char
    return not_guessed
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    print('You have 6 guesses to guess all the letters of the secret word.\n')
    print('Wrong answers will lose guesses. Consonants will lose one guess, vowels two.')
    print('The word contains', len(secret_word), 'letters.\n')
    
    letters_guessed = []
    guessNum = 0
    warnings = 3
    uniqueLet = 0
    while guessNum < 6 and is_word_guessed(secret_word, letters_guessed) == False:
        print('You have', 6-guessNum, 'guesses left.')
        print('The remaining letters of the word are: ', get_guessed_word(secret_word, letters_guessed))
        print('Letters not yet guessed: ', get_available_letters(letters_guessed))
        guess = input('Please guess a letter: ').lower()
        if guess in get_available_letters(letters_guessed) and guess != '':
            letters_guessed += guess
            if guess in secret_word:
                print('\n* The letter', guess, 'is in the word! \n')
                uniqueLet += 1
            else:
                print('\n* The letter', guess, 'is not in the word.\n')
                if guess in 'aeiou':
                    guessNum += 2                    
                else:
                    guessNum += 1
        elif guess not in get_available_letters(letters_guessed) and warnings > 0:
            warnings -= 1
            print('\n** Please choose only from the list of letters given. You have', warnings, 'warnings left. **\n')
        elif guess in letters_guessed:
            warnings -= 1
            print('\n** You have already guessed that letter! You have', warnings, 'warnings left. **\n')
        else:
            guessNum += 1
            print('\n*** Please choose only from the list of letters given. You have 0 warnings left. ***\n')

    if is_word_guessed(secret_word, letters_guessed):
        if 6-guessNum == 1: #single case
            print(get_guessed_word(secret_word, letters_guessed))
            print('You win! The word was', secret_word + '.')
            print('Your score was', (6-guessNum) * uniqueLet + '!')
            print('(Score is calculated by multiplying the length of the word by the number of guesses remaining.')
        else:
            print(get_guessed_word(secret_word, letters_guessed))
            print('You win! The word was', secret_word + '.')
            print('Your score was', (6-guessNum) * uniqueLet + '!')
            print('(Score is calculated by multiplying the length of the word by the number of guesses remaining.')
    else:
        print('You ran out of guesses. :( RIP')
        print('The part of the word you guessed was:', get_guessed_word(secret_word, letters_guessed))
        print('The solution was:', secret_word)



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_temp = ''
    chars_used = ''
    for char in my_word:
        if char != ' ':
            my_word_temp += char
        if char not in chars_used and char != '_' and char != ' ':
            chars_used += char
    if len(my_word_temp) == len(other_word):
        position_counter = 0
        for char in other_word:
            # print(char, my_word_temp[position_counter], position_counter)
            if my_word_temp[position_counter] == '_' and char in chars_used:
                # print(char, chars_used, position_counter)
                return False
            elif my_word_temp[position_counter] != char and my_word_temp[position_counter] != '_':
                # print('1')
                return False
            position_counter += 1
        return True
    else:
        return False



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    my_word_temp = ''
    for char in my_word:
        if char != ' ':
            my_word_temp += char
    for w in wordlist:
        if match_with_gaps(my_word_temp, w) == True:
            print(w)
    

# show_possible_matches('_ _ _ _ _')

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print('You have 6 guesses to guess all the letters of the secret word.\n')
    print('Wrong answers will lose guesses. Consonants will lose one guess, vowels two.')
    print('The word contains', len(secret_word), 'letters.\n')
    
    letters_guessed = []
    guessNum = 0
    warnings = 3
    uniqueLet = 0
    while guessNum < 6 and is_word_guessed(secret_word, letters_guessed) == False:
        print('You have', 6-guessNum, 'guesses left. Type * for a hint.')
        print('The remaining letters of the word are: ', get_guessed_word(secret_word, letters_guessed))
        print('Letters not yet guessed: ', get_available_letters(letters_guessed))
        guess = input('Please guess a letter: ').lower()
        if guess in get_available_letters(letters_guessed) and guess != '':
            letters_guessed += guess
            if guess in secret_word:
                print('\n* The letter', guess, 'is in the word! \n')
                uniqueLet += 1
            else:
                print('\n* The letter', guess, 'is not in the word.\n')
                if guess in 'aeiou':
                    guessNum += 2                    
                else:
                    guessNum += 1
        elif guess not in get_available_letters(letters_guessed) and warnings > 0 and guess != '*':
            warnings -= 1
            print('\n** Please choose only from the list of letters given. You have', warnings, 'warnings left. **\n')
        elif guess in letters_guessed:
            warnings -= 1
            print('\n** You have already guessed that letter! You have', warnings, 'warnings left. **\n')
        elif guess == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        else:
            guessNum += 1
            print('\n*** Please choose only from the list of letters given. You have 0 warnings left. ***\n')

    if is_word_guessed(secret_word, letters_guessed):
        print(get_guessed_word(secret_word, letters_guessed), '\n')
        print('You win! The word was', secret_word + '.')
        print('Your score was *', (6-guessNum) * uniqueLet, '* !')
        print('(Score is calculated by multiplying the length of the word by the number of guesses remaining.)')
    else:
        print('You ran out of guesses. :( RIP')
        print('The part of the word you guessed was:', get_guessed_word(secret_word, letters_guessed))
        print('The solution was:', secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)
    #hangman('apple')

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
