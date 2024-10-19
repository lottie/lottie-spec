import ast
from .python_to_ts import CLike, Range


class CppTranslator(CLike):
    keywords = {"or"}

    def function_def(self, name, args, returns, body, is_async, is_method, is_getter):
        prefix = ""
        suffix = ""

        prefix = "%s " % (returns or "void")
        if is_method:
            if name == "__init__":
                name = self.class_name
                prefix = ""
            elif name == "__repr__" or name == "__str__":
                name = "operator std::string"
                suffix = " const"

        start = prefix + "%s(" % self.styled_name(name)

        args_start = 0
        if self.class_name and len(args.args) > 0 and args.args[0].arg in ("self", "cls"):
            args_start = 1

        converted_args = []
        for i in range(args_start, len(args.args)):
            arg_name = self.styled_name(args.args[i].arg)
            arg_type = self.expression_to_string(args.args[i].annotation, True)
            arg = "%s %s" % (arg_type, arg_name)

            reverse_i = len(args.args) - i
            if reverse_i <= len(args.defaults):
                arg += " = %s" % self.expression_to_string(args.defaults[-reverse_i])
            converted_args.append(arg)

        start += ", ".join(converted_args) + ")" + suffix
        self.function_body(start, body)

    def declare(self, target, annotation, value, ast_value):
        code = "%s %s" % (annotation, target)
        if value:
            if isinstance(ast_value, ast.Call) and value.startswith(annotation):
                value = value[len(annotation)+1:-1]
                if annotation[0].isupper():
                    self.push_code("%s(%s);" % (code, value))
                    return
            code += " = %s" % value
        self.push_code(code + ";")

    def begin_for(self, target, iter, is_async):
        code_start = "for "
        if isinstance(iter, Range):
            iter.fill_defaults(False)
            code_start += "( int %s = %s; " % (target, iter.start)
            code_start += "%s < %s; " % (target, iter.stop)
            if iter.step is None:
                code_start += "%s++" % (target)
            else:
                code_start += "%s += %s" % (target, iter.step)
            code_start += " )"
        else:
            code_start += "( const auto& %s : %s )" % (target, iter)
        self.begin_block(code_start)

    def delete_statement(self, targets):
        self.push_code("delete %s;" % ", ".join(targets))

    def type_alias(self, obj):
        self.push_code("using %s = %s;" % list(map(self.expression_to_string, (obj.name, obj.value))))

    def convert_constant(self, value, annotation):
        if value is None:
            return "void" if annotation else "nullptr"
        return repr(value)

    def expr_sequence_literal(self, elements, type):
        return "{%s}" % ", ".join(elements)

    def expr_dict(self, items):
        return "{%s}" % ", ".join("{%s, %s}" % item for item in items)

    def convert_name(self, name, annotation):
        if name in ("min", "max", "round"):
            return "std::" + name
        return super().convert_name(name, annotation)

    def expr_attribute(self, object, member):
        if object == "math":
            if member == "pi":
                return "std::numbers::" + member
            return "std::%s" % member
        return super().expr_attribute(object, member)
