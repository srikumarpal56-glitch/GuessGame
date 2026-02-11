import random
import tkinter as tk
from tkinter import messagebox

# Try sound (Windows)
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

# Game stats
secret_number = 0
attempts = 0
wins = 0
games_played = 0
best_score = None
time_left = 30
timer_running = False

# Window
root = tk.Tk()
root.title("Guessing Game 🎮")
root.geometry("380x380")
root.resizable(False, False)

difficulty = tk.StringVar(value="Easy")

# ---------------- SOUND FUNCTIONS ---------------- #

def play_click():
    if SOUND_AVAILABLE:
        winsound.Beep(800, 100)
    else:
        root.bell()

def play_win():
    if SOUND_AVAILABLE:
        winsound.Beep(1200, 200)
        winsound.Beep(1500, 200)
    else:
        root.bell()

def play_game_over():
    if SOUND_AVAILABLE:
        winsound.Beep(400, 400)
    else:
        root.bell()

# ---------------- GAME FUNCTIONS ---------------- #

def start_new_game():
    global secret_number, attempts, games_played, time_left, timer_running

    attempts = 0
    time_left = 30
    timer_running = True
    games_played += 1

    if difficulty.get() == "Easy":
        secret_number = random.randint(1, 50)
        range_label.config(text="Range: 1 – 50")
    else:
        secret_number = random.randint(1, 100)
        range_label.config(text="Range: 1 – 100")

    entry.delete(0, tk.END)
    result_label.config(text="")
    attempts_label.config(text="Attempts: 0")
    games_label.config(text=f"Games Played: {games_played}")

    update_timer()

def check_guess():
    global attempts, wins

    if not timer_running:
        return

    guess = entry.get()

    if not guess.isdigit():
        messagebox.showerror("Error", "Enter a valid number!")
        return

    guess = int(guess)
    attempts += 1
    attempts_label.config(text=f"Attempts: {attempts}")

    if guess < secret_number:
        result_label.config(text="📉 Too Low!")
        play_click()
    elif guess > secret_number:
        result_label.config(text="📈 Too High!")
        play_click()
    else:
        wins += 1
        wins_label.config(text=f"Wins: {wins}")

        update_best_score()
        play_win()

        messagebox.showinfo("🎉 Correct!", f"You guessed it in {attempts} attempts!")
        start_new_game()

def update_best_score():
    global best_score

    if best_score is None or attempts < best_score:
        best_score = attempts
        best_label.config(text=f"Best Score: {best_score}")

def update_timer():
    global time_left, timer_running

    if timer_running:
        timer_label.config(text=f"⏱ Time Left: {time_left}s")

        if time_left > 0:
            time_left -= 1
            root.after(1000, update_timer)
        else:
            timer_running = False
            play_game_over()
            messagebox.showwarning("💥 Time Over!", f"Game Over!\nNumber was {secret_number}")

# ---------------- UI ---------------- #

title_label = tk.Label(root, text="Guess the Number 🎮", font=("Arial", 14))
title_label.pack(pady=10)

dropdown_frame = tk.Frame(root)
dropdown_frame.pack()

tk.Label(dropdown_frame, text="Difficulty:", font=("Arial", 11)).pack(side="left")
tk.OptionMenu(dropdown_frame, difficulty, "Easy", "Hard").pack(side="left")

range_label = tk.Label(root, text="Range: 1 – 50", font=("Arial", 11))
range_label.pack(pady=5)

timer_label = tk.Label(root, text="⏱ Time Left: 30s", font=("Arial", 12))
timer_label.pack(pady=5)

entry = tk.Entry(root, font=("Arial", 12), justify="center")
entry.pack(pady=5)

guess_button = tk.Button(root, text="Check Guess", command=check_guess)
guess_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=8)

# Stats 🏆
stats_frame = tk.Frame(root)
stats_frame.pack(pady=10)

attempts_label = tk.Label(stats_frame, text="Attempts: 0", font=("Arial", 11))
attempts_label.pack()

wins_label = tk.Label(stats_frame, text="Wins: 0", font=("Arial", 11))
wins_label.pack()

games_label = tk.Label(stats_frame, text="Games Played: 0", font=("Arial", 11))
games_label.pack()

best_label = tk.Label(stats_frame, text="Best Score: None", font=("Arial", 11))
best_label.pack()

new_game_button = tk.Button(root, text="New Game", command=start_new_game)
new_game_button.pack(pady=10)

# Start first game
start_new_game()

root.mainloop()
