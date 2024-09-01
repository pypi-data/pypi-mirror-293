import math
import svgwrite
from .ShapeModule import Rectangle, Triangle

class GraphicsPlane:
    def create_rectangle(self, width, height):
        # Crear una instancia de Rectangle
        shape = Rectangle(width, height, label="Rectangle")
        return shape

    def create_triangle(self, base, height):
        # Crear una instancia de Triangle
        shape = Triangle(base, height, label="Triangle")
        return shape

    def export_to_svg(self, shape, file_name):
        """Crea un archivo SVG utilizando svgwrite y exporta la figura."""
        dwg = svgwrite.Drawing(file_name, profile='tiny')

        # Crear un grupo de elementos de dibujo
        shape_group = dwg.add(dwg.g(id='shape', fill='none', stroke='black'))

        # Añadir los trazos de la figura al archivo SVG
        shape._draw_to_svg(shape_group, dwg)

        # Añadir la etiqueta al centro de la figura (si existe)
        if shape.label:
            label_position = self.calculate_label_position(shape)
            dwg.add(dwg.text(shape.label, insert=label_position, text_anchor="middle", alignment_baseline="central"))

        # Guardar el archivo SVG
        dwg.save()
        print(f"Figura exportada a {file_name}")

    def calculate_label_position(self, shape):
        """Calcula la posición para centrar la etiqueta en la figura."""
        if isinstance(shape, Rectangle):
            # Calcular el centro del rectángulo
            x = shape.width / 2
            y = shape.height / 2
        elif isinstance(shape, Triangle):
            # Calcular el centro del triángulo
            x = (shape.width / 2) / 2
            y = (shape.height / 2) / 2
        else:
            x, y = 0, 0
        return (x, y)
