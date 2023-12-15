import re
import json
import inspect
import dataclasses
from typing import Any
from pathlib import Path
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor
from markdown.util import HTML_PLACEHOLDER_RE, AtomicString

from schema_tools.schema import Schema


docs_path = Path(__file__).parent.parent / "docs"


class ReferenceLink:
    _link_mapping = None

    def __init__(self, page, anchor, name, group=None, cls=None):
        self.group = group
        self.cls = cls
        self.name = name
        self.page = page or group
        self.anchor = anchor or cls

    def url(self):
        return "/lottie-spec/specs/%s#%s" % (self.page, self.anchor)

    def to_element(self, parent, links):
        type_text = etree.SubElement(parent, "a")
        type_text.attrib["href"] = self.url()
        type_text.text = self.name
        type_text.tail = " "
        if self.cls == "int-boolean":
            type_text.text = "0-1 "
            etree.SubElement(type_text, "code").text = "integer"
        elif self.anchor == "properties" and len(links) == 1:
            type_text.text = "Animated"
            type_text.tail = " "
            if self.cls == "value":
                type_text = etree.SubElement(parent, "code").text = "number"
            else:
                type_text.tail += self.name.split(" ", 1)[1]

        return type_text


def ref_links(ref: str, data: Schema):
    ref = re.sub("all-([-a-z]+)s", "\\1", ref)
    chunks = ref.strip("#/").split("/")
    if len(chunks) > 0 and chunks[0] == "$defs":
        chunks.pop(0)
    else:
        ref = "#/$defs/" + ref

    if len(chunks) != 2:
        return []

    group = chunks[0]
    cls = chunks[1]

    values = {
        "extra": None,
        "page": group,
        "anchor": cls,
        "name": data.get_ref(ref).get("title", cls) if data else cls,
        "name_prefix": "",
    }

    links = []
    if values["page"]:
        links.append(ReferenceLink(
            values["page"], values["anchor"], values["name_prefix"] + values["name"], group, cls
        ))

    if values["extra"]:
        extra = values["extra"]
        links.append(ReferenceLink(
            extra["page"], extra["anchor"], extra["name"],
        ))

    return links


class SchemaString(InlineProcessor):
    def __init__(self, md, schema_data: Schema):
        super().__init__(r'\{schema_string:(?P<path>[^}]+)/(?P<attribute>[^}]+)\}', md)
        self.schema_data = schema_data

    def handleMatch(self, match, data):
        span = etree.Element("span")
        span.text = self.schema_data.get_ref("$defs/" + match.group("path")).get(match.group("attribute"), "")
        return span, match.start(0), match.end(0)


class SchemaLink(InlineProcessor):
    def __init__(self, md):
        pattern = r'{schema_link:([^:}]+)}'
        super().__init__(pattern, md)

    @staticmethod
    def element(path):
        href = "schema.md#/$defs/" + path
        element = etree.Element("a", {"href": href, "class": "schema-link"})
        element.text = "View Schema"
        return element

    @staticmethod
    def icon(path):
        href = "schema.md#/$defs/" + path
        element = etree.Element("a", {"href": href, "class": "schema-link"})
        element.attrib["title"] = "View Schema"
        element.append(etree_fontawesome("file-code"))
        return element

    @staticmethod
    def caniuse_icon(feature):
        href = "https://canilottie.com/" + feature
        element = etree.Element("a", {"href": href, "class": "schema-link"})
        element.attrib["title"] = "View Compatibility"
        element.append(etree_fontawesome("list-check"))
        return element

    def handleMatch(self, m, data):
        return SchemaLink.element(m.group(1)), m.start(0), m.end(0)


