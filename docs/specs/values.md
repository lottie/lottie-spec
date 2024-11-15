# Values

<h2 id="int-boolean">Integer Boolean</h2>

{schema_string:values/int-boolean/description}

<h2 id="vector">Vector</h2>

Vector data is represented by an array of numbers.
This is used any time a property with multiple components is needed.

An example would be a position, which would be represented as an array
with two numbers, the first corresponding to the _X_ coordinate and the
second corresponding to the _Y_.

<h2 id="color">Color</h2>

Colors are [Vectors](#vector) with values between 0 and 1 for the RGB components.

For example:

* {lottie_color:1, 0, 0}
* {lottie_color:1, 0.5, 0}

Note: sometimes you might find color values with 4 components (the 4th being alpha)
but most players ignore the last component.

<h2 id="hexcolor">Hex Color</h2>
Colors represented as a "#"-prefixed string, with two hexadecimal digits per
RGB component.

* {lottie_hexcolor: #FF8000}

<h2 id="gradient">Gradient</h2>

The gradient appearance is specified in terms of color stops and opacity stops.
Color stops are defined as `(position, color)` tuples, where the position is a normalized `[0..1]`value along the gradient axis `[startpoint -> endpoint]`, and the color is 3 floats representing the RGB components. Transparency (opacity) stops are defined as `(position, transparency)` tuples, where the position is a normalized `[0..1]`value along the gradient axis `[startpoint -> endpoint]`, and transparency is a `[0..1]` value.

All color and opacity stops are stored sequentially by ascending offsets in a flattened float array (color stops followed by opacity stops), with 4 floats per color stop and 2 floats per opacity stops. Thus, given color stops and opacity stops, the expected size for the gradient data array is `4 * Nc + 2 * No`.

The color stop count MUST be specified in a separate field from the gradient values, while the count of opacity stops can be inferred from the data array length: `No = (length - 4 * Nc)/2`.

<h3>Gradient without transparency</h3>

So let's say you want these colors:

* {lottie_color:0.16, 0.18, 0.46}
* {lottie_color:0.2, 0.31, 0.69}
* {lottie_color:0.77, 0.85, 0.96}

the array will look like the following:

{lottie_gradient:0, 0.16, 0.18, 0.46, 0.5, 0.2, 0.31, 0.69, 1, 0.77, 0.85, 0.96}

| Value     | Description |
|-----------|---|
| `0`       | Offset of the 1st color (`0` means at the start) |
| `0.16`    | Red component for the 1st color |
| `0.18`    | Green component for the 1st color |
| `0.46`    | Blue component for the 1st color |
| `0.5`     | Offset of the 2nd color (`0.5` means half way) |
| `0.2`     | Red component for the 2nd color |
| `0.31`    | Green component for the 2nd color |
| `0.69`    | Blue component for the 2nd color |
| `1`       | Offset of the 3rd color (`1` means at the end) |
| `0.77`    | Red component for the 3rd color |
| `0.85`    | Green component for the 3rd color |
| `0.96`    | Blue component for the 3rd color |

<h3>Gradient with transparency</h3>

Transparency stops are added at the end. Transparency stops may or may
not match the count and offset of color stops.

So assume the same colors as before, but opacity of 80% for the first color and 100% for the other two.

The array will look like this:

{lottie_gradient_alpha:0, 0.16, 0.18, 0.46, 0.5, 0.2, 0.31, 0.69, 1, 0.77, 0.85, 0.96, 0, 0.8, 0.5, 0.2, 1, 1}

It's the same array as the case without transparency but with the following values added at the end:


| Value     | Description |
|-----------|---|
| `0`       | Offset of the 1st color (`0` means at the start) |
| `0.8`     | Alpha component for the 1st color |
| `0.5`     | Offset of the 2nd color (`0.5` means half way) |
| `0.2`     | Alpha component for the 2nd color |
| `1`       | Offset of the 3rd color (`1` means at the end) |
| `1`       | Alpha component for the 3rd color |

<h3 class="print-site-plugin-ignore">Gradient Example</h3>

{editor_example:gradient}

<h2 id="bezier">Bezier Shape</h2>

{schema_string:values/bezier/description}

{schema_object:values/bezier}

{editor_example:bezier}

<h2 id="data-url">Data URL</h2>

Data URLs are embedded files (such as images) as defined in [RFC2397].
