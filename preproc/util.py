# coding=utf-8



from __future__ import print_function
import ast
import sys

import itertools

# Commented out for Python 3
# reload(sys)
# sys.setdefaultencoding('utf-8')

import token as tk
from tokenize import generate_tokens

try:
  from StringIO import StringIO
except:
  from io import StringIO


def detokenize_code(code_tokens):
    newline_pos = [i for i, x in enumerate(code_tokens) if x == '\n']
    newline_pos.append(len(code_tokens))
    start = 0
    lines = []
    for i in newline_pos:
        line = ' '.join(code_tokens[start: i])
        start = i + 1
        lines.append(line)

    code = '\n'.join(lines).strip()

    return code


def encode_tokenized_code(code_tokens):
    tokens = []
    for token in code_tokens:
        if token == '\t':
            tokens.append('_TAB_')
        elif token == '\n':
            tokens.append('_NEWLINE_')


def get_encoded_code_tokens(code):
    code = code.strip()
    print(code)
    token_stream = generate_tokens(StringIO(code).readline)
    tokens = []
    indent_level = 0
    new_line = False

    for toknum, tokval, (srow, scol), (erow, ecol), _ in token_stream:
        if toknum == tk.NEWLINE:
            tokens.append('#NEWLINE#')
            new_line = True
        elif toknum == tk.INDENT:
            indent_level += 1
            # new_line = False
            # for i in range(indent_level):
            #     tokens.append('#INDENT#')
        elif toknum == tk.STRING:
            tokens.append(tokval.replace(' ', '#SPACE#').replace('\t', '#TAB#').replace('\r\n', '#NEWLINE#').replace('\n', '#NEWLINE#'))
        elif toknum == tk.DEDENT:
            indent_level -= 1
            # for i in range(indent_level):
            #     tokens.append('#INDENT#')
            # new_line = False
        else:
            tokval = tokval.replace('\n', '#NEWLINE#')
            if new_line:
                for i in range(indent_level):
                    tokens.append('#INDENT#')

            new_line = False
            tokens.append(tokval)

    # remove ending None
    if len(tokens[-1]) == 0:
        tokens = tokens[:-1]

    if '\n' in tokval:
        pass

    return tokens


def tokenize(code):
    token_stream = generate_tokens(StringIO(code).readline)
    tokens = []
    for toknum, tokval, (srow, scol), (erow, ecol), _ in token_stream:
        if toknum == tk.ENDMARKER:
            break

        tokens.append(tokval)

    return tokens


def compare_ast(node1, node2):
    # Python 3
    # if not isinstance(node1, str) and not isinstance(node1, unicode):
    if not isinstance(node1, str):
        if type(node1) is not type(node2):
            return False
    if isinstance(node1, ast.AST):
        for k, v in list(vars(node1).items()):
            if k in ('lineno', 'col_offset', 'ctx'):
                continue
            if not compare_ast(v, getattr(node2, k)):
                return False
        return True
    elif isinstance(node1, list):
        return all(itertools.starmap(compare_ast, zip(node1, node2)))
    else:
        return node1 == node2


def encoded_code_tokens_to_code(encoded_tokens, indent=' '):
    decoded_tokens = []
    for i in range(len(encoded_tokens)):
        token = encoded_tokens[i]
        token = token.replace('#TAB#', '\t').replace('#SPACE#', ' ')

        if token == '#INDENT#': decoded_tokens.append(indent)
        elif token == '#NEWLINE#': decoded_tokens.append('\n')
        else:
            token = token.replace('#NEWLINE#', '\n')
            decoded_tokens.append(token)
            decoded_tokens.append(' ')

    code = ''.join(decoded_tokens).strip()

    return code


def find_sub_sequence(sequence, query_seq):
    for i in range(len(sequence)):
        if sequence[i: len(query_seq) + i] == query_seq:
            return i, len(query_seq) + i

    raise IndexError


def replace_sequence(sequence, old_seq, new_seq):
    matched = False
    for i in range(len(sequence)):
        if sequence[i: i + len(old_seq)] == old_seq:
            matched = True
            sequence[i:i + len(old_seq)] = new_seq
    return matched
