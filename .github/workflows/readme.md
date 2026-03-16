# workflows

GitHub Actions CI/CD workflow definitions for automated testing, linting, and package deployment.

## Files

- **`prod-tests.yml`** - Production CI pipeline triggered on pushes to `main`. Runs ruff linting, formatting checks, and the full test suite.
- **`stage-tests.yml`** - Staging CI pipeline triggered on pull requests to `stage`. Runs the same linting, formatting, and test checks as production.
- **`version-deployment.yml`** - CD pipeline triggered on GitHub release publication. Updates the version in `pyproject.toml` from the release tag, builds the package, and publishes to PyPI.
