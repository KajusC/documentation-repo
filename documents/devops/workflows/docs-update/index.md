# Workflows

## Purpose

This page documents the Docs slash command workflow, which responds to pull request issue comments and triggers the documentation update process.

## Who calls / is called by

- Triggered by GitHub issue comments on pull requests.
- Calls the `docs-update.yml` workflow in the `KajusC/documentation-repo` repository.

## Interfaces/Data/Configuration

- **Event:** `issue_comment` (types: `created`).
- **Conditions:** Must be on a pull request, comment must start with `/docs`, and author must have `OWNER`, `MEMBER`, or `COLLABORATOR` association.
- **Secrets:** Uses `DOCS_BOT_TOKEN` for API authentication.
- **Workflow Inputs:** Passes `code_repo` and `pr_number` to the downstream workflow.

## Architecture

Runs on `ubuntu-latest` with two steps:
1. Adds an `eyes` reaction to the triggering comment via GitHub API.
2. Triggers the remote `docs-update.yml` workflow using the GitHub CLI.

## Sources

- Code change adding the Docs slash command GitHub Actions workflow
