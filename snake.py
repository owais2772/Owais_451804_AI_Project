import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"

        self.ai_snake = [(300, 300), (310, 300), (320, 300)]
        self.ai_direction = "Left"

        # Set the time limit (in milliseconds)
        self.time_limit = 60000  # 60 seconds
        # Initialize score
        self.player_score = 0
        self.ai_score = 0

        # Create and place the score labels
        self.player_score_label = tk.Label(self.master, text="Player Score: 0", font=("Helvetica", 12), fg="white",
                                           bg="black")
        self.player_score_label.place(x=10, y=10)  # Adjust x and y as needed

        self.ai_score_label = tk.Label(self.master, text="AI Score: 0", font=("Helvetica", 12), fg="white", bg="black")
        self.ai_score_label.place(x=280, y=10)  # Adjust x and y as needed

        self.snake_tail = []
        self.food = self.create_food()
        self.obstacles = self.create_obstacles()  # Initialize obstacles
        self.master.bind("<KeyPress>", self.change_direction)

        self.update()

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red", tags="food")
        return food

    def update_score_labels(self):
        # Update the score labels
        self.player_score_label.config(text=f"Player Score: {self.player_score}")
        self.ai_score_label.config(text=f"AI Score: {self.ai_score}")

    def move_snake(self):
        head = self.snake[0]
        self.snake_tail.insert(0, self.snake.pop())

        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)
        self.snake.insert(0, new_head)

        #Collision with Boundary
        if head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
            self.game_over()

        # Check for obstacle collision
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            obstacle_head = (obstacle_coords[0], obstacle_coords[1])
            if head == obstacle_head:
                self.game_over()

        if len(self.snake) > 1 and new_head in self.snake[1:]:
            self.game_over()

    def move_ai_snake(self):
        ai_head = self.ai_snake[0]
        food_coords = self.canvas.coords(self.food)

        # Implement AI logic to move toward food while avoiding obstacles
        if ai_head[0] < food_coords[0] and not self.check_obstacle_collision("Right"):
            self.ai_direction = "Right"
        elif ai_head[0] > food_coords[0] and not self.check_obstacle_collision("Left"):
            self.ai_direction = "Left"
        elif ai_head[1] < food_coords[1] and not self.check_obstacle_collision("Down"):
            self.ai_direction = "Down"
        elif ai_head[1] > food_coords[1] and not self.check_obstacle_collision("Up"):
            self.ai_direction = "Up"

        # Move the AI snake
        if self.ai_direction == "Right":
            new_head = (ai_head[0] + 20, ai_head[1])
        elif self.ai_direction == "Left":
            new_head = (ai_head[0] - 20, ai_head[1])
        elif self.ai_direction == "Up":
            new_head = (ai_head[0], ai_head[1] - 20)
        elif self.ai_direction == "Down":
            new_head = (ai_head[0], ai_head[1] + 20)

        self.ai_snake.insert(0, new_head)
        self.ai_snake.pop()

    def check_obstacle_collision(self, direction):
        ai_head = self.ai_snake[0]

        # Calculate the new head position based on the specified direction
        if direction == "Right":
            new_head = (ai_head[0] + 20, ai_head[1])
        elif direction == "Left":
            new_head = (ai_head[0] - 20, ai_head[1])
        elif direction == "Up":
            new_head = (ai_head[0], ai_head[1] - 20)
        elif direction == "Down":
            new_head = (ai_head[0], ai_head[1] + 20)

        # Check if the new head position collides with any obstacles
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if new_head[0] == obstacle_coords[0] and new_head[1] == obstacle_coords[1]:
                return True  # Collision with obstacle

        return False  # No collision with obstacle

    def create_obstacles(self):
        # Initialize obstacles at specific coordinates
        obstacles = []
        for _ in range(5):  # Adjust the number of obstacles as needed
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            obstacle = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="blue", tags="obstacle")
            obstacles.append(obstacle)
        return obstacles

    def update(self,elapsed_time=0):
        if elapsed_time >= self.time_limit:
            self.game_over()
        self.move_snake()
        self.move_ai_snake()
        head = self.snake[0]
        self.canvas.delete("snake")
        self.canvas.delete("ai_snake")

        for segment in self.ai_snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="orange", tags="ai_snake")

        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake")

        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))  # Just to increase the length
            self.canvas.delete("food")
            self.food = self.create_food()
            self.player_score += 1
            self.update_score_labels()

        # Check if AI snake eats food
        ai_head = self.ai_snake[0]
        if ai_head[0] == food_coords[0] and ai_head[1] == food_coords[1]:
            self.ai_snake.append((0, 0))  # Just to increase the length
            self.canvas.delete("food")
            self.food = self.create_food()
            self.ai_score += 1
            self.update_score_labels()

        self.master.after(200, lambda : self.update(elapsed_time+200))

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", font=("Helvetica", 16), fill="white")
        self.master.after(200, self.master.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()