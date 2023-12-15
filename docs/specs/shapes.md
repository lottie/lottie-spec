# Shapes

The shape objects are divided in 4 categories:

* [Raw Shapes](#raw-shapes) that define the actual curves but have no styling information
* [Grouping](#grouping), used to organize collections of shape elements
* [Styles](#shape-style), that define the visual appearance of raw shapes
* [Modifiers](#modifier) alter the curves of the raw shapes

<h2 id="shape-element">Shape Element</h2>

{schema_string:shapes/shape-element/description}

{schema_object:shapes/shape-element}

The `ty` property defines the specific element type based on the following values:

{schema_subtype_table:shapes/all-shapes:ty}


## Raw Shapes

<h2 id="shape">Shapes</h2>

{schema_string:shapes/shape/description}

{schema_object:shapes/shape}


<h3 id="ellipse">Ellipse</h3>

{schema_string:shapes/ellipse/description}

{schema_object:shapes/ellipse}


<h3 id="path">Path</h3>

{schema_string:shapes/path/description}

{schema_object:shapes/path}


<h3 id="rectangle">Rectangle</h3>

{schema_string:shapes/rectangle/description}

{schema_object:shapes/rectangle}

## Grouping

<h3 id="group">Group</h3>

{schema_string:shapes/group/description}

{schema_object:shapes/group}

### Transform

{schema_string:shapes/transform/description}

{schema_object:shapes/transform}


<h2 id="shape-style">Styles</h3>

{schema_string:shapes/shape-style/description}

{schema_object:shapes/shape-style}


<h3 id="fill">Fill</h3>

{schema_string:shapes/fill/description}

{schema_object:shapes/fill}

<h2 id="modifier">Modifiers</h2>

{schema_string:shapes/modifier/description}

{schema_object:shapes/modifier}

<h3 id="trim-path">Trim Path</h3>

{schema_string:shapes/trim-path/description}

{schema_object:shapes/trim-path}
