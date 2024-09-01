import turtle
import math
import svgwrite

class Shape:
    def __init__(self, width, height, label):
        self.width = width
        self.height = height
        self.label = label

    def draw(self, drawer):
        raise NotImplementedError("Subclasses should implement this method.")

    def export_to_svg(self, drawer, file_name):
        # Crear un archivo SVG y añadir las formas
        dwg = svgwrite.Drawing(file_name, profile='tiny')

        # Crear un grupo de elementos de dibujo
        shape_group = dwg.add(dwg.g(id='shape', fill='none', stroke='black'))

        # Llamar al método draw de la subclase para añadir las formas al SVG
        self._draw_to_svg(shape_group, drawer)

        # Guardar el archivo SVG
        dwg.save()

    def _draw_to_svg(self, shape_group, drawer):
        raise NotImplementedError("Subclasses should implement this method for SVG export.")
    
    

class Rectangle(Shape):
    def draw(self, drawer):
        x = self.width
        y = self.height
        ob = drawer

        def draw_part():
            # Calcular las coordenadas para centrar el rectángulo
            center_x = x / 2
            center_y = y / 2

            # Mover el lápiz a la esquina superior izquierda del rectángulo
            ob.penup()
            ob.goto(-center_x, center_y)
            ob.pendown()

            # Dibujar el rectángulo
            for _ in range(2):
                ob.forward(x)
                ob.write(f"{x} cm", align="center", font=("Arial", 12, "normal"))
                ob.right(90)
                ob.forward(y)
                ob.right(90)
                ob.write(f"{y} cm", align="center", font=("Arial", 12, "normal"))

            # Mover el lápiz al centro del rectángulo
            ob.penup()
            ob.goto(0, 0)
            ob.pendown()

            # Escribir la etiqueta en el centro del rectángulo
            ob.penup()
            ob.goto(0, 0)
            ob.write(self.label, align="center", font=("Arial", 16, "normal"))
            ob.pendown()

        draw_part()

    def _draw_to_svg(self, shape_group, drawer):
        x = self.width
        y = self.height

        # Añadir el rectángulo al SVG
        shape_group.add(drawer.rect(insert=(-x/2, y/2), size=(x, y)))

        # Añadir la etiqueta en el centro
        shape_group.add(drawer.text(self.label, insert=(0, 0), text_anchor="middle", alignment_baseline="central"))

class Triangle(Shape):
    def draw(self, drawer):
        base_length = self.width
        triangle_height = self.height
        ob = drawer

        # Calcular la longitud de los otros dos lados del triángulo
        side_length = math.sqrt((base_length / 2) ** 2 + triangle_height ** 2)
        
        # Calcular el ángulo en la base
        angle_base = math.degrees(math.atan(triangle_height / (base_length / 2)))

        def draw_part():
            # Dibujar la base
            ob.forward(base_length)
            ob.left(180 - angle_base)  # Girar para dibujar el primer lado
            ob.forward(side_length)
            ob.left(2 * angle_base)    # Girar para dibujar el segundo lado
            ob.forward(side_length)
            ob.left(180 - angle_base)  # Volver a la posición original

            # Mover el lápiz al centro del triángulo y escribir la etiqueta
            ob.penup()
            ob.goto(0, 0)
            ob.write(self.label, align="center", font=("Arial", 16, "normal"))
            ob.pendown()

        draw_part()

    def _draw_to_svg(self, shape_group, drawer):
        base_length = self.width
        triangle_height = self.height

        # Coordenadas de los vértices del triángulo
        points = [(0, -triangle_height/2), (base_length/2, triangle_height/2), (-base_length/2, triangle_height/2)]
        
        # Añadir el triángulo al SVG
        shape_group.add(drawer.polygon(points))

        # Añadir la etiqueta en el centro
        shape_group.add(drawer.text(self.label, insert=(0, 0), text_anchor="middle", alignment_baseline="central"))

class DrawingTool:
    def __init__(self, turtle_obj):
        self.t = turtle_obj

    def draw_shape(self, shape):
        shape.draw(self.t)

    def draw_drawing_plane(self, width, height, label):
        plane = Rectangle(width, height, label)
        self.draw_shape(plane)

    def export_shape_to_svg(self, shape, file_name):
        shape.export_to_svg(svgwrite.Drawing(file_name, profile='tiny'), file_name)


