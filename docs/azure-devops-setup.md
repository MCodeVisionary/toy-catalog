# Azure DevOps + JFrog OIDC setup

Org/project: https://dev.azure.com/maharship0575/SolEng

- **JFrog service connection:** `mpate-solenglatest-platform` (JFrog Platform V2, OIDC provider `soleng-ado-mp`)
  -> solenglatest.jfrog.io. The OIDC identity mapping must allow read/deploy on `alpha-pypi-virtual` and build-info.
- **GitHub service connection:** `MCodeVision` -> MCodeVisionary/toy-catalog.
- **Flow:** OIDC login -> `poetry install` + pytest (resolves from `alpha-pypi-virtual`) -> `poetry build`
  -> `jf rt upload` to `alpha-pypi-virtual` (lands in `alpha-pypi-dev-local`) -> `jf rt build-publish`.
- Note: SolEng is a *public* project, so pipeline logs are publicly visible.
