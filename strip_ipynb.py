#!/usr/bin/env python
import json
import sys

files = sys.argv[1:]


def strip_output_from_cell(cell):
    """
    Remove variable fields such as outputs, prompt_number/execution_count from an IPython notebook.
    This allows a cleaner versioning with diffs only showing modifications of input cells.
    """
    if 'outputs' in cell:
        cell['outputs'] = []
    if 'prompt_number' in cell:
        del cell['prompt_number']
    if 'execution_count' in cell:
        cell['execution_count'] = None


def clean_notebook(file):
    notebook = json.load(open(file, 'r'))
    cells = notebook['worksheets'][0]['cells'] if 'worksheets' in notebook else notebook['cells']
    for cell in cells:
        strip_output_from_cell(cell)
    json.dump(notebook, open(file, 'w'), sort_keys=True, indent=2, separators=(',', ': '))


for file in files:
    clean_notebook(file)
