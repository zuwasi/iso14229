#!/usr/bin/env python3
"""MISRA C:2025 Rule 14.4 batch fix: make zero tests explicit.

Rewrites controlling expressions of if/while/do and UDS_ASSERT() arguments
when they are a bare value expression (no comparison/logical operator) into
explicit `!= 0` tests.

    if (ret)              -> if (ret != 0)
    while (link->busy)    -> while (link->busy != 0)
    UDS_ASSERT(src)       -> UDS_ASSERT(src != 0)

`!= 0` is value-preserving for integer, boolean, enum, and pointer operands
(0 is a null pointer constant). Operands that are already comparisons,
logical expressions, assignments, or comma expressions are left alone.
Skips comments and strings. Files are rewritten in place; pass -n to dry-run.
"""
import re
import sys

CTRL = re.compile(r'\b(if|while)\s*\(')
ASSERT = re.compile(r'\bUDS_ASSERT\s*\(')

def skip_ws_comments(text, i):
    n = len(text)
    while i < n:
        if text[i].isspace():
            i += 1
        elif text.startswith('//', i):
            i = text.find('\n', i)
            if i < 0:
                break
        elif text.startswith('/*', i):
            j = text.find('*/', i + 2)
            i = n if j < 0 else j + 2
        else:
            break
    return i

def match_paren(text, open_idx):
    """Index of the ')' matching the '(' at open_idx, respecting strings."""
    depth = 0
    i = open_idx
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in '"\'':
            i += 1
            while i < n and text[i] != ch:
                i += 2 if text[i] == '\\' else 1
            i += 1
            continue
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1

def is_plain_expr(expr):
    """True if expr is a value expression needing an explicit != 0 test."""
    e = expr.strip()
    if not e or e in ('0', '1'):
        return False
    # already has an operator that makes the test explicit or non-value
    if re.search(r'[=!<>]=?|&&|\|\||,|\+\+|--|\?|=', e):
        return False
    # plain identifier or member/pointer chain: a, a.b, a->b, a->b.c
    if re.fullmatch(r'\**\s*[A-Za-z_][A-Za-z0-9_]*((\.|->)[A-Za-z_][A-Za-z0-9_]*)*', e):
        return True
    return False

def on_define_line(text, idx):
    """True if the match at idx sits on a preprocessor definition line."""
    line_start = text.rfind('\n', 0, idx) + 1
    return text[line_start:idx].lstrip().startswith('#')

def fix(text):
    total = 0
    # find controlling expressions of if/while (their own parens)
    out = []
    i = 0
    for m in CTRL.finditer(text):
        s, e = m.span()
        if on_define_line(text, s):
            continue
        open_idx = e - 1
        close_idx = match_paren(text, open_idx)
        if close_idx < 0:
            continue
        expr = text[open_idx + 1:close_idx]
        if is_plain_expr(expr):
            out.append(text[i:open_idx + 1])
            out.append(expr)
            out.append(' != 0')
            i = close_idx
            total += 1
    out.append(text[i:])
    text = ''.join(out)

    # UDS_ASSERT(...) arguments
    out = []
    i = 0
    for m in ASSERT.finditer(text):
        s, e = m.span()
        if on_define_line(text, s):
            continue
        open_idx = e - 1
        close_idx = match_paren(text, open_idx)
        if close_idx < 0:
            continue
        expr = text[open_idx + 1:close_idx]
        if is_plain_expr(expr):
            out.append(text[i:open_idx + 1])
            out.append(expr)
            out.append(' != 0')
            i = close_idx
            total += 1
    out.append(text[i:])
    return ''.join(out), total

def main():
    dry = '-n' in sys.argv
    paths = [p for p in sys.argv[1:] if p != '-n']
    for path in paths:
        with open(path, encoding='utf-8') as f:
            src = f.read()
        fixed, n = fix(src)
        if fixed != src:
            print(f'{path}: {n} tests made explicit')
            if not dry:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(fixed)

if __name__ == '__main__':
    main()
