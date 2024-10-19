import ast

from . import python_to_ts, pseudocode, cpp


language_names = {
    "pseudo": "Pseudo-Code",
    "py": "Python",
    "cpp": "C++",
    "ts": "TypeScript",
}


def code_to_ast(source):
    return ast.parse(source, type_comments=True)


def code_to_samples(source):
    tree = code_to_ast(source)
    comments = python_to_ts.CommentData(source)
    return {
        "ast": tree,
        "pseudo": pseudocode.PseudoCode().convert(tree, comments),
        "py": source,
        "cpp": cpp.CppTranslator().convert(tree, comments),
        "ts": python_to_ts.Py2Ts().convert(tree, comments),
    }
