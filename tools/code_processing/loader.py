import re
import ast

from . import python_to_ts, pseudocode

RE_COMMENT = re.compile(r"(\s*)# ?(.*)")
RE_NOLINE = re.compile(r"^(\s*)$", flags=re.MULTILINE)


def indent_at(string, pos):
    if pos <= 0:
        return ""

    newline_before = string.rfind('\n', 0, pos-1)
    if newline_before == -1:
        return ""

    line_before = string[newline_before + 1:pos]

    additional = 0
    if line_before.endswith(":\n"):
        additional = 4

    return " " * (len(line_before) - len(line_before.lstrip()) + additional)


def gather_indent(m):
    spaces = m.group(1)
    if spaces:
        return spaces

    return indent_at(m.string, m.start())


def process_code(source):
    return RE_NOLINE.sub(
        lambda m: gather_indent(m) + "''",
        RE_COMMENT.sub(r"\1'''\2'''", source.strip())
    )


def code_to_ast(source):
    return ast.parse(process_code(source), type_comments=True)


def code_to_samples(source):
    tree = code_to_ast(source)
    return {
        "ast": tree,
        "pseudo": pseudocode.PseudoCode().convert(tree),
        "py": source.strip("\n"),
        "ts": python_to_ts.Py2Ts().convert(tree),
    }
