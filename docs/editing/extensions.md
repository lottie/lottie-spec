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

### `json_file`

Embed a JSON file into markdown, including syntax highlighting and reference links for JSON schema.

Example:

```
{json_file:lottie.schema.json}
```

## Lottie Player

### `<lottie>`

Embeds a lottie into the document


```xml
<lottie
    src="static/logo.json"
    width="200"
/>
```

<lottie
    src="static/logo.json"
    width="200"
/>