class JsonHtmlSerializer:
    def __init__(self, parent, md, json_data):
        self.parent = parent
        self.tail = None
        self.encoder = json.JSONEncoder()
        self.parent.text = ""
        self.md = md
        self.schema = Schema(json_data)

    def encode(self, json_object, indent, id=None):
        if isinstance(json_object, dict):
            self.encode_dict(json_object, indent, id)
        elif isinstance(json_object, list):
            self.encode_list(json_object, indent)
        elif isinstance(json_object, str):
            self.encode_item(json_object, "string", json_object if json_object.startswith("https://") else None)
        elif isinstance(json_object, (int, float)):
            self.encode_item(json_object, "number")
        elif isinstance(json_object, bool) or json_object is None:
            self.encode_item(json_object, "literal")
        else:
            raise TypeError(json_object)

    def encode_item(self, json_object, hljs_type, href=None):
        span = etree.Element("span", {"class": "hljs-"+hljs_type})
        span.text = self.encoder.encode(json_object)

        if href:
            link = etree.SubElement(self.parent, "a", {"href": href})
            link.append(span)
            self.tail = link
        else:
            self.tail = span
            self.parent.append(span)

        self.tail.tail = ""

    def encode_dict_key(self, key, id):
        if id is None:
            self.encode_item(key, "attr")
            return None

        child_id = id + "/" + key
        self.encode_item(key, "attr", "#" + child_id)
        self.tail.attrib["id"] = child_id
        if child_id.count("/") == 3:
            for link in ref_links(child_id, self.schema):
                self.tail.tail += " "
                self.tail = etree.SubElement(self.parent, "a")
                self.tail.attrib["href"] = link.url()
                self.tail.attrib["title"] = link.name
                self.tail.append(etree_fontawesome("book-open"))
                self.tail.tail = " "
        return child_id

    def encode_dict(self, json_object, indent, id):
        if len(json_object) == 0:
            self.write("{}")
            return

        self.write("{\n")

        child_indent = indent + 1
        for index, (key, value) in enumerate(json_object.items()):

            self.indent(child_indent)
            child_id = self.encode_dict_key(key, id if isinstance(value, dict) else None)
            self.write(": ")

            if key == "$ref" and isinstance(value, str):
                self.encode_item(value, "string", value)
            else:
                self.encode(value, child_indent, child_id)

            if index == len(json_object) - 1:
                self.write("\n")
            else:
                self.write(",\n")
        self.indent(indent)
        self.write("}")

    def encode_list(self, json_object, indent):
        if len(json_object) == 0:
            self.write("[]")
            return

        self.write("[\n")
        child_indent = indent + 1
        for index, value in enumerate(json_object):
            self.indent(child_indent)
            self.encode(value, child_indent)
            if index == len(json_object) - 1:
                self.write("\n")
            else:
                self.write(",\n")
        self.indent(indent)
        self.write("]")

    def indent(self, amount):
        self.write("    " * amount)

    def write(self, text):
        if self.tail is None:
            self.parent.text += text
        else:
            self.tail.tail += text


class JsonFile(InlineProcessor):
    def __init__(self, md):
        super().__init__(r'\{json_file:(?P<path>[^:]+)\}', md)

    def handleMatch(self, match, data):
        pre = etree.Element("pre")

        with open(docs_path / match.group("path")) as file:
            json_data = json.load(file)

        # Hack to prevent PrettifyTreeprocessor from messing up indentation
        etree.SubElement(pre, "span")

        code = etree.SubElement(pre, "code")

        JsonHtmlSerializer(code, self.md, json_data).encode(json_data, 0, "")

        return pre, match.start(0), match.end(0)


@dataclasses.dataclass
class SchemaProperty:
    description: str = ""
    const: Any = None
    type: str = ""
    item_type: str = ""
    title: str = ""


