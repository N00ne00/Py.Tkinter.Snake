#no sqlite version
import tkinter as tk
import random
from tkinter import messagebox

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.resizable(False, False)
        
        # Game constants
        self.cell_size = 20
        self.width = 20
        self.height = 20
        self.speed = 150  # milliseconds
        
        # Initialize game state
        self.snake = [(5, 5), (5, 4), (5, 3)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        
        # Create canvas
        self.canvas = tk.Canvas(
            master, 
            width=self.width * self.cell_size, 
            height=self.height * self.cell_size,
            bg="black"
        )
        self.canvas.pack()
        
        # Score display
        self.score_label = tk.Label(master, text=f"Score: {self.score}", font=('Arial', 14))
        self.score_label.pack()
        
        # Draw initial game state
        self.draw_snake()
        self.draw_food()
        
        # Bind keyboard events
        self.master.bind("<KeyPress>", self.change_direction)
        
        # Start game loop
        self.update()
    
    def create_food(self):
        while True:
            food = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1)
            )
            if food not in self.snake:
                return food
    
    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x * self.cell_size, y * self.cell_size,
                (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                fill="green", tag="snake"
            )
        # Draw head differently
        head = self.snake[0]
        self.canvas.create_rectangle(
            head[0] * self.cell_size, head[1] * self.cell_size,
            (head[0] + 1) * self.cell_size, (head[1] + 1) * self.cell_size,
            fill="dark green", tag="snake"
        )
    
    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(
            x * self.cell_size, y * self.cell_size,
            (x + 1) * self.cell_size, (y + 1) * self.cell_size,
            fill="red", tag="food"
        )
    
    def change_direction(self, event):
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            # Prevent reversing direction
            if (key == "Up" and self.direction != "Down" or
                key == "Down" and self.direction != "Up" or
                key == "Left" and self.direction != "Right" or
                key == "Right" and self.direction != "Left"):
                self.direction = key
    
    def move_snake(self):
        if self.game_over:
            return
        
        head = self.snake[0]
        if self.direction == "Up":
            new_head = (head[0], head[1] - 1)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 1)
        elif self.direction == "Left":
            new_head = (head[0] - 1, head[1])
        elif self.direction == "Right":
            new_head = (head[0] + 1, head[1])
        
        # Check for collisions
        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
            self.master.destroy()
            return
        
        self.snake.insert(0, new_head)
        
        # Check if snake ate food
        if new_head == self.food:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.create_food()
            self.draw_food()
        else:
            self.snake.pop()
    
    def update(self):
        self.move_snake()
        self.draw_snake()
        if not self.game_over:
            self.master.after(self.speed, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
