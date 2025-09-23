#!/usr/bin/env python3
import sys

"""
A tiny demo pattern: prints lines from the input that look "wise" (heuristic: contain the word 'should' or 'always').
Purpose: simple, easy-to-read code for learning.
"""

def extract_wisdom(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if 'should' in line.lower() or 'always' in line.lower():
                print(line.strip())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: extract_wisdom.py <input_file>')
        sys.exit(1)
    extract_wisdom(sys.argv[1])

