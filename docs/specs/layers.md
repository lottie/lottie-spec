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

The `tm` property specifies a time remap function, which offers full control over the precomp
timeline.  It maps the current layer time (in the frame index $[in..out]$ domain) to a precomp
time expressed in seconds, and evaluates all animatable precomp properties based on the new
time value:

$$t\prime = TM(t) * FPS$$

Note: the global frame rate factor $FPS$ ([Animation](composition.md#Animation) `fr` property) is
required to convert back into the frame index domain.

When both time stretch (`sr`) and time remap (`tm`) are specified, time stretch is applied first.


<lottie-playground example="time_remap.json">
    <title>Example</title>
    <form>
        <select title="Time Remap">
            <option value="0">Linear</option>
            <option value="1">Easing 1</option>
            <option value="2">Easing 2</option>
            <option value="3">Easing-Reverse</option>
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
        const precomp_layer = lottie.layers[1];
        precomp_layer.tm = time_maps[data["Time Remap"]];
        const time_shape = lottie.layers[0].shapes[1].it[0];
        time_shape.ks.k = time_paths[data["Time Remap"]];
    </script>
</lottie-playground>
