# Helpers

<h2 id="transform">Transform</h2>

{schema_string:helpers/transform/description}

{schema_object:helpers/transform}

To make the anchor point properly line up with the center of location, `p` and `a` should have the same value.

This example allows you to tweak transform attributes and see how the shape changes.
{: .print-site-plugin-ignore }

The anchor point is highlighted with an orange dot.
{: .print-site-plugin-ignore }

<lottie-playground example="transform.json">
    <form>
        <input title="Anchor X" type="range" min="0" value="256" max="512"/>
        <input title="Anchor Y" type="range" min="0" value="256" max="512"/>
        <input title="Position X" type="range" min="0" value="256" max="512"/>
        <input title="Position Y" type="range" min="0" value="256" max="512"/>
        <input title="Scale X" type="range" min="0" value="100" max="200"/>
        <input title="Scale Y" type="range" min="0" value="100" max="200"/>
        <input title="Rotation" type="range" min="-360" value="0" max="360"/>
        <input title="Skew" type="range" min="0" value="0" max="360"/>
        <input title="Skew Angle" type="range" min="0" value="0" max="360"/>
        <input title="Opacity" type="range" min="0" value="100" max="100"/>
    </form>
    <json>lottie.layers[1].ks</json>
    <script>
    lottie.layers[0].ks.p.k[0] = data["Anchor X"];
    lottie.layers[1].ks.a.k[0] = data["Anchor X"];
    lottie.layers[0].ks.p.k[1] = data["Anchor Y"];
    lottie.layers[1].ks.a.k[1] = data["Anchor Y"];
    lottie.layers[1].ks.p.k[0] = data["Position X"];
    lottie.layers[1].ks.p.k[1] = data["Position Y"];
    lottie.layers[1].ks.s.k[0] = data["Scale X"];
    lottie.layers[1].ks.s.k[1] = data["Scale Y"];
    lottie.layers[1].ks.r.k = data["Rotation"];
    lottie.layers[1].ks.sk.k = data["Skew"];
    lottie.layers[1].ks.sa.k = data["Skew Angle"];
    lottie.layers[1].ks.o.k = data["Opacity"];
    </script>
</lottie-playground>

Transforms the parent's coordinate system.

When calculating the final transform, properties MUST be applied as follows:

1. Translate by $-a$
1. Scale by $\frac{s}{100}$
1. If $sk \neq 0$:
    1. Rotate by $-sa$
    1. Skew x by $\tan(-sk)$
    1. Rotate by $sa$
1. Rotate by $-r$
1. Translate by $p$

Steps that have no effect MAY be skipped.

