function extract_schema_ty(schema)
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
                let ty = extract_schema_ty(sub_schema);
                if ( ty !== undefined )
                    return ty;
            }
        }
    }
}

function patch_docs_links(schema, url, name, docs_name, within_properties)
{
    if ( typeof(schema) == "object" )
    {
        if ( Array.isArray(schema) )
        {
            for ( let item of schema )
                patch_docs_links(item, url, name, docs_name);
        }
        else
        {
            for ( let [pname, val] of Object.entries(schema) )
            {
                var sub_name = name;
                if ( within_properties )
                    sub_name += "." + pname;

                patch_docs_links(val, url, sub_name, docs_name, pname == "properties");
            }

            if ( !within_properties )
            {
                schema._docs = url;
                schema._docs_name = docs_name;
                schema._name = name;
            }
        }
    }
}

class PropertyList
{
    constructor(schema)
    {
        this.properties = new Set();
        this.references = new Set();
        this.schema = schema;
        this.resolved = false;
        this.skip = false;
    }

    valid()
    {
        return !this.skip && (this.properties.size > 0 || this.references.size > 1);
    }
}

class PropertyMap
{
    constructor()
    {
        this.map = new Map();
        this.all_references = new Set();
    }

    create(id, schema)
    {
        var map = new PropertyList(schema);
        this.map.set(id, map);
        return map;
    }

    finalize()
    {
        for ( let [name, prop_list] of this.map )
        {
            if ( prop_list.valid() && !this.all_references.has(name) )
                prop_list.schema.warn_extra_props = this._get_all_props(prop_list);
        }
    }

    _get_all_props(prop_list)
    {
        if ( !prop_list.resolved )
        {
            prop_list.resolved = true;
            for ( let ref of prop_list.references )
                for ( let prop of this.get_all_props(ref) )
                    prop_list.properties.add(prop);
        }

        return prop_list.properties;
    }

    get_all_props(id)
    {
        return this._get_all_props(this.map.get(id));
    }

    extract_all_properties(schema, id, prop_list, referencing_base)
    {
        if ( typeof schema != "object" || schema === null )
            return;

        if ( Array.isArray(schema) )
        {
            for ( let i = 0; i < schema.length; i++ )
                this.extract_all_properties(schema[i], id + `/${i}`, prop_list, false);

            return;
        }

        for ( let [name, sub_schema] of Object.entries(schema) )
        {
            if ( name == "properties" )
            {
                for ( let [prop_name, prop] of Object.entries(sub_schema) )
                {
                    prop_list.properties.add(prop_name);
                    let prop_id = id + "/properties/" + prop_name;
                    this.extract_all_properties(prop, prop_id, this.create(prop_id, prop), false);
                }
            }
            else if ( name == "oneOf" )
            {
                for ( let i = 0; i < sub_schema.length; i++ )
                {
                    let oneof_id = id + "/oneOf/" + i;
                    let oneof_schema = sub_schema[i];
                    let oneof_list = id.endsWith("-property") ? prop_list : this.create(oneof_id, oneof_schema);
                    this.extract_all_properties(oneof_schema, oneof_id, oneof_list, false);
                }
            }
            else if ( name == "allOf" )
            {
                for ( let i = 0; i < sub_schema.length; i++ )
                {
                    let oneof_id = id + "/allOf/" + i;
                    let oneof_schema = sub_schema[i];
                    this.extract_all_properties(oneof_schema, oneof_id, prop_list, true);
                }
            }
            else if ( name == "additionalProperties" )
            {
                prop_list.skip = true;
            }
            else if ( name == "$ref" )
            {
                prop_list.references.add(sub_schema);
                if ( referencing_base )
                    this.all_references.add(sub_schema);
            }
            else if ( name != "not" )
            {
                this.extract_all_properties(sub_schema, id + "/" + name, prop_list, false);
            }
        }
    }
}


function kebab_to_title(kebab)
{
    return kebab.split("-").map(chunk => chunk.charAt(0).toUpperCase() + chunk.substring(1).toLowerCase()).join(" ");
}


function custom_discriminator(propname, fail_unknown, default_value=undefined)
{
    function validate_fn(schema, data, parent_schema, data_cxt)
    {
        var value = data[propname]

        // Error will be generated by required
        if ( value === undefined )
        {
            if ( default_value === undefined )
                return true;
            value = default_value;
        }

        var sub_schema = schema[value];
        if ( sub_schema === undefined )
        {
            validate_fn.errors = [{
                message: `has unknown '${propname}' value ` + JSON.stringify(value),
                type: fail_unknown ? "error" : "warning",
                warning: "type",
                instancePath: data_cxt.instancePath,
                parentSchema: parent_schema,
            }];
            return false;
        }

        var validate = this.getSchema(sub_schema.id);
        if ( !validate(data, data_cxt) )
        {
            validate_fn.errors = validate.errors;
            return false;
        }
        return true;
    }

    return validate_fn;
}

