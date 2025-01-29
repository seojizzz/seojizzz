#changelog: added music nad upgraded window size

import tkinter as tk
import random
import time
import pygame

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]
PENALTY_TIMES = [0.1, 0.1, 0.2, 0.3, 0.5, 0.8, 1.3, 2.1, 3.4, 5.5, 8.9, 14.4]

class PrimeFactorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Prime Factorization Game")
        self.root.geometry("1000x400")  # Set larger window size
        
        pygame.mixer.init()
        pygame.mixer.music.load("C:\\Users\\sjin5\\OneDrive\\Documents\\Code\\math club\\copyrighted tetrio music.mp3")  # Ensure the file is in the same folder
        pygame.mixer.music.set_volume(0.5)  # Lower the volume
        pygame.mixer.music.play(-1)  # Loop the music
        
        self.time_limit = 60  # Change to 120 for 2 minutes
        self.start_time = time.time()
        self.mistakes = 0
        self.current_number = self.generate_number()
        
        self.label = tk.Label(root, text=f"Factorize: {self.current_number}", font=("Arial", 16))
        self.label.pack()
        
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()
        
        self.buttons = {}
        for prime in PRIMES:
            btn = tk.Button(self.buttons_frame, text=str(prime), command=lambda p=prime: self.factorize(p), width=5, height=2, font=("Arial", 14))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.buttons[prime] = btn
        
        self.time_label = tk.Label(root, text=f"Time Left: {self.time_limit}s", font=("Arial", 14))
        self.time_label.pack()
        
        self.update_timer()

    def generate_number(self):
        num_factors = random.randint(2, 5)
        factors = random.choices(PRIMES, k=num_factors)
        return self.prod(factors)
    
    def prod(self, factors):
        result = 1
        for f in factors:
            result *= f
        return result
    
    def factorize(self, prime):
        if self.current_number % prime == 0:
            self.current_number //= prime
            self.highlight_button(prime, "#90EE90")  # Light pastel green
            if self.current_number == 1:
                self.label.config(text="Correct! Generating new number...")
                self.root.after(1000, self.new_round)
            else:
                self.label.config(text=f"Factorize: {self.current_number}")
        else:
            self.mistakes += 1
            if self.mistakes < len(PENALTY_TIMES):
                penalty = PENALTY_TIMES[self.mistakes - 1]
            else:
                penalty = PENALTY_TIMES[-1] * 1.6  # Continue Fibonacci-like growth
                PENALTY_TIMES.append(penalty)
            
            self.time_limit -= penalty
            self.label.config(text=f"Wrong! Penalty: {penalty:.1f}s. Factorize: {self.current_number}")
            self.highlight_button(prime, "#FFB6C1")  # Light pastel red
    
    def highlight_button(self, prime, color):
        btn = self.buttons.get(prime)
        if btn:
            btn.config(bg=color)
            self.root.after(500, lambda: btn.config(bg="SystemButtonFace"))
    
    def new_round(self):
        self.current_number = self.generate_number()
        self.label.config(text=f"Factorize: {self.current_number}")
    
    def update_timer(self):
        elapsed = time.time() - self.start_time
        remaining_time = max(0, self.time_limit - elapsed)
        self.time_label.config(text=f"Time Left: {remaining_time:.1f}s")
        if remaining_time > 0:
            self.root.after(100, self.update_timer)
        else:
            self.end_game()
    
    def end_game(self):
        self.label.config(text="Time's up! Game Over.")
        for widget in self.buttons_frame.winfo_children():
            widget.config(state=tk.DISABLED)
        pygame.mixer.music.stop()
        # pygame.mixer.music.load("C:\\Users\\sjin5\\OneDrive\\Documents\\Code\\math club\\game_over.mp3")  # Load different music
        # pygame.mixer.music.play()

if __name__ == "__main__":
    root = tk.Tk()
    game = PrimeFactorGame(root)
    root.mainloop()
