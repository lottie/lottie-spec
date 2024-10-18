import re
import ast
import pprint
import inspect


def snake_to_lower_camel(string):
    return re.sub("_[a-z]", lambda p: p.group(0)[1].upper(), string)


class IndentationManager:
    def __init__(self, converter, is_class):
        self.converter = converter
        self.is_class = is_class
        self.start_in_class = converter.in_class

    def __enter__(self):
        if self.is_class:
            self.converter.in_method = True
        self.converter.in_class = self.is_class
        self.converter.indent_up()

    def __exit__(self, *a):
        if self.is_class:
            self.converter.in_method = False
        self.converter.in_class = self.start_in_class
        self.converter.indent_down()


class CommentData:
    RE_COMMENT = re.compile(r"^\s*(.+)?# ?(.*)$")

    class Comment:
        def __init__(self, line, text, is_tail):
            self.line = line
            self.text = text
            self.is_tail = is_tail

    class CommentReader:
        def __init__(self, comments):
            self.comments = comments
            self.next_line = None
            self.current_line = 0
            self.index = 0
            self.get_next()

        def prepare(self, node):
            if hasattr(node, "lineno"):
                self.current_line = node.lineno

        def get_next(self):
            self.next_line = self.current_comment().line if self.index < len(self.comments) else None

        def current_comment(self):
            return self.comments[self.index]

        def has_line_comment(self):
            if self.next_line is None:
                return False

            if self.current_line >= self.next_line:
                return not self.current_comment().is_tail

            return False

        def has_tail_comment(self):
            if self.next_line is None:
                return False

            if self.current_line >= self.next_line:
                return self.current_comment().is_tail

            return False

        def get_comment(self):
            return self.current_comment().text

        def next(self):
            self.index += 1
            self.get_next()

    def __init__(self, source):
        self.comments = []

        for lineno, line in enumerate(source.splitlines()):
            match = self.RE_COMMENT.match(line)
            if match:
                self.add_comment(lineno + 1, match.group(2), match.group(1) is not None)
            elif line.strip() == "":
                self.add_empty(lineno + 1)

    def add_comment(self, line, text, is_tail):
        self.comments.append(self.Comment(line, text, is_tail))

    def add_empty(self, line):
        self.comments.append(self.Comment(line, None, False))

    def reader(self):
        return self.CommentReader(self.comments)


class Range:
    def __init__(self, ast_node, translator):
        self.ast_node = ast_node
        self.start = None
        self.stop = None
        self.step = None
        self.translator = translator
        if len(ast_node.args) == 1:
            self.stop = translator.expression_to_string(ast_node.args[0], False)
        else:
            self.start = translator.expression_to_string(ast_node.args[0], False)
            self.stop = translator.expression_to_string(ast_node.args[1], False)
            if len(ast_node.args) > 2:
                self.step = translator.expression_to_string(ast_node.args[2], False)

    def fill_defaults(self, step=False):
        if self.start is None:
            self.start = self.translator.expression_to_string(ast.Constant(0), False)
        if step and self.step is None:
            self.step = self.translator.expression_to_string(ast.Constant(1), False)

    def __str__(self):
        return self.translator.expression_to_string(self.ast_node, False)


