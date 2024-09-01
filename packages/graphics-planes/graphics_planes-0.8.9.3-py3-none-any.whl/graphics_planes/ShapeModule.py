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
    def _draw_to_svg(self, shape_group, drawer):
        x = self.width
        y = self.height

        # Añadir el rectángulo al SVG
        shape_group.add(drawer.rect(insert=(-x/2, y/2), size=(x, y)))

        # Añadir la etiqueta en el centro
        shape_group.add(drawer.text(self.label, insert=(0, 0), text_anchor="middle", dominant_baseline="middle"))

class Triangle(Shape):
    def _draw_to_svg(self, shape_group, drawer):
        base_length = self.width
        triangle_height = self.height

        # Coordenadas de los vértices del triángulo
        points = [(0, -triangle_height/2), (base_length/2, triangle_height/2), (-base_length/2, triangle_height/2)]
        
        # Añadir el triángulo al SVG
        shape_group.add(drawer.polygon(points))

        # Añadir la etiqueta en el centro
        shape_group.add(drawer.text(self.label, insert=(0, 0), text_anchor="middle", dominant_baseline="middle"))
