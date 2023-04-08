import random
import pathlib
from string import ascii_letters, ascii_uppercase
from rich import print
from rich.console import Console
from rich.theme import Theme
import contextlib

console = Console(width=40, theme=Theme({"warning": "red on yellow"}))
num_trys = 6
num_letters = 5
words_path = pathlib.Path(__file__).parent / "wordlist.txt"


def refresh_page(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")


def get_random_word(word_list: list):
    """Get a random five-letter word from a list of strings.

    ## Example:

    >>> get_random_word(["snake", "worm", "it'll"])
    'SNAKE'
    """
    if Words := [
        word.upper()
        for word in word_list
        # makes sure that all words are len of num_letters char long and all ascii letters
        if len(word) == num_letters and all(letter in ascii_letters for letter in word)
    ]:
        return random.choice(Words)
    else:
        console.print(
            f"No words of length {num_letters} in the word list", style="warning"
        )
        raise SystemExit()


def guess_word(previous_guesses):
    guess = console.input("\nGuess word: ").upper()

    if guess in previous_guesses:
        console.print(f"You've already guessed {guess}.", style="warning")
        return guess_word(previous_guesses)

    if len(guess) != num_letters:
        console.print(f"Your guess must be {num_letters} letters.", style="warning")
        return guess_word(previous_guesses)

    if any((invalid := letter) not in ascii_letters for letter in guess):
        console.print(
            f"Invalid letter: '{invalid}'.\nPlease use English letters.",
            style="warning",
        )
        return guess_word(previous_guesses)
    return guess


def show_guesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    for guess in guesses:
        styled_guess = []
        letter_counts = {letter: word.count(letter) for letter in set(word)}
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
                letter_counts[letter] -= 1

        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"     
            elif letter in word and letter_counts[letter] > 0:
                style = "bold white on yellow"
                letter_counts[letter] -= 1
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"

            styled_guess.append(f"[{style}]{letter}[/]")

            if letter != "_":
                letter_status[letter] = f"[{style}]{letter}[/]"

        console.print("".join(styled_guess), justify="center")
    console.print("\n"+" ".join(letter_status.values()),justify= "center")



def game_over(guesses: list, word: str, guessed_correctly: bool):
    if guessed_correctly:
        refresh_page(headline="You Won")
        console.print(f"\n[bold white on green]Correct, the word is{word}[/]")
    else:
        refresh_page(headline="Game Over")
        console.print(f"\n[bold white on red]Sorry, the word is {word}[/]")
    show_guesses(guesses, word)


def main():
    word = get_random_word(words_path.read_text(encoding="utf-8").split("\n"))
    guesses = ["_" * num_letters] * num_trys

    with contextlib.suppress(KeyboardInterrupt):
        for idx in range(num_trys):
            refresh_page(headline=f"Guess {idx +1}/{num_trys}")
            show_guesses(guesses, word)

            guesses[idx] = guess_word(previous_guesses=guesses[:idx])
            if guesses[idx] == word:
                break

            

    game_over(guesses, word, guessed_correctly=guesses[idx] == word)


if __name__ == "__main__":
    main()
