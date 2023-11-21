'''
Algorithm to Calculate the Most Likely Word:
- For each letter, calculate the likelihood the letter will be at the position
- Use these calculations to find the most likely words by scoring each word
- Guess the word with the highest score
'''
import copy

master_word_list = []
with open('./words.txt', 'r') as file:
    master_word_list = [line.strip() for line in file.readlines()]

word_probabilities_list = [0 for i in range(len(master_word_list))] #Probabilities of each word being the correct word
letter_probabilities = [[0 for i in range(5)] for j in range(26)] #Probabilities of each letter at each position in a word

def calc_probabilities_letter(letter):
  #calculates the probability of each letter appearing at each position of a 5-letter word
  for i in master_word_list:
    if i[0] == letter:
      letter_probabilities[ord(letter) - ord("a")][0] += 1
    if i[1] == letter:
      letter_probabilities[ord(letter) - ord("a")][1] += 1
    if i[2] == letter:
      letter_probabilities[ord(letter) - ord("a")][2] += 1
    if i[3] == letter:
      letter_probabilities[ord(letter) - ord("a")][3] += 1
    if i[4] == letter:
      letter_probabilities[ord(letter) - ord("a")][4] += 1
  for i in range(5):
    letter_probabilities[ord(letter) - ord("a")][i] /= len(master_word_list)
    
def calc_word_probabilities(word_copy):
  #calculates the probability of each word being the correct word based on the proabilities of each individual letter
  for i in range(len(word_copy)):
    if word_copy[i][0] == '!':
      word_probabilities_list[i] = 0
      continue
    p = 1
    for j in range(5):
      p *= letter_probabilities[ord(word_copy[i][j]) - ord("a")][j]
    word_probabilities_list[i] = p

def remove_grey(letter, word_copy):
  #updates the probabilities of each grey letter to 0 and effectively removes any word with this letter
  for i in range(len(word_copy)):
    if letter in word_copy[i]:
      word_copy[i] = "!!!!!"
  for i in range(5):
    letter_probabilities[ord(letter) - ord("a")][i] = 0

def change_yellow (letter, position, word_copy, multiplier):
  '''updates the probabilities of each yellow letter and increases the probability of a word with that letter
    at a different position'''
  for i in range(len(word_copy)):
    if letter in word_copy[i]:
      if word_copy[i][position] == letter:
        word_copy[i] = "!!!!!"
    else:
      word_copy[i] = "!!!!!"
  letter_probabilities[ord(letter) - ord("a")][position] = 0
  for i in range(5):
    if i != position:
      letter_probabilities[ord(letter) - ord("a")][i] *= multiplier

def change_green(letter, position, word_copy):
  #updates the probability of each green/correct letter and effectively removes any word without this letter
  for i in range(len(word_copy)):
    if word_copy[i][position] != letter:
      word_copy[i] = "!!!!!"
  letter_probabilities[ord(letter) - ord("a")][position] = 1

def compare_word(actual_word, guessed_word, word_copy, multiplier):
  if actual_word == guessed_word:
    return True
  for i in range(len(actual_word)):
    temp = actual_word.find(guessed_word[i])
    if actual_word[i] == guessed_word[i]:
      change_green(guessed_word[i], i, word_copy)
    elif temp != -1:
      change_yellow(guessed_word[i], i, word_copy, multiplier)
    else:
      remove_grey(guessed_word[i], word_copy)
  return False

def play_game(true_word, multiplier):
  #wordle bot guesses the word with the highest probability, receives feedback, updates probabilities, and then guesses again
  word_copy =  copy.deepcopy(master_word_list)
  found = False
  guesses = 0
  while not found:
    guess = word_copy[word_probabilities_list.index(max(word_probabilities_list))]
    print(guess)
    guesses += 1
    if compare_word(true_word, guess, word_copy, multiplier):
      found = True
    calc_word_probabilities(word_copy)
  return guesses

for i in range(26):
  calc_probabilities_letter(chr(ord('a') + i))
calc_word_probabilities(master_word_list)

#example game
play_game("ardor", 1)