class SchemaObject(BlockProcessor):
    re_fence_start = re.compile(r'^\s*\{schema_object:([^}]+)\}\s*(?:\n|$)')
    re_row = re.compile(r'^\s*(\w+)\s*:\s*(.*)')
    prop_fields = {f.name for f in dataclasses.fields(SchemaProperty)}

    def __init__(self, parser, schema_data: Schema):
        super().__init__(parser)
        self.schema_data = schema_data

    def test(self, parent, block):
        return self.re_fence_start.match(block)

    def _type(self, prop):
        if "$ref" in prop and "type" not in prop:
            return prop["$ref"]
        if "type" in prop:
            type = prop["type"]
            if type == "array" and prop.get("items", {}).get("type", "") == "number":
                return "Vector"
            return type
        if "oneOf" in prop:
            return [self._type(t) for t in prop["oneOf"]]
        return ""

    def _add_properties(self, schema_props, prop_dict):
        for name, prop in schema_props.items():
            data = dict((k, v) for k, v in prop.items() if k in self.prop_fields)
            data["type"] = self._type(prop)
            if "title" in prop:
                data["title"] = prop["title"]
                if "description" not in prop:
                    data["description"] = prop["title"]
            if "items" in prop:
                data["item_type"] = self._type(prop["items"])

            prop_dict[name] = SchemaProperty(**data)

    def _conditional_properties(self, object, prop_dict, base_list):
        if "if" in object:
            self._object_properties(object["then"], prop_dict, base_list)
            if "else" in object:
                self._object_properties(object["else"], prop_dict, base_list)

    def _object_properties(self, object, prop_dict, base_list):
        if "properties" in object:
            self._add_properties(object["properties"], prop_dict)

        if "allOf" in object:
            for chunk in object["allOf"]:
                if "properties" in chunk:
                    self._add_properties(chunk["properties"], prop_dict)
                elif "$ref" in chunk:
                    base_list.append(chunk["$ref"])
                self._conditional_properties(chunk, prop_dict, base_list)

        self._conditional_properties(object, prop_dict, base_list)

    def _base_link(self, parent, ref):
        link = ref_links(ref, self.schema_data)[0]
        a = etree.SubElement(parent, "a")
        a.text = link.name
        a.attrib["href"] = "%s.md#%s" % (link.page, link.anchor)
        return a

    def _base_type(self, type, parent):
        if isinstance(type, list):
            type_text = etree.SubElement(parent, "span")
            for t in type:
                type_child = self._base_type(t, type_text)
                type_child.tail = " or "
            type_child.tail = ""
        elif type.startswith("#/$defs/"):
            links = ref_links(type, self.schema_data)
            for link in links:
                type_text = link.to_element(parent, links)
        else:
            type_text = etree.SubElement(parent, "code")
            type_text.text = type

        return type_text

    def run(self, parent, blocks):
        object_name = self.test(parent, blocks[0]).group(1)

        schema_data = self.schema_data.get_ref("$defs/" + object_name)

        prop_dict = {}
        base_list = []
        order = []
        self._object_properties(schema_data, prop_dict, base_list)

        # Override descriptions if specified from markdown
        rows = blocks.pop(0)
        for row in rows.split("\n")[1:]:
            match = self.re_row.match(row)
            if match:
                name = match.group(1)
                if name == "EXPAND":
                    prop_dict_base = {}
                    base = match.group(2)
                    self._object_properties(self.schema_data.get_ref(base), prop_dict_base, [])
                    try:
                        base_list.remove(base)
                    except ValueError:
                        pass
                    order += list(prop_dict_base.keys())
                    prop_dict_base.update(prop_dict)
                    prop_dict = prop_dict_base
                elif name == "SKIP":
                    what = match.group(2)
                    prop_dict.pop(what, None)
                    try:
                        base_list.remove(what)
                    except ValueError:
                        pass
                else:
                    if match.group(2):
                        if name not in prop_dict:
                            raise Exception("Property %s not in %s" % (name, schema_data.path))
                        prop_dict[name].description = match.group(2)
                    order.append(name)

        div = etree.SubElement(parent, "div")

        has_own_props = len(prop_dict)

        if len(base_list):
            p = etree.SubElement(div, "p")
            if not has_own_props:
                p.text = "Has the attributes from"
            else:
                p.text = "Also has the attributes from"

            if len(base_list) == 1:
                p.text += " "
                self._base_link(p, base_list[0]).tail = "."
            else:
                p.text += ":"
                ul = etree.SubElement(p, "ul")
                for base in base_list:
                    self._base_link(etree.SubElement(ul, "li"), base)

        if has_own_props:
            table = etree.SubElement(div, "table")
            thead = etree.SubElement(etree.SubElement(table, "thead"), "tr")
            etree.SubElement(thead, "th").text = "Attribute"
            etree.SubElement(thead, "th").text = "Type"
            etree.SubElement(thead, "th").text = "Title"
            desc = etree.SubElement(thead, "th")
            desc.text = "Description "
            desc.append(SchemaLink.icon(object_name))
            if "caniuse" in schema_data:
                desc.append(SchemaLink.caniuse_icon(schema_data["caniuse"]))

            tbody = etree.SubElement(table, "tbody")

            for name in order:
                if name in prop_dict:
                    self.prop_row(name, prop_dict.pop(name), tbody)

            for name, prop in prop_dict.items():
                self.prop_row(name, prop, tbody)

        return True

    def prop_row(self, name, prop, tbody):
        tr = etree.SubElement(tbody, "tr")
        etree.SubElement(etree.SubElement(tr, "td"), "code").text = name

        type_cell = etree.SubElement(tr, "td")

        type_text = self._base_type(prop.type, type_cell)
        if prop.type == "array" and prop.item_type:
            type_text.tail = " of "
            type_text = self._base_type(prop.item_type, type_cell)

        if prop.const is not None:
            type_text.tail = " = "
            etree.SubElement(type_cell, "code").text = repr(prop.const)

        description = etree.SubElement(tr, "td")
        self.parser.parseBlocks(description, [prop.title])

        description = etree.SubElement(tr, "td")
        self.parser.parseBlocks(description, [prop.description])


