# JupyterLab Open Warning

[![PyPI Latest Release](https://img.shields.io/pypi/v/jupyterlab-open-warning)](https://pypi.org/project/jupyterlab-open-warning/)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/jupyterlab-open-warning)](https://pypi.org/project/jupyterlab-open-warning/)
[![License](https://img.shields.io/pypi/l/jupyterlab-open-warning)](https://github.com/PainterQubits/jupyterlab-open-warning/blob/main/LICENSE)
[![CI](https://github.com/PainterQubits/jupyterlab-open-warning/actions/workflows/ci.yml/badge.svg)](https://github.com/PainterQubits/jupyterlab-open-warning/actions/workflows/ci.yml)

JupyterLab extension to display a warning dialog when opening a file that another user has open.

## Installation

Install the latest version of JupyterLab Open Warning using pip:

```
pip install -U jupyterlab-open-warning
```

This extension should run alongside
[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)
version 4 and the
[JupyterLab Real-Time Collaboration](https://jupyterlab-realtime-collaboration.readthedocs.io/en/latest/)
extension.

To automatically install along with Real-Time Collaboration, use the `rtc` extra:

```
pip install -U "jupyterlab-open-warning[rtc]"
```

While the Real-Time Collaboration extension is required in order to display open warning
dialogs, the collaboration functionality can be disabled by running JupyterLab with the
following option:

```
jupyter lab --YDocExtension.disable_rtc True
```

## Development

To develop, the following dependencies must be installed:

- [Python](https://www.python.org/downloads/)
- [Hatch](https://hatch.pypa.io/latest/install/)
- [Node.js](https://nodejs.org/en/download)

To build the extension and start up a JupyterLab server for development, run:

```bash
hatch run dev
```

When the source code changes, the extension should be automatically rebuilt, and the
updated extension will be used when the page is reloaded.

> [!NOTE]  
> On Windows, symbolic links must be activated for `hatch run dev` to work. On Windows 10
> or above, this can be done by
> [activating developer mode](https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development).
>
> Alternatively, you can run
>
> ```bash
> hatch run clean
> hatch env remove default
> hatch run jupyter lab
> ```
>
> to completely reinstall the extension and start JupyterLab each time the source code
> changes.
