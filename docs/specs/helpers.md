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

Transforms the parent's coordinate system.

When calculating a transform matrix, properties SHOULD be applied as follows:

1. Translate by $-a$
1. Scale by $\frac{s}{100}$
1. If $sk \neq 0$:
    1. Rotate by $-sa$
    1. Skew x by $\tan(-sk)$
    1. Rotate by $sa$
1. Rotate by $-r$
1. Translate by $p$

Assuming a transform matrix with the following layout, with the labels equivalent to the
[CSS matrix transform](https://developer.mozilla.org/en-US/docs/Web/CSS/transform-function/matrix):

$$
\begin{pmatrix}
a & b & 0 & 0 \\
c & d & 0 & 0 \\
0 & 0 & 1 & 0 \\
tx & ty & 0 & 1
\end{pmatrix}
$$

The final transform is given by:

$$
\begin{split}
&
\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
-a.x & -a.y & 0 & 1
\end{pmatrix}

\times

\begin{pmatrix}
\frac{s.x}{100} & 0 & 0 & 0 \\
0 & \frac{s.y}{100} & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}


\times \\ \times &

\begin{pmatrix}
\cos(-sa) & \sin(-sa) & 0 & 0 \\
-\sin(-sa) & \cos(-sa) & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}

\times

\begin{pmatrix}
1 & \tan(-sk) & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}

\times

\begin{pmatrix}
\cos(sa) & \sin(sa) & 0 & 0 \\
-\sin(sa) & \cos(sa) & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}

\times \\ \times &

\begin{pmatrix}
\cos(-r) & \sin(-r) & 0 & 0 \\
-\sin(-r) & \cos(-r) & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}

\times

\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
p.x & p.y & 0 & 1
\end{pmatrix}
\end{split}
$$

<h2 id="visual-object">Visual Object</h2>

{schema_string:helpers/visual-object/description}

{schema_object:helpers/visual-object}


<h2 id="marker">Marker</h2>

{schema_string:helpers/marker/description}

{schema_object:helpers/marker}
