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
    $$T_{shape} = \prod_{n=0}^{Scope(shape)} Transform(scope_n)$$
  * compute the total style transformation by composing all transforms within the style scope chain:
    $$T_{style} = \prod_{n=0}^{Scope(style)} Transform(scope_n)$$

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
implementaions MAY consider similar values to be equal to overcome numerical instability.

### Drawing Commands

Drawing instructions will contain the following commands:

* _add vertex_: Adds a vertex to the bezier shape in global coordinates
* _set in tangent_: Sets the cubic tangent to the last added vertex, with coordinates relative to it.  If omitted, tangents MUST be $(0, 0)$.
* _set out tangent_: Sets the cubic tangent from the last added vertex, with coordinates relative to it.  If omitted, tangents MUST be $(0, 0)$.
* _lerp_: Linerarly interpolates two points or scalars by a given amount.


### Approximating Ellipses with Cubic Bezier

An elliptical quadrant can be approximated by a cubic bezier segment
with tangents of length $radius \cdot E_t.

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

An ellipse is drawn from the top quandrant point going clockwise:

$$
\begin{align*}
radius & = \frac{s}{2} \\
tangent & = radius \cdot E_t \\
x & = p.x \\
y & = p.y \\
\end{align*}
$$

1. Add vertex $(x, y - radius.y)$
1. Set in tangent $(-tangent.x, 0)$
1. Set out tangent $(tangent.x, 0)$
1. Add vertex $(x + radius.x, y)$
1. Set in tangent $(0, -tangent.y)$
1. Set out tangent $(0, tangent.y)$
1. Add vertex $(x, y + radius.y)$
1. Set in tangent $(tangent.x, 0)$
1. Set out tangent $(-tangent.x, 0)$
1. Add vertex $(x - radius.x, y)$
1. Set in tangent $(0, tangent.y)$
1. Set out tangent $(0, -tangent.y)$

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


Definitions:

$$
\begin{align*}
left & = p.x - \frac{s.x}{2} \\
right & = p.x + \frac{s.x}{2} \\
top & = p.y - \frac{s.y}{2} \\
bottom & = p.y + \frac{s.y}{2} \\
\end{align*}
$$

If $r = 0$, then the rectangle is rendered from the top-right going clockwise:

1. Add vertex $(right, top)$
1. Add vertex $(right, bottom)$
1. Add vertex $(left, bottom)$
1. Add vertex $(left, top)$

If $r > 0$, the rounded corners must be taken into account.

$$
\begin{align*}
rounded & = \min\left(\frac{s.x}{2}, \frac{s.y}{2}, r\right) \\
tangent & = rounded \cdot E_t \\
\end{align*}
$$

1. Add vertex $(right, top + rounded)$
1. Set in tangent $(0, -tangent)$
1. Add vertex $(right, bottom - rounded)$
1. Set out tangent $(0, tangent)$
1. Add vertex $(right - rounded, bottom)$
1. Set in tangent $(tangent, 0)$
1. Add vertex $(left + rounded, bottom)$
1. Set out tangent $(-tangent, 0)$
1. Add vertex $(left, bottom - rounded)$
1. Set in tangent $(0, tangent)$
1. Add vertex $(left, top + rounded)$
1. Set out tangent $(0, -tangent)$
1. Add vertex $(left + rounded, top)$
1. Set in tangent $(-tangent, 0)$
1. Add vertex $(right - rounded, top)$
1. Set out tangent $(tangent, 0)$

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


Definitions:

$$
\begin{align*}
points & = \lfloor pt \rceil \\
\theta  & = \frac{\pi}{points} \\
\alpha & = \frac{\pi}{180} \cdot r \\
tan_{out} &= \frac{os}{100} \cdot \frac{or \cdot 2 \pi}{points \cdot 4} \\
tan_{in} &= \frac{is}{100} \cdot \frac{ir \cdot 2 \pi}{points \cdot 4} \\
\end{align*}
$$

1. For $i$ in $[0, points)$
    1. Let $\beta = -\frac{\pi}{2} + \alpha + i \cdot 2 \dot \theta$
    1. Let $V_{out} = (or \cdot \cos(\beta), or \cdot \sin(\beta))$
    1. Add vertex $p + V_{out}$
    1. If $or \neq 0$, we need to add bezier tangent
        1. Let $T_{out} = (V_{out} \cdot \frac{tan_{out}}{or})$
        1. Set in tangent $V_{out}$
        1. Set out tangent $-V_{out}$
    1. If $sy = 1$, we need to add a vertex towards the inner radius to make a star
        1. Let $V_{in} = (ir \cdot \cos(\beta + \theta), or \cdot \sin(\beta + \theta))$
        1. Add vertex $p + V_{in}$
        1. If $ir \neq 0$, we need to add bezier tangent
            1. Let $T_{in} = (V_{in} \cdot \frac{tan_{in}}{or})$
            1. Set in tangent $V_{in}$
            1. Set out tangent $-V_{in}$

<h2 id="grouping">Grouping</h2>

<h3 id="group">Group</h3>

{schema_string:shapes/group/description}

{schema_object:shapes/group}

<h3 id="transform">Transform</h3>

{schema_string:shapes/transform/description}

{schema_object:shapes/transform}


<h2 id="shape-style">Style</h2>

{schema_string:shapes/shape-style/description}

{schema_object:shapes/shape-style}


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


<h2 id="modifier">Modifiers</h2>

{schema_string:shapes/modifier/description}


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

* When `m` has a value of `1` (Parallel), each shape MUST considered
separately, $start$ and $end$ being applied to each shape.

* When `m` has a value of `2` (Sequential), all the shapes MUST be considered
as following each other in render order.  $start$ and $end$ refer to the whole
length created by concatenating each shape.
