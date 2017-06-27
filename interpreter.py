#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Creative Name

A language that probably hopefully does something.

Sumant Bhaskaruni
v0.2.0 (basically, don't use it)
"""

import argparse
import collections
import math
import re

commands = {
    '+':
        lambda stacks, stk_no, stack: stack.push(stack.pop() + stack.pop()),
    '-':
        lambda stacks, stk_no, stack: stack.push(stack.pop() - stack.pop()),
    '×':
        lambda stacks, stk_no, stack: stack.push(stack.pop() * stack.pop()),
    '÷':
        lambda stacks, stk_no, stack: stack.push(stack.pop() / stack.pop()),
    '%':
        lambda stacks, stk_no, stack: stack.push(stack.pop() % stack.pop()),
    '*':
        lambda stacks, stk_no, stack: stack.push(stack.pop() ** stack.pop()),
    '√':
        lambda stacks, stk_no, stack: stack.push(math.sqrt(stack.pop())),
    '↓':
        lambda stacks, stk_no, stack: print(stack.pop(), end = ''),
    '↑':
        lambda stacks, stk_no, stack: stack.pop(),
    '¬':
        lambda stacks, stk_no, stack: stack.push(int(not stack.pop())),
    '∧':
        lambda stacks, stk_no, stack: stack.push(int(stack.pop() and stack.pop())),
    '∨':
        lambda stacks, stk_no, stack: stack.push(int(stack.pop() or stack.pop())),
    'i':
        lambda stacks, stk_no, stack: stack.push(int(stack.pop())),
    'f':
        lambda stacks, stk_no, stack: stack.push(float(stack.pop())),
    's':
        lambda stacks, stk_no, stack: stack.push(str(stack.pop())),
    'c':
        lambda stacks, stk_no, stack: stack.push(chr(stack.pop())),
    'o':
        lambda stacks, stk_no, stack: stack.push(ord(stack.pop())),
    '⊢':
        lambda stacks, stk_no, stack: stack.push(stack.pop()[stack.pop():]),
    '⊣':
        lambda stacks, stk_no, stack: stack.push(stack.pop()[:stack.pop()]),
    '⟛':
        lambda stacks, stk_no, stack: stack.push(stack.pop()[::stack.pop()]),
    '&':
        lambda stacks, stk_no, stack: stack.push(stack.pop() & stack.pop()),
    '|':
        lambda stacks, stk_no, stack: stack.push(stack.pop() | stack.pop()),
    '^':
        lambda stacks, stk_no, stack: stack.push(stack.pop() ^ stack.pop()),
    '~':
        lambda stacks, stk_no, stack: stack.push(~ stack.pop()),
    '«':
        lambda stacks, stk_no, stack: stack.push(stack.pop() << stack.pop()),
    '»':
        lambda stacks, stk_no, stack: stack.push(stack.pop() >> stack.pop()),
    ':':
        lambda stacks, stk_no, stack: stack.push(stack.peek()),
    '<':
        lambda stacks, stk_no, stack: stack.push(stack.pop() < stack.pop()),
    '>':
        lambda stacks, stk_no, stack: stack.push(stack.pop() > stack.pop()),
    '=':
        lambda stacks, stk_no, stack: stack.push(stack.pop() == stack.pop())
}

class UnknownCommand(Exception):
    """An Exception that is raised on an invalid command."""

    def __init__(self, command):
        super(UnknownCommand,
              self).__init__('Unknown command: {}'.format(command))


class Stack:

    def __init__(self, items = []):
        self.items = items

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def __len__(self):
        return len(self.items)


def tokenize(code):
    """Splits the code into tokens.

    Positional arguments:
        code (str): the code to be tokenized

    Returns:
        tokens (list): a list of all the tokens in the code
    """
s    Token = collections.namedtuple('Token', ['type', 'value'])

    token_specs = [
        ('string', r'"([^\\]|\\[\s\S])*?"'),
        ('number', r'-?\d+(\.\d*)?'),
        ('noop', r'[ \t\n]+'),
        ('command', r'.')
    ]
    token_regex = '|'.join(r'(?P<{}>{})'.format(*i) for i in token_specs)
    tokens = []

    for token in re.finditer(token_regex, code):
        _type = token.lastgroup
        value = token.group(_type)

        if _type == 'noop':
            pass
        elif _type == 'command':
            if value in commands:
                tokens.append(Token(_type, value))
            else:
                raise UnknownCommand(value)
        else:
            tokens.append(Token(_type, value))

    return tokens


def run(code, args):
    tokens = tokenize(code)
    stacks = [Stack()]
    stk_no = 0

    for arg in args:
        if re.match(r'-?\d+$', arg):
            stacks[stk_no].push(int(arg))
        elif re.match(r'-?\d+(\.\d*)?$', arg):
            stacks[stk_no].push(float(arg))
        else:
            stacks[stk_no].push(arg)

    for token in tokens:
        if token[0] == 'number':
            try:
                stacks[stk_no].push(int(token[1]))
            except ValueError:
                stacks[stk_no].push(float(token[1]))
        elif token[0] == 'string':
            stacks[stk_no].push(token[1][1:-1])
        else:
            commands[token[1]](stacks, stk_no, stacks[stk_no])

    try:
        print(stacks.pop())
    except IndexError:
        print()

def main():
    parser = argparse.ArgumentParser(
        description = 'An interpreter for the Creative Name language.')
    parser.add_argument('file', help = 'program read from script file',
                        type = open)
    parser.add_argument('args', help = 'arguments for the script',
                        nargs = argparse.REMAINDER)

    arguments = parser.parse_args()
    with arguments.file as f:
        run(f.read(), arguments.args)


if __name__ == '__main__':
    main()
