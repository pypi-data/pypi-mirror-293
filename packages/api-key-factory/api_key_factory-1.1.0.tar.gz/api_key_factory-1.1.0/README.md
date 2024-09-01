# `api-key-factory`

[![Software License](https://img.shields.io/badge/license-MIT-informational.svg?style=for-the-badge)](LICENSE)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release&style=for-the-badge)](https://github.com/semantic-release/semantic-release)
[![Pipeline Status](https://img.shields.io/gitlab/pipeline-status/op_so/projects/api-key-factory?style=for-the-badge)](https://gitlab.com/op_so/projects/api-key-factory/pipelines)

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://op_so.gitlab.io/projects/api-key-factory/) Source code documentation

<img src="https://gitlab.com/op_so/projects/api-key-factory/-/raw/main/api_key_factory.png?ref_type=heads" alt="Logo of api-key-factory" width="150px" height="150px" style="display: block; margin: 0 auto; border: solid; border-color: #5f6368; border-radius: 20px;">

## Overview

`api-key-factory` is a CLI tool to generate API keys and their corresponding [SHA-256](https://en.wikipedia.org/wiki/SHA-2) hashes. The secret part of the key is an [UUID (Universally Unique Identifier) version 4 (random)](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)).

Example of generated a API key:

```bash
mykey-8590efb6-0a68-4390-8537-99a54928c669
```

```bash
Usage: api-key-factory [OPTIONS] COMMAND [ARGS]...

  A simple CLI tool to generate API keys and their corresponding SHA-256
  hashes.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  generate  Command to generate API keys and their corresponding SHA-256...
```

## `generate`

Generate api keys and hashes in standart terminal output (stdout) or in 2 distinct files (`[prefix_]keys.txt`, `[prefix_]hashes.txt`) in a defined directory.

```bash
Usage: api-key-factory generate [OPTIONS]

  Command to generate API keys and their corresponding SHA-256 hashes.

  Raises:     click.ClickException: Error when writing output file

Options:
  -n, --num INTEGER RANGE  Number of API keys to generate  [x>=1]
  --help                   Show this message and exit.
```

Example:

```bash
$ api-key-factory generate
e4feb87a-ff10-4cce-bbe2-3b9dcbeb019c   1e6d309d41b3a1b7a4855aba3382bdafcb7476db97416a7ecd9fcabe4292c5ca
```

## Installation

### With `Python` environment

To use:

- Minimal Python version: 3.10

Installation with Python `pip`:

```bash
python3 -m pip install api-key-factory
api-key-factory --help
```

## Develpement

### With [Rye](https://rye.astral.sh/)

To use:

- Minimal Python version: 3.10

Installation documentation: [https://rye.astral.sh/guide/installation/](https://rye.astral.sh/guide/installation/)

```bash
# Set environment
rye sync
# Lint
rye run lint
# Tests
rye run test
# Run
rye run api-key-factory --help
```

## Authors

<!-- vale off -->
- **FX Soubirou** - *Initial work* - [GitLab repositories](https://gitlab.com/op_so)
<!-- vale on -->

## License

<!-- vale off -->
This program is free software: you can redistribute it and/or modify it under the terms of the MIT License (MIT).
See the [LICENSE](https://opensource.org/licenses/MIT) for details.
<!-- vale on -->
