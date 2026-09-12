# ECMP26 SIRF Workshop

Workshop material for the **ECMP26 SIRF workshop**.

The exercises use [SIRF](https://github.com/SyneRBI/SIRF) together with the [SIMIND Python Connector](https://github.com/samdporter/simind-python-connector) and [phantomgen](https://github.com/varzakis/phantomgen).

The recommended environment is based on the SyneRBI SIRF Docker image:

```text
ghcr.io/synerbi/sirf:latest
```

## Requirements

Before starting, install:

* [Docker](https://docs.docker.com/engine/install/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [VS Code Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
* Git

The workshop has been designed to run inside the SIRF Docker environment rather than requiring SIRF and its dependencies to be installed directly on the host computer.

## 1. Clone the workshop repository

Clone this repository:

```bash
git clone <WORKSHOP-REPOSITORY-URL>
cd <WORKSHOP-REPOSITORY>
```

Open the repository in VS Code:

```bash
code .
```

## 2. Obtain the SIRF Docker image

Pull the SyneRBI SIRF image:

```bash
docker pull ghcr.io/synerbi/sirf:latest
```

You can confirm that the image is available with:

```bash
docker images
```

You should see an entry corresponding to:

```text
ghcr.io/synerbi/sirf    latest
```

## 3. Open the workshop using VS Code Dev Containers

This repository contains a `.devcontainer/devcontainer.json` configuration that uses the SIRF Docker image.

In VS Code, open the Command Palette:

```text
Ctrl+Shift+P
```

and select:

```text
Dev Containers: Reopen in Container
```

VS Code will start a container based on:

```text
ghcr.io/synerbi/sirf:latest
```

and mount the workshop repository inside the container.

The workshop directory is available inside the container at:

```text
/home/jovyan/sirf-demo
```

A VS Code terminal should therefore show a prompt similar to:

```text
jovyan@ECMP26:/home/jovyan/sirf-demo$
```

## 4. Install phantomgen

The workshop uses the `phantomgen` package for generating numerical NEMA/IEC nuclear medicine phantoms.

Clone the package inside the container:

```bash
mkdir -p /home/jovyan/sirf-demo/.packages
cd /home/jovyan/sirf-demo/.packages

git clone https://github.com/varzakis/phantomgen.git
cd phantomgen

python -m pip install -e .
```

The editable installation allows Python to use the package directly from the cloned source directory.

Check the installation with:

```bash
python -m pip show phantomgen
```

or:

```bash
python -c "import phantomgen; print(phantomgen.__file__)"
```

## 5. Install the SIMIND Python Connector

Clone the SIMIND Python Connector:

```bash
cd /home/jovyan/sirf-demo/.packages

git clone https://github.com/samdporter/simind-python-connector.git
cd simind-python-connector

python -m pip install -e .
```

Check the installation:

```bash
python -m pip show simind-python-connector
```

and:

```bash
python -c "import simind_python_connector; print(simind_python_connector.__file__)"
```

The SIRF Docker image already provides the SIRF/STIR environment required by the workshop.

## 6. SIMIND

The `simind-python-connector` package provides the Python interface to SIMIND, but **does not distribute the SIMIND Monte Carlo program itself**.

SIMIND therefore needs to be installed separately.

SIMIND is developed by the Medical Radiation Physics group at Lund University:

https://www.msf.lu.se/en/research/simind-monte-carlo-program

Follow the SIMIND installation instructions before running exercises that perform Monte Carlo simulations.

The workshop expects the SIMIND executable and its associated data files to be accessible from within the container.

Check that SIMIND is available with:

```bash
which simind
```

and, where appropriate:

```bash
echo $SMC_DIR
```

## 7. Check the environment

Before starting the exercises, verify that the main components can be imported:

```bash
python -c "import sirf; print('SIRF OK')"
python -c "import phantomgen; print('phantomgen OK')"
python -c "import simind_python_connector; print('SIMIND connector OK')"
```

You can inspect the Python environment with:

```bash
python -m pip list
```

## Repository structure

The repository is organised approximately as follows:

```text
ECMP26_SIRF_demo/
├── .devcontainer/
│   └── devcontainer.json
│
├── .packages/
│   ├── phantomgen/
│   └── simind-python-connector/
│
├── SIRF-demo-1/
│   ├── ...
│   └── workshop scripts and data
│
├── SIRF-demo-1/
│   ├── ...
│   └── workshop scripts and data
|
├── README.md
└── .gitignore
```

## Updating the external packages

Because the packages are installed as editable Git repositories, they can be updated independently.

For `phantomgen`:

```bash
cd /home/jovyan/sirf-demo/.packages/phantomgen
git pull
```

For the SIMIND Python Connector:

```bash
cd /home/jovyan/sirf-demo/.packages/simind-python-connector
git pull
```

## Troubleshooting

### Check which Python is being used

```bash
which python
python --version
python -m pip --version
```

All workshop commands should be executed from inside the SIRF container.

### Package cannot be imported

Check whether it is installed:

```bash
python -m pip list
```

and inspect its installation location:

```bash
python -m pip show <package-name>
```

### SIMIND cannot be found

Check:

```bash
which simind
```

and:

```bash
echo $SMC_DIR
```

The SIMIND executable must be available on `PATH`, and the SIMIND data directory must be configured correctly.

## Software used

* [SIRF](https://github.com/SyneRBI/SIRF) — Synergistic Image Reconstruction Framework
* [phantomgen](https://github.com/varzakis/phantomgen) — numerical NEMA/IEC nuclear medicine phantom generation
* [simind-python-connector](https://github.com/samdporter/simind-python-connector) — Python interface and adaptors for the SIMIND Monte Carlo simulator
* [SIMIND](https://www.msf.lu.se/en/research/simind-monte-carlo-program) — Monte Carlo simulation software for SPECT

## Licence

The workshop material and each external software package are subject to their respective licences. Refer to the individual software repositories for licence information.