class AstTranslator:
    def __init__(self):
        self.indent_spaces = 4
        self.indent_level = 0
        self.output = ""
        self.in_class = False
        self.in_method = False
        self.scope = [{}]

    def convert(self, obj, comments: CommentData):
        self.output = ""
        self.comments = comments.reader()
        self.next_comment = None
        if comments.comments:
            self.next_comment = comments.comments[0].line

        self.comment_line = 0
        self.convert_ast(obj)
        return self.output

    def push_scope(self):
        self.scope.insert(0, {})

    def pop_scope(self):
        self.scope.pop(0)

    def var_add(self, var, type):
        if type is None:
            type = ""
        elif not isinstance(type, str):
            type = self.expression_to_string(type, True)
        self.scope[0][var] = type

    def get_var_type(self, var):
        for scope in self.scope:
            if var in scope:
                return scope[var]
        return ""

    def maybe_range(self, ast_node):
        if isinstance(ast_node, ast.Call) and isinstance(ast_node.func, ast.Name) and ast_node.func.id == "range":
            return Range(ast_node, self)
        return self.expression_to_string(ast_node, False)

    @property
    def indent(self):
        return (self.indent_level * self.indent_spaces) * " "

    def unknown(self, obj, as_string=False):
        # breakpoint()
        raise ValueError(repr(obj) + "\n" + pprint.pformat(obj.__dict__))
        # unknown = "\n" + repr(obj) + "\n" + pprint.pformat(obj.__dict__) + "\n"
        # if as_string:
        #     return unknown
        # self.ts_code += unknown

    def push_code(self, code):
        while self.comments.has_line_comment():
            comment = self.comments.get_comment()
            if comment is None:
                self.output += "\n"
            else:
                self.output += self.indent + self.convert_line_comment(comment) + "\n"
            self.comments.next()

        self.output += self.indent + code

        if self.comments.has_tail_comment():
            self.output += " " + self.convert_line_comment(self.comments.get_comment())
            self.comments.next()

        self.output += "\n"

    def indent_up(self):
        self.indent_level += 1

    def indent_down(self):
        self.indent_level -= 1

    def format_comment(self, comment):
        self.push_code(comment)

    def format_doc_comment(self, comment):
        self.format_comment(comment)

    def convert_doc_comment(self, body):
        if len(body) > 0 and isinstance(body[0], ast.Expr):
            expr = body[0].value
            if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
                comment = expr.value
                if comment.startswith("!"):
                    comment = comment[1:]
                self.format_doc_comment(inspect.cleandoc(comment).splitlines())
                return body[1:]
        return body

    def function_def(self, name, args, body, is_async, is_method, is_getter):
        raise NotImplementedError

    def values_to_string(self, *args, annotation=False):
        return tuple(self.expression_to_string(v, annotation) for v in args)

    def begin_class(self, obj):
        raise NotImplementedError

    def end_block(self):
        pass

    def declare(self, target, annotation, value):
        raise NotImplementedError

    def assign(self, targets, value):
        raise NotImplementedError

    def assign_op(self, target, op, value):
        raise NotImplementedError

    def begin_if(self, expr):
        raise NotImplementedError

    def begin_for(self, target, iter, is_async):
        raise NotImplementedError

    def begin_else(self):
        raise NotImplementedError

    def begin_while(self, cond):
        raise NotImplementedError

    def basic_statement(self, statement):
        raise NotImplementedError

    def return_statement(self, value):
        raise NotImplementedError

    def begin_switch(self, expr):
        raise NotImplementedError

    def begin_switch_case(self, pattern):
        raise NotImplementedError

    def end_switch_case(self):
        raise NotImplementedError

    def import_statement(self, obj):
        raise NotImplementedError

    def import_from_statement(self, obj):
        raise NotImplementedError

    def delete_statement(self, targets):
        raise NotImplementedError

    def type_alias(self, obj):
        raise NotImplementedError

    def expr_func(self, name, args):
        raise NotImplementedError

    def expression_statement(self, v):
        self.push_code(v)

    def convert_ast(self, obj):
        self.comments.prepare(obj)

        if isinstance(obj, ast.Module):
            self.convert_ast(obj.body)
        elif isinstance(obj, list):
            self.push_scope()
            for code in obj:
                self.convert_ast(code)
            self.pop_scope()
        elif isinstance(obj, ast.ClassDef):
            body = self.convert_doc_comment(obj.body)
            self.begin_class(obj.name)
            with IndentationManager(self, True):
                self.convert_ast(body)
        elif isinstance(obj, ast.Expr):
            self.convert_ast(obj.value)
        elif isinstance(obj, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = self.convert_doc_comment(obj.body)
            is_async = isinstance(obj, ast.AsyncFunctionDef)
            is_getter = False
            is_method = self.in_class

            if self.in_class:
                for deco in obj.decorator_list:
                    if isinstance(deco, ast.Name) and deco.id == "property":
                        is_getter = True

            self.push_scope()
            self.function_def(obj.name, obj.args, body, is_async, is_method, is_getter)
            self.pop_scope()
        elif isinstance(obj, ast.Assign):
            targets = list(map(self.expression_to_string, obj.targets))
            value = self.expression_to_string(obj.value)
            self.assign(targets, value)

        elif isinstance(obj, ast.AnnAssign):
            target = self.expression_to_string(obj.target)
            annotation = self.expression_to_string(obj.annotation, annotation=True)
            value = self.expression_to_string(obj.value) if obj.value else None
            self.var_add(target, annotation)
            self.declare(target, annotation, value)
        elif isinstance(obj, ast.If):
            self.begin_if(self.expression_to_string(obj.test))
            with IndentationManager(self, False):
                self.convert_ast(obj.body)
            if obj.orelse:
                self.begin_else()
                with IndentationManager(self, False):
                    self.convert_ast(obj.orelse)
            self.end_block()
        elif isinstance(obj, ast.Constant):
            self.format_comment(inspect.cleandoc(str(obj.value)).splitlines())
        elif isinstance(obj, ast.expr):
            self.expression_statement(self.expression_to_string(obj))
        elif isinstance(obj, ast.Continue):
            self.basic_statement("continue")
        elif isinstance(obj, ast.Break):
            self.basic_statement("break")
        elif isinstance(obj, ast.Return):
            self.return_statement(None if obj.value is None else self.expression_to_string(obj.value))
        elif isinstance(obj, ast.AugAssign):
            self.assign_op(*self.values_to_string(obj.target, obj.op, obj.value))
        elif isinstance(obj, (ast.For, ast.AsyncFor)):
            is_async = isinstance(obj, ast.AsyncFor)
            target = self.expression_to_string(obj.target)
            iter = self.maybe_range(obj.iter)
            self.begin_for(target, iter, is_async)
            with IndentationManager(self, False):
                self.convert_ast(obj.body)
            self.end_block()
        elif isinstance(obj, ast.While):
            cond = self.expression_to_string(obj.test)
            self.begin_while(cond)
            with IndentationManager(self, False):
                self.convert_ast(obj.body)
            self.end_block()
        elif isinstance(obj, ast.Pass):
            pass
        elif isinstance(obj, ast.Match):
            expr = self.expression_to_string(obj.subject)
            self.begin_switch(expr)
            with IndentationManager(self, False):
                self.convert_ast(obj.cases)
            self.end_block()
        elif isinstance(obj, ast.match_case):
            if isinstance(obj.pattern, ast.MatchAs) and obj.pattern.name is None:
                pattern = None
            else:
                pattern = self.expression_to_string(obj.pattern)
            self.begin_switch_case(pattern)
            with IndentationManager(self, False):
                self.convert_ast(obj.body)
                self.end_switch_case()
        elif isinstance(obj, ast.Import):
            self.import_statement(obj)
        elif isinstance(obj, ast.ImportFrom):
            self.import_from_statement(obj)
        elif isinstance(obj, ast.Delete):
            self.delete_statement(map(self.expression_to_string, obj.targets))
        elif isinstance(obj, ast.TypeAlias):
            self.type_alias(obj)
        else:
            self.unknown(obj)

    def convert_constant(self, value):
        return repr(value)

    def convert_name(self, name, annotation):
        return name

    def expr_unop(self, op, value):
        return "%s%s" % (op, value)

    def expr_binop(self, op, *operands):
        return (" %s " % op).join(operands)

    def other_expression(self, value, annotation):
        return self.unknown(value, True)

    def expr_attribute(self, object, member):
        return "%s.%s" % (object, member)

    def convert_line_comment(self, comment):
        raise NotImplementedError

    def expression_to_string(self, value, annotation=False):
        if isinstance(value, ast.Constant):
            return self.convert_constant(value.value)
        if isinstance(value, ast.Name):
            return self.convert_name(value.id, annotation)
        if isinstance(value, ast.Attribute):
            object = self.expression_to_string(value.value, annotation)
            member = value.attr
            return self.expr_attribute(object, member)
        if isinstance(value, (ast.cmpop, ast.operator, ast.unaryop, ast.boolop)):
            return self.ops[value.__class__.__name__]
        if isinstance(value, ast.Call):
            name = self.expression_to_string(value.func, annotation)
            args = [self.expression_to_string(v, annotation) for v in value.args]
            return self.expr_func(name, args)
        if isinstance(value, ast.BinOp):
            return self.expr_binop(*self.values_to_string(value.op, value.left, value.right, annotation=annotation))
        if isinstance(value, ast.UnaryOp):
            return self.expr_unop(*self.values_to_string(value.op, value.operand, annotation=annotation))
        if isinstance(value, ast.BoolOp):
            op = self.expression_to_string(value.op, annotation)
            return self.expr_binop(op, *(self.expression_to_string(v, annotation) for v in value.values))
        return self.other_expression(value, annotation)


class Py2Ts(AstTranslator):
    ops = {
        "Eq": "==",
        "NotEq": "!=",
        "Lt": "<",
        "LtE": "<=",
        "Gt": ">",
        "GtE": ">=",
        "Is": "===",
        "IsNot": "!==",
        "In": " <in>",
        "NotIn": "<not in>",
        "Add": "+",
        "Sub": "-",
        "Mult": "*",
        "MatMult": "*",
        "Div": "/",
        "Mod": "%",
        "LShift": "<<",
        "RShift": ">>",
        "BitOr": "|",
        "BitXor": "^",
        "BitAnd": "&",
        "FloorDiv": "//",
        "Pow": "**",
        "Invert": "~",
        "Not": "!",
        "UAdd": "+",
        "USub": "-",
        "And": "&&",
        "Or": "||",
    }

    def __init__(self):
        super().__init__()
        self.type_annotations = True

    def function_def(self, name, args, body, is_async, is_method, is_getter):
        start = ""

        if is_async:
            start = "async "

        if not is_method:
            start += "function "
        elif name == "__init__":
            name = "constructor"
        elif name == "__repr__" or name == "__str__":
            name = "toString"

        start += "%s(" % self.camel_snake(name)

        args_start = 0
        if self.in_class and len(args.args) > 0 and args.args[0].arg in ("self", "cls"):
            args_start = 1

        ts_args = []
        for i in range(args_start, len(args.args)):
            ts_arg = self.camel_snake(args.args[i].arg)
            if args.args[i].annotation is not None and self.type_annotations:
                ts_arg += ": " + self.expression_to_string(args.args[i].annotation, True)

            reverse_i = len(args.args) - i
            if reverse_i <= len(args.defaults):
                ts_arg += " = %s" % self.expression_to_string(args.defaults[-reverse_i])
            ts_args.append(ts_arg)

        start += ", ".join(ts_args) + ") {"
        self.push_code(start)
        with IndentationManager(self, False):
            self.convert_ast(body)
        self.push_code("}")

    def camel_snake(self, id):
        if "_" in id:
            return snake_to_lower_camel(id)
        return id

    def begin_class(self, obj):
        self.push_code("class %s {" % obj.name)

    def end_block(self):
        self.push_code("}")

    def assign(self, targets, value):
        ts_code = " = ".join(targets)
        ts_code += " = %s;" % value
        self.push_code(ts_code)

    def assign_op(self, target, op, value):
        self.push_code("%s %s= %s;" % (target, op, value))

    def declare(self, target, annotation, value):
        ts_code = "let %s" % target
        if self.type_annotations:
            ts_code += ": %s" % annotation
        if value:
            ts_code += " = %s;" % value
        self.push_code(ts_code)

    def begin_if(self, expr):
        self.push_code("if ( %s ) {" % expr)

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
            code_start += "( let %s of %s ) {" % (target, iter)
        self.push_code(code_start)

    def begin_else(self):
        self.push_code("} else {")

    def begin_while(self, cond):
        self.push_code("while ( %s ) {" % cond)

    def basic_statement(self, statement):
        self.push_code(statement + ";")

    def return_statement(self, value):
        if value is None:
            self.push_code("return;")
        else:
            self.push_code("return %s;" % value)

    def begin_switch(self, expr):
        self.push_code("switch ( %s ) {" % expr)

    def begin_switch_case(self, pattern):
        if pattern is None:
            self.push_code("default:")
        else:
            self.push_code("case %s:" % pattern)

    def end_switch_case(self):
        self.push_code("break;")

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

    def convert_constant(self, value):
        if value is None:
            return "null"
        if isinstance(value, bool):
            return str(value).lower()
        return repr(value)

    def convert_name(self, name, annotation):
        if self.in_method and name == "self":
            return "this"
        if name == "math":
            return "Math"
        if name == "NVector":
            return "Vector"
        if name in ("min", "max"):
            return "Math." + name
        if name == "float" or name == "int":
            return "number" if annotation else "Number"
        return self.camel_snake(name)

    def expr_func(self, name, args):
        ts_code = name
        if name[0].isupper() and name.isalnum():
            ts_code = "new %s" % name
        ts_code += "("
        ts_code += ", ".join(args)
        ts_code += ")"
        return ts_code

    def expr_attribute(self, object, member):
        if object == "Math":
            if member == "pi":
                member = member.upper()
        return "%s.%s" % (object, self.camel_snake(member))

    def other_expression(self, value, annotation):
        if isinstance(value, ast.Compare):
            all = []
            left = self.expression_to_string(value.left, annotation)
            for cmp, op in zip(value.comparators, value.ops):
                right = self.expression_to_string(cmp, annotation)
                all.append("%s %s %s" % (left, self.expression_to_string(op, annotation), right))
                left = right
            if len(all) == 1:
                return all[0]
            return "(%s)" % " && ".join(all)
        if isinstance(value, (ast.Tuple, ast.List)):
            return "[%s]" % ", ".join(self.expression_to_string(v, annotation) for v in value.elts)
        if isinstance(value, ast.MatchValue):
            return self.expression_to_string(value.value, annotation)
        if isinstance(value, ast.MatchAs):
            return value.name
        if isinstance(value, ast.Subscript):
            if isinstance(value.slice, ast.Slice):
                slice = value.slice
                args = ", ".join(self.expression_to_string(v, annotation) if v is not None else "undefined" for v in [slice.lower, slice.upper])
                return "%s.slice(%s)" % (self.expression_to_string(value.value, annotation), args)
            return "%s[%s]" % self.values_to_string(value.value, value.slice, annotation=annotation)
        if isinstance(value, ast.Set):
            return "new Set([%s])" % ", ".join(self.expression_to_string(v, annotation) for v in value.elts)
        if isinstance(value, ast.Dict):
            return "{%s}" % ", ".join("%s: %s" % self.values_to_string(*it, annotation=annotation) for it in zip(value.keys, value.values))
        if isinstance(value, ast.IfExp):
            return "%s ? %s : %s" % self.values_to_string(value.test, value.body, value.orelse, annotation=annotation)
        if isinstance(value, ast.Starred):
            return "...%s" % self.expression_to_string(value.value, annotation)
        return self.unknown(value, True)

    def format_doc_comment(self, comment):
        self.push_code("/**")
        for line in comment:
            self.push_code(" * " + line)
        self.push_code(" */")

    def format_comment(self, value):
        if len(value) > 1:
            self.push_code("/*")
            for line in value:
                self.push_code(line)
            self.push_code("*/")
        elif value:
            self.push_code("// " + value[0])
        else:
            self.push_code("")

    def expression_statement(self, v):
        self.push_code(v + ";")

    def convert_line_comment(self, comment):
        return "// " + comment
