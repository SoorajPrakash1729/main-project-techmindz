from tkinter import *
import random

# initializing some constants which are important for the game
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 100
SPACE_SIZE = 10
BODY_PARTS = 3
SNAKE_COLOR = 'GREEN'
FRUIT_COLOR = 'RED'
BACKGROUND_COLOR = 'BLACK'

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])#each body part starts at [0, 0]
        for x, y in self.coordinates:
            square= canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag='Snake')
            self.squares.append(square)#identifier of the corresponding rectangle on the canvas, and the list grows as new rectangles are added.
        print(self.squares)
        print(self.coordinates)

class Fruit:
    def __init__(self):
        x = random.randint(0, (int(GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
        y = random.randint(0, (int(GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FRUIT_COLOR, tag='Fruit')

        #(x, y) represents the top-left corner coordinates of the oval (fruit).
        #(x + SPACE_SIZE, y + SPACE_SIZE) represents the bottom-right corner coordinates of the oval(same as in rectangle)

def next_turn(snake,fruit):
    x, y = snake.coordinates[0]
    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE
    snake.coordinates.insert(0, (x, y))#inserting new coordinate @ the beginning
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    if x == fruit.coordinates[0] and y == fruit.coordinates[1]:
        global score
        score += 1#updates the score
        label.config(text="Score:{}".format(score))#display the new score
        canvas.delete('Fruit')#delete the fruit visually
        fruit = Fruit()#creating a new fruit again
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares.pop())#visually removing last second added square (last one is head now ,in index 0)
        #this part makes us feel the object is moving..

    if check_collision():
        game_over()
        print(snake.squares)
    else:
        window.after(SPEED, next_turn, snake, fruit)


def change_direction(event):
    global direction
    new_direction = event.keysym.lower()#converts the typed key into words 
    opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"} # Capitalize key symbols
    if new_direction != opposites.get(direction):
        direction = new_direction

def check_collision():
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        print("GAME OVER")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text='GAME OVER', fill='red', tag='gameover')


window = Tk()  # creates the main window for the game or screen for the game
window.title("Snake Game")
score = 0
direction = 'right'
window.resizable(False, False)  # ensures that the window can't be resized
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()  # placing the label within the main window
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)  # creating the space where the snake runs
canvas.pack()
window.update()  # Update the window to ensure it's drawn on the screen
window_width = window.winfo_width()  # returns current width of the window
window_height = window.winfo_height()  # returns current height of the window
screen_width = window.winfo_screenwidth()  # returns current width of the laptop screen in pixels
screen_height = window.winfo_screenheight()  # returns current height of laptop screen in pixels

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # locate the window in the center of our screen, no need to drag manually.

window.bind('<Key>', change_direction)  #linking any key press event to the change_direction function


snake = Snake()
fruit = Fruit()

next_turn(snake,fruit)

window.mainloop()  # allows the game to respond to user actions until the window is closed or the program is terminated.
