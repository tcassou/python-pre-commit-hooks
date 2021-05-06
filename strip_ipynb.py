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

    return modified, cell


def get_notebook_cells(notebook):
    """Retrieve notebook cells depending on the version/structure."""
    return notebook['worksheets'][0]['cells'] if 'worksheets' in notebook else notebook['cells']


def set_notebook_cells(notebook, celles):
    """Set notebook cells the right way depending on the version/structure."""
    if 'worksheets' in notebook:
        notebook['worksheets'][0]['cells'] = cells
    else:
        notebook['cells'] = cells


def clean_notebook(file):
    """
    Go through all notebook cells and strip undesired attributes. Write the file back if it was modified.
    """
    notebook = json.load(open(file, 'r'))

    modif_cells = []
    clean_cells = []
    for cell in get_notebook_cells(notebook):
        modified, clean_cell = strip_output_from_cell(cell)
        fixed_cells.append(modified)
        clean_cells.append(clean_cell)

    if any(modif_cells):
        print(f"Fixing {file}")
        set_notebook_cells(notebook, clean_cells)
        with open(file, 'w') as outfile:
            json.dump(notebook, outfile, sort_keys=True, indent=1, separators=(',', ': '))
            outfile.write('\n')


if __name__ == "__main__":
    files = sys.argv[1:]
    for file in files:
        clean_notebook(file)