def enum_values(schema: Schema, name):
    enum = schema.get_ref(["$defs", "constants", name])
    data = []
    for item in enum["oneOf"]:
        data.append((item["const"], item["title"], item.get("description", "")))
    return data


class SchemaEnum(BlockProcessor):
    re_fence_start = re.compile(r'^\s*\{schema_enum:([^}]+)\}\s*(?:\n|$)')
    re_row = re.compile(r'^\s*(\w+)\s*:\s*(.*)')

    def __init__(self, parser, schema_data: Schema):
        super().__init__(parser)
        self.schema_data = schema_data

    def test(self, parent, block):
        return self.re_fence_start.match(block)

    def run(self, parent, blocks):
        enum_name = self.test(parent, blocks[0]).group(1)

        enum_data = enum_values(self.schema_data, enum_name)

        table = etree.SubElement(parent, "table")
        descriptions = {}

        for value, name, description in enum_data:
            if description:
                descriptions[str(value)] = description

        # Override descriptions if specified from markdown
        rows = blocks.pop(0)
        for row in rows.split("\n")[1:]:
            match = self.re_row.match(row)
            if match:
                descriptions[match.group(0)] = match.group(1)

        thead = etree.SubElement(etree.SubElement(table, "thead"), "tr")
        etree.SubElement(thead, "th").text = "Value"
        etree.SubElement(thead, "th").text = "Name "
        if descriptions:
            etree.SubElement(thead, "th").text = "Description "

        thead[-1].append(SchemaLink.icon("constants/" + enum_name))

        tbody = etree.SubElement(table, "tbody")

        for value, name, _ in enum_data:
            tr = etree.SubElement(tbody, "tr")
            etree.SubElement(etree.SubElement(tr, "td"), "code").text = repr(value)
            etree.SubElement(tr, "td").text = name
            if descriptions:
                etree.SubElement(tr, "td").text = descriptions.get(str(value), "")

        return True


def find_property(object_schema: Schema, property: str, root_schema: Schema|None = None) -> Schema|None:
    if "properties" in object_schema:
        props = object_schema / "properties"
        if property in props:
            return props[property]

    for switch in ["allOf", "oneOf", "anyOf"]:
        if switch in object_schema:
            for val in reversed(list(object_schema / switch)):
                found = find_property(val, property, root_schema)
                if found is not None:
                    return found

    if "$ref" in object_schema and root_schema:
        return find_property(root_schema.get_ref(object_schema.get("$ref")), property, root_schema)


