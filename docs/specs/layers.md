# Layers

## Common Properties

<h3 id="layer">Layer</h3>

{schema_string:layers/layer/description}

{schema_object:layers/layer}

The `ty` property defines the specific layer type based on the following values:

{schema_subtype_table:layers/all-layers:ty}

<h3 id="visual-layer">Visual Layer</h3>

{schema_string:layers/visual-layer/description}

{schema_object:layers/visual-layer}

#### Parenting

Layer parenting offers a way to connect layers such that the movement of one layer (child) follows
the movement of another (parent). Multiple child layers can reference the same parent (this is
useful for applying the same transform animation to a group of layers).

When the `parent` property points to another layer, the referencing layer's current transformation
matrix (CTM) is composed with the parent CTM:

$$CTM(child) = CTM(parent) \times Transform(child)$$

Parenting is transitive, and reference cycles are not allowed (undefined behavior).


#### Hidden Layers

The hidden flag `hd` determines whether a layer is rendered: hidden layers are not rendered as
part of the normal layer tree, but their properties and content are evaluated when used as a
reference target in other contexts.

Specifically, hidden layers

* contribute to a layer's total transform when used as a `parent`
* contribute to a layer's track matte when used as a matte source

`hd` only affects the layer for which it is defined, it does not transitively apply to other
referencing layers.

#### Mattes

A matte allows using a layer as a mask for another layer.

