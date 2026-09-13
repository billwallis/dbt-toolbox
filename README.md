<span align="center">

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![tests](https://github.com/billwallis/dbt-toolbox/actions/workflows/tests.yaml/badge.svg)](https://github.com/billwallis/dbt-toolbox/actions/workflows/tests.yaml)
[![coverage](https://raw.githubusercontent.com/billwallis/dbt-toolbox/refs/heads/main/coverage.svg)](https://smarie.github.io/python-genbadge/)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/dbt-toolbox/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/dbt-toolbox/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/dbt-toolbox)](https://shields.io/badges/git-hub-last-commit)

</span>

---

# dbt Toolbox

Toolbox to facilitate dbt work.

This is my personal alternative to tools like:

- [dbt-codegen](https://github.com/dbt-labs/dbt-codegen)
- [dbt-coves](https://github.com/datacoves/dbt-coves)

I'm building this alternative just to customise it to my own preferences.

## Contributing

Install the dependencies:

```shell
pip install --editable . --group dev --group test
pre-commit install --install-hooks
```
