# OpenFisca Canada 

This repository holds OpenFisca code written to represent the services and benefits
relevant to tools under development in Service Canada. **It is a work in progress and
should not be relied upon for any real-world purpose.** 

## Requirements

This package requires [Python 3.7](https://www.python.org/downloads/release/python-370/), and pip version 9.0 or higher. More recent versions should work, but are not tested.

Installing this package will also install OpenFisca as a dependency.

## Installation

This package is not currently made available for install through `pip`.

In order to limit dependencies conflicts, we recommend using a [virtual environment](https://www.python.org/dev/peps/pep-0405/) with [venv](https://docs.python.org/3/library/venv.html).

To install, clone this Country Package on your machine:

```sh
git clone https://github.com/JasonMorrisSC/openfisca-canada.git
cd openfisca-canada
pip install --editable .[dev]
```

You can make sure that everything is working by running the provided tests with `make test`.

## Usage

To serve the Openfisca Web API locally, run:

```sh
openfisca serve --port 5000
```

You can make sure that your instance of the API is working by requesting:

```sh
curl "http://localhost:5000/spec"
```

You can test the Web API by sending it example JSON data located in the `situation_examples` folder.

Note that if you are running OpenFisca inside a Docker container, you may need to use the
`--bind 0.0.0.0:5000` option in place of the `--port` option.

## Contributions

Thank you for your contributions to this open source package.

We follow [GitHub Flow](https://guides.github.com/introduction/flow/) and [semantic versioning](https://semver.org).

Major version numbers change when there is a backward-incompatible change in the API. Minor version numbers change when there is a backward-compatible functional change in the API. Patch
version numbers change for everything else. Pre-releases are noted with `-alpha` and `-beta` suffixes.

The `main` branch is the primary branch, and releases will be tagged in that branch only. Pull requests should be made against the `devel` branch.

Please include appropriate changes to the CHANGELOG with your pull requests.

Make the title of the changelog entry the version number, and link it to the relevant release or pull request.

The Changelog entry should list, briefly:
* issues resolved
* bugs fixed
* features added
* features deprecated
* features removed
* features changed
* a link to the relevant pull request

If the change makes substantive changes to the rules encoded in the package, include the
following details:
* affected time periods
* parameter, reform, variables, or entities modified
* the prior state
* the new state, with usage details
* the motivation for the change

## Additional Information

* [OpenFisca Website](https://openfisca.org/)
* [OpenFisca Web API documentation](https://openfisca.org/doc/openfisca-web-api/index.html)
