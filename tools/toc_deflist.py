import xml.etree.ElementTree as etree

from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
from markdown.extensions import toc

from lottie_markdown import get_url


class TocDefListTreeProcessor(Treeprocessor):
    old_nest = toc.nest_toc_tokens

    def __init__(self, md):
        super().__init__(md)
        self.extra_toc = []
        # Patch toc.nest_toc_tokens to show glossary terms in the
        # table of contents (Hack)
        toc.nest_toc_tokens = self.patched_nest_toc_tokens

    def patched_nest_toc_tokens(self, toc_list):
        tl = TocDefListTreeProcessor.old_nest(toc_list + self.extra_toc)
        self.extra_toc = []
        return tl

    def run(self, root):
        self.extra_toc = []

        term: etree.Element
        for term in root.findall(".//dt"):
            if "id" not in term.attrib:
                text = toc.unescape(toc.stashedHTML2text(toc.get_name(term), self.md))
                id = toc.slugify(text, "-")
                term.attrib["id"] = id
                link = etree.Element("a")
                for child in term:
                    term.remove(child)
                    link.append(child)
                link.text = term.text
                term.text = ""
                term.append(link)
                link.attrib["href"] = "#" + id
                self.extra_toc.append({
                    "level": 2,
                    "id": id,
                    "name": text
                })


class GlossaryLink(InlineProcessor):
    def __init__(self, md):
        super().__init__(r'\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]', md)

    def handleMatch(self, match, data):
        link = etree.Element("a")
        title = match.group(1)
        id = toc.slugify(title, "-")
        link.attrib["href"] = get_url(self.md, "specs/glossary.md", id)
        link.text = match.group(2) or title
        return link, match.start(0), match.end(0)


class TocDefListExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.treeprocessors.register(TocDefListTreeProcessor(md), "toc_deflist", 175)
        md.inlinePatterns.register(GlossaryLink(md), "glossary_link", 175)


def makeExtension(**kwargs):
    return TocDefListExtension(**kwargs)
