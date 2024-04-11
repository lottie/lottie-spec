# Enumerations


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

<h2 id="stroke-dash-type">Stroke Dash Type</h2>

{schema_string:constants/stroke-dash-type/description}

{schema_enum:stroke-dash-type}
