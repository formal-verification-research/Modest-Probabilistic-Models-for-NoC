# Contributing

To contribute new research, follow the setup steps below, then please create a new branch and open a pull-request with a detailed description of the added research.

## Setup

1. Install the [Modest Toolset](https://www.modestchecker.net/).
2. Clone this repository.
3. Set up the necessary Python tooling (see below).

### Setting Up the Python Environment

#### Creating a Virtual Environment (New Machine)

Create a new virtual environment using the following.

```bash
python -m venv .venv
```

And then activate it.

```bash
source .venv/bin/activate
```

#### Initial Setup (New Machine)

To reproduce the environment and link the internal Tool library, activate your virtual environment and run:

```bash
# Install external libraries (numpy, etc.)
pip install -r requirements.txt
```

```bash
# Link the local source code in "editable" mode
pip install -e .
```

#### Updating Dependencies

If you install a new package, update requirements.txt to freeze the versions. Use the command below to exclude the local project path (-e file://...) and keep the build portable:

```bash
# Generate new requirements, and remove local packages
pip freeze | grep -v "\-e file" > requirements.txt
```