Assuming a transform matrix with the following layout, with the labels equivalent to the
[CSS matrix transform](https://drafts.csswg.org/css-transforms/#MatrixDefined):

$$
\begin{pmatrix}
a & b & 0 \\
c & d & 0 \\
e & f & 1
\end{pmatrix}
$$

The final transform is given by chaining transform matrices for each transform step:

$$
\begin{split}
&
\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
-a.x & -a.y & 1
\end{pmatrix}

\times

\begin{pmatrix}
\frac{s.x}{100} & 0 & 0 \\
0 & \frac{s.y}{100} & 0 \\
0 & 0 & 1
\end{pmatrix}


\times \\ \times &

\begin{pmatrix}
\cos(-sa) & \sin(-sa) & 0 \\
-\sin(-sa) & \cos(-sa)& 0 \\
0 & 0 & 1
\end{pmatrix}

\times

\begin{pmatrix}
1 & \tan(-sk) & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{pmatrix}

\times

\begin{pmatrix}
\cos(sa) & \sin(sa) & 0 \\
-\sin(sa) & \cos(sa) & 0 \\
0 & 0 & 1
\end{pmatrix}

\times \\ \times &

\begin{pmatrix}
\cos(-r) & \sin(-r) & 0 \\
-\sin(-r) & \cos(-r) & 0 \\
0 & 0 & 1
\end{pmatrix}

\times

\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
p.x & p.y & 1
\end{pmatrix}
\end{split}
$$

Note that if the transform matrix is transposed compared to the above:

$$
\begin{pmatrix}
a & c & e \\
b & d & f \\
0 & 0 & 1
\end{pmatrix}
$$

The operations need to be chained using right multiplication instead of left multiplication.

<h2 id="visual-object">Visual Object</h2>

{schema_string:helpers/visual-object/description}

{schema_object:helpers/visual-object}


<h2 id="marker">Marker</h2>

{schema_string:helpers/marker/description}

{schema_object:helpers/marker}

<h2 id="slots">Slots</h2>

Slots are a way to define a property value once and use the value in multiple
properties. Slot definitions are in a dictionary, the slot definition key is the
key that is used to match all properties with a `sid` field to the same key for
replacement.

<h3 id="slot">Slot</h3>

{schema_string:helpers/slot/description}

{schema_object:helpers/slot}

<h3 id="slottable-object">Slottable Object</h3>

{schema_string:helpers/slottable-object/description}

{schema_object:helpers/slottable-object}

<h3 id="slottable-property">Slottable Property</h3>

{schema_string:helpers/slottable-property/description}

{schema_object:helpers/slottable-property}

<h3 id="slot-validation-rules">Slot Validation Rules</h3>

**Type Consistency Rule:**

- The type of a Slot's `p` property MUST match the type of the property that references it via `sid`
- Vector-type slots MAY target Position properties if the number of dimensions match, as implementations perform simple value substitution

**Duplicate Slot ID Rule:**

- Multiple properties MAY reference the same `sid` value
- All properties referencing the same `sid` MUST have compatible types
- If multiple `sid` values with identical names but incompatible types exist, implementations SHOULD treat this as an error

**Missing Reference Handling:**

- If a property's `sid` references a slot that does not exist in the `slots` dictionary, implementations MUST use the property's own `a` and `k` values as fallback
- If a property has only `sid` (no `a`/`k` fallback) and the referenced slot is missing, implementations SHOULD ignore the property or use a type-appropriate default value
- Slots defined in the `slots` dictionary that are not referenced by any property MAY be ignored

**Type Determination:**

- The expected type of a slot is determined by its `p` value
- When parsing, implementations SHOULD check that properties referencing a slot via `sid` are type-compatible with the slot's `p` value
- If a type mismatch is detected, implementations SHOULD treat this as an error

Valid example — scalar slot referenced by a scalar property:

```json
{
    "slots": {
        "my_rotation": { "p": { "a": 0, "k": 45 } }
    }
}
```
```json
{ "a": 0, "k": 0, "sid": "my_rotation" }
```

Valid example — vector slot referenced by a position property (dimensions match):

```json
{
    "slots": {
        "my_position": { "p": { "a": 0, "k": [100, 200] } }
    }
}
```
```json
{ "a": 0, "k": [0, 0], "sid": "my_position" }
```

Valid example — bezier slot referenced by a bezier property:

```json
{
    "slots": {
        "my_path": { "p": { "a": 0, "k": { "c": true, "v": [[0, 0], [100, 0], [100, 100]], "i": [[0, 0], [0, 0], [0, 0]], "o": [[0, 0], [0, 0], [0, 0]] } } }
    }
}
```
```json
{ "a": 0, "k": { "c": true, "v": [[0, 0]], "i": [[0, 0]], "o": [[0, 0]] }, "sid": "my_path" }
```

Invalid example — scalar slot referenced by a vector property (type mismatch):

```json
{
    "slots": {
        "my_scale": { "p": { "a": 0, "k": 50 } }
    }
}
```
```json
{ "a": 0, "k": [100, 100], "sid": "my_scale" }
```

<lottie-playground example="slots.json">
    <form>
        <input title="Scale X" type="range" min="0" value="100" max="200"/>
        <input title="Scale Y" type="range" min="0" value="100" max="200"/>
        <input title="Rotation" type="range" min="-360" value="0" max="360"/>
        <input title="Opacity" type="range" min="0" value="100" max="100"/>
    </form>
    <json>lottie.slots</json>
    <script>
    lottie.slots.rotation.p.k = data["Rotation"];
    lottie.slots.opacity.p.k = data["Opacity"];
    lottie.slots.scale.p.k[0] = data["Scale X"];
    lottie.slots.scale.p.k[1] = data["Scale Y"];
    </script>
</lottie-playground>

<h2 id="metadata">Metadata</h2>

{schema_string:helpers/metadata/description}

{schema_object:helpers/metadata}

The `x` (Custom Metadata) property is an open-ended object that accepts any
key/value pairs. Authors can use this to attach tool-specific or
workflow-specific data to an animation without conflicting with the standard
metadata fields.

Implementations SHOULD preserve custom metadata when reading and writing
animations. Implementations MUST NOT rely on any particular keys or structure
within `x`.

<h2 id="mask">Mask</h2>

{schema_string:helpers/mask/description}

{schema_object:helpers/mask}

Masks provide single-channel coverage information (alpha channel) that modulates the layer's
content.

When multiple masks are specified, they are combined (blended) into a single coverage buffer,
in order, based on the [`mode`](constants.md#mask-mode) operator.

Masks are specified in terms of a `Path` plus additional properties.  For a given mask path,
the coverage $C_{path}$ is $1$ inside the path, $0$ outside the path, and possibly in the $[0..1]$
range along the path edges (anti-aliasing).

The coverage for a given `Mask` is

$$C = \begin{cases}{lr}
  C_{path} \cdot opacity, & \text{when } inv = false \\
  C_{path}^{-1} \cdot opacity, & \text{when } inv = true \\
\end{cases}$$

and the cumulative coverage for all masks is

$$C_{cumulative} = \prod_{k=1}^{n} C_k$$

where the product operator is determined by [`mode`](constants.md#mask-mode).
Then the final layer coverage (alpha channel) is

$$C_{layer}\prime = C_{layer} \cdot C_{cumulative}$$

<lottie-playground example="mask.json">
    <title>Example</title>
    <form>
        <input type="range" min="0" max="100" value="100" title="Opacity"/>
    </form>
    <json>lottie.layers[1].masksProperties[0]</json>
    <script>
        let mask = lottie.layers[1].masksProperties[0];
        mask.o.k = Number(data["Opacity"]);
    </script>
</lottie-playground>

