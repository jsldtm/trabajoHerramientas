"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges? (Not implemented here)
3. How would you move the food? (Implemented) ## ya realizado
4. Change the snake to respond to mouse clicks. (Not implemented here) ## ya realizado
"""

from random import randrange, choice
from turtle import *

from freegames import square, vector

# Definir los colores posibles (sin contar 'rojo')
colors = ['blue', 'green', 'yellow', 'purple', 'orange']

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
game_width = 400  # Definir el ancho de la pantalla de juego
game_height = 400  # Definir la altura de la pantalla de juego

def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y


def inside(head, width=game_width, height=game_height):
    """Return True if head inside boundaries."""
    return -width // 2 < head.x < width // 2 and -height // 2 < head.y < height // 2


def move_food():
    
    """Mueve la comida a una posición aleatoria entre el área del juego."""
    
    while True:
        # Se generan coordenadas aleatorias dentro del área del juego:
        new_food_x = randrange(-game_width // 20 + 1, game_width // 20 - 1) * 10
        new_food_y = randrange(-game_height // 20 + 1, game_height // 20 - 1) * 10

        # Se revisa si ‘tal’ nueva posición es válida (no ocupada por la serpiente)
        valid_position = True
        for body in snake:
            if new_food_x == body.x and new_food_y == body.y:
                valid_position = False
                break

        # Si es así, se sale del ‘for’ anterior, y se define la nueva posición
        if valid_position:
            food.x = new_food_x
            food.y = new_food_y
            break


def move():
    """Move snake forward one segment."""
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    food_color = choice(colors.copy())  # Copiar para evitar la modificación del Arreglo

    if head == food:
        print('Snake:', len(snake))
        move_food()  # Generate new food position

        ### Modificaciones de 'color de serpiente':
        # Escoger un color aleatorio (del arreglo anterior 'colors')
        snake_color = choice(colors)
    

    else:
        snake.pop(0)
        snake_color = choice(colors)  # Actualizar el color de la serpiente en cada 'movida'

    clear()

    for body in snake:
        square(body.x, body.y, 9, snake_color)

    square(food.x, food.y, 9, 'green')
    update()
    ontimer(move, 100)

setup(game_width, game_height, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
move_food()  # Se llama a la funcion 'move_food()' para generar una posición inicial (de la 'comida')
move()
done()
