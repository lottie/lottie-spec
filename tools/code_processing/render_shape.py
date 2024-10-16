import re
import ast
import math
import lottie


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
    '''
    @param foo bar
    '''
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


def gather_indent(m):
    spaces = m.group(1)
    if spaces:
        return spaces

    if m.start() == 0:
        return ""

    newline_before = m.string.rfind('\n', 0, m.start()-1)
    if newline_before == -1:
        return ""

    line_before = m.string[newline_before + 1:m.start()]

    return " " * (len(line_before) - len(line_before.lstrip()))


processed_code = re.sub(
    r"^(\s*)$", lambda m: gather_indent(m) + "''",
    re.sub(r"(\s*)# ?(.*)", r"\1'''\2'''", code.strip()),
    flags=re.MULTILINE
)
print(processed_code)
parsed = ast.parse(processed_code, type_comments=True)

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

import python_to_ts
import pseudocode


py2ts = python_to_ts.Py2Ts()
# py2ts.type_annotations = False
py2ts.convert_ast(parsed)
print(py2ts.output)


print(pseudocode.PseudoCode().convert(parsed))
