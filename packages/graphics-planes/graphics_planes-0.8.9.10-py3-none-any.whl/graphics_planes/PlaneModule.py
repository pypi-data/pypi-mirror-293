import svgwrite
from .ShapeModule import Shape, Rectangle, Triangle

class Plane:
    def __init__(self, name="Drawing"):
        self.name = name
        self.shapes = []

    def add_shape(self, shape):
        if not isinstance(shape, Shape):
            raise TypeError("Expected an instance of Shape.")
        self.shapes.append(shape)

    def export_to_svg(self, filename):
        dwg = svgwrite.Drawing(filename, profile='tiny')
        shape_group = dwg.add(dwg.g(id='shapes', fill='none', stroke='black'))

        for shape in self.shapes:
            shape._draw_to_svg(shape_group, dwg)

        dwg.save()
        print(f"Dibujo exportado a {filename}")

    def show_shapes(self):
        for shape in self.shapes:
            print(f"Forma: {shape.label}")

            if isinstance(shape, Rectangle):
                print(f"  Tipo: Rectángulo")
                print(f"  Anchura: {shape.width}")
                print(f"  Altura: {shape.height}")
                print(f"  Posición: ({shape.x}, {shape.y})")
            elif isinstance(shape, Triangle):
                print(f"  Tipo: Triángulo")
                print(f"  Base: {shape.width}")
                print(f"  Altura: {shape.height}")
                print(f"  Posición: ({shape.x}, {shape.y})")
            else:
                print("  Tipo: Forma desconocida")
