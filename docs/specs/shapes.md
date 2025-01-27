# Shapes

The graphical elements are divided in 4 categories:

* [Shapes](#shape) that define the actual curves but have no styling information
* [Grouping](#grouping), used to organize collections of graphic elements
* [Styles](#shape-style), that define the visual appearance of shapes
* [Modifiers](#modifier) alter the curves of the shapes

## Shape Rendering Model

### Grouping and Ordering Rules

* **Shapes** are rendered in reverse order, bottom->top. Shapes at the beginning of the array
  are rendered on top of shapes with larger indices.
* **Groups** offer a scoping mechanism for transforms, styles, modifiers, and shapes. All group
  children, including sub-groups and their children, are considered part of the group's scope.
* **Transforms** adjust the coordinate system for all elements within their group, and transitively
  for all other group-nested elements.
* **Styles** and **modifiers** apply to all preceding shapes within the current scope,
  including subgroup-nested shapes.
* When **multiple styles** apply to the same shape, the shape is rendered repeatedly for each style,
  in reverse order.
* When **multiple modifiers** apply to the same shape, they are composed in reverse order
  (e.g. $Trim(Trim(shape))$).
* When **multiple transforms** apply to the same shape due to scope nesting, they compose in group
  nesting order (transforms are additive).
* **Group opacity** (property of the group transform) applies atomically to all elements in scope -
  i.e. opacity applies to the result of compositing all group content, and not to individual
  elements.

More formally:

* for each $(shape, style)$ tuple, where $Index(shape) < Index(style)$ and $shape \in Scope(style)$:
  * for each $modifier$, in increasing index order, where $Index(shape) < Index(modifier)$ and
    $shape \in Scope(modifier)$:
    * $shape = modifier(shape)$
  * compute the total shape transformation by composing all transforms within the shape scope chain:
    $T_{shape} = \prod_{n=0}^{Scope(shape)} Transform(scope_n)$
  * compute the total style transformation by composing all transforms within the style scope chain:
    $T_{style} = \prod_{n=0}^{Scope(style)} Transform(scope_n)$

  * $Render(shape \times T_{shape}, style \times T_{style})$

### Notes

1. Certain modifier operations (e.g. sequential $Trim$) may require information about shapes
from different groups, thus $Render()$ calls cannot always be issued based on single-pass local
knowledge.

2. Transforms can affect both shapes and styles (e.g. stroke width).  For a given $(shape, style)$,
the shape and style transforms are not necessarily equal.

3. Shapes without an applicable style are not rendered.

4. This rendering model is based on AfterEffects' Shape Layer semantics.

## Rendering Convention

Shapes defined in this section contain rendering instructions.
These instructions are used to generate the path as a bezier curve.

Implementations MAY use different algorithms or primitives to render
the shapes but the result MUST be equivalent to the paths defined here.

Some instructions define named values for clarity and illustrative purposes,
implementations are not required to have them explicitly defined in
their rendering process.

When referencing animated properties, the rendering instruction will
use the same name as in the JSON but it's assumed they refer to their
value at a given point in time rather than the property itself.
For {link:values/vector} values, $value.x$ and $value.y$ in
the instructions are equivalent to `value[0]` and `value[1]` respectively.

All paths MUST be closed unless specified otherwise in the rendering instructions.

When instructions call for an equality comparison between two values,
implementations MAY consider similar values to be equal to overcome numerical instability.

### Bezier Conversions

This documents includes algorithms to convert parametric shapes into bezier curves.

Implementations MAY use different implementations than the algorithms provided here
but the output shape MUST be visually indistinguishable from the output of these algorithms.

Furthermore, when drawing individual shapes the stroke order and direction is not importand
but implementations of Trim Path MUST follow the stroke order as defined by these algorithms.

Drawing instructions will contain the following commands:

* _Add vertex_: Adds a vertex to the bezier shape in global coordinates
* _Set in tangent_: Sets the cubic tangent to the last added vertex, with coordinates relative to it.  If omitted, tangents MUST be $(0, 0)$.
* _Set out tangent_: Sets the cubic tangent from the last added vertex, with coordinates relative to it.  If omitted, tangents MUST be $(0, 0)$.


### Approximating Ellipses with Cubic Bezier

An elliptical quadrant can be approximated by a cubic bezier segment
with tangents of length $radius * E_t.

Where

$$E_t \approx 0.5519150244935105707435627$$

See [this article](https://spencermortensen.com/articles/bezier-circle/) for the math behind it.

When implementations render elliptical arcs using bezier curves, they SHOULD
use this constant, a similar approximation, or elliptical arc drawing primitives.


<h2 id="graphic-element">Graphic Element</h2>

{schema_string:shapes/graphic-element/description}

{schema_object:shapes/graphic-element}

The `ty` property defines the specific element type based on the following values:

{schema_subtype_table:shapes/all-graphic-elements:ty}

Hidden shapes (`hd: True`) are ignored, and do not contribute to rendering nor modifier operations.

<h2 id="shape">Shapes</h2>

{schema_string:shapes/shape/description}

{schema_object:shapes/shape}


<h3 id="ellipse">Ellipse</h3>

{schema_string:shapes/ellipse/description}

{schema_object:shapes/ellipse}

<lottie-playground example="ellipse.json">
    <title>Example</title>
    <form>
        <input title="Position x" type="range" min="0" max="512" value="256"/>
        <input title="Position y" type="range" min="0" max="512" value="256"/>
        <input title="Width" type="range" min="0" max="512" value="256"/>
        <input title="Height" type="range" min="0" max="512" value="256"/>
    </form>
    <json>lottie.layers[0].shapes[0].it[0]</json>
    <script>
    lottie.layers[0].shapes[0].it[0].p.k = [
        data["Position x"], data["Position y"]
    ];
    lottie.layers[0].shapes[0].it[0].s.k = [
        data["Width"], data["Height"]
    ];
    </script>
</lottie-playground>


<algorithm>
def ellipse(shape: Bezier, p: Vector2D, s: Vector2D):
    # An ellipse is drawn from the top quadrant point going clockwise:
    radius = s / 2
    tangent = radius * ELLIPSE_CONSTANT
    x = p.x
    y = p.y

    shape.closed = True
    shape.add_vertex(Vector2D(x, y - radius.y))
    shape.set_in_tangent(Vector2D(-tangent.x, 0))
    shape.set_out_tangent(Vector2D(tangent.x, 0))
    shape.add_vertex(Vector2D(x + radius.x, y))
    shape.set_in_tangent(Vector2D(0, -tangent.y))
    shape.set_out_tangent(Vector2D(0, tangent.y))
    shape.add_vertex(Vector2D(x, y + radius.y))
    shape.set_in_tangent(Vector2D(tangent.x, 0))
    shape.set_out_tangent(Vector2D(-tangent.x, 0))
    shape.add_vertex(Vector2D(x - radius.x, y))
    shape.set_in_tangent(Vector2D(0, tangent.y))
    shape.set_out_tangent(Vector2D(0, -tangent.y))
</algorithm>

Implementations MAY use elliptical arcs to render an ellipse.

![Ellipse rendering guide](../static/img/ellipse-guide.svg)


<h3 id="rectangle">Rectangle</h3>

{schema_string:shapes/rectangle/description}

{schema_object:shapes/rectangle}

<lottie-playground example="rectangle.json">
    <title>Example</title>
    <form>
        <input title="Position x" type="range" min="0" max="512" value="256"/>
        <input title="Position y" type="range" min="0" max="512" value="256"/>
        <input title="Width" type="range" min="0" max="512" value="256"/>
        <input title="Height" type="range" min="0" max="512" value="256"/>
        <input title="Roundness" type="range" min="0" max="512" value="0"/>
    </form>
    <json>lottie.layers[0].shapes[0].it[0]</json>
    <script>
    lottie.layers[0].shapes[0].it[0].p.k = [
        data["Position x"], data["Position y"]
    ];
    lottie.layers[0].shapes[0].it[0].s.k = [
        data["Width"], data["Height"]
    ];
    lottie.layers[0].shapes[0].it[0].r.k = data["Roundness"];
    </script>
</lottie-playground>

Rendering algorithm:

<algorithm>
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
</algorithm>

![Rectangle rendering guide](../static/img/rect-guide.svg)


<h3 id="path">Path</h3>

{schema_string:shapes/path/description}

{schema_object:shapes/path}

<lottie-playground example="path.json">
    <title>Example</title>
    <form>
        <input title="Shape" type="bezier"/>
    </form>
    <json>lottie.layers[0].shapes[0].it[0]</json>
    <script>
        var shape = lottie.layers[0].shapes[0].it[0];
        if ( data["Shape"] )
            shape.ks.k = data["Shape"];
    </script>
</lottie-playground>


<h3 id="polystar">PolyStar</h3>

{schema_string:shapes/polystar/description}

{schema_object:shapes/polystar}

<lottie-playground example="star.json">
    <title>Example</title>
    <form>
        <input title="Position x" type="range" min="0" max="512" value="256"/>
        <input title="Position y" type="range" min="0" max="512" value="256"/>
        <input title="Points" type="range" min="3" max="10" value="5"/>
        <input title="Rotation" type="range" min="0" max="360" value="0"/>
        <input title="Outer Radius" type="range" min="0" max="300" value="200"/>
        <input title="Inner Radius" type="range" min="0" max="300" value="100"/>
        <input title="Outer Roundness" type="range" min="0" max="100" value="0"/>
        <input title="Inner Roundness" type="range" min="0" max="100" value="0"/>
        <enum title="Star Type">star-type</enum>
    </form>
    <json>lottie.layers[0].shapes[0].it[0]</json>
    <script>
        var star = {
            "ty": "sr",
            "nm": "PolyStar",
            "sy": Number(data["Star Type"]),
            "p": {
                "a": 0,
                "k": [data["Position x"], data["Position y"]]
            },
            "r": {
                "a": 0,
                "k": data["Rotation"]
            },
            "pt": {
                "a": 0,
                "k": data["Points"]
            },
            "or": {
                "a": 0,
                "k": data["Outer Radius"]
            },
            "os": {
                "a": 0,
                "k": data["Outer Roundness"]
            },
        };
        if ( data["Star Type"] == "1" )
        {
            star = {
                ...star,
                "ir": {
                    "a": 0,
                    "k": data["Inner Radius"]
                },
                "is": {
                    "a": 0,
                    "k": data["Inner Roundness"]
                },
            };
        }
        lottie.layers[0].shapes[0].it[0] = star;
    </script>
</lottie-playground>

<algorithm>
def polystar(shape: Bezier, p: Vector2D, pt: float, r: float, or_: float, os: float, sy: int, ir: float, is_: float):
    points: int = int(round(pt))
    alpha: float = -r * math.pi / 180 - math.pi / 2
    theta: float = -math.pi / points
    tan_len_out: float = (2 * math.pi * or_) / (4 * points) * (os / 100)
    tan_len_in: float = (2 * math.pi * ir) / (4 * points) * (is_ / 100)

    shape.closed = True

    for i in range(points):
        beta: float = alpha + i * theta * 2
        v_out: Vector2D = Vector2D(or_ * math.cos(beta),  or_ * math.sin(beta))
        shape.add_vertex(p + v_out)

        if os != 0 and or_ != 0:
            # We need to add bezier tangents
            tan_out: Vector2D = v_out * tan_len_out / or_
            shape.set_in_tangent(Vector2D(-tan_out.y, tan_out.x))
            shape.set_out_tangent(Vector2D(tan_out.y, -tan_out.x))

        if sy == 1:
            # We need to add a vertex towards the inner radius to make a star
            v_in: Vector2D = Vector2D(ir * math.cos(beta + theta), ir * math.sin(beta + theta))
            shape.add_vertex(p + v_in)

            if is_ != 0 and ir != 0:
                # We need to add bezier tangents
                tan_in = v_in * tan_len_in / ir
                shape.set_in_tangent(Vector2D(-tan_in.y, tan_in.x))
                shape.set_out_tangent(Vector2D(tan_in.y, -tan_in.x))
</algorithm>

<h2 id="grouping">Grouping</h2>

<h3 id="group">Group</h3>

{schema_string:shapes/group/description}

{schema_object:shapes/group}

A group defines a [[render stack]], elements within a group MUST be
rendered in reverse order (the first object in the list will appear on
top of elements further down).

1. Apply the transform
1. Render Styles and child groups in the transformed [[local coordinates|coordinate system]].

<h3 id="transform">Transform</h3>

{schema_string:shapes/transform/description}

{schema_object:shapes/transform}

Transform shapes MUST always be present in the group and they MUST be
the last item in the `it` array.

They modify the group's [[local coordinates|coordinate system]] the same way as Layer {link:helpers/transform}.


<h2 id="shape-style">Style</h2>

{schema_string:shapes/shape-style/description}

{schema_object:shapes/shape-style}

Shapes styles MUST apply their style to the [[collected shapes]] that
come before them in [[stacking order]].


<h3 id="fill">Fill</h3>

{schema_string:shapes/fill/description}

{schema_object:shapes/fill}

<lottie-playground example="fill.json">
    <title>Example</title>
    <form>
        <input title="Red" type="range" min="0" max="1" step="0.01" value="1"/>
        <input title="Green" type="range" min="0" max="1" step="0.01" value="0.98"/>
        <input title="Blue" type="range" min="0" max="1" step="0.01" value="0.28"/>
        <input title="Opacity" type="range" min="0" max="100" value="100"/>
        <enum title="Fill Rule">fill-rule</enum>
    </form>
    <json>lottie.layers[0].shapes[0].it[1]</json>
    <script>
        var shape = lottie.layers[0].shapes[0].it[1];
        shape.c.k = [data["Red"], data["Green"], data["Blue"]];
        shape.o.k = data["Opacity"];
        shape.r = Number(data["Fill Rule"]);
    </script>
</lottie-playground>


<h3 id="stroke"><span id="base-stroke">Stroke</span></h3>

{schema_string:shapes/stroke/description}

{schema_object:shapes/stroke}

<lottie-playground example="stroke.json">
    <title>Example</title>
    <form>
        <input title="Red" type="range" min="0" max="1" step="0.01" value="1"/>
        <input title="Green" type="range" min="0" max="1" step="0.01" value="0.98"/>
        <input title="Blue" type="range" min="0" max="1" step="0.01" value="0.28"/>
        <input type="range" min="0" max="100" value="32" title="Width"/>
        <input title="Opacity" type="range" min="0" max="100" value="100"/>
        <enum title="Line Cap" value="2">line-cap</enum>
        <enum title="Line Join" value="2">line-join</enum>
        <input type="range" min="0" max="10" value="3" title="Miter Limit"/>
    </form>
    <json>lottie.layers[0].shapes[2]</json>
    <script>
        var shape = lottie.layers[0].shapes[2];
        shape.c.k = [data["Red"], data["Green"], data["Blue"]];
        shape.o.k = data["Opacity"];
        shape.w.k = data["Width"];
        shape.lc = Number(data["Line Cap"]);
        shape.lj = Number(data["Line Join"]);
        shape.ml = data["Miter Limit"];
        shape.d = undefined;
    </script>
</lottie-playground>


<h4 id="stroke-dash">Stroke Dashes</h4>

{schema_string:shapes/stroke-dash/description}

A stroke dash array consists of `n` dash entries, `[n-1,n]` gap entries and `[0-1]` offset entries.

Dash and gap entries MUST all be in a continuous order and alternate between dash and gap, starting with dash. If there are an odd number of dashes + gaps, the sequence will repeat with dashes and gaps reversed. For example a sequence of `[4d, 8g, 16d]` MUST be rendered as `[4d, 8g, 16d, 4g, 8d, 16g]`.

Offset entry, if present, MUST be at the end of the array. 

{schema_object:shapes/stroke-dash}

<lottie-playground example="stroke.json">
    <title>Example</title>
    <form>
        <input title="Red" type="range" min="0" max="1" step="0.01" value="1"/>
        <input title="Green" type="range" min="0" max="1" step="0.01" value="0.98"/>
        <input title="Blue" type="range" min="0" max="1" step="0.01" value="0.28"/>
        <input type="range" min="0" max="100" value="32" title="Width"/>
        <input title="Opacity" type="range" min="0" max="100" value="100"/>
        <enum title="Line Cap" value="2">line-cap</enum>
        <enum title="Line Join" value="2">line-join</enum>
        <input type="range" min="0" max="10" value="3" title="Miter Limit"/>
        <input type="range" min="0" max="512" value="0" title="Dash Offset"/>
        <input type="range" min="0" max="512" value="30" title="Dash Length"/>
        <input type="range" min="0" max="512" value="50" title="Dash Gap"/>
    </form>
    <json>lottie.layers[0].shapes[2]</json>
    <script>
        var shape = lottie.layers[0].shapes[2];
        shape.c.k = [data["Red"], data["Green"], data["Blue"]];
        shape.o.k = data["Opacity"];
        shape.w.k = data["Width"];
        shape.lc = Number(data["Line Cap"]);
        shape.lj = Number(data["Line Join"]);
        shape.ml = data["Miter Limit"];
        shape.d[0].v.k = data["Dash Offset"];
        shape.d[1].v.k = data["Dash Length"];
        shape.d[2].v.k = data["Dash Gap"];
        var trim = lottie.layers[0].shapes[1];
        trim.e.k = 100;
        trim.o.k = 0;
    </script>
</lottie-playground>

<h3 id="gradient-fill"><span id="gradient-fill">Gradient Fill</span></h3>

{schema_string:shapes/gradient-fill/description}

{schema_object:shapes/gradient-fill}

<lottie-playground example="gradient.json">
    <title>Example</title>
    <form>
        <input title="Start X" type="range" min="0" max="512"  value="256"/>
        <input title="Start Y" type="range" min="0" max="512"  value="496"/>
        <input title="End X" type="range" min="0" max="512"  value="256"/>
        <input title="End Y" type="range" min="0" max="512"  value="16"/>
        <enum title="Type" value="1">gradient-type</enum>
        <input title="Highlight" type="range" min="0" max="100"  value="0"/>
        <input title="Highlight Angle" type="range" min="0" max="360"  value="0"/>
    </form>
    <json>lottie.layers[1].shapes[0].it[1]</json>
    <script>
    var gradient = lottie.layers[1].shapes[0].it[1];
    var start_marker = lottie.layers[0].shapes[1].it[1];
    var end_marker = lottie.layers[0].shapes[0].it[1];
    gradient.s.k = start_marker.p.k = [data["Start X"], data["Start Y"]];
    gradient.e.k = end_marker.p.k = [data["End X"], data["End Y"]];
    gradient.t = Number(data["Type"]);
    if (gradient.t === 2) {
        gradient.h = {
            a: 0, 
            k: data["Highlight"]
        };
        gradient.a = {
            a: 0, 
            k: data["Highlight Angle"]
        };
    } else {
        delete gradient.h;
        delete gradient.a;
    }
    </script>
</lottie-playground>

<h3 id="gradient-stroke"><span id="gradient-stroke">Gradient Stroke</span></h3>

{schema_string:shapes/gradient-stroke/description}

{schema_object:shapes/gradient-stroke}

<lottie-playground example="gradient-stroke.json">
    <title>Example</title>
    <form>
        <input title="Start X" type="range" min="0" max="512"  value="256"/>
        <input title="Start Y" type="range" min="0" max="512"  value="496"/>
        <input title="End X" type="range" min="0" max="512"  value="256"/>
        <input title="End Y" type="range" min="0" max="512"  value="16"/>
        <enum title="Type" value="1">gradient-type</enum>
        <input title="Highlight" type="range" min="0" max="100"  value="0"/>
        <input title="Highlight Angle" type="range" min="0" max="360"  value="0"/>
    </form>
    <json>lottie.layers[1].shapes[1]</json>
    <script>
    var gradient = lottie.layers[1].shapes[1];
    var start_marker = lottie.layers[0].shapes[1].it[1];
    var end_marker = lottie.layers[0].shapes[0].it[1];
    gradient.s.k = start_marker.p.k = [data["Start X"], data["Start Y"]];
    gradient.e.k = end_marker.p.k = [data["End X"], data["End Y"]];
    gradient.t = Number(data["Type"]);
    if (gradient.t === 2) {
        gradient.h = {
            a: 0, 
            k: data["Highlight"]
        };
        gradient.a = {
            a: 0, 
            k: data["Highlight Angle"]
        };
    } else {
        delete gradient.h;
        delete gradient.a;
    }
    </script>
</lottie-playground>

<h2 id="modifier">Modifiers</h2>

{schema_string:shapes/modifier/description}

Modifiers replace shapes in the [[render stack]] by applying operating
on the bezier path of to the [[collected shapes]] that
come before it in [[stacking order]].


<h3 id="trim-path">Trim Path</h3>

{schema_string:shapes/trim-path/description}

{schema_object:shapes/trim-path}

<lottie-playground example="trim_path.json">
    <form>
        <input title="Start" type="range" min="0" value="0" max="100"/>
        <input title="End" type="range" min="0" value="50" max="100"/>
        <input title="Offset" type="range" min="0" value="0" max="360"/>
        <enum title="Multiple Shapes">trim-multiple-shapes</enum>
    </form>
    <json>lottie.layers[0].shapes[4]</json>
    <script>
        lottie.layers[0].shapes[4].s.k = data["Start"];
        lottie.layers[0].shapes[4].e.k = data["End"];
        lottie.layers[0].shapes[4].o.k = data["Offset"];
        lottie.layers[0].shapes[4].m = Number(data["Multiple Shapes"]);
    </script>
</lottie-playground>

When rendering trim path, the order of bezier points MUST be the same as
rendering instructions given for each shape in this section.

Rendering trim path can be rather complex.

Given

$$
\begin{align*}
offset & =
\begin{cases}
\frac{o}{360} - \lfloor \frac{o}{360} \rfloor & o \ge 0 \\
\frac{o}{360} - \lceil \frac{o}{360} \rceil & o < 0
\end{cases} \\
start & = offset + \min\left(1, \max\left(0, \frac{\min(s, e)}{100}\right)\right) \\
end & = offset + \min\left(1, \max\left(0, \frac{\max(s, e)}{100}\right)\right) \\
\end{align*}
$$

If $s$ and $e$ are equal, implementations MUST NOT render any shapes.

If $s = 0$ and $e = 1$, the input shape MUST be rendered as-is.

To render trim path, implementations MUST consider the actual length of
each shape (they MAY use approximations). Once the shapes are collected,
the segment to render is given by the percentages $start$ and $end$.

When trim path is applied to multiple shapes, the `m` property MUST
be considered when applying the modifier:

* When `m` has a value of `1` (Parallel), each shape MUST be considered
separately, $start$ and $end$ being applied to each shape.

* When `m` has a value of `2` (Sequential), all the shapes MUST be considered
as following each other in render order.  $start$ and $end$ refer to the whole
length created by concatenating each shape.
