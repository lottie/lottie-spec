# Helpers

<h2 id="transform">Transform</h2>

{schema_string:helpers/transform/description}

{schema_object:helpers/transform}


To make the anchor point properly line up with the center of location, `p` and `a` should have the same value.


This example allows you to tweak transform attributes and see how the shape changes.

The anchor point is highlighted with an orange dot.

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

<h2 id="visual-object">Visual Object</h2>

{schema_string:helpers/visual-object/description}

{schema_object:helpers/visual-object}


<h2 id="marker">Marker</h2>

{schema_string:helpers/marker/description}

{schema_object:helpers/marker}

<h2 id="slots">Slots</h2>

Slots are a way to define a property value once and use the value in multiple
properties. Slot definitions are in a dictionary, the slot definition key is the
key that is used to match all properties with an `sid` field to the same key for
replacement.

<h3 id="slot">Slot</h3>

{schema_string:helpers/slot/description}

{schema_object:helpers/slot}

<h3 id="slottable-property">Slotabble Property</h3>

{schema_string:helpers/slottable-property/description}

{schema_object:helpers/slottable-property}

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

