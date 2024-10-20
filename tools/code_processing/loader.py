from .python_source import SourceCode
from .langs import ts, pseudocode, cpp


language_names = {
    "pseudo": "Pseudo-Code",
    "py": "Python",
    "cpp": "C++",
    "ts": "TypeScript",
}


def code_to_samples(source):
    data = SourceCode(source)
    return {
        "ast": data.ast,
        "pseudo": pseudocode.PseudoCode().convert(data),
        "py": source,
        "cpp": cpp.CppTranslator().convert(data),
        "ts": ts.TypeScriptTranslator().convert(data),
    }
