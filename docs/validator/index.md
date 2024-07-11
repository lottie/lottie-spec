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
.tabs {
    display: flex;
    gap: 5px;
    padding: 0;
    margin: 0;
    list-style: none;
}
.tabs li {
    display: flex;
}
.tabs a {
    border-radius: 5px 5px 0 0;
    padding: 10px;
    text-decoration: none !important;
    background-color: #ccc;
}
.tabs a:not(.active) {
    cursor: pointer;
}
.tabs a.active, .tab-content {
    background-color: #eee;
}
.tab-content {
    padding: 1em;
}
.tab-content input {
    width: 100%;
}

.validate-button {
    margin: 1em auto 0;
    display: block;
}

#tab-content-upload {
    border: 1px solid black;
    margin: 20px auto;
    padding: 60px;
    box-sizing: border-box;
    text-align: center;
    border-radius: 5px;
    position: relative;
    background: #fff;
}

#tab-content-upload input {
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0;
    left: 0px;
    top: 0px;
    cursor: pointer;
}

</style>

<div id="system-loading">
    Loading the JSON schema...
</div>
<div id="system-error" class="hidden">
    Could not load the JSON schema.
</div>
<div id="validator-container" class="hidden">
    <ul class="tabs">
        <li>
            <a class="active" id="tab-head-url" onclick="tab_click(this)">Validate by URL</a>
        </li>
        <li>
            <a id="tab-head-upload" onclick="tab_click(this)">Validate by File Upload</a>
        </li>
        <li>
            <a id="tab-head-text" onclick="tab_click(this)">Validate by Direct Input</a>
        </li>
    </ul>
    <div class="tab-content">
        <div id="tab-content">
            <div id="tab-content-url">
                <input id="input-url" type="url" placeholder="Lottie URL" />
                <button class="validate-button" onclick="validate_string(document.getElementById('input-text').value)">Validate</button>
            </div>
            <div id="tab-content-upload" class="hidden">
                <p>Drop a JSON file or click to browse</p>
                <input id="input-file" type="file" accept="application/json" onchange="on_file_input(event)" />
            </div>
            <div id="tab-content-text" class="hidden">
                    <textarea id="input-text"></textarea>
                <button class="validate-button" onclick="validate_string(document.getElementById('input-text').value)">Validate</button>
            </div>
        </div>
    </div>
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
}

function show_errors(errors)
{
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
        tr.appendChild(document.createElement("td")).appendChild(document.createTextNode(error.message));
        let td = tr.appendChild(document.createElement("td"));
        if ( error.docs )
        {
            let link = td.appendChild(document.createElement("a"));
            link.setAttribute("href", error.docs);
            link.appendChild(document.createTextNode(error.name));
        }
    }
}

function validate_string(value)
{
    show_errors(validator.validate(value));
}

function on_file_input(ev)
{
    const files = ev.target.files;
    if ( files.length > 0 )
    {
        show_errors([]);
        validate_file(files[0]);
    }
    else
    {
        show_errors([{
            "type": "error",
            "message": "No file selected"
        }]);
    }
}

function validate_file(file)
{
    const reader = new FileReader();
    reader.onload = function (e) {
        validate_string(e.target.result);
    };
    reader.onerror = e => show_errors([{
        "type": "error",
        "message": "Could not load file"
    }])
    reader.readAsText(file);
}

function validate_url(url)
{
    fetch(url).then(r => r.text()).then(validate_string).catch(e => show_errors([{
        type: "error",
        message: "Failed to load from URL",
    }]));
}

function initialize()
{
    fetch("/lottie-spec/lottie.schema.json").then(response => {
        if ( !response.ok )
            throw new Error("Request failed");
        return response.json();
    }).then(json => on_load_ok(json)).catch(e => on_load_error(e));
}

function tab_click(tab)
{
    let id = tab.id.replace("head", "content");
    document.querySelectorAll("#tab-content > div").forEach(element => {
        if ( element.id == id )
            show_element(element);
        else
            hide_element(element);
    });
    document.querySelectorAll(".tabs a").forEach(element => {
        if ( element !== tab )
            element.classList.remove("active");
        else
            element.classList.add("active");
    })
}


var validator;
initialize();

</script>
