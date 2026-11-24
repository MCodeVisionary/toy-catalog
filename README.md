# toy-catalog

Sample Poetry app that generates a random toy product catalog (name, price, category such as car/truck) as JSON and lists it.

```sh
poetry install
poetry run toy-catalog generate -n 12 --seed 42
poetry run toy-catalog list
poetry run toy-catalog list -c truck
poetry run toy-catalog search turbo
poetry run toy-catalog stats
poetry run toy-catalog sale 25 -c car
poetry run toy-catalog add "Turbo Racer" 14.99 car
poetry run toy-catalog set-price 1 9.99
poetry run toy-catalog remove 2
poetry run pytest
```

Dependencies resolve from the JFrog virtual repo `alpha-pypi-virtual` (solenglatest.jfrog.io).
Configure credentials once:

```sh
poetry config http-basic.alpha-pypi-virtual <user> <token>
```

## CI/CD
`.github/workflows/build.yml` is the GitHub Actions equivalent (OIDC provider `github-docportal`, same as node-goat).

`.github/workflows/frogbot.yml` runs Frogbot PR and repository scans.

`azure-pipelines.yml` builds with Poetry using JFrog OIDC (no stored tokens), collects build-info with JFrog CLI and publishes to `alpha-pypi-virtual`. See `docs/azure-devops-setup.md`.
