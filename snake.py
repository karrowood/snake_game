# Kyle Arrowood
# 5/17/2020
# Snake_Game

import pygame
import random
from tkinter import *
from tkinter import messagebox as mb

pygame.init()

# Global Variables
width = 1000 
height = 600
rows = 60
columns = 100
window = pygame.display.set_mode([width, height])

class food:
    def __init__(self, starting_point):
        self.starting_point = starting_point
    def draw_square(self):
        length = width / columns
        x = self.starting_point[0]
        y = self.starting_point[1]
        pygame.draw.rect(window, (255, 0, 0), (int(x * length), int(y * length), int(length), int(length)))
class square:
    def __init__(self, point, x_direction=1, y_direction=0):
        self.point = point
        self.x_direction = x_direction
        self.y_direction = y_direction
    def draw_square(self):
        length = width / columns
        x = self.point[0]
        y = self.point[1]
        pygame.draw.rect(window, (0, 100, 0), (int(x * length), int(y * length), int(length), int(length)))
    def move_square(self, x_direction, y_direction):
        self.x_direction = x_direction
        self.y_direction = y_direction
        self.point = (self.point[0] + self.x_direction, self.point[1] + self.y_direction)
class snake:
    def __init__(self, head):
        self.head = head
        self.body = [self.head]
        self.x_direction = 1
        self.y_direction = 0
        self.turn_points = {} #Dictionary
    def move_snake(self, score):
        # Clicked window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pressed = pygame.key.get_pressed()
            for key in pressed:
                if pressed[pygame.K_LEFT]:
                    self.x_direction = -1
                    self.y_direction = 0
                    self.turn_points[self.head.point] = [self.x_direction, self.y_direction]
                elif pressed[pygame.K_RIGHT]:
                    self.x_direction = 1
                    self.y_direction = 0
                    self.turn_points[self.head.point] = [self.x_direction, self.y_direction]
                elif pressed[pygame.K_UP]:
                    self.x_direction = 0
                    self.y_direction = -1
                    self.turn_points[self.head.point] = [self.x_direction, self.y_direction]
                elif pressed[pygame.K_DOWN]:
                    self.x_direction = 0
                    self.y_direction = 1
                    self.turn_points[self.head.point] = [self.x_direction, self.y_direction]
        for i, sq in enumerate(self.body):
            position = sq.point
            # Checks to see if the specific body link is in turn_points,
            # and if it is, then turn at that point
            if position in self.turn_points:
                change_dir = self.turn_points[position]
                sq.move_square(change_dir[0], change_dir[1])
                # Removes turn from turn_points list after all links have gone through
                if i == len(self.body) - 1:
                    self.turn_points.pop(position)
            else:
                # Checks if snake hits itself
                for j in range(1, len(self.body)):
                    if self.body[0].point == self.body[j].point:
                        goodbye_message(score)
                # Checks if snake hits edges
                if sq.x_direction == -1 and sq.point[0] <= 0: # Left Wall
                    goodbye_message(score)
                elif sq.x_direction == 1 and sq.point[0] >= columns - 1: # Right Wall
                    goodbye_message(score)
                elif sq.y_direction == 1 and sq.point[1] >= rows - 1:
                    goodbye_message(score)
                elif sq.y_direction == -1 and sq.point[1] <= 0:
                    goodbye_message(score)
                # Snake did not hit edges 
                else:
                    sq.move_square(sq.x_direction, sq.y_direction)

    def add_link(self):
        tail = self.body[-1]
        if tail.x_direction == 1 and tail.y_direction == 0: # Going Right
            self.body.append(square((tail.point[0] - 1, tail.point[1]), tail.x_direction, tail.y_direction))
        elif tail.x_direction == -1 and tail.y_direction == 0: # Going Left
            self.body.append(square((tail.point[0] + 1, tail.point[1]), tail.x_direction, tail.y_direction))
        elif tail.x_direction == 0 and tail.y_direction == 1: # Going Down
            self.body.append(square((tail.point[0], tail.point[1] - 1), tail.x_direction, tail.y_direction))
        elif tail.x_direction == 0 and tail.y_direction == -1: # Going Up
            self.body.append(square((tail.point[0], tail.point[1] + 1), tail.x_direction, tail.y_direction))
    def draw_snake(self):
        for sq in self.body:
            sq.draw_square()
def refresh(food, snake):
    window.fill((153, 204, 255))
    food.draw_square()
    snake.draw_snake()
    pygame.display.update()
class difficulty_message:
    def __init__(self):
        self.speed = 0
        self.message = ""
    def show_window(self):
        window = Tk()
        window.title("Choose a difficult:")
        label = Label(window, text = "Choose a difficulty:")
        def easy_cb():
            self.speed = 20
            self.message = "Easy"
            window.destroy()
        def medium_cb():
            self.speed = 30
            self.message = "Medium"
            window.destroy()
        def hard_cb():
            self.speed = 45
            self.message = "Hard"
            window.destroy()
        def extreme_cb():
            self.speed = 100
            self.message = "Extreme"
            window.destroy()
        button1 = Button(window, text = "Easy", command = easy_cb)
        button2 = Button(window, text = "Medium", command = medium_cb)
        button3 = Button(window, text = "Hard", command = hard_cb)
        button4 = Button(window, text = "Extreme", command = extreme_cb)
        label.pack()
        button1.pack(side = LEFT, padx = 5, pady = 10)
        button2.pack(side = LEFT, padx = 5, pady = 10)
        button3.pack(side = LEFT, padx = 5, pady = 10)
        button4.pack(side = LEFT, padx = 5, pady = 10)
        window.mainloop()
def goodbye_message(score):
    window = Tk()
    window.title("Game Over!")
    label = Label(window, text = "You scored: " + str(score) + "\nDo you want to play again?")
    def yes_cb():
        window.destroy()
        main()
    def no_cb():
        mb.showinfo("Goodbye!", "Thanks for playing!")
        pygame.quit()
        window.destroy()
        quit()
    yes = Button(window, text = "Yes", command = yes_cb)
    no = Button(window, text = "No", command = no_cb)
    label.pack()
    yes.pack(side = LEFT, padx = 30, pady = 10)
    no.pack(side = LEFT, padx = 5, pady = 10)
    window.mainloop()
def main():
    score = 0
    pygame.display.set_caption("Snake Game!")
    # Fills window with white
    window.fill((153, 204, 255))
    # Starting point of food
    start = (random.randrange(1, columns), random.randrange(1, rows))
    foo = food(start)
    foo.draw_square()
    # Creates a head square object and a snake
    point = (5, 5)
    head = square(point)
    sn = snake(head)
    sn.draw_snake()
    # Shows difficulty message and assigns speed
    dif = difficulty_message()
    dif.show_window()
    # Game Loop
    clock = pygame.time.Clock()
    running = True
    while running:
        pygame.time.delay(10)
        clock.tick(dif.speed)
        sn.move_snake(score)
        if sn.body[0].point == foo.starting_point:
            for i in range(10):
                sn.add_link()
            start = (random.randrange(1, columns), random.randrange(1, rows))
            foo = food(start)
            foo.draw_square()
            score += 10
            pygame.display.set_caption("Snake: " + dif.message + " Score: " + str(score))
        refresh(foo, sn)
main()
