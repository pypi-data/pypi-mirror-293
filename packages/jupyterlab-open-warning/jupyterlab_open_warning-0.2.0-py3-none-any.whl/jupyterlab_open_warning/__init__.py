"""
JupyterLab extension to display a warning dialog when opening a file that another user
has open.
"""


# Required for symlinking in development ("jupyter labextension develop --overwrite .")
def _jupyter_labextension_paths() -> list[dict[str, str]]:
    return [{"src": "../labextension", "dest": "jupyterlab-open-warning"}]