class SubTypeTable(InlineProcessor):
    def __init__(self, md, schema_data: Schema):
        super().__init__(r'\{schema_subtype_table:(?P<path>[^:}]+):(?P<attribute>[^:}]+)\}', md)
        self.schema_data = schema_data

    def handleMatch(self, match, data):
        table = etree.Element("table")
        tr = etree.SubElement(etree.SubElement(table, "thead"), "tr")
        attribute = match.group("attribute") or "ty"
        etree.SubElement(etree.SubElement(tr, "th"), "code").text = attribute
        etree.SubElement(tr, "th").text = "Type"

        tbody = etree.SubElement(table, "tbody")

        schema_obj = self.schema_data.get_ref("$defs/" + match.group("path"))
        schema_types = schema_obj.get_ref("oneOf")

        for row in schema_types:
            ref = row.get("$ref")
            row = self.schema_data.get_ref(ref)

            tr = etree.SubElement(tbody, "tr")
            prop_schema = find_property(row, attribute, self.schema_data)
            etree.SubElement(etree.SubElement(tr, "td"), "code").text = str(prop_schema.get("const"))

            td = etree.SubElement(tr, "td")
            links = ref_links(ref, self.schema_data)
            for link in links:
                link.to_element(td, links)

        return table, match.start(0), match.end(0)


class RawHTML(BlockProcessor):
    """
    Needlessly complex workaround to allow HTML-style headings `<h1>foo</h1>`
    to show up in the table of contents
    """
    headers = ["h%s" % h for h in range(1, 7)]

    def __init__(self, parser, schema_data: Schema, extra_elements):
        super().__init__(parser)
        self.schema_data = schema_data
        self.tag_names = set(self.headers + extra_elements)

    def test(self, parent: etree.Element, block):
        return HTML_PLACEHOLDER_RE.match(block)

    def run(self, parent: etree.Element, blocks):
        match = HTML_PLACEHOLDER_RE.match(blocks[0])
        index = int(match.group(1))
        raw_string = self.parser.md.htmlStash.rawHtmlBlocks[index]
        if not raw_string:
            return False
        element = etree.fromstring(raw_string)

        if element.tag not in self.tag_names:
            return False

        self.parser.md.htmlStash.rawHtmlBlocks.pop(index)
        self.parser.md.htmlStash.rawHtmlBlocks.insert(index, '')

        parent.append(element)
        return True


def etree_fontawesome(icon, group="fas"):
    el = etree.Element("i")
    el.attrib["class"] = "%s fa-%s" % (group, icon)
    return el


class LottieRenderer:
    _id = 0

    @staticmethod
    def get_id():
        id = LottieRenderer._id
        LottieRenderer._id += 1
        return id

    def __init__(self, *, parent: etree.Element = None, download_file=None,
                 width=None, height=None, buttons=True, button_parent=None, background=None):
        self.id = LottieRenderer.get_id()

        element = etree.Element("div")

        if parent is not None:
            parent.append(element)

        self.animation_container = etree.SubElement(element, "div")
        self.animation_container.attrib["class"] = "animation-container"
        if not background:
            self.animation_container.attrib["class"] += " animation-container-alpha"
        else:
            self.animation_container.attrib["style"] = "background: %s" % background

        self.animation = etree.SubElement(self.animation_container, "div")
        self.animation.attrib["id"] = "lottie_target_%s" % self.id

        self.width = width
        self.height = height

        if width:
            self.animation.attrib["style"] = "width:%spx;height:%spx" % (width, height)

        if buttons:
            self.button_container = etree.SubElement(button_parent or element, "div")

            self.add_button(
                id="lottie_play_{id}".format(id=self.id),
                onclick=(
                    "lottie_player_{id}.play(); " +
                    "document.getElementById('lottie_pause_{id}').style.display = 'inline-block'; " +
                    "this.style.display = 'none'"
                ).format(id=self.id),
                icon="play",
                title="Play",
                style="display:none"
            )

            self.add_button(
                id="lottie_pause_{id}".format(id=self.id),
                onclick=(
                    "lottie_player_{id}.pause(); " +
                    "document.getElementById('lottie_play_{id}').style.display = 'inline-block'; " +
                    "this.style.display = 'none'"
                ).format(id=self.id),
                icon="pause",
                title="Pause"
            )

            if download_file:
                download = etree.Element("a")
                self.button_container.append(download)
                download.attrib["href"] = download_file
                # download.attrib["download"] = ""
                download.attrib["title"] = "Download"
                download_button = etree.Element("button")
                download.append(download_button)
                download_button.append(etree_fontawesome("download"))

        self.element = element
        self.variable_name = "lottie_player_{id}".format(id=self.id)
        self.target_id = "lottie_target_{id}".format(id=self.id)

    def populate_script(self, script_src):
        script = etree.Element("script")
        self.element.append(script)
        script.text = AtomicString(script_src)

    @staticmethod
    def render(
        *, parent: etree.Element = None, url=None, json_data=None, download_file=None,
        width=None, height=None, extra_options="{}", buttons=True, background=None
    ):
        obj = LottieRenderer(parent=parent, download_file=download_file, width=width, height=height, buttons=buttons, background=background)
        if json_data is None:
            script_src = """
                var lottie_player_{id} = new LottiePlayer(
                    'lottie_target_{id}',
                    '{file}',
                    true,
                    {extra_options}
                );
            """.format(id=obj.id, file=url, extra_options=extra_options)
        else:
            script_src = """
                var lottie_player_{id} = new LottiePlayer(
                    'lottie_target_{id}',
                    {json_data},
                    true,
                    {extra_options}
                );
            """.format(id=obj.id, json_data=json.dumps(json_data), extra_options=extra_options)

        obj.populate_script(script_src)
        return (obj.element, obj.id)

    def add_button(self, *, text=None, icon=None, **attrib):
        button = etree.SubElement(self.button_container, "button")
        button.attrib = attrib
        if icon:
            icon_element = etree_fontawesome(icon)
            if text:
                icon_element.tail = text
            button.append(icon_element)
        elif text:
            button.text = text

        return button


