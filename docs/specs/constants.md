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


<h2 id="shape-direction">Shape Direction</h2>

{schema_string:constants/shape-direction/description}

{schema_enum:shape-direction}
