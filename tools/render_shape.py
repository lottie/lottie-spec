#!/usr/bin/env python3
import sys
import math
import inspect
import argparse
import lottie
from code_processing.loader import code_to_samples, SourceCode


class Bezier(lottie.objects.bezier.BezierView):
    def __init__(self):
        super().__init__(lottie.objects.bezier.Bezier(), False)

    def add_vertex(self, p: lottie.NVector):
        self.append(p)

    def set_in_tangent(self, p: lottie.NVector):
        self[-1].in_tangent = p

    def set_out_tangent(self, p: lottie.NVector):
        self[-1].out_tangent = p

    @property
    def closed(self):
        return self.bezier.closed

    @closed.setter
    def closed(self, v):
        self.bezier.closed = v


exec_globals = {
    "Color": lottie.Color,
    "Vector2D": lottie.NVector,
    "ELLIPSE_CONSTANT": 0.5519150244935105707435627,
    "Bezier": Bezier,
    "math": math,
}

default_args = {
    "NVector": lottie.NVector(200, 200),
    "float": 50,
    "int": 5,
}


def render_shape(func, args):
    anim = lottie.objects.Animation()
    lay = lottie.objects.layers.ShapeLayer()
    anim.add_layer(lay)
    lay.in_point = anim.in_point
    lay.out_point = anim.out_point

    shape = Bezier()
    func(shape, *args)
    lay.shapes.append(lottie.objects.shapes.Path(shape.bezier))
    lay.shapes.append(lottie.objects.shapes.Stroke(lottie.Color(1, 0.5, 0), 6))
    lay.shapes.append(lottie.objects.shapes.Fill(lottie.Color(1, 1, 0)))
    return anim


def main(argv):
    if argv.input:
        with open(argv.input) as f:
            code = f.read()
    else:
        print("Type code (end with ^D)")
        code = sys.stdin.read()

    if argv.view_code:
        data = code_to_samples(code)
        print(data[argv.view_code])
        parsed = data["ast"]
    else:
        parsed = SourceCode(code).ast

    local = {}
    exec(compile(parsed, "", "exec"), exec_globals, local)

    default_func = next(iter(local.keys()))

    if argv.func is not None:
        func_name = argv.func
    else:
        sys.stdout.write("Function name [%s]: " % default_func)
        sys.stdout.flush()
        func_name = sys.stdin.readline().strip()

    func = local[func_name or default_func]

    arg_spec = inspect.getfullargspec(func)

    given_args = {}

    if argv.args:
        for i in range(0, len(argv.args), 2):
            given_args[argv.args[i]] = argv.args[i + 1]

    args = []
    for i, arg in enumerate(arg_spec.args):
        if i == 0 and arg == "shape":
            continue
        annot = arg_spec.annotations[arg]
        typename = annot.__name__
        value = default_args[typename]
        if arg in given_args:
            value_raw = given_args[arg]
        else:
            sys.stdout.write("%s (%s) [%s]: " % (arg, typename, value))
            sys.stdout.flush()
            value_raw = sys.stdin.readline().strip()
        if value_raw:
            value = annot(*eval("[%s]" % value_raw))
        args.append(value)

    anim = render_shape(func, args)

    lottie.exporters.core.export_embedded_html(anim, "/tmp/out.html")


parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="File for the code input")
parser.add_argument("--func", "-f", default=None, help="Function name")
parser.add_argument("--args", nargs="+", help="Argument values for the function")
parser.add_argument("--view-code", "-c", metavar="lang", help="Display rendered code")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
