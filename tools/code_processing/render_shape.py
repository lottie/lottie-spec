import re
import ast
import math
import lottie

from . import loader

Color = lottie.Color
Vector2D = lottie.NVector
ELLIPSE_CONSTANT = 0.5519150244935105707435627


class Bezier(lottie.objects.bezier.BezierView):
    def __init__(self):
        super().__init__(lottie.objects.bezier.Bezier(), False)

    def add_vertex(self, p: Vector2D):
        self.append(p)

    def set_in_tangent(self, p: Vector2D):
        self[-1].in_tangent = p

    def set_out_tangent(self, p: Vector2D):
        self[-1].out_tangent = p

    @property
    def closed(self):
        return self.bezier.closed

    @closed.setter
    def closed(self, v):
        self.bezier.closed = v


code = """
def rectangle(shape: Bezier, p: Vector2D, s: Vector2D, r: float):
    left: float = p.x - s.x / 2
    right: float = p.x + s.x / 2
    top: float = p.y - s.y / 2
    bottom: float = p.y + s.y / 2

    shape.closed = True

    if r <= 0:
        # The rectangle is rendered from the top-right going clockwise
        shape.add_vertex(Vector2D(right, top))
        shape.add_vertex(Vector2D(right, bottom))
        shape.add_vertex(Vector2D(left, bottom))
        shape.add_vertex(Vector2D(left, top))
    else:
        # Rounded corners must be taken into account
        rounded: float = min(s.x/2, s.y/2, r)
        tangent: float = rounded * ELLIPSE_CONSTANT

        shape.add_vertex(Vector2D(right, top + rounded))
        shape.set_in_tangent(Vector2D(0, -tangent))
        shape.add_vertex(Vector2D(right, bottom - rounded))
        shape.set_out_tangent(Vector2D(0, tangent))
        shape.add_vertex(Vector2D(right - rounded, bottom))
        shape.set_in_tangent(Vector2D(tangent, 0))
        shape.add_vertex(Vector2D(left + rounded, bottom))
        shape.set_out_tangent(Vector2D(-tangent, 0))
        shape.add_vertex(Vector2D(left, bottom - rounded))
        shape.set_in_tangent(Vector2D(0, tangent))
        shape.add_vertex(Vector2D(left, top + rounded))
        shape.set_out_tangent(Vector2D(0, -tangent))
        shape.add_vertex(Vector2D(left + rounded, top))
        shape.set_in_tangent(Vector2D(-tangent, 0))
        shape.add_vertex(Vector2D(right - rounded, top))
        shape.set_out_tangent(Vector2D(tangent, 0))
"""

samples = loader.code_to_samples(code)
parsed = samples["ast"]
print(parsed)
exec(compile(parsed, "", "exec"), globals(), locals())

anim = lottie.objects.Animation()
lay = lottie.objects.layers.ShapeLayer()
anim.add_layer(lay)
lay.in_point = anim.in_point
lay.out_point = anim.out_point

shape = Bezier()
rectangle(shape, Vector2D(256, 256), Vector2D(200, 200), 10)
lay.shapes.append(lottie.objects.shapes.Path(shape.bezier))
lay.shapes.append(lottie.objects.shapes.Fill(Color(1, 1, 0)))

lottie.exporters.core.export_embedded_html(anim, "/tmp/out.html")

print(samples["pseudo"])
