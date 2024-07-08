# Properties

## Introduction

Properties in Lottie can be animated.

Their structure depends on whether it's animated or not:

| Attribute | Type | Title | Description |
|-----------|------|-------|-------------|
| `a`       | {link:values/int-boolean} | Animated | Whether the property is animated |
| `k`       | | Value or Keyframes | When it's not animated, `k` will contain the value directly. When animated, `k` will be an array of keyframes. |

<h3 id="base-keyframe">Keyframes</h3>

{schema_object:properties/base-keyframe}

Keyframe arrays MUST be stored in order of strictly ascending `t` frame number. Two keyframes cannot have the same `t` value.

If `h` is present and it's 1, you don't need `i` and `o`, as the property will keep the same value
until the next keyframe.

If the first keyframe occurs after the start of the animation, the initial property value will be from the first keyframe. Similarly if the last keyframe is before the end of the animation, the last keyframe value will be held until the end.

<h3 id="easing-handle">Keyframe Easing</h3>

Keyframe easing handles are objects with `x` and `y` attributes, which are numbers within 0 and 1.

{schema_object:properties/easing-handle}

For vector properties, these are arrays, with one element
per dimension so you can have different easing curves per dimension.

They represent a cubic bezier, starting at `[0,0]` and ending at `[1,1]` where
the value determines the easing function.

The `x` axis represents time, a value of 0 is the time of the current keyframe,
a value of 1 is the time of the next keyframe.

The `y` axis represents the value interpolation factor, a value of 0
represents the value at the current keyframe, a value of 1 represents the
value at the next keyframe.

Unlike `x` values, `y` values are not clamped to `[0 .. 1]`.  Supernormal `y`
values allow the interpolated value to overshoot (extrapolate) beyond the
specified keyframe values range.

When you use easing you have two easing handles for the keyframe:

`o` is the "out" handle, and is the first one in the bezier, determines the curve
as it exits the current keyframe.


`i` is the "in" handle, and it's the second one in the bezier, determines the curve
as it enters the next keyframe.


For linear interpolation you'd have

```json
{
    "o": {"x": [0, 0], "y": [0, 0]},
    "i": {"x": [1, 1], "y": [1, 1]}
}
```

For easing in and out, you move the `x` towards the center, this makes the animation more fluid:

```json
{
    "o": {"x": [0.333, 0.333], "y": [0, 0]},
    "i": {"x": [0.667, 0.667], "y": [1, 1]}
}
```

<h4>Easing example</h4>
In the following example, the ball moves left and right, on the background you can see and edit a representation of its easing function.

{editor_example:easing}


## Property types


<h3 id="vector-property">Vector</h3>

Animatable {link:values/vector}.

{schema_object:properties/vector-property}


<h4 id="vector-keyframe">Vector Keyframe</h4>

{schema_string:properties/vector-keyframe/description}

{schema_object:properties/vector-keyframe}


<h3 id="scalar-property">Scalar</h3>

Animatable scalar (single number value).

Note that when animated it uses {link:properties/vector-keyframe:Vector Keyframes},
so instead of scalars keyframes have arrays with a single values.

{schema_object:properties/scalar-property}


<h3 id="position-property">Position</h3>

Animatable 2D {link:values/vector} with optional spatial tangents.

{schema_object:properties/position-property}


<h4 id="position-keyframe">Position Keyframe</h4>

{schema_string:properties/position-keyframe/description}

{schema_object:properties/position-keyframe}


<h3 id="bezier-property">Bezier Shape</h3>

Animatable {link:values/bezier}.

{schema_object:properties/bezier-property}


<h4 id="bezier-keyframe">Bezier Shape Keyframe</h4>

{schema_string:properties/bezier-keyframe/description}

{schema_object:properties/bezier-keyframe}

<h3 id="color-property">Color</h3>

Animatable {link:values/color}.

{schema_object:properties/color-property}


<h4 id="color-keyframe">Color Keyframe</h4>

{schema_string:properties/color-keyframe/description}

{schema_object:properties/color-keyframe}
