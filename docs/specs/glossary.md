# Glossary

local coordinates
:   The local coordinate system is the coordinate system of the current
    group or layer, with the X coordinate increasing towards the right
    and the Y coordinate increasing towards the bottom.
render stack
:   A render stack is a list if rendering primitive to be drawn in inverse
    stack order. A render stack can contain child stacks.
stacking order
:   The order in which objects appear in the [[render stack]].
collected shapes
:   When collecting shapes for a rendering operation, implementations MUST
    traverse the [[render stack]] in reverse order.
    All {link:shapes/shape:Shapes} encountered in the stack traversal MUST
    be included, until the beginning of the stack is reached or a {link:shapes/modifier}
    is encountered. If a {link:shapes/modifier} is found, it MUST be applied to
    its own _collected shapes_ and the output added to the shape collection.
