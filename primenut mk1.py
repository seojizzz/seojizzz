import tkinter as tk
import random
import time

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]
PENALTY_TIMES = [0.1, 0.1, 0.2, 0.3, 0.5, 0.8, 1.3, 2.1, 3.4, 5.5, 8.9, 14.4]

class PrimeFactorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Prime Factorization Game")
        self.root.geometry("500x300")  # Set larger window size
        
        self.time_limit = 120  # Change to 120 for 2 minutes
        self.start_time = time.time()
        self.mistakes = 0
        self.current_number = self.generate_number()
        
        self.label = tk.Label(root, text=f"Factorize: {self.current_number}", font=("Arial", 23))
        self.label.pack()
        
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()
        
        self.buttons = {}
        for prime in PRIMES:
            btn = tk.Button(self.buttons_frame, text=str(prime), command=lambda p=prime: self.factorize(p))
            btn.pack(side=tk.LEFT, padx=15, pady=15)
            self.buttons[prime] = btn
        
        self.time_label = tk.Label(root, text=f"Time Left: {self.time_limit}s", font=("Arial", 17))
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
            penalty = PENALTY_TIMES[min(self.mistakes - 1, len(PENALTY_TIMES) - 1)]
            self.time_limit -= penalty
            self.label.config(text=f"Wrong! Penalty: {penalty}s. Factorize: {self.current_number}")
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
            self.label.config(text="Time's up! Game Over.")
            for widget in self.buttons_frame.winfo_children():
                widget.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = PrimeFactorGame(root)
    root.mainloop()

