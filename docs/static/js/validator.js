function extraxt_schema_ty(schema)
{
    if ( !schema )
        return;

    if ( "properties" in schema )
    {
        let ty_prop = schema.properties.ty;
        if ( !ty_prop )
            return;
        return ty_prop.const;
    }

    for ( let prop of ["oneOf", "anyOf", "allOf"] )
    {
        if ( schema[prop] )
        {
            for ( let sub_schema of schema[prop] )
            {
                let ty = extraxt_schema_ty(sub_schema);
                if ( ty !== undefined )
                    return ty;
            }
        }
    }
}

function patch_docs_links(schema, url, name)
{
    if ( typeof(schema) == "object" )
    {
        if ( Array.isArray(schema) )
        {
            for ( let item of schema )
                patch_docs_links(item, url, name);
        }
        else
        {
            for ( let val of Object.values(schema) )
                patch_docs_links(val, url, name);
            schema._docs = url;
            schema._name = name;
        }
    }
}

function kebab_to_title(kebab)
{
    return kebab.split("-").map(chunk => chunk.charAt(0).toUpperCase() + chunk.substring(1).toLowerCase()).join(" ");
}

class Validator
{
    constructor(AjvClass, schema_json)
    {
        this.schema = schema_json;
        for ( let [cat, sub_schemas] of Object.entries(this.schema["$defs"]) )
        {
            let cat_docs = `/lottie-spec/specs/${cat}/`;
            let cat_name = kebab_to_title(cat);
            for ( let [obj, sub_schema] of Object.entries(sub_schemas) )
            {
                let obj_docs = cat_docs;
                let obj_name = cat_name;
                if ( sub_schema.type && obj != "base-gradient" )
                {
                    obj_docs += "#" + obj;
                    obj_name = kebab_to_title(obj);
                }
                patch_docs_links(sub_schema, obj_docs, obj_name);
            }
        }
        let schema_id = this.schema["$id"];
        this.sub_schemas = {
            layers: this._extract_ty_discriminated_schema(schema_id, "layers", "all-layers"),
            shapes: this._extract_ty_discriminated_schema(schema_id, "shapes", "all-graphic-elements"),
        };

        this.validator = new AjvClass({
            // allErrors: true,
            verbose: true,
            // inlineRefs: false,
            strict: false,
            keywords: [{keyword: "_docs"}, {keyword: "_name"}],
            schemas: [this.schema],
        });
        this._validate_internal = this.validator.getSchema(schema_id);

        for ( let sub_obj of Object.values(this.sub_schemas) )
        {
            for ( let subs of Object.values(sub_obj) )
                subs.validator = this.validator.getSchema(subs.id);
        }
    }

    _extract_ty_discriminated_schema(id_base, category, all)
    {
        this.schema["$defs"][category][all] = {
            _docs: this.schema["$defs"][category][all],
        };

        let found = {};
        for ( let [name, sub_schema] of Object.entries(this.schema["$defs"][category]) )
        {
            let ty = extraxt_schema_ty(sub_schema);
            if ( ty !== undefined )
            {
                let id = `${id_base}#/$defs/${category}/${name}`;
                found[ty] = {
                    id: id,
                    docs: `/lottie-spec/specs/${category}#${name}`,
                }
            }
        }
        return found;
    }

    validate(string)
    {
        var data;
        try {
            data = JSON.parse(string);
        } catch(e) {
            return [{
                type: "error",
                name: "Document",
                message: "is not a valid JSON file",
            }];
        }

        let errors = [];
        if ( !this._validate_internal(data) )
            errors = this._validate_internal.errors.map(e => this._cleaned_error(e));

        this._validate_layers(data, "/", errors);
        this._validate_assets(data, errors);
        return errors;
    }

    _cleaned_error(error, prefix="")
    {
        console.log(error);
        return {
            type: "error",
            message: error.message,
            path: prefix + (error.instancePath ?? ""),
            name: error.parentSchema?._name ?? "Value",
            docs: error.parentSchema?._docs,
        };
    }

    _validate_assets(data, errors)
    {
        if ( !data.assets )
            return;

        for ( let i = 0; i < data.assets.length; i++ )
        {
            if ( data.assets[i].layers )
                this._validate_layers(data.assets[i], `/assets/${i}/`, errors);
        }

    }

    _validate_layers(data, path, errors)
    {
        for ( let i = 0; i < data.layers.length; i++ )
        {
            this._validate_layer(data.layers[i], `${path}layers/${i}`, errors);
        }
    }

    _validate_layer(layer, path, errors)
    {
        if ( typeof layer != "object" || Array.isArray(layer) )
        {
            errors.push({
                type: "error",
                path: path,
                name: "Layer",
                docs: "/lottie-spec/specs/layers/",
                message: "must be an object",
            });
            return;
        }

        if ( layer.ty === undefined )
        {
            errors.push({
                type: "error",
                path: path,
                docs: "/lottie-spec/specs/layers/",
                name: "Layer",
                message: "is missing 'ty'",
            });
            return;
        }

        let sub_schema = this.sub_schemas.layers[layer.ty];
        if ( sub_schema === undefined )
        {
            errors.push({
                type: "warning",
                path: path + "/ty",
                name: "Layer",
                docs: "/lottie-spec/specs/layers/",
                message: "has unknown 'ty' " + layer.ty,
            });
            return;
        }

        if ( !sub_schema.validator(layer) )
        {
            for ( let error of sub_schema.validator.errors )
                errors.push(this._cleaned_error(error, path));
        }

        if ( layer.ty === 4 && layer.shapes )
        {
            for ( let i = 0; i < layer.shapes.length; i++ )
            {
                this._validate_shape(layer.shapes[i], `${path}/shapes/${i}/`, errors);
            }
        }
    }

    _validate_shape(shape, path, errors)
    {
        if ( typeof shape != "object" || Array.isArray(shape) )
        {
            errors.push({
                type: "error",
                path: path,
                name: "Shape",
                docs: "/lottie-spec/specs/shapes/",
                message: "must be an object",
            });
            return;
        }

        if ( shape.ty === undefined )
        {
            errors.push({
                type: "error",
                path: path,
                docs: "/lottie-spec/specs/shapes/",
                name: "Shape",
                message: "is missing 'ty'",
            });
            return;
        }

        let sub_schema = this.sub_schemas.shapes[shape.ty];
        if ( sub_schema === undefined )
        {
            errors.push({
                type: "warning",
                path: path + "/ty",
                docs: "/lottie-spec/specs/shapes/",
                name: "Shape",
                message: "has unknown 'ty' " + layer.ty,
            });
            return;
        }

        if ( !sub_schema.validator(shape) )
        {
            for ( let error of sub_schema.validator.errors )
                errors.push(this._cleaned_error(error, path));
        }
    }
}

