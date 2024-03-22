""" Cannon, hitting targets with projectiles.

Exercises

1. Keep score by counting target hits (already implemented). 
2. Vary the effect of gravity (already implemented). Ya está
3. Apply gravity to the targets (already implemented).
4. Change the speed of the ball (and targets). Ya está

"""

from random import randrange
from turtle import *

from freegames import vector

ball = vector(-200, -200)
speed = vector(0, 0)  # Se aumenta la velocidad 'inicial' para el proyectil
targets = []


def tap(x, y):
    """Respond to screen 'click'."""
    if not inside(ball):
        ball.x = -199
        ball.y = -199
        # Aumentando la velocidad 'inicial' partiendo en su máxima posición vertical
        speed.x = (x + 200) / 15  # Modifique el compnente 'horizontal' de la velocidad
        speed.y = (y + 220) / 15  # Modifique el compnente 'vertical' de la velocidad


def inside(xy):
    """Return True if xy within screen."""
    return -200 < xy.x < 200 and -200 < xy.y < 200


def draw():
    """Draw ball and targets."""
    clear()

    for target in targets:
        goto(target.x, target.y)
        dot(20, 'blue')

    if inside(ball):
        goto(ball.x, ball.y)
        dot(6, 'red')

    update()


def move():
    """Move ball and targets."""
    if randrange(40) == 0:
        y = randrange(-150, 150)
        target = vector(200, y)
        targets.append(target)

    # Modificar para la velocidad de los 'objetivos' (azules)
    for target in targets:
        target.x -= 1  # Modificar a la velocidad deseada
        
        ## Modificación 2 (reposicionar objetivos)

        # Reposicionar los objetivos (azules) que salgan de la pantalla por el extremo derecho
        if target.x < -200:
            target.x = 200

        ## Modificación 2 (reposicionar objetivos)

    if inside(ball):
        speed.y -= 0.5  # Aumenta la fuerza gravitacional del proyectil
        ball.move(speed)

    dupe = targets.copy()
    targets.clear()

    for target in dupe:
        if abs(target - ball) > 13:
            targets.append(target)

    draw()

    # Se incrementa la 'frecuencia de actualización' para una ancimación más fluida
    ontimer(move, 25)


setup(420, 420, 370, 0)
hideturtle()
up()
tracer(False)
onscreenclick(tap)
move()
done()
