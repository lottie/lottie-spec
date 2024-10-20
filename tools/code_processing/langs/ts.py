import ast
from ..python_source import CLike, Range, snake_to_lower_camel, KandRStyle


class TypeScriptTranslator(CLike):
    ops = {
        **CLike.ops,
        "Is": "===",
        "IsNot": "!==",
    }
    keywords = {"in"}

    def __init__(self, type_annotations=True):
        super().__init__(KandRStyle())
        self.type_annotations = type_annotations

    def function_def(self, name, args, returns, body, is_async, is_method, is_getter):
        start = ""
        suffix = ""

        if returns:
            suffix = " : %s" % returns

        if is_async:
            start = "async "

        if not is_method:
            start += "function "
        elif name == "__init__":
            name = "constructor"
        elif name == "__repr__" or name == "__str__":
            name = "toString"

        start += "%s(" % self.styled_name(name)

        args_start = 0
        if self.class_name and len(args.args) > 0 and args.args[0].arg in ("self", "cls"):
            args_start = 1

        ts_args = []
        for i in range(args_start, len(args.args)):
            ts_arg = self.styled_name(args.args[i].arg)
            if args.args[i].annotation is not None and self.type_annotations:
                ts_arg += ": " + self.expression_to_string(args.args[i].annotation, True)

            reverse_i = len(args.args) - i
            if reverse_i <= len(args.defaults):
                ts_arg += " = %s" % self.expression_to_string(args.defaults[-reverse_i])
            ts_args.append(ts_arg)

        start += ", ".join(ts_args) + ")" + suffix
        self.function_body(start, body)

    def styled_name(self, id):
        id = super().styled_name(id)
        if "_" in id[:-1]:
            return snake_to_lower_camel(id)
        return id

    def declare(self, target, annotation, value, ast_value):
        ts_code = "let %s" % target
        if self.type_annotations:
            ts_code += ": %s" % annotation
        if value:
            ts_code += " = %s" % value
        self.push_code(ts_code + ";")

    def begin_for(self, target, iter, is_async):
        code_start = "for "
        if is_async:
            code_start += "await "
        if isinstance(iter, Range):
            iter.fill_defaults(False)
            code_start += "( let %s = %s; " % (target, iter.start)
            code_start += "%s < %s; " % (target, iter.stop)
            if iter.step is None:
                code_start += "%s++" % (target)
            else:
                code_start += "%s += %s" % (target, iter.step)
            code_start += " )"
        else:
            code_start += "( let %s of %s )" % (target, iter)
        self.begin_block(code_start)

    def import_statement(self, obj):
        for alias in obj.names:
            self.push_code("import * as %s from %r;" % (alias.asname or alias.name, alias.name))

    def import_from_statement(self, obj):
        names = []
        for alias in obj.names:
            if alias.asname:
                names.append("%s as %s" % (alias.name, alias.asname))
            else:
                names.append(alias.name)
        self.push_code("import %s from %r;" % (names, obj.module))

    def delete_statement(self, targets):
        self.push_code("delete %s;" % ", ".join(targets))

    def type_alias(self, obj):
        self.push_code("type %s = %s;" % list(map(self.expression_to_string, (obj.name, obj.value))))

    def convert_constant(self, value, annotation):
        if value is None:
            return "null"
        return super().convert_constant(value, annotation)

    def convert_name(self, name, annotation):
        if name == "math":
            return "Math"
        if name == "NVector":
            return "Vector"
        if name in ("min", "max"):
            return "Math." + name
        return super().convert_name(name, annotation)

    def expr_func(self, name, args):
        if name[0].isupper() and name.isalnum():
            name = "new %s" % name
        return super().expr_func(name, args)

    def expr_attribute(self, object, member):
        if object == "Math":
            if member == "pi":
                member = member.upper()
        return super().expr_attribute(object, member)

    def expr_sequence_literal(self, elements, type):
        if type is set:
            return "new Set([%s])" % ", ".join(elements)
        return "[%s]" % ", ".join(elements)

    def expr_dict(self, items):
        return "{%s}" % ", ".join("%s: %s" % item for item in items)

    def expr_subscript_range(self, value, index):
        args = ", ".join(v if v is not None else "undefined" for v in [index.start, index.stop, index.step])
        return "%s.slice(%s)" % (value, args)

    def other_expression(self, value, annotation):
        if isinstance(value, ast.MatchAs):
            return value.name
        return self.unknown(value, True)
