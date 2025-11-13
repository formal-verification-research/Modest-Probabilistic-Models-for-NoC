# Formal NoC Verification

This repository is dedicated to probabilistic NoC verification using the
Modest toolset under Dr. Zhen Zhang at Utah State University.

## Repository Layout

Each sub-directory in this repository has it's own README file with
instructions on how to read, use, and extend the work in that
directory.

- [CurrentModels](./CurrentModels/): Contains probabilistic NoC models in
  Modest.
- [PreviousModels](./PreviousModels/): Contains previous works (both
  published and not published).
= [Tools](./Tools/): Contains tools for automating verification.

> [!NOTE]
> This repository used to be laid out quite differently. If you would
> like to see the old layout, check out the
> ["`pre-cleanup`"](https://github.com/formal-verification-research/Modest-Probabilistic-Models-for-NoC/releases/tag/pre-cleanup) tag.

## Contributing

Currently, there is really only one contributor to this repository at a
time, so they will contribute however they would like. However, to
maintain ease of use it's recommended that careful consideration to
file organization is made when working in this repository.

## Setting Up the Python Environment

### Creating a Virtual Environment (New Machine)

Create a new virtual environment using the following.

```bash
python -m venv .venv
```

And then activate it.

```bash
source .venv/bin/activate
```

### Initial Setup (New Machine)

To reproduce the environment and link the internal Tool library, activate your virtual environment and run:

```bash
# Install external libraries (numpy, etc.)
pip install -r requirements.txt
```

```bash
# Link the local source code in "editable" mode
pip install -e .
```

### Updating Dependencies

If you install a new package, update requirements.txt to freeze the versions. Use the command below to exclude the local project path (-e file://...) and keep the build portable:

```bash
# Generate new requirements, and remove local packages
pip freeze | grep -v "\-e file" > requirements.txt
```

## Related Works

These are some of the published papers that have come out of this work.

### Probabilistic Verification for Reliable Network-on-Chip System Design

```bibtex
@inproceedings{lewis_probabilistic_2019,
  title = {Probabilistic {{Verification}} for {{Reliable Network-on-Chip System Design}}},
  booktitle = {Formal {{Methods}} for {{Industrial Critical Systems}}},
  author = {Lewis, Benjamin and Hartmanns, Arnd and Basu, Prabal and Jayashankara Shridevi, Rajesh and Chakraborty, Koushik and Roy, Sanghamitra and Zhang, Zhen},
  editor = {Larsen, Kim Guldstrand and Willemse, Tim},
  year = 2019,
  pages = {110--126},
  publisher = {Springer International Publishing},
  doi = {10.1007/978-3-030-27008-7_7},
  isbn = {978-3-030-27008-7},
}
```

### Probabilistic Verification for Reliability of a Two-by-Two Network-on-Chip System

```bibtex
@inproceedings{roberts_probabilistic_2021,
  title = {Probabilistic {{Verification}} for {{Reliability}} of a {{Two-by-Two Network-on-Chip System}}},
  booktitle = {Formal {{Methods}} for {{Industrial Critical Systems}}},
  author = {Roberts, Riley and Lewis, Benjamin and Hartmanns, Arnd and Basu, Prabal and Roy, Sanghamitra and Chakraborty, Koushik and Zhang, Zhen},
  editor = {Lluch Lafuente, Alberto and Mavridou, Anastasia},
  year = 2021,
  pages = {232--248},
  publisher = {Springer International Publishing},
  doi = {10.1007/978-3-030-85248-1_16},
}
```