def get_url(md, path):
    # Mkdocs adds a tree processor to adjust urls, but it won't work with lottie js so we do the same here
    processor = next(proc for proc in md.treeprocessors if proc.__class__.__module__ == 'mkdocs.structure.pages')
    page = processor.files.get_file_from_path(path)
    if not page:
        raise Exception("Page not found at %s" % path)
    return page.url_relative_to(processor.file)


class LottieBlock(BlockProcessor):
    def __init__(self, md):
        self.md = md
        super().__init__(md.parser)

    def test(self, parent, block):
        return block.startswith("<lottie")

    def run(self, parent, blocks):
        raw_string = blocks.pop(0)
        md_element = etree.fromstring(raw_string)
        filename = md_element.attrib.pop("src")
        lottie_url = get_url(self.md, filename)
        width = md_element.attrib.pop("width", None)
        height = md_element.attrib.pop("height", None)
        buttons = md_element.attrib.pop("buttons", "true") == "true"
        background = md_element.attrib.pop("background", None)
        element = LottieRenderer.render(
            url=lottie_url,
            download_file=lottie_url,
            width=width,
            height=height,
            extra_options=json.dumps(md_element.attrib),
            buttons=buttons,
            background=background,
        )[0]

        parent.append(element)

        return True


class LottiePlaygroundBuilder:
    def __init__(self, parent, schema_data, width, height, buttons):
        self.parent = parent
        self.schema_data = schema_data

        self.element = etree.SubElement(parent, "div")
        self.element.attrib["class"] = "playground"

        self.renderer = LottieRenderer(
            parent=self.element, width=width, height=height,
            buttons=buttons, button_parent=self.element
        )
        self.player_container = self.renderer.element
        self.player_container.attrib["class"] = "animation-json"

        self.controls_container = etree.Element("table", {"class": "table-plain", "style": "width: 100%"})
        self.element.insert(0, self.controls_container)

        self.control_id_counter = 0

    @property
    def anim_id(self):
        return self.renderer.id

    @property
    def add_button(self):
        return self.renderer.add_button

    def control_id(self):
        self.control_id_counter += 1
        return "playground_{id}_{index}".format(id=self.anim_id, index=self.control_id_counter)

    def add_control(self, label, input):
        tr = etree.SubElement(self.controls_container, "tr")

        label_cell = etree.SubElement(tr, "td", {"style": "white-space: pre"})
        label_element = etree.SubElement(label_cell, "label")
        label_element.text = label

        if input is None:
            label_cell.tag = "th"
            label_cell.attrib["colspan"] = "2"
            label_element.tag = "span"
            return

        label_element.tail = " "
        td = etree.SubElement(tr, "td", {"style": "width: 100%"})
        input_wrapper = input

        if input.tag == "enum":
            enum_id = input.text
            default_value = input.attrib.get("value", "")

            input = input_wrapper = etree.Element("select")
            for value, opt_label, _ in enum_values(self.schema_data, enum_id):
                option = etree.SubElement(input, "option", {"value": str(value)})
                option.text = opt_label
                if str(value) == default_value:
                    option.attrib["selected"] = "selected"
        elif input.tag == "highlight":
            input_wrapper = etree.Element("div", {"class": "highlighted-input"})
            lang = input.attrib.get("lang", "javascript")
            contents = input.text.strip()
            input = etree.SubElement(input_wrapper, "textarea", {
                "spellcheck": "false",
                "oninput": "syntax_edit_update(this, this.value); syntax_edit_scroll(this);",
                "onscroll": "syntax_edit_scroll(this);",
                "onkeydown": "syntax_edit_tab(this, event);",
                "data-lang": lang,
            })
            input.text = contents
            pre = etree.SubElement(input_wrapper, "pre", {"aria-hidden": "true"})
            code = etree.SubElement(pre, "code", {"class": "language-js hljs"})
            code.text = AtomicString(contents)

        input.attrib.setdefault("oninput", "")
        input.attrib["oninput"] += "lottie_player_{id}.reload();".format(id=self.anim_id)
        input.attrib["data-lottie-input"] = str(self.anim_id)
        input.attrib["autocomplete"] = "off"
        if "name" not in input.attrib:
            input.attrib["name"] = label
        td.append(input_wrapper)

        id_base = self.control_id()
        if input.attrib.get("type", "") == "range":
            etree.SubElement(td, "span", {
                "id": id_base + "_span"
            }).text = input.attrib["value"]
            input.attrib["oninput"] += (
                "document.getElementById('{span}').innerText = event.target.value;"
                .format(span=id_base + "_span")
            )
        elif input.tag == "textarea":
            tr.remove(td)
            tr = etree.SubElement(self.controls_container, "tr")
            tr.append(td)
            td.attrib["colspan"] = "2"
            label_cell.attrib["colspan"] = "2"
            input.attrib["rows"] = str(max(3, input.text.count("\n")))
            input.attrib["class"] = "code-input"
            input.attrib["style"] = "width: 100%"


