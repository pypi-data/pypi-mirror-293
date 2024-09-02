# `zampy` developer documentation

If you're looking for user documentation, go [here](index.md).

## Development install

```shell
# Create a virtual environment, e.g. with
python3 -m venv env

# activate virtual environment
source env/bin/activate

# make sure to have a recent version of pip and hatch
python3 -m pip install --upgrade pip hatch

# (from the project root directory)
# install s2spy as an editable package
python3 -m pip install --no-cache-dir --editable .
# install development dependencies
python3 -m pip install --no-cache-dir --editable .[dev]
```

Afterwards check that the install directory is present in the `PATH` environment variable.

## Running the tests

Running tests has been configured using `hatch`, and can be started by running:

```shell
hatch run test
```

The second is to use `tox`, which can be installed separately (e.g. with `pip install tox`), i.e. not necessarily inside the virtual environment you use for installing `zampy`, but then builds the necessary virtual environments itself by simply running:

### Test coverage

In addition to just running the tests to see if they pass, they can be used for coverage statistics, i.e. to determine how much of the package's code is actually executed during tests.
Inside the package directory, run:

```shell
hatch run coverage
```

This runs tests and prints the results to the command line, as well as storing the result in a `coverage.xml` file (for analysis by, e.g. SonarCloud).

## Running linters locally

For linting we will use `flake8`, `black` and `isort`. We additionally use `mypy` to check the type hints.
All tools can simply be run by doing:

# linter
```shell
hatch run lint
```

To easily comply with `black` and `isort`, you can also run:

```shell
hatch run format
```

This will apply the `black` and `isort` formatting, and then check the code style.


## Generating the documentation
To generate the documentation, simply run the following command. This will also test the documentation code snippets. Note that you might need to install [`pandoc`](https://pandoc.org/) to be able to generate the documentation.

```shell
hatch run docs:build
```

The documentation will be in `docs/_build/html`.

## Versioning

Bumping the version across all files is done with [bump-my-version](https://github.com/callowayproject/bump-my-version), e.g.

```shell
bumpversion bump major
bumpversion bump minor
bumpversion bump patch
```

## Making a release

This section describes how to make a release in 3 parts: preparation, release and validation.

### Preparation

1. Update the <CHANGELOG.md> (don't forget to update links at bottom of page)
2. Verify that the information in `CITATION.cff` is correct, and that `.zenodo.json` contains equivalent data
3. Make sure the [version has been updated](#versioning).
4. Run the unit tests with `hatch run test`

### Making the GitHub release

Make a release and tag on GitHub.com. This will:

 - trigger Zenodo into making a snapshot of your repository and sticking a DOI on it.
 - start a GitHub action that builds and uploads the new version to [PyPI](https://pypi.org/project/zampy/).

### Validation

After making the release, you should check that:

- The [publishing action](https://github.com/EcoExtreML/zampy/.github/workflows/publish.yml) ran successfully, and that `pip install zampy` installs the new version.
