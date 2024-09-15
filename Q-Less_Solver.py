import time
import random
from itertools import permutations
import os.path

# TODO: After a certain amount of tries with (currently) 7 letter words, try again with 6 of the letters from the same dice.
#       Ensure that we are using the same 12 letter group each time
# TODO: Ask at the start of the program how many times to try, and then loop that many times
# TODO: Multi-threading

diceDict = [['M', 'M', 'L', 'L', 'B', 'Y'],
           ['V', 'E', 'G', 'K', 'P', 'P'],
           ['H', 'H', 'N', 'N', 'R', 'R'],
           ['D', 'F', 'R', 'L', 'L', 'W'],
           ['R', 'R', 'D', 'L', 'G', 'G'],
           ['X', 'K', 'B', 'S', 'Z', 'N'],
           ['W', 'H', 'H', 'T', 'T', 'P'],
           ['C', 'C', 'B', 'T', 'J', 'D'],
           ['C', 'C', 'M', 'T', 'T', 'S'],
           ['O', 'I', 'I', 'N', 'N', 'Y'],
           ['A', 'E', 'I', 'O', 'U', 'U'],
           ['A', 'A', 'E', 'E', 'O', 'O']]

def roll_the_dice():
  rolled_dice = []
  for i in range(1, 13):
    rolled_dice.append(diceDict[i - 1][random.randint(0, 5)])
  return rolled_dice
  

def load_dictionary():
  # Find path to dictionary.txt file
  scriptDirectory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
  dictionaryPath = os.path.join(scriptDirectory, 'dictionary.txt')  # Join script directory and filename
    
  if not os.path.exists(dictionaryPath):
    print("Dictionary file not found!")
    return []

  # Load wordlist into a Python list (array)
  with open(dictionaryPath, 'r') as file:
    # Read each line and strip any trailing whitespace/newlines
    words = [line.strip() for line in file]
  return words


def get_word_to_search():
  word = input("What word do you want to search for: ")
  return word.upper()


def search_for_word(word, dictionary):
  for i in range(len(dictionary)):
    if dictionary[i] == word:
      # results = word
      return i
      

def make_word_arr(w_len, rolled_dice):
  print("Making word array")
  vowels = ['A', 'E', 'I', 'O', 'U', 'Y']
  word_letters = []
  noRedoArray = []
  areVowels = False

  while not areVowels:
    word_letters.clear()
    i = 0
    while i < w_len:
      randLetterIndex = random.randint(0, 11)
    
      if randLetterIndex not in noRedoArray:
        word_letters.append(rolled_dice[randLetterIndex])
        noRedoArray.append(randLetterIndex)
        i += 1
    print(word_letters)
    for i in range(len(word_letters)):
      if word_letters[i] in vowels:
        areVowels = True
  
  print("Word array being returned")
  time.sleep(1)
  return word_letters


def descramble_word_arr(word_letters):
  print("Descrambling word array")
  wordString = ''.join(word_letters)
  global perms
  perms = [''.join(p) for p in permutations(wordString)]
  print(perms)
  

def search_perms_for_words():
    # Check if any permutation is a valid word in the dictionary
    i = 0
    for perm in perms:
        if perm in dictionary:
            print(f"Found valid word: {perm}")
            return perm  # Return the first found word
        i += 1
        if i == 1000000:
          break


def try_until_found(found_word, rolled_dice, w_len):
  while found_word is None:
    print("Trying again")
    time.sleep(1)
    startTime = time.time()
    descramble_word_arr(make_word_arr(w_len, rolled_dice))
    endTime = time.time()

    totalTime = int((endTime - startTime))
    print(f"All permutations found in {totalTime} seconds")

    print(f"Looking for words in {len(perms)}permutations")
    startTime = time.time()

    found_word = search_perms_for_words()
    endTime = time.time()
    totalTime = str(endTime - startTime)
    print(f"Search completed in {totalTime} seconds")
      # Check if a word was found
    if found_word:
        print("The program found this solution with the given dice: ", found_word)
    else:
        print("No valid word found with the given dice.")
        time.sleep(1)


def start_up_ops():
  # Initialize the variable found_word
  global found_word
  found_word = None

  # Turn the dictionary.txt into a list (array) and store it globally
  global dictionary 
  dictionary = load_dictionary()

  # Create the array of rolled dice that can be used to play
  # TODO: Fetch these from user input, 
  # rather than the whole game be computerized
  global rolledDice
  rolledDice = roll_the_dice()

  print("Rolled Dice")
  print(rolledDice)

  w_len = int(input("What word length do you want to search for? : "))

  return found_word, rolledDice, w_len


def main():
  returned_tuple = start_up_ops()
  try_until_found(returned_tuple[0], returned_tuple[1], returned_tuple[2])



main()
