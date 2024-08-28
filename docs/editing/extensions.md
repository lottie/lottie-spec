# Markdown Extensions

This documentation comes with several markdown extensions that allow
interactive elements and data pulled from the schema.

## Schema Integration

### `schema_string`

Using a reference to a value in the JSON schema (without `$defs`) will embed that string
into the markdown text.

Example:

```
{schema_string:shapes/graphic-element/description}
```

Output:

{schema_string:shapes/graphic-element/description}

### `link`

Links to the relevant section in the specs.

Example:

```
{link:shapes/ellipse}
```

Output:

{schema_link:shapes/ellipse}


### `schema_link`

Link to the relevant section in the formatted schema.

Example:

```
{schema_link:shapes/ellipse}
```

Output:

{schema_link:shapes/ellipse}

### `schema_subtype_table`

Used to list all the `ty` values for Layer / Shape etc.


Example:

```
{schema_subtype_table:layers/all-layers:ty}
```

Output:

{schema_subtype_table:layers/all-layers:ty}

### `schema_object`

Embeds a property table from the schema.

Example:

```
{schema_object:shapes/ellipse}
```

Output:

{schema_object:shapes/ellipse}

### `schema_enum`

Same as `schema_object` but for enumerations.

Example:

```
{schema_enum:fill-rule}
```

Output:

{schema_enum:fill-rule}

### `schema_inheritance`

Shows the inheritance diagram for an object type.

Example:

```
{schema_inheritance:shapes/ellipse}
```

Output:

{schema_inheritance:shapes/ellipse}

### `json_file`

Embed a JSON file into markdown, including syntax highlighting and reference links for JSON schema.

Example:

```
{json_file:lottie.schema.json}
```

## Lottie Player

### `<lottie>`

Embeds a lottie into the document

Example:

```xml
<lottie
    src="static/logo.json"
    width="200"
    background="white"
/>
```

Output:

<lottie
    src="static/logo.json"
    width="200"
    background="white"
/>


### `lottie-playground`

Embeds a player side by side to a JSON snipped and controls to tweak the animation

Example:

```html
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
```

Output:

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

## Miscellaneous

### `[RFC]`

Links to a IETF RFC.

Example:

```
[RFC9402]
```

Output:

[RFC9402]


### BCP14

Automatically highlights keywords from BCP 14 ([RFC2119] [RFC8174]).

Example:

```
MUST
```

Output:

MUST

### Math Input

You can embed $\LaTeX$ math mode code.

Example:

```
Normal text with inline $\LaTeX$: $\frac{1}{x}$.

$$\sum\limits_{i=1}^n{n\choose i}t^i(1-t)^{n-1}P_i$$
```

Output:


Normal text with inline $\LaTeX$: $\frac{1}{x}$.

$$\sum\limits_{i=1}^n{n\choose i}t^i(1-t)^{n-1}P_i$$


### `lottie_color`

Shows an inline preview of a lottie color array.

Example:

```
{lottie_color:1, 0.5, 0}
```

Output:

{lottie_color:1, 0.5, 0}


### `lottie_hexcolor`

Shows an inline preview of a color from hex code.

Example:

```
{lottie_hexcolor:#FF8000}
```

Output:

{lottie_hexcolor:#FF8000}


### `lottie_gradient`

Shows an inline preview of a lottie gradient (without alpha).

Example:

```
{lottie_gradient:0, 0.16, 0.18, 0.46, 0.5, 0.2, 0.31, 0.69, 1, 0.77, 0.85, 0.96}
```

Output:

{lottie_gradient:0, 0.16, 0.18, 0.46, 0.5, 0.2, 0.31, 0.69, 1, 0.77, 0.85, 0.96}


### `lottie_gradient_alpha`

Shows an inline preview of a lottie gradient (with alpha).

Alpha stop offsets need to match the color stop offsets.

Example:

```
{lottie_gradient_alpha:0, 0.16, 0.18, 0.46, 0.5, 0.2, 0.31, 0.69, 1, 0.77, 0.85, 0.96, 0, 0.8, 0.5, 0.2, 1, 1}
```

Output:

{lottie_gradient_alpha:0, 0.16, 0.18, 0.46, 0.5, 0.2, 0.31, 0.69, 1, 0.77, 0.85, 0.96, 0, 0.8, 0.5, 0.2, 1, 1}


### Glossary Terms

Glossary terms can be linked to using Mediawiki-style syntax:

Example:

```
[[local coordinates]] or [[local coordinates|coordinate system]]
```

Output:

[[local coordinates]] or [[local coordinates|coordinate system]]
