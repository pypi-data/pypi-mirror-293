[![PyPI - Downloads](https://img.shields.io/pypi/dm/file-tree)](https://pypi.org/project/file-tree/)
[![Documentation](https://img.shields.io/badge/Documentation-file--tree-blue)](https://open.win.ox.ac.uk/pages/fsl/file-tree/)
[![Documentation](https://img.shields.io/badge/Documentation-fsleyes-blue)](https://open.win.ox.ac.uk/pages/fsl/fsleyes/fsleyes/userdoc/filetree.html)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6576809.svg)](https://doi.org/10.5281/zenodo.6576809)
[![Pipeline status](https://git.fmrib.ox.ac.uk/fsl/file-tree/badges/master/pipeline.svg)](https://git.fmrib.ox.ac.uk/fsl/file-tree/-/pipelines)
[![Coverage report](https://git.fmrib.ox.ac.uk/fsl/file-tree/badges/master/coverage.svg)](https://open.win.ox.ac.uk/pages/fsl/file-tree/htmlcov)

Framework to represent structured directories in python as FileTree objects. FileTrees can be read in from simple text files describing the directory structure. This is particularly useful for pipelines with large number of input, output, and intermediate files. It can also be used to visualise the data in structured directories using FSLeyes or `file-tree` on the command line.

- General documentation: https://open.win.ox.ac.uk/pages/fsl/file-tree/
- FSLeyes documentation on using FileTrees: https://open.win.ox.ac.uk/pages/fsl/fsleyes/fsleyes/userdoc/filetree.html 

## Running tests
Tests are run using the [pytest](https://docs.pytest.org) framework. After installation (`pip install pytest`) they can be run from the project root as:
```shell
pytest src/tests
```

## Release procedure
- Create a new release branch
- Make sure "CHANGELOG.md" is up to date
    - All commits can be seen in gitlab by clicking the "Unreleased" link in "CHANGELOG.md"
    - Add new header just below "## [Unreleased]" with the new version
    - Update the footnotes for both the new version and [Unreleased]
- Run bump2version patch/minor/major
- Merge branch on gitlab
- Push to pypi by running custom pipeline job in gitlab