function patch_schema_enum(schema)
{
    if ( "oneOf" in schema )
    {
        schema.enum_oneof = schema.oneOf;
        delete schema.oneOf;
    }
}

function keyframe_has_t(kf)
{
    return typeof kf == "object" && typeof kf.t == "number";
}

class Validator
{
    constructor(AjvClass, schema_json, docs_url="")
    {
        this.schema = schema_json;
        this.defs = this.schema["$defs"];
        var prop_map = new PropertyMap();

        for ( let [cat, sub_schemas] of Object.entries(this.defs) )
        {
            let cat_docs = `${docs_url}/specs/${cat}/`;
            let cat_name = kebab_to_title(cat.replace(/s$/, ""));
            for ( let [obj, sub_schema] of Object.entries(sub_schemas) )
            {
                let obj_docs = cat_docs;
                let obj_name = cat_name;
                if ( sub_schema.type && obj != "base-gradient" )
                {
                    obj_docs += "#" + obj;
                    obj_name = sub_schema.title || kebab_to_title(obj);
                }
                patch_docs_links(sub_schema, obj_docs, obj_name, obj_name);

                let id = `#/$defs/${cat}/${obj}`;
                prop_map.extract_all_properties(sub_schema, id, prop_map.create(id, sub_schema), false);
            }
        }
        let schema_id = this.schema["$id"];
        this._patch_ty_schema(schema_id, "layers", "all-layers");
        this._patch_ty_schema(schema_id, "shapes", "all-graphic-elements");
        for ( let [pname, pschema] of Object.entries(this.defs.properties) )
        {
            if ( pname.endsWith("-property") )
                this._patch_property_schema(pschema, schema_id + "#/$defs/properties/" + pname);
        }
        this.defs.properties["base-keyframe"].keyframe = true;

        for ( let enum_schema of Object.values(this.defs.constants) )
            patch_schema_enum(enum_schema);

        this.defs.assets["all-assets"] = {
            "type": "object",
            "asset_oneof": schema_id,
        };

        for ( let layer_type of ["image-layer", "precomposition-layer"])
        {
            let layer_schema = this.defs.layers[layer_type];
            layer_schema.allOf[1].properties.refId.reference_asset = true;
        }

        prop_map.finalize();

        this.validator = new AjvClass({
            allErrors: true,
            verbose: true,
            // inlineRefs: false,
            // strict: false,
            keywords: [
                {keyword: ["_docs", "_name", "_docs_name", "$version"]},
                {
                    keyword: "ty_oneof",
                    validate: custom_discriminator("ty", false),
                },
                {
                    keyword: "prop_oneof",
                    validate: custom_discriminator("a", true),
                },
                {
                    keyword: "asset_oneof",
                    validate: function validate_asset(schema, data, parent_schema, data_cxt)
                    {
                        validate_asset.errors = [];

                        if ( typeof data != "object" || data === null )
                            return true;

                        var target_schema;

                        if ( "layers" in data )
                            target_schema = this.getSchema(schema + "#/$defs/assets/precomposition");
                        else
                            target_schema = this.getSchema(schema + "#/$defs/assets/image");

                        if ( !target_schema(data, data_cxt) )
                        {
                            validate_asset.errors = target_schema.errors;
                            return false;
                        }
                        return true;
                    },
                },
                {
                    keyword: "splitpos_oneof",
                    validate: custom_discriminator("s", false, false),
                },
                {
                    keyword: "keyframe",
                    validate: function validate_keyframe(schema, data, parent_schema, data_cxt)
                    {
                        validate_keyframe.errors = [];

                        var require_io = true;
                        if ( data.h )
                            require_io = false;

                        var index = data_cxt.parentData.indexOf(data);
                        if ( index == data_cxt.parentData.length - 1 )
                            require_io = false;

                        if ( require_io )
                        {
                            for ( var prop of "io" )
                            {
                                if ( !("i" in data) )
                                {
                                    validate_keyframe.errors.push({
                                        message: `must have required property 'i'`,
                                        type: "error",
                                        instancePath: data_cxt.instancePath,
                                        parentSchema: parent_schema,
                                    });
                                }
                            }
                        }

                        if ( index > 0 )
                        {
                            var prev_kf = data_cxt.parentData[index-1];
                            if ( keyframe_has_t(prev_kf) && typeof data.t == "number" )
                            {
                                if ( data.t < prev_kf.t )
                                {
                                    validate_keyframe.errors.push({
                                        message: `keyframe 't' must be in ascending order`,
                                        type: "error",
                                        instancePath: data_cxt.instancePath,
                                        parentSchema: parent_schema,
                                    });
                                }
                                else if ( data.t == prev_kf.t && index > 1 )
                                {
                                    var prev_prev = data_cxt.parentData[index-2];
                                    if ( keyframe_has_t(prev_prev) && data.t == prev_prev.t )
                                    {
                                        validate_keyframe.errors.push({
                                            message: `there can be at most 2 keyframes with the same 't' value`,
                                            type: "error",
                                            instancePath: data_cxt.instancePath,
                                            parentSchema: parent_schema,
                                        });
                                    }
                                }
                            }
                        }

                        return validate_keyframe.errors.length == 0;
                    }
                },
                {
                    keyword: "enum_oneof",
                    validate: function validate_enum(schema, data, parent_schema, data_cxt)
                    {
                        validate_enum.errors = [];
                        for ( let value of schema )
                            if ( value.const === data )
                                return true;

                        validate_enum.errors.push({
                            message: `${data} is not a valid enumeration value`,
                            type: "error",
                            instancePath: data_cxt.instancePath,
                            parentSchema: parent_schema,
                        });
                        return false;
                    },
                },
                {
                    keyword: "reference_asset",
                    validate: function validate_asset_reference(schema, data, parent_schema, data_ctx)
                    {
                        validate_asset_reference.errors = [];

                        if ( Array.isArray(data_ctx.rootData.assets) )
                        {
                            for ( let asset of data_ctx.rootData.assets )
                            {
                                if ( asset.id === data )
                                {
                                    // TODO: Validate asset type?
                                    return true;
                                }
                            }
                        }

                        validate_asset_reference.errors.push({
                            message: `${JSON.stringify(data)} is not a valid asset id`,
                            type: "error",
                            instancePath: data_ctx.instancePath,
                            parentSchema: parent_schema,
                        });
                        return false;
                    },
                },
                {
                    keyword: "warn_extra_props",
                    validate: function warn_extra_props(schema, data, parent_schema, data_cxt)
                    {
                        warn_extra_props.errors = [];

                        if ( typeof data != "object" || data === null )
                            return true;

                        for ( let prop of Object.keys(data) )
                        {
                            if ( !schema.has(prop) )
                            {
                                warn_extra_props.errors.push({
                                    message: `has unknown property '${prop}'`,
                                    type: "warning",
                                    warning: "property",
                                    instancePath: data_cxt.instancePath,
                                    parentSchema: parent_schema,
                                });
                            }
                        }

                        return warn_extra_props.errors.length == 0;
                    },
                },
            ],
            schemas: [this.schema]
        });
        this._validate_internal = this.validator.getSchema(schema_id);

    }