The way it works is the layer defining the mask has a `tt` attribute with the
appropriate [value](constants.md#matte-mode).
The layer being masked is indicated by the `tp` attribute, which has the index (`ind`) of the layer that is being masked.

In this example there's a layer with a rectangle and a star being masked by an ellipse:
{: .print-site-plugin-ignore }


<lottie-playground example="matte.json">
    <title>Example</title>
    <form>
        <input type="checkbox" checked="checked" title="Enable Matte"/>
        <enum title="Matte Mode" value="1">matte-mode</enum>
    </form>
    <json>{...lottie.layers[1], shapes: [], ks: {}}</json>
    <script>
        if ( data["Enable Matte"] )
        {
            lottie.layers[1].tt = Number(data["Matte Mode"]);
            lottie.layers[1].tp = 1;
            lottie.layers[0].td = 1;
        }
        else
        {
            lottie.layers[1].tt = undefined;
            lottie.layers[1].tp = undefined;
            lottie.layers[0].td = undefined;
        }
    </script>
</lottie-playground>


## Layer types


<h3 id="shape-layer">Shape Layer</h3>

{schema_string:layers/shape-layer/description}

{schema_object:layers/shape-layer}

<h3 id="image-layer">Image Layer</h3>

{schema_string:layers/image-layer/description}

{schema_object:layers/image-layer}

<h3 id="null-layer">Null Layer</h3>

{schema_string:layers/null-layer/description}

{schema_object:layers/null-layer}

<h3 id="solid-layer">Solid Layer</h3>

{schema_string:layers/solid-layer/description}

{schema_object:layers/solid-layer}

<h3 id="precomposition-layer">Precomposition Layer</h3>

{schema_string:layers/precomposition-layer/description}

{schema_object:layers/precomposition-layer}

<h4 id="precomposition-time-stretch">Time Stretch</h4>

The `st` property specifies a start time offset, while `sr` defines a time stretch factor,
to be applied when evaluating animated properties pertaining to the layer:

$$t\prime = \dfrac{t}{stretch} - start$$

`sr` values less than $1$ increase the layer playback speed, while values greater than $1$
decrease it ("stretching" the layer timeline).

<lottie-playground example="time_stretch.json">
    <title>Example</title>
    <form>
        <input type="range" min="0.5" max="2" value="1" step="0.01" title="Time Stretch"/>
    </form>
    <json>lottie.layers[0]</json>
    <script>
        var layer = lottie.layers[0];
        layer.sr =  Number(data["Time Stretch"]);
    </script>
</lottie-playground>

<h4 id="precomposition-time-remap">Time Remap</h4>

The `tm` property specifies a time remap function as an animatable property, allowing full control
over the precomp timeline (subset, speedup/slowdown, reverse, frame-freeze, or any other arbitrary
transformation).

It maps the current layer time (in the frame index $[ip \ldots op]$ domain) to a precomp time
expressed in seconds, and evaluates all animatable precomp properties based on the new time value:

$$tm \colon \left[ip \ldots op\right] \mapsto seconds$$
$$t\prime = tm(t) \cdot FPS$$

Note: the global frame rate factor $FPS$ ([Animation](composition.md#Animation) `fr` property) is
required to convert back into the frame index domain.

When both time stretch (`sr`) and time remap (`tm`) are specified, time stretch is applied first.


<lottie-playground example="time_remap.json">
    <title>Example</title>
    <form>
        <select title="Time Remap">
            <option value="0">Linear</option>
            <option value="1">Reverse</option>
            <option value="2">Subset</option>
            <option value="3">Discrete</option>
            <option value="4">Easing 1</option>
            <option value="5">Easing 2</option>
            <option value="6">Easing-Reverse</option>
        </select>
    </form>
    <json>lottie.layers[1].tm</json>
    <script>
        const time_maps = [
            { 'a': 1, k: [
                { 't':   0, 's': [ 0], 'o': { 'x': [0], 'y': [0]}, 'i': { 'x': [1], 'y': [1] }},
                { 't': 600, 's': [10] }
            ]},
            { 'a': 1, k: [
                { 't':   0, 's': [10], 'o': { 'x': [0], 'y': [0]}, 'i': { 'x': [1], 'y': [1] }},
                { 't': 600, 's': [ 0] }
            ]},
            { 'a': 1, k: [
                { 't':   0, 's': [3], 'o': { 'x': [0], 'y': [0]}, 'i': { 'x': [1], 'y': [1] }},
                { 't': 600, 's': [7] }
            ]},
            { 'a': 1, k: [
                { 't':   0, 's': [ 0.0], 'o': { 'x': [0], 'y': [0]}, 'i': { 'x': [1], 'y': [1] }, 'h': 1 },
                { 't': 150, 's': [ 2.5], 'o': { 'x': [0], 'y': [0]}, 'i': { 'x': [1], 'y': [1] }, 'h': 1 },
                { 't': 300, 's': [ 5.0], 'o': { 'x': [0], 'y': [0]}, 'i': { 'x': [1], 'y': [1] }, 'h': 1 },
                { 't': 450, 's': [ 7.5], 'o': { 'x': [0], 'y': [0]}, 'i': { 'x': [1], 'y': [1] }, 'h': 1 },
                { 't': 600, 's': [10.0] }
            ]},
            { 'a': 1, k: [
                { 't':   0, 's': [ 0], 'o': { 'x': [0], 'y': [0.5]}, 'i': { 'x': [0.5], 'y': [1] }},
                { 't': 600, 's': [10] }
            ]},
            { 'a': 1, k: [
                { 't':   0, 's': [ 0], 'o': { 'x': [0], 'y': [0.5]}, 'i': { 'x': [1], 'y': [0.5] }},
                { 't': 600, 's': [10] }
            ]},
            { 'a': 1, k: [
                { 't':   0, 's': [ 0], 'o': { 'x': [0.2], 'y': [0]}, 'i': { 'x': [0.8], 'y': [1] }},
                { 't': 300, 's': [ 7], 'o': { 'x': [0.2], 'y': [0]}, 'i': { 'x': [0.8], 'y': [1] }},
                { 't': 600, 's': [ 0] }
            ]},
        ];
        const time_paths = [
            {
                'v': [[-250, 50], [250, -50]],
                'o': [[   0,  0], [  0,   0]],
                'i': [[   0,  0], [  0,   0]],
                'c': false
            }, {
                'v': [[250, 50], [-250, -50]],
                'o': [[  0,  0], [   0,   0]],
                'i': [[  0,  0], [   0,   0]],
                'c': false
            }, {
                'v': [[250, 20], [-250, -20]],
                'o': [[  0,  0], [   0,   0]],
                'i': [[  0,  0], [   0,   0]],
                'c': false
            }, {
                'v': [[-250, 50], [-125, 50], [-125, 25], [0, 25], [0, 0], [125, 0], [125, -25], [250, -25]],
                'o': [[   0,  0], [  0,   0], [   0,  0], [0,  0], [0, 0], [  0, 0], [  0,   0], [  0,   0]],
                'i': [[   0,  0], [  0,   0], [   0,  0], [0,  0], [0, 0], [  0, 0], [  0,   0], [  0,   0]],
                'c': false
            }, {
                'v': [[-250,  50], [ 250, -50]],
                'o': [[   0, -50], [   0,   0]],
                'i': [[   0,   0], [-250,   0]],
                'c': false
            }, {
                'v': [[-250,  50], [250, -50]],
                'o': [[   0, -50], [  0,   0]],
                'i': [[   0,   0], [  0,  50]],
                'c': false
            }, {
                'v': [[-250, 50], [   0, -20], [ 250, 50]],
                'o': [[ 100,  0], [ 100,   0], [   0,  0]],
                'i': [[   0,  0], [-100,   0], [-100,  0]],
                'c': false
            },
        ];
        const sample_index = data["Time Remap"];
        const precomp_layer = lottie.layers[1];
        precomp_layer.tm = time_maps[sample_index];
        const time_shape = lottie.layers[0].shapes[1].it[0];
        time_shape.ks.k = time_paths[sample_index];
    </script>
</lottie-playground>
