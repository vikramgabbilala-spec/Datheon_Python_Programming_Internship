import random

WORD_BANK = [
    "python",
    "hangman",
    "terminal",
    "keyboard",
    "gallows",
    "programming",
    "computer",
    "challenge",
    "rocket",
    "banana",
]

MAX_WRONG_GUESSES = 6


def clear_screen():
    print("\n" * 2)


def build_gallows(wrong_guesses):
    stages = [
        """
  +---+
  |   |
  |   
  |   
  |   
  |   
  =========
""",
        """
  +---+
  |   |
  |   O
  |   
  |   
  |   
  =========
""",
        """
  +---+
  |   |
  |   O
  |   |
  |   
  |   
  =========
""",
        """
  +---+
  |   |
  |   O
  |  /|
  |   
  |   
  =========
""",
        """
  +---+
  |   |
  |   O
  |  /|\\
  |   
  |   
  =========
""",
        """
  +---+
  |   |
  |   O
  |  /|\\
  |  / 
  |   
  =========
""",
        """
  +---+
  |   |
  |   O
  |  /|\\
  |  / \\
  |   
  =========
""",
    ]
    return stages[wrong_guesses]


def display_state(word, guessed_letters, wrong_guesses):
    print(build_gallows(wrong_guesses))
    print("Word:", " ".join(letter if letter in guessed_letters else "_" for letter in word))
    print("Guessed letters:", " ".join(sorted(guessed_letters)) if guessed_letters else "None")
    print(f"Attempts left: {MAX_WRONG_GUESSES - wrong_guesses}")


def display_title():
    print(r"""
    _    _   _   _   _   _   _   _   _
   | |  | | | | | | | | | | | | | | |
   | |__| | | | | | | | | | | | | | |
   |  __  | | | | | | | | | | | | | |
   | |  | | | | | | | | | | | | | | |
   |_|  |_| |_| |_| |_| |_| |_| |_| |_|
        _                                              _
       | |                                            | |
       | |__   __ _ _ __   __ _  ___  _ __   ___  ___ | |
       | '_ \ / _` | '_ \ / _` |/ _ \| '_ \ / _ \/ _ \| |
       | | | | (_| | | | | (_| | (_) | | | |  __/  __/| |
       |_| |_|\__,_|_| |_|\__, |\___/|_| |_|\___|\___||_|
                           __/ |
                          |___/
""")


def get_valid_guess(used_letters):
    while True:
        guess = input("Enter a letter: ").strip().lower()

        if not guess:
            print("Please enter a letter.")
            continue
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabetic letter.")
            continue
        if guess in used_letters:
            print(f"You already guessed '{guess}'. No penalty for that duplicate.")
            return None
        return guess


def play_round():
    word = random.choice(WORD_BANK)
    guessed_letters = set()
    wrong_guesses = 0
    solved = False

    print("\nNew round! Guess the hidden word one letter at a time.")

    while wrong_guesses < MAX_WRONG_GUESSES and not solved:
        clear_screen()
        print("-" * 40)
        display_state(word, guessed_letters, wrong_guesses)

        guess = get_valid_guess(guessed_letters)
        if guess is None:
            print("Try a different letter.")
            input("Press Enter to continue...")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(f"Correct! '{guess}' is in the word.")
            if all(letter in guessed_letters for letter in set(word)):
                solved = True
        else:
            wrong_guesses += 1
            print(f"Wrong! '{guess}' is not in the word.")

        input("Press Enter to continue...")

    clear_screen()
    print("-" * 40)
    print(build_gallows(wrong_guesses))

    if solved:
        print("You win! The word was:", word)
    else:
        print("Game over! The word was:", word)

    print("You guessed:", " ".join(sorted(guessed_letters)) if guessed_letters else "No letters")


def main_menu():
    while True:
        clear_screen()
        display_title()
        print("1) Play Hangman")
        print("2) Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            play_round()
            again = input("Play another round? (y/n): ").strip().lower()
            while again not in {"y", "n"}:
                again = input("Please enter 'y' or 'n': ").strip().lower()
            if again == "n":
                print("Thanks for playing!")
                break
        elif choice == "2":
            print("Thanks for playing!")
            break
        else:
            print("Invalid option. Please choose 1 or 2.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()
