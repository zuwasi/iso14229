#!/usr/bin/env python3
"""rule75_v1.py -- MISRA C:2025 Rule 7.5 fix script, v1 (value-preserving).

Applies two mechanical transforms to the given files, in place:

  1. Suffix removal:   UINT32_C(0xFFUL)  -> UINT32_C(0xFF)
  2. Minus relocation: INT32_C(-40)      -> (-INT32_C(40))

Excluded (reported to stdout, left untouched, routed to a human expert):

  * Signed minimum: INTn_C(-2147483648) / INTn_C(-9223372036854775808)
    cannot be rewritten as (-INTn_C(2147483648)); the compliant form
    is ((-INTn_C(2147483647))-1) and requires an expert decision.
  * Non-literal arguments: INTn_C(OTHER_MACRO), INTn_C(2+3), ...

Usage: rule75_v1.py FILE [FILE ...]
"""

import re
import sys

MACRO = r'(?:INT8|INT16|INT32|INT64|UINT8|UINT16|UINT32|UINT64)_C'

# Signed-minimum values per macro family: the magnitude does not fit the
# positive range of the signed type, so minus relocation is not safe.
SIGNED_MIN = {
    'INT8_C': 128, 'INT16_C': 32768, 'INT32_C': 2147483648,
    'INT64_C': 9223372036854775808,
}

RE_SUFFIX = re.compile(rf'\b({MACRO})\(\s*([0-9]+|0[xX][0-9a-fA-F]+)\s*[uUlL]+\s*\)')
RE_NEGATIVE = re.compile(rf'\b({MACRO})\(\s*-\s*([0-9]+)\s*\)')
RE_NONLITERAL = re.compile(rf'\b{MACRO}\(\s*([^)\s][^)]*)\)')


def transform(text, path, report):
    def fix_suffix(m):
        report.append(f'{path}: suffix removed: {m.group(0)}')
        return f'{m.group(1)}({m.group(2)})'

    def fix_negative(m):
        macro, digits = m.group(1), m.group(2)
        value = int(digits, 0)
        if value == SIGNED_MIN.get(macro):
            report.append(f'{path}: SKIPPED, signed minimum, expert fix needed: {m.group(0)}')
            return m.group(0)
        report.append(f'{path}: minus relocated: {m.group(0)} -> (-{macro}({digits}))')
        return f'(-{macro}({digits}))'

    text = RE_SUFFIX.sub(fix_suffix, text)
    text = RE_NEGATIVE.sub(fix_negative, text)

    # Anything still holding a non-literal argument is reported, not touched.
    for m in RE_NONLITERAL.finditer(text):
        arg = m.group(1).strip()
        if arg.startswith('-'):
            continue  # signed minimum, already reported
        if not re.fullmatch(r'[0-9]+|0[xX][0-9a-fA-F]+', arg):
            report.append(f'{path}: SKIPPED, non-literal argument, expert fix needed: {m.group(0)}')
    return text


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    report = []
    for path in argv[1:]:
        with open(path, encoding='utf-8') as fh:
            original = fh.read()
        updated = transform(original, path, report)
        if updated != original:
            with open(path, 'w', encoding='utf-8', newline='') as fh:
                fh.write(updated)
    print('\n'.join(report) if report else 'no matching occurrences')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