class LottiePlayground(BlockProcessor):
    def __init__(self, md, schema_data):
        self.md = md
        self.schema_data = schema_data
        super().__init__(md.parser)

    def test(self, parent, block):
        return block.startswith("<lottie-playground")

    def run(self, parent, blocks):
        raw_string = blocks.pop(0)
        md_element: etree.Element = etree.fromstring(raw_string)

        md_title = md_element.find("./title")
        if md_title is not None:
            md_title.tag = "p"
            parent.append(md_title)

        width = md_element.attrib.pop("width", None)
        height = md_element.attrib.pop("height", None)
        buttons = md_element.attrib.pop("buttons", False)

        builder = LottiePlaygroundBuilder(parent, self.schema_data, width=width, height=height, buttons=buttons)

        md_form = md_element.find("./form")
        if md_form:
            for input in md_form:
                if not input.attrib.get("title", ""):
                    input.attrib["title"] = input.attrib["name"]
                elif not input.attrib.get("name", ""):
                    input.attrib["name"] = input.attrib["title"]
                builder.add_control(input.attrib["title"], input)

        md_json = md_element.find("./json")
        json_parent = etree.SubElement(builder.player_container, "div")
        json_parent.attrib["class"] = "json-parent"
        json_viewer_id = self.add_json_viewer(builder, json_parent)
        json_viewer_path = md_json.text
        #
        # filename = element.attrib.pop("src")
        # lottie_url = get_url(self.md, filename)
        # buttons = md_element.attrib.pop("buttons", "true") == "true"
        # element = LottieRenderer.render(
        #     url=lottie_url,
        #     download_file=lottie_url,
        #     width=width,
        #     height=height,
        #     extra_options=json.dumps(element.attrib),
        #     buttons=buttons,
        # )[0]

        # parent.append(element)

        example_id = md_element.attrib.pop("example")
        json_data = self.example_json(example_id)
        extra = json.dumps(md_element.attrib)
        md_script = md_element.find("./script")
        self.populate_script(md_script, builder, json_data, extra, json_viewer_id, json_viewer_path)

        return True

    def example_json(self, filename):
        """
        Returns minified JSON string
        """
        with open(docs_path / "static" / "examples" / filename) as file:
            return json.dumps(json.load(file))

    def populate_script(self, script_element, builder, json_data, extra_options, json_viewer_id, json_viewer_path):
        # <script> are gobbled up by a preprocessor
        script = ""
        if script_element is not None:
            script = script_element.text

        if json_viewer_path:
            script += "this.json_viewer_contents = %s;" % json_viewer_path

        builder.renderer.populate_script("""
        var lottie_player_{id} = new PlaygroundPlayer(
            {id},
            '{json_viewer_id}',
            'lottie_target_{id}',
            {json_data},
            function (lottie, data)
            {{
                {on_load}
            }},
            {extra_options}
        );
        """.format(
            id=builder.anim_id,
            json_viewer_id=json_viewer_id,
            on_load=script,
            json_data=json_data,
            extra_options=extra_options
        ))

    def add_json_viewer(self, builder, parent):
        code_viewer_id = builder.control_id()
        parent.attrib["id"] = code_viewer_id + "_parent"

        pre = etree.SubElement(parent, "pre")
        code = etree.SubElement(pre, "code", {"id": code_viewer_id, "class": "language-json hljs"})
        code.text = ""
        return code_viewer_id


