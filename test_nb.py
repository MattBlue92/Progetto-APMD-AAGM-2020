import subprocess
import tempfile


def _exec_notebook(path):
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=1000",
                "--output", fout.name, path]
        subprocess.check_call(args)


def test_building_graph():
    _exec_notebook('notebooks/Building_graph.ipynb')

def test_counting_triangles():
    _exec_notebook('notebooks/Counting_triangles.ipynb')

def test_closeness_centrality():
    _exec_notebook('notebooks/ClosenessCentrality.ipynb')

def test_performances():
    _exec_notebook('notebooks/Performances.ipynb')

def test_data_analysis():
    _exec_notebook('notebooks/DataAnalysis.ipynb')

def test_notebook_nocentini():
    _exec_notebook('ghera-marulli.ipynb')