import svgwrite
from .ShapeModule import Shape

class Plane:
    def __init__(self, name="Drawing"):
        self.name = name
        self.shapes = []

    def add_shape(self, shape):
        """Añade una forma al dibujo."""
        if not isinstance(shape, Shape):
            raise TypeError("Expected an instance of Shape.")
        self.shapes.append(shape)

    def export_to_svg(self, filename):
        """Exporta todo el dibujo a un archivo SVG."""
        dwg = svgwrite.Drawing(filename, profile='tiny')

        # Crear un grupo de elementos de dibujo
        shape_group = dwg.add(dwg.g(id='shapes', fill='none', stroke='black'))

        for shape in self.shapes:
            # Usar el método _draw_to_svg de la forma para añadirla al SVG
            shape._draw_to_svg(shape_group, dwg)

        dwg.save()
        print(f"Dibujo exportado a {filename}")
    def show_shapes(self):
        """Muestra información sobre todas las formas en el dibujo (para fines de depuración)."""
        for shape in self.shapes:
            print(f"Forma: {shape.label}")

            # Mostrar detalles específicos según el tipo de forma
            if isinstance(shape, Rectangle):
                print(f"  Tipo: Rectángulo")
                print(f"  Anchura: {shape.width}")
                print(f"  Altura: {shape.height}")
            elif isinstance(shape, Triangle):
                print(f"  Tipo: Triángulo")
                print(f"  Base: {shape.width}")
                print(f"  Altura: {shape.height}")
            else:
                print("  Tipo: Forma desconocida")