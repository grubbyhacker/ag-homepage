# Pull Request Workflow

> **Location in repo:** `.agent/pull-requests.md`  

## Opening PRs Automatically

Agents working in this repository are expected to manage the full lifecycle of a feature, which includes opening the Pull Request. **Do not ask the human to open the PR.**

When your git branch is pushed to `origin` and is ready for review:
1. Verify that `make format` and `make lint` have passed locally.
2. Use the GitHub CLI (`gh`) to open the PR against `staging`.
3. If you are operating in an environment where Windows is the host but Git/GitHub credentials reside in WSL, prefix your commands with `wsl` (e.g., `wsl gh pr create`).

### Git Commit Author Tracking

Every commit made by an AI agent must explicitly declare the agent identity and model used via **Git Trailers** at the bottom of the commit message. 

```bash
git commit -m "feat(scope): some change

Agent: <Agent Name>
Model: <Model Name>"
```

### PR Creation Command

```bash
gh pr create \
  --base staging \
  --title "<type>(<scope>): <subject>" \
  --body "Explanation of the changes, focusing on *why* they were made."
```

*(Note: Always target the `staging` branch, never `main`, as per branching rules).*

### Review Loop

If the human reviewer requests changes:
1. Ensure you are on the correct branch.
2. Make the requested fixes.
3. Run formatting and linting again (`make format && make lint`).
4. Commit and push the updates. Do not open a new PR; pushing to the existing branch will update the open PR automatically.
