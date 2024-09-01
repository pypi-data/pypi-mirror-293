import math
import svgwrite
from .ShapeModule import Shape

class GraphicsPlane:
    def create_rectangle(self, width, height):
        shape = Shape("Rectangle")
        x, y = 0, 0

        shape.add_trace((x, y), (x + width, y))
        shape.add_trace((x + width, y), (x + width, y - height))
        shape.add_trace((x + width, y - height), (x, y - height))
        shape.add_trace((x, y - height), (x, y))

        return shape

    def create_triangle(self, base, height):
        shape = Shape("Triangle")
        x, y = 0, 0

        side = math.sqrt((base / 2) ** 2 + height ** 2)
        x2, y2 = base / 2, -height
        x3, y3 = -base / 2, -height

        shape.add_trace((x, y), (x2, y2))
        shape.add_trace((x2, y2), (x3, y3))
        shape.add_trace((x3, y3), (x, y))

        return shape

    def export_to_svg(self, shape, file_name):
        # Crear un archivo SVG utilizando svgwrite
        dwg = svgwrite.Drawing(file_name, profile='tiny')

        # Añadir los trazos de la figura al archivo SVG
        for trace in shape.traces:
            start, end = trace
            dwg.add(dwg.line(start=start, end=end, stroke=svgwrite.rgb(0, 0, 0, '%')))

        # Añadir la etiqueta al centro de la figura (si existe)
        if shape.label:
            label_position = self.calculate_label_position(shape)
            dwg.add(dwg.text(shape.label, insert=label_position, text_anchor="middle", alignment_baseline="central"))

        # Guardar el archivo SVG
        dwg.save()

    def calculate_label_position(self, shape):
        # Este método calcula la posición para centrar la etiqueta en la figura
        if shape.type == "Rectangle":
            x = (shape.traces[0][0][0] + shape.traces[1][0][0]) / 2
            y = (shape.traces[1][0][1] + shape.traces[2][0][1]) / 2
        elif shape.type == "Triangle":
            x = (shape.traces[0][0][0] + shape.traces[1][0][0] + shape.traces[2][0][0]) / 3
            y = (shape.traces[0][0][1] + shape.traces[1][0][1] + shape.traces[2][0][1]) / 3
        else:
            x, y = 0, 0
        return (x, y)