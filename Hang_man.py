import random
import os
from time import sleep

#GLOBAL VARIABLES
playing = True
list_of_words = []
tries = 7
_score = 0

#=================GRABS LIST OF WORDS FROM THE FILE hang_man_words.txt=======================|
with open("hang_man_words.txt", 'r') as words:
    words = words.read()
    words = words.split("\n")
    for word in words:
        if len(word) > 3:
            list_of_words.append(word.lower())


#creates and updates the new highscore
def score_checker(tries, _score):
    _score = _score + 10 * tries
    return _score


#if the guess is in the word, modify unders to place the letter in the appropriate spots
def mod_unders(user_guess, unders, indexes, word):
    for indx in indexes:
        unders.insert(indx, user_guess)
        unders.pop(indx+1)

    return unders


#make placeholders out of underscores to match length of word
def make_unders(words):
    unders = []
    for i in range(len(word)):
        unders.append('_')

    return unders

#This function will grab the index of all the letters in the word that match with the users guess
def grab_word_indexes(word, u_guess):
    indx = []
    for i in range(len(word)):
        if u_guess == word[i]:
            indx.append(i)

    return indx


#check if the letter in the word
def still_playing(word, user_guess, tries, used_letters):
    if user_guess not in word and user_guess not in used_letters:
        tries -= 1

    return tries


#gets users guess and checks if it's a valid input
def guess(playing, tries, word, unders, _score):
    used_letters = []
    while playing:
        if "".join(unders) == word:
            os.system('cls')
            print("You won the word was {}".format(word))
            new_high_score = score_checker(tries, _score)
            print("YOUR SCORE: {}".format(new_high_score))
            playing = False
            return new_high_score

        os.system('cls')
        print(f"Letters you have used, {used_letters}" )
        print(f'Your score: {_score}pts\n\n')
        print(f'You have {tries} tries left:\n')
        print(" ".join(unders))
        user_guess = input("Guess a letter: ").lower()

        if len(user_guess) == 1:

            # checks if player still has any tries left before continuing
            tries = still_playing(word, user_guess, tries, used_letters)  # increments tries
            if tries == 0:
                print("Sorry you lost. The word was {}".format(word))
                sleep(2)
                os.system('cls')
                return _score

            # continue with main game
            indx = grab_word_indexes(word, user_guess)

            if user_guess in word:
                unders = mod_unders(user_guess, unders, indx, word) #replaces the unders with the correct letters

            elif user_guess in used_letters:
                print("You already guess the letter \"{}\"".format(user_guess))
                sleep(1.5)

            elif user_guess not in word:
                used_letters.append(user_guess)

        else:
            print("please select only one letter")


#start of game
while playing:
    with open('highscore.txt', 'r') as score:
        big_score = score.read()
        print(f'The HIGH SCORE is: {big_score}')

    print("\nWould you like to play Hangman?")
    ans = input("Enter yes or no: ").lower()

    if ans == 'yes' or ans == "y":
        word = random.choice(list_of_words)  # grab word from list of words before playing again
        unders = make_unders(word)
        _score = guess(playing, tries, word, unders, _score) #Gets new score for high score

        with open('highscore.txt', 'r') as score_file:
            old_score = int(score_file.read())
            if _score > old_score:
                with open('highscore.txt', 'w') as score_file:
                    score_file.write(str(_score))

        playing = True

    elif ans == 'no' or ans == 'n':
        print("Goodbye! :)")
        playing = False

    else:
        print("That's not a valid option...")

exit()
