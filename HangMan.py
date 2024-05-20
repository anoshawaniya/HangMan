import random
import itertools
from tkinter import messagebox

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.words = ["SNACK", "PYTHON", "BANANA", "APPLE", "CHOCOLATE", "JUICE", "JAVA", "DATASTRUCTURE", "PROGRAMMING","FISH","MANGO"]  # Array of words
        self.word = ""
        self.guessed_letters = set()
        self.correct_letters = set()
        self.incorrect_letters = set()
        self.attempts_left = 6
        self.hangman_images = [
            tk.PhotoImage(file="hangman0.png"),
            tk.PhotoImage(file="hangman1.png"),
            tk.PhotoImage(file="hangman2.png"),
            tk.PhotoImage(file="hangman3.png"),
            tk.PhotoImage(file="hangman4.png"),
            tk.PhotoImage(file="hangman5.png"),
            tk.PhotoImage(file="hangman6.png")
        ]
        self.current_hangman_image = self.hangman_images[0]
        self.time_limit = 60  # Time limit in seconds
        self.remaining_time = self.time_limit

        # Define colors
        self.title_color = "#FF5722"
        self.word_color = "#4CAF50"
        self.result_color = "#F44336"
        self.guessed_letters_color = "#9C27B0"
        self.timer_color = "#2196F3"
        self.restart_button_color = "#FF9800"

        # Create GUI elements
        self.title_label = tk.Label(master, text="Hangman Game", font=("Arial", 15, "italic"), fg=self.title_color)
        self.title_label.pack(pady=8)

        self.word_frame = tk.Frame(master)
        self.word_frame.pack()

        self.hangman_label = tk.Label(self.word_frame, image=self.current_hangman_image)
        self.hangman_label.grid(row=0, column=0, columnspan=1)

        self.word_label = tk.Label(self.word_frame, text="", font=("Arial", 14, "bold"), fg=self.word_color)
        self.word_label.grid(row=1, column=0, columnspan=2, pady=8)

        self.hint_label = tk.Label(master, text="", font=("Arial", 14), fg=self.word_color)
        self.hint_label.pack()

        self.input_frame = tk.Frame(master)
        self.input_frame.pack()

        self.input_label = tk.Label(self.input_frame, text="Enter a letter:", font=("Arial", 20))
        self.input_label.grid(row=0, column=0, padx=5)

        self.input_entry = tk.Entry(self.input_frame, font=("Arial", 14))
        self.input_entry.grid(row=0, column=1, padx=5)

        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.submit_guess, font=("Arial", 14, "bold"))
        self.submit_button.grid(row=0, column=2, padx=5)

        self.result_label = tk.Label(master, text="", font=("Arial", 16), fg=self.result_color)
        self.result_label.pack(pady=8)

        self.guessed_label = tk.Label(master, text="Guessed Letters:", font=("Arial", 14), fg=self.guessed_letters_color)
        self.guessed_label.pack()

        self.guessed_letters_text = tk.StringVar()
        self.guessed_letters_text.set("")
        self.guessed_letters_label = tk.Label(master, textvariable=self.guessed_letters_text, font=("Arial", 14), fg=self.guessed_letters_color)
        self.guessed_letters_label.pack()

        self.timer_label = tk.Label(master, text=f"Time Left: {self.remaining_time} seconds", font=("Arial", 10), fg=self.timer_color)
        self.timer_label.pack(pady=6)

        self.restart_button = tk.Button(master, text="Restart", command=self.restart_game, font=("Arial", 12, "bold"), fg="white", bg=self.restart_button_color, state=tk.DISABLED)
        self.restart_button.pack(pady=8)

        self.new_game()

    def new_game(self):
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.correct_letters = set()
        self.incorrect_letters = set()
        self.attempts_left = 6
        self.current_hangman_image = self.hangman_images[0]
        self.word_label.config(text=self.get_word_display())
        self.result_label.config(text="")
        self.hangman_label.config(image=self.current_hangman_image)
        self.restart_button.config(state=tk.DISABLED)
        self.update_guessed_letters()
        self.start_timer()

        # Generate a hint by scrambling the word
        scrambled_word = ''.join(random.sample(self.word, len(self.word)))
        hint_word = self.unscramble_word(scrambled_word)
        hint_text = f"Hint: {scrambled_word} {hint_word}"
        self.hint_label.config(text=hint_text)

    def start_timer(self):
        self.remaining_time = self.time_limit
        self.update_timer_label()
        self.timer_id = self.master.after(1000, self.update_timer)

    def update_timer(self):
        self.remaining_time -= 1
        self.update_timer_label()
        if self.remaining_time <= 0:
            self.master.after_cancel(self.timer_id)
            self.submit_button.config(state=tk.DISABLED)
            self.show_game_over_message("Time's up! You lost.")
            self.restart_button.config(state=tk.NORMAL)
        else:
            self.timer_id = self.master.after(1000, self.update_timer)

    def update_timer_label(self):
        self.timer_label.config(text=f"Time Left: {self.remaining_time} seconds")

    def get_word_display(self):
        display = ""
        for letter in self.word:
            if letter in self.correct_letters:
                display += letter
            else:
                display += "_"
            display += " "
        return display

    def unscramble_word(self, scrambled_word):
       word_length = len(scrambled_word)
       possible_words = [''.join(perm) for perm in itertools.permutations(scrambled_word)]
       unscrambled_words =" "
       for word in possible_words:
           if word in self.words and word != self.word:
               unscrambled_words.append(word)
       return unscrambled_words
    def submit_guess(self):
        guess = self.input_entry.get().upper()
        self.input_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid Guess", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Duplicate Guess", "You have already guessed this letter.")
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            self.correct_letters.add(guess)
        else:
            self.incorrect_letters.add(guess)
            self.attempts_left -= 1
            self.update_hangman_image()

        self.word_label.config(text=self.get_word_display())
        self.result_label.config(text=self.get_result_message())
        self.update_guessed_letters()

        if self.is_game_over():
            self.master.after_cancel(self.timer_id)
            self.show_game_over_message()
            self.restart_button.config(state=tk.NORMAL)

    def update_hangman_image(self):
        self.current_hangman_image = self.hangman_images[6 - self.attempts_left]
        self.hangman_label.config(image=self.current_hangman_image)

    def get_result_message(self):
        if self.is_word_guessed():
            return "Congratulations! You won the game."
        elif self.is_game_over():
            return f"Game Over! You lost. The word was {self.word}."
        else:
            return f"Attempts Left: {self.attempts_left}"

    def is_word_guessed(self):
        return set(self.word) == self.correct_letters
    def is_game_over(self):
        return self.attempts_left == 0 or self.is_word_guessed()

    def show_game_over_message(self, message=""):
        messagebox.showinfo("Game Over", message or self.get_result_message())
    def restart_game(self):
        self.master.after_cancel(self.timer_id)
        self.new_game()
    def update_guessed_letters(self):
        guessed_letters = ", ".join(sorted(self.guessed_letters))
        self.guessed_letters_text.set(guessed_letters)

root = tk.Tk()
root.title("Hangman Game")
root.configure(bg="#ECEFF1")  # Set background color

hangman = HangmanGame(root)
root.mainloop()
