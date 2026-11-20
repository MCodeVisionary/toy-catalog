# Azure DevOps + JFrog OIDC setup

Org: https://dev.azure.com/maharship0575/

1. **Azure service connection (workload identity federation)**
   Project settings → Service connections → New → Azure Resource Manager → *Workload identity federation*.
   Name it `azure-oidc-connection` (or change `AZURE_SERVICE_CONNECTION` in the pipeline).
2. **JFrog OIDC integration** (solenglatest.jfrog.io)
   Administration → Security → OIDC Integrations → New. Provider type: Azure. Name: `azure-devops-oidc`.
   Add an identity mapping to a user/group with deploy rights on `alpha-pypi-virtual` and build-info (`artifactory-build-info`).
   Match the token claims (issuer `https://vstoken.dev.azure.com/<org-id>`, subject
   `sc://maharship0575/<project>/azure-oidc-connection`) and set the audience if the mapping enforces one.
3. **Pipeline**: Pipelines → New → GitHub → MCodeVisionary/toy-catalog → existing `azure-pipelines.yml`.
   Needs the Azure Pipelines GitHub app installed on the repo/org.

The pipeline: JFrog OIDC login → `poetry install` + pytest (resolves from `alpha-pypi-virtual`) → `poetry build`
→ `jf rt upload` to `alpha-pypi-virtual` (lands in `alpha-pypi-dev-local`) → `jf rt build-publish`.
