
"""Paint, for drawing shapes.

Exercises

1. Added color (already implemented) # ya está
2. Complete circle (implemented here) # ya está
3. Complete rectangle. (not modified)
4. Complete triangle. (not modified)
5. Added width parameter. (not modified)
"""

from turtle import *
from random import randrange, choice

from freegames import vector

def line(start, end):
    """Draw line from start to end."""
    up()
    goto(start.x, start.y)
    down()
    pencolor(get_random_color())  # Se define un 'color' aleatorio para cada segmento de línea
    goto(end.x, end.y)


def square(start, end):
    """Draw square from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(4):
        forward(end.x - start.x)
        left(90)

    end_fill()


## Función círculo:
def circle(start, end):
    """Dibuje un círculo de inicio a fin:"""
    up()
    goto(start.x, start.y)
    down()
    pencolor(color)  # Set color before drawing
    radius = (end.x - start.x) // 2  # Calculate circle radius based on start and end points
    circle(start.x, start.y)


def rectangle(start, end):
    """Draw rectangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    # Calcular el 'ancho' y la 'altura' partiendo de los extremos del movimiento del cursor
    width = end.x - start.x
    height = end.y - start.y

    # Dibujar un rectánulo mediante 'giros' hacia la izquierda y derecha
    for _ in range(2):
        forward(width)
        left(90)
        forward(height)
        left(90)

    end_fill()


def triangle(start, end):
    """Draw triangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    # Calculate base and height based on start and end points
    base = end.x - start.x
    height = end.y - start.y

    # Draw triangle using forward and left turns
    for _ in range(3):
        forward(base)
        left(120)  # Angle for equilateral triangle

    end_fill()


def tap(x, y):
    """Start or continue drawing shape."""
    start = state['start']

    if start is None:
        state['start'] = vector(x, y)
    else:
        end = vector(x, y)
        shape = state['shape']
        shape(start, end)
        state['start'] = end  # Update start point for continuous drawing


def get_random_color():
    """Generando un color aleatorio"""
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    return choice(colors)


def store(key, value):
    """Store value in state at key"""
    state[key] = value


state = {'start': None, 'shape': line}
setup(420, 420, 370, 0)
onscreenclick(tap)  # Call tap on click (hold)
listen()
onkey(undo, 'u')
onkey(lambda: color('black'), 'K')
onkey(lambda: color('white'), 'W')
onkey(lambda: color('green'), 'G')
onkey(lambda: color('blue'), 'B')
onkey(lambda: color('red'), 'R')
onkey(lambda: store('shape', line), 'l')
onkey(lambda: store('shape', square), 's')
onkey(lambda: store('shape', circle), 'c')
onkey(lambda: store('shape', rectangle), 'r')
onkey(lambda: store('shape', triangle), 't')
done()
