from source_translator import AstTranslator, IndentationManager
from source_translator.naming import snake_to_lower_camel


class PseudoCode(AstTranslator):
    ops = {
        "Eq": "=",
        "NotEq": r"\neq",
        "Lt": "<",
        "LtE": r"\leq",
        "Gt": ">",
        "GtE": r"\geq",
        "Is": "=",
        "IsNot": r"\neq",
        "In": r"\in",
        "NotIn": r"\notin",
        "Add": "+",
        "Sub": "-",
        "Mult": r"\cdot",
        "MatMult": r"\times",
        "Div": r"\frac",
        "Mod": "%",
        "LShift": "<<",
        "RShift": ">>",
        "BitOr": "|",
        "BitXor": "^",
        "BitAnd": "&",
        "FloorDiv": "//",
        "Pow": "^",
        "Invert": "~",
        "Not": "\\neg",
        "UAdd": "+",
        "USub": "-",
        "And": "\\land",
        "Or": "\\lor",
    }

    def snake_sentence(self, name, upper):
        sentence = name.replace("_", " ")
        if upper:
            return sentence[0].upper() + sentence[1:]
        return sentence

    def expr_attribute(self, object, member):
        if object == "shape":
            if member == "closed":
                return "shape closed"
            return self.snake_sentence(member, True)
        if object == "math":
            return "\\" + member
        return "%s.%s" % (object, member)

    def begin_if(self, expr):
        self.push_code("If $%s$" % expr)

    def end_block(self):
        pass

    def begin_else(self):
        self.push_code("Otherwise")

    def declare(self, target, type, value, ast_value):
        self.push_code("$%s \\coloneq %s$" % (self.decorate_name(target), value))

    def format_comment(self, value):
        if len(value) == 0:
            self.push_code("")
        for line in value:
            self.push_code(line)

    def expression_statement(self, expr):
        if " " in expr or "$" in expr:
            self.push_code(expr)
        else:
            self.push_code("$%s$" % expr)

    def decorate_name(self, name):
        type = self.get_var_type(name)
        if type.startswith("\\mathbb{R}^"):
            return "\\vec{%s}" % name
        return name

    def expr_func(self, name, args):
        if name == "int":
            return args[0]

        if name == "round":
            return r"\lfloor %s \rceil" % ", ".join(args)

        if name == "floor":
            return r"\lfloor %s \rfloor" % ", ".join(args)

        if name == "ceil":
            return r"\lceil %s \rceil" % ", ".join(args)

        if name == "range":
            start = "0"
            end = "0"
            if len(args) == 1:
                end = args[0]
            elif len(args) == 2:
                start, end = args
            else:
                raise NotImplementedError

            return "[%s, %s)" % (start, end)

        is_sentence = " " in name
        if name == "Vector2D":
            name = ""
        code = name
        if is_sentence:
            code += " $"
        else:
            code += r"\left("
        code += ", ".join(args)
        if is_sentence:
            code += "$"
        else:
            code += r"\right)"
        return code

    def convert_name(self, name, annotation):
        if annotation:
            if name == "float":
                return "\\mathbb{R}"
            elif name == "int":
                return "\\mathbb{Z}"
            elif name == "Vector2D":
                return "\\mathbb{R}^2"

        if name in ("min", "max"):
            return "\\" + name
        if name == "ELLIPSE_CONSTANT":
            return "E_t"
        if name in ("alpha", "beta", "theta"):
            return "\\" + name

        name = name.strip("_")
        chunks = name.rsplit("_", 1)
        name = snake_to_lower_camel(chunks[0])
        if len(chunks) == 2:
            name += "_{%s}" % chunks[1]
        return self.decorate_name(name)

    def convert_constant(self, value, annotation):
        if value is None:
            return "nil"
        if isinstance(value, bool):
            return str(value).lower()
        return repr(value)

    def expr_binop(self, op, *operands):
        if op == "\\frac":
            return "%s{%s}{%s}" % (op, operands[0], operands[1])
        return (" %s " % op).join(operands)

    def assign(self, targets, value):
        for target in targets:
            if " " in target:
                if value == "true":
                    self.push_code("Set %s" % (target))
                elif value == "false":

                    self.push_code("Unset %s" % (target))
                else:
                    self.push_code("Set %s to %s" % (target, value))
            else:
                self.push_code("$%s \\coloneq %s$" % (target, value))

    def function_def(self, name, args, returns, body, is_async, is_method, is_getter):
        self.push_code(self.snake_sentence(name, True))

        with IndentationManager(self, False):
            args_start = 0
            if is_method and len(args.args) > 0 and args.args[0].arg in ("self", "cls"):
                args_start = 1

            if len(args.args) > args_start and args.args[args_start].arg == "shape":
                args_start += 1

            if len(args.args) > args_start:
                self.push_code("Inputs:")

                with IndentationManager(self, False):
                    for i in range(args_start, len(args.args)):
                        name = self.convert_name(args.args[i].arg, False)
                        if args.args[i].annotation:
                            type = self.expression_to_string(args.args[i].annotation, True)
                        else:
                            type = None
                        self.var_add(name, type)
                        arg = "$" + self.decorate_name(name)
                        if type:
                            arg += " \\in " + type

                        reverse_i = len(args.args) - i
                        if reverse_i <= len(args.defaults):
                            arg += " = %s" % self.expression_to_string(args.defaults[-reverse_i])
                        arg += "$"
                        self.push_code(arg)
                self.push_code("")

        with IndentationManager(self, False):
            self.convert_ast(body)

    def expr_compare(self, value, annotation):
        expr = self.expression_to_string(value.left, annotation)
        for cmp, op in zip(value.comparators, value.ops):
            expr += " " + self.expression_to_string(op, annotation)
            expr += " " + self.expression_to_string(cmp, annotation)
        return expr

    def begin_for(self, target, iter, is_async):
        code_start = "For each $%s$ in $%s$" % (target, iter)
        self.push_code(code_start)

    def convert_line_comment(self, comment):
        return comment or ""
