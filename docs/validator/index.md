full_page: 1
disable_toc: 1

# Lottie Validator

<script src="https://cdnjs.cloudflare.com/ajax/libs/ajv/8.16.0/ajv2020.min.js" integrity="sha512-OunSQfwE+NRzXE6jEJfFCyVkFQgMOk+oxD34iU8Xc21cUYfFH5TKBc7Z3RqKC4EW1tlllWIIOdq2Kf5F/5wKOw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="/lottie-spec/static/js/validator.js"></script>

<style>
.hidden {
    display: none !important;
}
textarea {
    display: block;
    width: 100%;
    min-height: 500px;
}
#error-out td:first-child {
    font-family: monospace;
}

</style>

<div id="system-loading">
    Loading the JSON schema...
</div>
<div id="system-error" class="hidden">
    Could not load the JSON schema.
</div>
<div id="validator-container" class="hidden">
    <textarea id="input-text">{"-ip": 0, "op": 10, "w": 10, "h": 10, "fr": 60, "layers": [{
"ty": 4,  "ip": 0, "op": 10, "-st": 1, "ks": {"a": {"a":0, "k": "a"}}, "shapes": [
{"ty": "el"},
{"ty": "??"}
]
}, {"ty": 123}

]}</textarea>
    <button onclick="validate_string(document.getElementById('input-text').value)">Validate</button>
</div>
<table id="error-out" class="hidden">
    <thead>
        <tr>
            <th>Path</th>
            <th>Severity</th>
            <th>Message</th>
            <th>Docs</th>
        </tr>
    </thead>
    <tbody></tbody>
</table>

<script>

function show_element(element)
{
    element.classList.remove("hidden")
}

function hide_element(element)
{
    element.classList.add("hidden")
}

function on_load_error(err)
{
    hide_element(document.getElementById("system-loading"));
    show_element(document.getElementById("system-error"));
    console.error(err);
}

function on_load_ok(schema_obj)
{
    validator = new Validator(ajv2020.Ajv2020, schema_obj);
    hide_element(document.getElementById("system-loading"));
    show_element(document.getElementById("validator-container"));

    // TODO remove
    validate_string(document.getElementById('input-text').value);
}

function validate_string(value)
{
    var errors = validator.validate(value);

    var container = document.getElementById("error-out");
    container.classList.remove("table-striped");
    if ( errors.length == 0 )
    {
        hide_element(container);
        return;
    }

    show_element(container);
    var body = container.querySelector("tbody");
    body.innerHTML = "";
    for ( let error of errors )
    {
        let tr = body.appendChild(document.createElement("tr"));
        tr.classList.add(error.type == "error" ? "danger" : error.type);
        tr.appendChild(document.createElement("td")).appendChild(document.createTextNode(error.path));
        tr.appendChild(document.createElement("td")).appendChild(document.createTextNode(error.type));
        tr.appendChild(document.createElement("td")).appendChild(document.createTextNode(error.name + " " + error.message));
        let td = tr.appendChild(document.createElement("td"));
        if ( error.docs )
        {
            let link = td.appendChild(document.createElement("a"));
            link.setAttribute("href", error.docs);
            link.appendChild(document.createTextNode(error.docs_name));
        }
    }
}


var validator;

fetch("/lottie-spec/lottie.schema.json").then(response => {
    if ( !response.ok )
        throw new Error("Request failed");
    return response.json();
}).then(json => on_load_ok(json)).catch(e => on_load_error(e));

</script>
