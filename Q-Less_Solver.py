import time
import random
from itertools import permutations
import os.path

# TODO: Seperate "preperation" operatinos. I.e. only load the dictionary once, not over and over when trying again
# TODO: Ask at the start of the program how many times to try, and then loop that many times

global foundWord
foundWord = None

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

def rollTheDice(): 
  rolledDice = []
  for i in range(1, 13):
    rolledDice.append(diceDict[i-1][random.randint(0, 5)])
  return rolledDice
  

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


def getWordToSearch():
  word = input("What word do you want to search for: ")
  return word.upper()


def searchForWord(word, dictionary):
  for i in range(len(dictionary)):
    if dictionary[i] == word:
      # results = word
      return i
      



def makeWordArr(wLen, rolledDice):
  print("Making word array")
  vowels = ['A', 'E', 'I', 'O', 'U', 'Y']
  wordLetters = []
  noRedoArray = []
  areVowels = False

  while areVowels == False:
    wordLetters.clear()
    i = 0
    while i < wLen:
      randLetterIndex = random.randint(0, 11)
    
      if randLetterIndex not in noRedoArray:
        wordLetters.append(rolledDice[randLetterIndex])
        noRedoArray.append(randLetterIndex)
        i += 1
    print(wordLetters)
    for i in range(len(wordLetters)): 
      if wordLetters[i] in vowels:
        areVowels = True
  
  print("Word array being returned")
  return wordLetters


def descrambleWordArr(wordLetters):
  print("Descrambling word array")
  wordString = ''.join(wordLetters)
  global perms
  perms = [''.join(p) for p in permutations(wordString)]
  print(perms)
  

def searchPermsForWords():
    # Check if any permutation is a valid word in the dictionary
    i = 0
    for perm in perms:
        if perm in dictionary:
            print(f"Found valid word: {perm}")
            return perm  # Return the first found word
        i += 1
        if i == 1000000:
          break



def mainProgram():
  # Turn the dictionary.txt into a list (array) and store it globally
  global dictionary 
  dictionary = load_dictionary()

  # Create the array of rolled dice that can be used to play
  # TODO: Fetch these from user input, 
  # rather than the whole game be computerized
  rolledDice = rollTheDice()

  print("Rolled Dice")
  print(rolledDice)


  startTime = time.time()
  descrambleWordArr(makeWordArr(7, rolledDice))
  endTime = time.time()

  totalTime = str(endTime - startTime)
  print(f"All permutations found in {totalTime} seconds")

  
  print("Looking for words in permutations")
  startTime = time.time()

  foundWord = searchPermsForWords()
  endTime = time.time()
  totalTime = str(endTime - startTime)
  print(f"Search completed in {totalTime} seconds")
    # Check if a word was found
  if foundWord:
      print("The program found this solution with the given dice: ", foundWord)
  else:
      print("No valid word found with the given dice.")



def tryUntilFound():
  while foundWord == None:
    # Print "Trying again" 5 times
    for i in range(5):
      print("Trying again")  
    mainProgram()




tryUntilFound()
