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

for example:

* {lottie_color:1, 0, 0}
* {lottie_color:1, 0.5, 0}

Note sometimes you might find color values with 4 components (the 4th being alpha)
but most players ignore the last component.

<h2 id="hexcolor">Hex Color</h2>
Colors represented as a "#"-prefixed string, with two hexadecimal digits per
RGB component.

* {lottie_hexcolor: #FF8000}

<h2 id="gradient">Gradient</h2>

{schema_string:values/gradient/description}

The count of color components is typically specified in a separate field from
the gradient values. Any remaining values after reaching the specified count of
color components are transparency components.

The offset is expressed as a percentage between start (0) and end (1).

Components must be arranged in ascending offset order. 

<h3>Gradient without transparency</h3>

So let's say you want these colors:

* {lottie_color:0.16, 0.18, 0.46}
* {lottie_color:0.2, 0.31, 0.69}
* {lottie_color:0.77, 0.85, 0.96}

the array will look like the following:

`[0, 0.16, 0.18, 0.46, 0.5, 0.2, 0.31, 0.69, 1, 0.77, 0.85, 0.96]`

| Value     | Description |
|-----------|---|
| `0`       | Offset of the 1st color (`0` means at the start) |
| `0.16`   | Red component for the 1st color |
| `0.18`   | Green component for the 1st color |
| `0.46`   | Blue component for the 1st color |
| `0.5`     | Offset of the 2nd color (`0.5` means half way) |
| `0.2`   | Red component for the 2nd color |
| `0.31`   | Green component for the 2nd color |
| `0.69`    | Blue component for the 2nd color |
| `1`       | Offset of the 3rd color (`1` means at the end) |
| `0.77`   | Red component for the 3rd color |
| `0.85`   | Green component for the 3rd color |
| `0.96`   | Blue component for the 3rd color |

<h3>Gradient with transparency</h3>

Transparency components are added at the end. Transparency components may or may
not match the count and offset of color components.

So assume the same colors as before, but opacity of 80% for the first color and 100% for the other two.

The array will look like this:

`[0, 0.16, 0.18, 0.46, 0.5, 0.2, 0.31, 0.69, 1, 0.77, 0.85, 0.96, 0, 0.8, 0.5, 1, 1, 1]`

It's the same array as the case without transparency but with the following values added at the end:


| Value     | Description |
|-----------|---|
| `0`       | Offset of the 1st color (`0` means at the start) |
| `0.8`     | Alpha component for the 1st color |
| `0.5`     | Offset of the 2nd color (`0.5` means half way) |
| `1`       | Alpha component for the 2nd color |
| `1`       | Offset of the 3rd color (`1` means at the end) |
| `1`       | Alpha component for the 3rd color |

<h3>Gradient Example</h3>

{editor_example:gradient}

<h2 id="bezier">Bezier Shape</h2>

{schema_string:values/bezier/description}

{schema_object:values/bezier}

{editor_example:bezier}

<h2 id="data-url">Data URL</h2>

Data URLs are embedded files (such as images) as defined in [RFC2397](https://datatracker.ietf.org/doc/html/rfc2397).
