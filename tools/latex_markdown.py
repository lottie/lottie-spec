import latex2mathml.converter

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.blockprocessors import BlockProcessor


class InlineLatex(InlineProcessor):
    def __init__(self, md):
        super().__init__(r'\$([^\$\n]+)\$', md)

    def handleMatch(self, match, data):
        element = latex2mathml.converter.convert_to_element(match.group(1))
        return element, match.start(0), match.end(0)


class BlockLatex(BlockProcessor):
    fence = "$$"

    def __init__(self, md):
        super().__init__(md.parser)

    def test(self, parent, block):
        return block.startswith("$$")

    def run(self, parent, blocks):
        code = ""
        last_block = blocks.pop(0)[2:]
        while True:
            if last_block.endswith("$$"):
                code += last_block[:-2]
                break
            else:
                code += last_block
                last_block = blocks.pop(0)

        for chunk in code.split("$$\n$$"):
            element = latex2mathml.converter.convert_to_element(chunk, display="block")
            parent.append(element)

        return True


class LatexExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(InlineLatex(md), "inline_latex", 175)
        md.parser.blockprocessors.register(BlockLatex(md), "block_latex", 175)


def makeExtension(**kwargs):
    return LatexExtension(**kwargs)
