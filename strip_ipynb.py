#!/usr/bin/env python
import json
import sys



def strip_output_from_cell(cell):
    """
    Remove variable fields such as outputs, prompt_number/execution_count from an IPython notebook.
    This allows a cleaner versioning with diffs only showing modifications of input cells.
    """
    modified = False
    if cell.get('outputs', []):
        cell['outputs'] = []
        modified = True

    if cell.get('prompt_number', None):
        cell['prompt_number'] = None
        modified = True

    if cell.get('execution_count', None):
        cell['execution_count'] = None
        modified = True

    return modified


def clean_notebook(file):
    notebook = json.load(open(file, 'r'))
    cells = notebook['worksheets'][0]['cells'] if 'worksheets' in notebook else notebook['cells']

    if any(strip_output_from_cell(cell) for cell in cells):
        print(f"Fixing {file}")
        json.dump(notebook, open(file, 'w'), sort_keys=True, indent=1, separators=(',', ': '))


if __name__ == "__main__":
    files = sys.argv[1:]
    for file in files:
        clean_notebook(file)
