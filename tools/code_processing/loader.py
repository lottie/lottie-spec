import ast

from . import python_to_ts, pseudocode


def code_to_ast(source):
    return ast.parse(source, type_comments=True)


def code_to_samples(source):
    tree = code_to_ast(source)
    comments = python_to_ts.CommentData(source)
    return {
        "ast": tree,
        "pseudo": pseudocode.PseudoCode().convert(tree, comments),
        "py": source.strip("\n"),
        "ts": python_to_ts.Py2Ts().convert(tree, comments),
    }
