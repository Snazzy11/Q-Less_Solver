from itertools import permutations
import os.path
import time

global word_letters
# user_string = "YELKCF" # 6 letter example, FECKLY
# user_string = "ccnirotava" # 10 letter example, VACCINATOR
# user_string = "letsigu" # 7 letter example, UGLIEST
# user_string = "kcissenwa" # 9 letter example, WACKINESS
# user_string = "aagrmwsotesn" # 12 letter example, WAGONMASTERS #DOESNT WORK, not in dictionary
user_string = "briafcaiotn" # 11 letter example, FABRICATION

word_letters = user_string.upper()

class TrieNode:
   def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

global words
def load_dictionary():
    # Find path to dictionary.txt file
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    dictionaryPath = os.path.join(scriptDirectory, 'dictionary.txt')  # Join script directory and filename

    if not os.path.exists(dictionaryPath):
        print("Dictionary file not found!")
        return []

    # Load wordlist into a Python list (array)
    with open(dictionaryPath, 'r') as file:
        words = [line.strip() for line in file]
    return words

def descramble_word_arr(word_letters):
  print("Descrambling word array")
  wordString = ''.join(word_letters)
  global perms
  perms = [''.join(p) for p in permutations(wordString)]
  print(perms)

def insert_words(dictionary, trie):
    for word in dictionary:
        trie.insert(word)

def search_perms_for_words(dictionary):
    # Check if any permutation is a valid word in the dictionary
    i = 0
    for perm in perms:
        if perm in dictionary:
            print(f"Found valid word: {perm}")
            return perm
        i += 1
        if i == 1000000:
          break

def search_perms_with_trie(perms, trie, given_length = len(word_letters)):
    def backtrack(path, used):
        word = ''.join(path)
        if len(word) == given_length and trie.search(word):  # Check if the current path is a valid word
            print(f"Found valid word: {word}")
            return word

        for i, letter in enumerate(perms):
            if i not in used and len(word) < given_length and trie.starts_with(word + letter):  # Check if the current path + next letter can form a prefix
                found = backtrack(path + [letter], used | {i})
                if found:
                    return found
        print("No valid word found?")
        return None

    return backtrack([], set())

def main():
    startTime = time.time()
    dictionary = load_dictionary()
    stopTime = time.time()
    print(f"Time taken to load dictionary: {stopTime - startTime}")

    startTime = time.time()
    descramble_word_arr(word_letters)
    stopTime = time.time()
    print(f"Time taken to find permutations: {stopTime - startTime}")
    print(f"Number of permutations: {len(perms)}")

    trie = Trie()
    startTime = time.time()
    insert_words(dictionary, trie)
    stopTime = time.time()
    print(f"Time taken to insert into trie: {stopTime - startTime}")

    # startTime = time.time()
    # search_perms_for_words(dictionary)
    # stopTime = time.time()
    # print(f"Time taken to normal search: {stopTime - startTime}")

    trieStartTime = time.time()
    search_perms_with_trie(perms, trie)
    trieStopTime = time.time()
    print(f"Time taken to search trie: {trieStopTime - trieStartTime}")


main()