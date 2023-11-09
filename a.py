from sense_hat import SenseHat
import random
from time import sleep
from datetime import datetime

sense = SenseHat()
game_speed = 0.4
basket = [7, 4]
score = 0

w = (0, 0, 0)
r = (255, 0, 0)
b = (0, 0, 255)
game_space = [w, w, w, w, w, w, w, w,
              w, w, w, w, w, w, w, w,
              w, w, w, w, w, w, w, w,
              w, w, w, w, w, w, w, w,
              w, w, w, w, w, w, w, w,
              w, w, w, w, w, w, w, w,
              w, w, w, w, w, w, w, w,
              w, w, w, b, b, w, w, w]

def update_space(x, y, colour):
    p = 8 * x + y
    game_space[p] = colour
    sense.set_pixels(game_space)

def left(event):
    if event.action == 'pressed':
        if basket[0] - 1 == 0:
            pass
        else:
            update_space(basket[0], basket[1], w)
            basket[1] -= 1
            update_space(basket[0], basket[1] - 1, b)

def right(event):
    if event.action == 'pressed':
        if basket[1] + 1 == 8:
            pass
        else:
            update_space(basket[0], basket[1] - 1, w)
            basket[1] += 1
            update_space(basket[0], basket[1], b)

sense.stick.direction_left = left
sense.stick.direction_right = right

sense.clear()
sleep(1)
game_alive = True

last_update_time = datetime.now()

while game_alive:
    current_time = datetime.now()
    if (current_time - last_update_time).total_seconds() >= game_speed:
        last_update_time = current_time

        x = 0
        y = random.randint(0, 7)
        d = random.choice([-1, 1])
        k = 1
        update_space(x, y, r)

        while True:
            sleep(game_speed)
            update_space(x, y, w)
            if x == 7:
                if y >= basket[1] - 1 and y <= basket[1] + 1:
                    update_space(x, y, b)
                    score += 1
                    k = -1
                else:  
                    game_alive = False
                    break
            if y == 7 and d == 1:  
                d = -1
            elif y == 0 and d == -1:  
                d = 1
            y += d
            x += k
            update_space(x, y, r)
            if x == 0:
                k = 1

sense.clear()
sense.show_message('Game over', scroll_speed=0.06, back_colour=w)
sense.show_message('Score: ' + str(score), scroll_speed=0.06, back_colour=w)