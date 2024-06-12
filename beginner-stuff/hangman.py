from random import randint


def hangman(word, current_guess, guess_letter):
    result = False
    for i in range(len(word)):
        if guess_letter == word[i]:
            current_guess[i] = guess_letter
            result = True
    if not result:
        print("Incorrect guess, lost a life.")
    else:
        print("Correct guess, letter is present in the word.")
    for letter in current_guess:
        print(letter, end="")
    print("")
    return result


def hangman_main(bank, lives):
    word = bank[randint(0, 20)][:-1].lower()
    current_guess = []
    for n in range(len(word)):
        current_guess.append("_")

    while current_guess.count("_") != 0:
        guess_letter = input("Enter your guess letter : ")
        if not hangman(word, current_guess, guess_letter):
            lives -= 1
        print("Lives remaining : " + str(lives))
        if lives == 0:
            print("You lose! The word was \"" + word + "\"")
            break
    if current_guess.count("_") == 0:
        print("You win!")
    choice = input("Enter y if you want to play again : ")
    if choice.lower() == "y":
        hangman_main(bank, 7)


file = open("word_bank.txt", "r")
word_bank = file.readlines()
file.close()
hangman_main(word_bank, 7)
