"""
Run all cells of the notebook one by one, reporting success/failure for each.
Uses nbclient to execute cells in order.
"""
import os, sys
os.environ["MPLBACKEND"] = "Agg"

import nbformat
from nbclient import NotebookClient

NB_PATH = "Data_Exploration_and_Visualization_Tips.ipynb"

print(f"Loading notebook: {NB_PATH}")
nb = nbformat.read(NB_PATH, as_version=4)

# Filter only code cells
code_cells = [(i, c) for i, c in enumerate(nb.cells) if c.cell_type == "code"]
print(f"Found {len(code_cells)} code cells to execute.\n")

client = NotebookClient(
    nb,
    timeout=120,
    kernel_name="python3",
    resources={"metadata": {"path": os.path.dirname(os.path.abspath(NB_PATH)) or "."}},
)

# Start kernel
with client.setup_kernel():
    for idx, (cell_index, cell) in enumerate(code_cells, 1):
        src = cell.source.strip()
        preview = src[:120].replace("\n", " | ")
        print(f"--- Cell {idx}/{len(code_cells)} (notebook cell #{cell_index}) ---")
        print(f"    Preview: {preview}...")
        try:
            client.execute_cell(cell, cell_index)
            print(f"    [OK] SUCCESS\n")
        except Exception as e:
            err_msg = str(e)
            # Print a manageable error
            lines = err_msg.split("\n")
            short = [l for l in lines if l.strip() and not l.startswith("---")]
            if short:
                # Print last few meaningful lines
                for line in short[-5:]:
                    print(f"    {line.strip()}")
            else:
                print(f"    [FAIL] ERROR: {err_msg[:300]}")
            print()

print("\n=== All cells processed ===")