def css_style(**args):
    string = ""
    for k, v in args.items():
        string += "%s:%s;" % (k.replace("_", "-"), v)

    return string


class LottieColor(InlineProcessor):
    def __init__(self, pattern, md, mult):
        super().__init__(pattern, md)
        self.mult = mult

    def handleMatch(self, match, data):
        span = etree.Element("span")
        span.attrib["style"] = "font-family: right"

        if self.mult == -1:
            hex = match.group(1)
        else:
            comp = [float(match.group(i)) / self.mult for i in range(2, 5)]
            hex = "#" + "".join("%02x" % round(x * 255) for x in comp)

        color = etree.SubElement(span, "span")
        color.attrib["style"] = css_style(background_color=hex)
        color.attrib["class"] = "color-preview"
        code = etree.SubElement(span, "code")

        if self.mult == -1:
            code.text = hex
        else:
            code.text = "[%s]" % ", ".join("%.3g" % x for x in comp)

        return span, match.start(0), match.end(0)


class LottieExtension(Extension):
    def extendMarkdown(self, md):
        with open(docs_path / "lottie.schema.json") as file:
            schema_data = Schema(json.load(file))

        md.inlinePatterns.register(SchemaString(md, schema_data), "schema_string", 175)
        md.inlinePatterns.register(JsonFile(md), "json_file", 175)
        md.inlinePatterns.register(SchemaLink(md), "schema_link", 175)
        md.inlinePatterns.register(SubTypeTable(md, schema_data), "schema_subtype_table", 175)
        md.inlinePatterns.register(LottieColor(r'{lottie_color:(([^,]+),\s*([^,]+),\s*([^,]+))}', md, 1), 'lottie_color', 175)

        md.parser.blockprocessors.register(
            RawHTML(
                md.parser,
                schema_data,
                ["lottie", "lottie-playground"]
            ),
            "raw_heading",
            100
        )
        md.parser.blockprocessors.register(LottiePlayground(md, schema_data), "lottie-playground", 200)
        md.parser.blockprocessors.register(LottieBlock(md), "lottie", 175)
        md.parser.blockprocessors.register(SchemaObject(md.parser, schema_data), "schema_object", 175)
        md.parser.blockprocessors.register(SchemaEnum(md.parser, schema_data), "schema_enum", 175)


def makeExtension(**kwargs):
    return LottieExtension(**kwargs)
