# This code creates a simple GUI simulation of the Stone-Paper-Scissor game using Tkinter.
import tkinter as tk
import random
# Emojis
STONE = "🪨"
PAPER = "📄"
SCISSOR = "✂️"

# Rules: (A beats B → A turns B into A)
rules = {
    (STONE, PAPER): PAPER,
    (PAPER, SCISSOR): SCISSOR,
    (SCISSOR, STONE): STONE
}

class Emoji:
    def __init__(self, canvas, emoji, x, y):
        self.canvas = canvas
        self.emoji = emoji
        self.x = x
        self.y = y
        self.dx = random.choice([-2, -1, 1, 2])
        self.dy = random.choice([-2, -1, 1, 2])
        self.label = canvas.create_text(x, y, text=emoji, font=("Arial", 20))

    def move(self):
        self.x += self.dx
        self.y += self.dy
        # Bounce off edges
        if not (20 < self.x < 480): self.dx *= -1
        if not (20 < self.y < 480): self.dy *= -1
        self.canvas.move(self.label, self.dx, self.dy)

    def coords(self):
        return self.canvas.coords(self.label)

    def update_emoji(self, new_emoji):
        self.emoji = new_emoji
        self.canvas.itemconfig(self.label, text=new_emoji)

class Game:
    def __init__(self, root, count=30):
        self.root = root
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()
        self.emojis = []

        # Add random emojis
        for _ in range(count):
            emoji = random.choice([STONE, PAPER, SCISSOR])
            x, y = random.randint(30, 470), random.randint(30, 470)
            self.emojis.append(Emoji(self.canvas, emoji, x, y))

        self.running = True
        self.animate()

    def animate(self):
        if not self.running:
            return

        for emoji in self.emojis:
            emoji.move()

        self.check_collisions()
        self.root.after(50, self.animate)

        if self.check_winner():
            self.running = False

    def check_collisions(self):
        for i in range(len(self.emojis)):
            for j in range(i + 1, len(self.emojis)):
                e1 = self.emojis[i]
                e2 = self.emojis[j]

                x1, y1 = e1.coords()
                x2, y2 = e2.coords()

                # Distance between emojis
                if abs(x1 - x2) < 20 and abs(y1 - y2) < 20:
                    pair = (e1.emoji, e2.emoji)
                    if pair in rules:
                        winner = rules[pair]
                        e1.update_emoji(winner)
                        e2.update_emoji(winner)
                    elif (pair[::-1]) in rules:
                        winner = rules[pair[::-1]]
                        e1.update_emoji(winner)
                        e2.update_emoji(winner)

    def check_winner(self):
        first = self.emojis[0].emoji
        if all(e.emoji == first for e in self.emojis):
            self.canvas.create_text(250, 250, text=f"🏆 Winner: {first}", font=("Arial", 24), fill="green")
            return True
        return False

# Run the game
root = tk.Tk()
root.title("Stone Paper Scissor Simulation")
game = Game(root)
root.mainloop()
# This code creates a simple GUI simulation of the Stone-Paper-Scissor game using Tkinter.
# Emojis move around the canvas, and when they collide, they follow the game rules to determine the winner.
# The game continues until all emojis become the same type, at which point a winner is declared.
# The emojis bounce off the edges of the canvas and change based on the rules defined.