    _patch_ty_schema(id_base, category, all)
    {

        let found = {};
        for ( let [name, sub_schema] of Object.entries(this.defs[category]) )
        {
            let ty = extract_schema_ty(sub_schema);
            if ( ty !== undefined )
            {
                let id = `${id_base}#/$defs/${category}/${name}`;
                found[ty] = {
                    id: id
                };
            }
        }
        this.defs[category][all].ty_oneof = found;
        delete this.defs[category][all].oneOf;

        return found;
    }

    _patch_property_schema(schema, id)
    {
        if ( id.endsWith("gradient-property") )
        {
            return this._patch_property_schema(schema.properties.k, id + "/properties/k");
        }


        if ( id.endsWith("splittable-position-property") )
        {
            delete schema.oneOf;
            schema.splitpos_oneof = {
                [true]: {id: this.schema["$id"] + "#/$defs/properties/split-position"},
                [false]: {id: this.schema["$id"] + "#/$defs/properties/position-property"},
            };

            return;
        }

        schema.prop_oneof = [];
        for ( let opt of schema.oneOf )
        {
            schema.prop_oneof.push({
                schema: {
                    type: "object",
                    ...opt
                },
                id: id + "/prop_oneof/" + schema.prop_oneof.length + "/schema",
            });
        }
        delete schema.oneOf;
    }

    validate(string)
    {
        var data;
        try {
            data = JSON.parse(string);
        } catch(e) {
            return [
                {
                    type: "error",
                    message: "Document is not a valid JSON file",
                },
                {
                    type: "error",
                    message: e.message,
                }
            ];
        }

        let errors = [];
        if ( !this._validate_internal(data) )
            errors = this._validate_internal.errors
                .map(e => this._cleaned_error(e, data));

        return errors.sort((a, b) => {
            if ( a.path < b.path )
                return -1;
            if ( a.path > b.path )
                return 1;
            return 0;
        });
    }

    _cleaned_error(error, data, prefix="")
    {
        const path_parts = error.instancePath.split('/');

        const path_names = [];
        for (const path_part of path_parts)
        {
            if (path_part === '#' || path_part === '')
                continue;
      
            data = data[path_part];
        
            if (!data)
                break;
      
            // Every layer with a type may be named
            // Push a null value if it doesn't exist so display code can handle
            if (data.ty)
                path_names.push(data.nm);
        }

        return {
            type: error.type ?? "error",
            warning: error.warning,
            message: (error.parentSchema?._name ?? "Value") + " " + error.message,
            path: prefix + (error.instancePath ?? ""),
            name: error.parentSchema?._docs_name ?? "Value",
            docs: error.parentSchema?._docs,
            path_names,
        };
    }
}


if ( typeof module !== "undefined" )
    module.exports = {Validator: Validator};
