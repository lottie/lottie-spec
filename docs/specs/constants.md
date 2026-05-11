# Enumerations

<h2 id="blend-mode">Blend Mode</h2>

{schema_string:constants/blend-mode/description}

Renderers MUST ensure each blend mode is consistent with the equivalent CSS blend mode
as defined by the W3C [Compositing and Blending Level 1](https://www.w3.org/TR/compositing-1/) recommendation.

<table class="table table-striped table-hover">
<thead>
<tr>
<th>Value</th>
<th>Name <a class="schema-link" href="../schema/#/$defs/constants/blend-mode" title="View Schema"><i class="fas fa-file-code"></i></a></th>
<th>CSS</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>0</code></td>
<td>Normal</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingnormal"><code>normal</code></a></td>
</tr>
<tr>
<td><code>1</code></td>
<td>Multiply</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingmultiply"><code>multiply</code></a></td>
</tr>
<tr>
<td><code>2</code></td>
<td>Screen</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingscreen"><code>screen</code></a></td>
</tr>
<tr>
<td><code>3</code></td>
<td>Overlay</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingoverlay"><code>overlay</code></a></td>
</tr>
<tr>
<td><code>4</code></td>
<td>Darken</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingdarken"><code>darken</code></a></td>
</tr>
<tr>
<td><code>5</code></td>
<td>Lighten</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendinglighten"><code>lighten</code></a></td>
</tr>
<tr>
<td><code>6</code></td>
<td>Color Dodge</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingcolordodge"><code>color-dodge</code></a></td>
</tr>
<tr>
<td><code>7</code></td>
<td>Color Burn</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingcolorburn"><code>color-burn</code></a></td>
</tr>
<tr>
<td><code>8</code></td>
<td>Hard Light</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendinghardlight"><code>hard-light</code></a></td>
</tr>
<tr>
<td><code>9</code></td>
<td>Soft Light</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingsoftlight"><code>soft-light</code></a></td>
</tr>
<tr>
<td><code>10</code></td>
<td>Difference</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingdifference"><code>difference</code></a></td>
</tr>
<tr>
<td><code>11</code></td>
<td>Exclusion</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingexclusion"><code>exclusion</code></a></td>
</tr>
<tr>
<td><code>12</code></td>
<td>Hue</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendinghue"><code>hue</code></a></td>
</tr>
<tr>
<td><code>13</code></td>
<td>Saturation</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingsaturation"><code>saturation</code></a></td>
</tr>
<tr>
<td><code>14</code></td>
<td>Color</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingcolor"><code>color</code></a></td>
</tr>
<tr>
<td><code>15</code></td>
<td>Luminosity</td>
<td><a href="https://www.w3.org/TR/compositing-1/#blendingluminosity"><code>luminosity</code></a></td>
</tr>
</tbody>
</table>

In the following example you can change the blend mode of the top layer

<lottie-playground example="blend-mode.json">
    <title>Example</title>
    <form>
        <input title="Opacity" type="range" min="0" value="50" max="100"/>
        <enum title="Blend Mode">blend-mode</enum>
    </form>
    <json>{...lottie.layers[0], ks: {}, shapes: []}</json>
    <script>
        lottie.layers[0].bm = Number(data["Blend Mode"]);
        lottie.layers[0].ks.o.k = data["Opacity"];
    </script>
</lottie-playground>


<h2 id="fill-rule">Fill Rule</h2>

{schema_string:constants/fill-rule/description}

{schema_enum:fill-rule}

<lottie-playground example="fill.json">
    <title>Example</title>
    <form>
        <enum title="Fill Rule">fill-rule</enum>
    </form>
    <json>lottie.layers[0].shapes[0].it[1]</json>
    <script>
        var shape = lottie.layers[0].shapes[0].it[1];
        shape.r = Number(data["Fill Rule"]);
    </script>
</lottie-playground>


<h2 id="trim-multiple-shapes">Trim Multiple Shapes</h2>

{schema_string:constants/trim-multiple-shapes/description}

{schema_enum:trim-multiple-shapes}

<lottie-playground example="trim_path.json">
    <form>
        <enum title="Multiple Shapes">trim-multiple-shapes</enum>
    </form>
    <json>lottie.layers[0].shapes[4]</json>
    <script>
        lottie.layers[0].shapes[4].m = Number(data["Multiple Shapes"]);
    </script>
</lottie-playground>


<h2 id="shape-direction">Shape Direction</h2>

{schema_string:constants/shape-direction/description}

{schema_enum:shape-direction}

<lottie-playground example="trim_path.json">
    <form>
        <enum title="Shape Direction">shape-direction</enum>
    </form>
    <json>lottie.layers[0].shapes[1]</json>
    <script>
        for ( let shape of lottie.layers[0].shapes )
            shape.d = Number(data["Shape Direction"]);
    </script>
</lottie-playground>


<h2 id="star-type">Star Type</h2>

{schema_string:constants/star-type/description}

{schema_enum:star-type}

<lottie-playground example="star.json">
    <title>Example</title>
    <form>
        <enum title="Star Type">star-type</enum>
    </form>
    <json>lottie.layers[0].shapes[0].it[0]</json>
    <script>
        var star = lottie.layers[0].shapes[0].it[0];
        star.sy = Number(data["Star Type"]);
        if ( data["Star Type"] == "1" )
        {
            star["ir"] = {"a": 0, "k": 100};
            star["is"] = {"a": 0, "k": 0};
        }
        else
        {
            delete star["ir"];
            delete star["is"];
        }
        lottie.layers[0].shapes[0].it[0] = star;
    </script>
</lottie-playground>


<h2 id="line-cap">Line Cap</h2>

{schema_string:constants/line-cap/description}

{schema_enum:line-cap}

<lottie-playground example="stroke.json">
    <title>Example</title>
    <form>
        <enum title="Line Cap" value="2">line-cap</enum>
    </form>
    <json>lottie.layers[0].shapes[2]</json>
    <script>
        var shape = lottie.layers[0].shapes[2];
        shape.lc = Number(data["Line Cap"]);
        shape.d = undefined;
    </script>
</lottie-playground>


<h2 id="line-join">Line Join</h2>

{schema_string:constants/line-join/description}

{schema_enum:line-join}

<lottie-playground example="stroke.json">
    <title>Example</title>
    <form>
        <enum title="Line Join" value="2">line-join</enum>
        <input type="range" min="0" max="10" value="3" title="Miter Limit"/>
    </form>
    <json>lottie.layers[0].shapes[2]</json>
    <script>
        var shape = lottie.layers[0].shapes[2];
        shape.lj = Number(data["Line Join"]);
        shape.ml = data["Miter Limit"];
        shape.d = undefined;
        var trim = lottie.layers[0].shapes[1];
        trim.e.k = 100;
    </script>
</lottie-playground>

<h2 id="mask-mode">Mask Mode</h2>

{schema_string:constants/mask-mode/description}

{schema_enum:mask-mode}

<lottie-playground example="masks.json">
    <title>Example</title>
    <form>
        <enum title="Mask Mode" value="a">mask-mode</enum>
        <input type="range" min="0" max="100" value="100" title="Mask1 Opacity"/>
        <input type="range" min="0" max="100" value="100" title="Mask2 Opacity"/>
    </form>
    <json>lottie.layers[1].masksProperties[1]</json>
    <script>
        let mask1 = lottie.layers[1].masksProperties[0];
        let mask2 = lottie.layers[1].masksProperties[1];
        mask1.o.k = Number(data["Mask1 Opacity"]);
        mask2.o.k = Number(data["Mask2 Opacity"]);
        mask2.mode = data["Mask Mode"];
    </script>
</lottie-playground>

<h2 id="stroke-dash-type">Stroke Dash Type</h2>

{schema_string:constants/stroke-dash-type/description}

{schema_enum:stroke-dash-type}

<h2 id="matte-mode">Matte Mode</h2>

{schema_string:constants/matte-mode/description}

The value for Luma is calculated according to [Rec.709](https://www.itu.int/rec/R-REC-BT.709) standard:

$$Y = 0.2126 R + 0.7152 G + 0.0722 B$$

{schema_enum:matte-mode}

<lottie-playground example="matte.json">
    <title>Example</title>
    <form>
        <enum title="Matte Mode" value="1">matte-mode</enum>
    </form>
    <json>{...lottie.layers[1], shapes: [], ks: {}}</json>
    <script>
        lottie.layers[1].tt = Number(data["Matte Mode"]);
    </script>
</lottie-playground>

<h2 id="gradient-type">Gradient Type</h2>

{schema_string:constants/gradient-type/description}

{schema_enum:gradient-type}

<lottie-playground example="gradient.json">
    <title>Example</title>
    <form>
        <enum title="Type" value="1">gradient-type</enum>
    </form>
    <json>lottie.layers[1].shapes[0].it[1]</json>
    <script>
    var gradient = lottie.layers[1].shapes[0].it[1];
    gradient.t = Number(data["Type"]);
    </script>
</lottie-playground>

<h2 id="property-type">Property Type</h2>

{schema_string:constants/property-type/description}

{schema_enum:property-type}

For examples of each property type, see the [Property types](properties.md#vector-property) section.
