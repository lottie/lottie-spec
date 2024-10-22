from source_translator import SourceCode
from source_translator.langs import cpp, ts
from . import pseudocode


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
