"""Harpy syntax highlighter lexer for Sphinx documentation.

Configures Pygments tokenization rules to support syntax highlighting of
Harpy source code in reStructuredText documentation.
"""

import pygments


class Lexer(pygments.lexer.RegexLexer):
    """Pygments Lexer for the Harpy programming language.

    Defines regular expression rules for matching Harpy grammar
    constructs, including keywords, primitive constants, decorators,
    numbers in various bases, strings, operators, and function calls.
    Manages state transitions between default expression parsing in
    'root', multiline comments enclosed in '|- ... -|', and inline
    assembly blocks inside 'assembly { ... }' to handle register
    variables and custom syntax scoping.
    """

    name: str = "Harpy"
    aliases: list[str] = ["harpy", "hrp"]
    filenames: list[str] = ["*.hrp"]
    tokens: dict[
        str,
        list[
            tuple[str, pygments.token._TokenType]
            | tuple[str, pygments.token._TokenType, str]
            | tuple[pygments.lexer.words, pygments.token._TokenType]
            | tuple[
                str,
                tuple[
                    pygments.token._TokenType,
                    pygments.token._TokenType,
                    pygments.token._TokenType,
                ],
            ]
        ],
    ] = {
        "root": [
            (r"\s+", pygments.token.Whitespace),
            (r"#.*$", pygments.token.Comment.Single),
            (r"\|-", pygments.token.Comment.Multiline, "comment"),
            (
                r"\bassembly\b(\s*)(\{)",
                pygments.lexer.bygroups(
                    pygments.token.Keyword,
                    pygments.token.Whitespace,
                    pygments.token.Punctuation,
                ),
                "assembly",
            ),
            (r'"""[\s\S]*?"""', pygments.token.String.Multiline),
            (r'"[^"]*"', pygments.token.String),
            (r"'[^']?'", pygments.token.String.Char),
            (
                r"\b\d[0-9_]*\.\d[0-9_]*([eE][+-]?[0-9_]+)?\b",
                pygments.token.Number.Float,
            ),
            (
                r"\b\d[0-9_]*[eE][+-]?[0-9_]+\b",
                pygments.token.Number.Float,
            ),
            (r"\b0x[0-9a-fA-F_]+\b", pygments.token.Number.Hex),
            (r"\b0b[01_]+\b", pygments.token.Number.Bin),
            (r"\b0o[0-7_]+\b", pygments.token.Number.Oct),
            (r"\b\d[0-9_]*\b", pygments.token.Number.Integer),
            (
                pygments.lexer.words(
                    (
                        "package",
                        "type",
                        "subtype",
                        "var",
                        "val",
                        "const",
                        "interface",
                        "implements",
                        "pub",
                        "priv",
                        "static",
                        "import",
                        "from",
                        "if",
                        "else",
                        "loop",
                        "while",
                        "for",
                        "match",
                        "break",
                        "continue",
                        "alias",
                        "restrict",
                        "fragment",
                        "defer",
                        "try",
                        "return",
                        "requires",
                        "ensures",
                        "fun",
                        "as",
                        "is",
                        "in",
                        "at",
                        "addr",
                    ),
                    suffix=r"\b",
                ),
                pygments.token.Keyword,
            ),
            (
                pygments.lexer.words(
                    ("true", "false", "null", "nothing"),
                    suffix=r"\b",
                ),
                pygments.token.Keyword.Constant,
            ),
            (r"@[a-zA-Z_]\w*", pygments.token.Name.Decorator),
            (r"\.[a-zA-Z_]\w*", pygments.token.Name.Property),
            (
                r"([a-zA-Z_]\w*)(\s*)(\()",
                pygments.lexer.bygroups(
                    pygments.token.Name.Function,
                    pygments.token.Whitespace,
                    pygments.token.Punctuation,
                ),
            ),
            (
                r"(->|=>|[\(\)\[\]\{\};,:\.])",
                pygments.token.Punctuation,
            ),
            (
                r"("
                r"<<<=|>>>="
                r"|<<<|>>>|<<=|>>=|===|!==|\.\.=|<=>|<->"
                r"|\+!|-!|\*!|/=\|\+=|-=|\*=|<<|>>"
                r"|:\?|&=|\|=|\^=|==|!=|<=|>=|&&|\|\||\^\^"
                r"|\.\?|\?\?|\.\.|~>"
                r"|<|>|\+|\-|\*|/|%|=|&|\||\^|~|!|\?"
                r")",
                pygments.token.Operator,
            ),
            (r"[a-zA-Z_]\w*", pygments.token.Name),
        ],
        "comment": [
            (r"-\|", pygments.token.Comment.Multiline, "#pop"),
            (r"[^|\-]+", pygments.token.Comment.Multiline),
            (r"[|\-]", pygments.token.Comment.Multiline),
        ],
        "assembly": [
            (r"\}", pygments.token.Punctuation, "#pop"),
            (r"\s+", pygments.token.Whitespace),
            (r"#.*$", pygments.token.Comment.Single),
            (r"%[a-zA-Z_]\w*", pygments.token.Name.Variable),
            (
                r"\b(0x[0-9a-fA-F_]+|0b[01_]+|0o[0-7_]+|\d[0-9_]*)\b",
                pygments.token.Number,
            ),
            (r'"[^"]*"', pygments.token.String),
            (r"[,:\[\]]", pygments.token.Punctuation),
            (r"[a-zA-Z_]\w*", pygments.token.Name),
        ],
    }
