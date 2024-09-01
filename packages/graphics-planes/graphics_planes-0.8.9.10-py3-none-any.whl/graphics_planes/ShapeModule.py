import math
import svgwrite

class Shape:
    def __init__(self, width, height, label, x=0, y=0):
        self.width = width
        self.height = height
        self.label = label
        self.x = x
        self.y = y

    def draw(self, drawer):
        raise NotImplementedError("Subclasses should implement this method.")

    def export_to_svg(self, drawer, file_name):
        dwg = svgwrite.Drawing(file_name, profile='tiny')
        shape_group = dwg.add(dwg.g(id='shape', fill='none', stroke='black'))
        self._draw_to_svg(shape_group, drawer)
        dwg.save()

    def _draw_to_svg(self, shape_group, drawer):
        raise NotImplementedError("Subclasses should implement this method for SVG export.")
    
class Rectangle(Shape):
    def draw(self, drawer):
        x = self.height
        y = self.width
        ob = drawer
        label = self.label

        def dibujar_parte():
            # Calcula las coordenadas para centrar el rectángulo
            centro_x = x / 2
            centro_y = y / 2

            # Mueve el lápiz a la esquina superior izquierda del rectángulo
            ob.penup()
            ob.goto(-centro_x, centro_y)
            ob.pendown()

            # Dibuja el rectángulo
            for _ in range(2):
                ob.forward(x)
                ob.write(f"{x} cm", align="center", font=("Arial", 12, "normal"))
                ob.right(90)
                ob.forward(y)
                ob.right(90)
                ob.write(f"{y} cm", align="center", font=("Arial", 12, "normal"))
            
            # Mueve el lápiz al centro del rectángulo
            ob.penup()
            ob.goto(0, 0)
            ob.pendown()

            # Escribe la etiqueta en el centro del rectángulo
            ob.penup()
            ob.goto(0, 0)
            ob.write(label, align="center", font=("Arial", 16, "normal"))
            ob.pendown()

        dibujar_parte()

    def _draw_to_svg(self, shape_group, drawer):
        x = self.width
        y = self.height

        # Añadir el rectángulo al SVG
        shape_group.add(drawer.rect(insert=(self.x - x/2, self.y + y/2), size=(x, y)))

        # Añadir la etiqueta en el centro
        shape_group.add(drawer.text(self.label, insert=(self.x, self.y), text_anchor="middle"))

class Triangle(Shape):
    def draw(self, drawer):
        base_length = self.width
        triangle_height = self.height
        ob = drawer

        side_length = math.sqrt((base_length / 2) ** 2 + triangle_height ** 2)
        angle_base = math.degrees(math.atan(triangle_height / (base_length / 2)))

        def draw_part():
            ob.forward(base_length)
            ob.left(180 - angle_base)
            ob.forward(side_length)
            ob.left(2 * angle_base)
            ob.forward(side_length)
            ob.left(180 - angle_base)

            ob.penup()
            ob.goto(self.x, self.y)
            ob.write(self.label, align="center", font=("Arial", 16, "normal"))
            ob.pendown()

        draw_part()

    def _draw_to_svg(self, shape_group, drawer):
        base_length = self.width
        triangle_height = self.height

        points = [(self.x, self.y - triangle_height/2),
                  (self.x + base_length/2, self.y + triangle_height/2),
                  (self.x - base_length/2, self.y + triangle_height/2)]
        
        # Añadir el triángulo al SVG
        shape_group.add(drawer.polygon(points))

        # Añadir la etiqueta en el centro
        shape_group.add(drawer.text(self.label, insert=(self.x, self.y), text_anchor="middle"))
