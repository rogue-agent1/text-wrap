#!/usr/bin/env python3
"""Text wrapping and formatting — word wrap, justify, indent, columns."""
import sys

def word_wrap(text, width=80):
    words = text.split()
    lines, current, length = [], [], 0
    for w in words:
        if length + len(w) + len(current) > width:
            lines.append(" ".join(current)); current = [w]; length = len(w)
        else:
            current.append(w); length += len(w)
    if current: lines.append(" ".join(current))
    return lines

def justify(text, width=80):
    lines = word_wrap(text, width); result = []
    for i, line in enumerate(lines):
        words = line.split()
        if i == len(lines) - 1 or len(words) == 1:
            result.append(line); continue
        total_spaces = width - sum(len(w) for w in words)
        gaps = len(words) - 1
        base = total_spaces // gaps; extra = total_spaces % gaps
        justified = ""
        for j, w in enumerate(words):
            justified += w
            if j < gaps: justified += " " * (base + (1 if j < extra else 0))
        result.append(justified)
    return result

NL = "\n"

def indent(text, prefix="  ", first_line=None):
    lines = text.split(NL)
    result = []
    for i, line in enumerate(lines):
        p = first_line if (i == 0 and first_line is not None) else prefix
        result.append(p + line)
    return NL.join(result)

def columnize(items, width=80, padding=2):
    if not items: return ""
    max_w = max(len(s) for s in items) + padding
    cols = max(1, width // max_w)
    rows = (len(items) + cols - 1) // cols
    lines = []
    for r in range(rows):
        line = ""
        for c in range(cols):
            idx = r + c * rows
            if idx < len(items): line += items[idx].ljust(max_w)
        lines.append(line.rstrip())
    return NL.join(lines)

def main():
    if len(sys.argv) < 2: print("Usage: text_wrap.py <demo|test>"); return
    if sys.argv[1] == "test":
        lines = word_wrap("the quick brown fox jumps over the lazy dog", 20)
        assert all(len(l) <= 20 for l in lines)
        assert " ".join(lines) == "the quick brown fox jumps over the lazy dog"
        j = justify("the quick brown fox jumps over the lazy dog", 20)
        assert len(j[0]) == 20
        assert j[-1] == "dog"
        i = indent("line1" + NL + "line2", ">> ")
        assert i == ">> line1" + NL + ">> line2"
        i2 = indent("first" + NL + "second", "  ", first_line="* ")
        assert i2.startswith("* first")
        c = columnize(["alpha","beta","gamma","delta","epsilon"], width=30, padding=2)
        assert len(c.split(NL)) >= 1
        assert word_wrap("", 80) == []
        assert columnize([], 80) == ""
        print("All tests passed!")
    else:
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        for line in justify(text, 40): print(line)

if __name__ == "__main__": main()
