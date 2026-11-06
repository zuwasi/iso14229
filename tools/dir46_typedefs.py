#!/usr/bin/env python3
"""MISRA C:2025 Dir 4.6 batch fix: replace standard basic integer types with
stdint.h typedefs.

Rewrites bare `int`, `unsigned`, `short`, `long` (and `unsigned int`,
`unsigned short`, `unsigned long`) as fixed-width stdint typedefs in the
source files given on the command line. Skips comments, strings, and
identifiers that merely contain the words.

Mapping (LP64 Linux / typical embedded targets where int == 32 bits):
    int            -> int32_t
    unsigned int   -> uint32_t
    unsigned       -> uint32_t
    unsigned short -> uint16_t
    short          -> int16_t
    unsigned long  -> uint64_t
    long           -> int64_t

Type-preserving on all targets where those basic types have the sizes above;
verify with the compiler before shipping.
"""
import re
import sys

MAPPING = [
    (re.compile(r'\bunsigned\s+int\b'), 'uint32_t'),
    (re.compile(r'\bunsigned\s+short\b'), 'uint16_t'),
    (re.compile(r'\bunsigned\s+long\b'), 'uint64_t'),
    (re.compile(r'\bunsigned\b'), 'uint32_t'),
    (re.compile(r'\blong\s+long\b'), 'int64_t'),
    (re.compile(r'\bint\b'), 'int32_t'),
    (re.compile(r'\bshort\b'), 'int16_t'),
    (re.compile(r'\blong\b'), 'int64_t'),
]

def mask_spans(text):
    """Return a bytearray mask: 1 where text is code, 0 in comments/strings."""
    mask = bytearray([1]) * len(text)
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ''
        if ch == '/' and nxt == '/':
            j = text.find('\n', i)
            j = n if j < 0 else j
            for k in range(i, j):
                mask[k] = 0
            i = j
        elif ch == '/' and nxt == '*':
            j = text.find('*/', i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                mask[k] = 0
            i = j
        elif ch in '"\'':
            quote = ch
            k = i + 1
            while k < n:
                if text[k] == '\\':
                    k += 2
                    continue
                if text[k] == quote:
                    k += 1
                    break
                k += 1
            for m in range(i, k):
                mask[m] = 0
            i = k
        else:
            i += 1
    return mask

def fix(text):
    mask = mask_spans(text)
    # protect masked regions by splitting into code/comment runs per pattern pass
    for pat, repl in MAPPING:
        out = []
        i = 0
        for m in pat.finditer(text):
            s, e = m.span()
            if 0 in mask[s:e]:
                continue  # overlaps a comment/string, skip
            if s >= i:
                out.append(text[i:s])
                out.append(repl)
                i = e
        out.append(text[i:])
        text = ''.join(out)
        mask = mask_spans(text)  # lengths changed, recompute
    return text

def main():
    for path in sys.argv[1:]:
        with open(path, encoding='utf-8') as f:
            src = f.read()
        fixed = fix(src)
        if fixed != src:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed)
            print(f'fixed {path}')

if __name__ == '__main__':
    main()
