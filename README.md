# Lottie Animation Format Documentation

This repository is for the development of the Lottie Animation Format.

All work here is guided by the [Community Specification License](Community_Specification_License-v1.md).


## Scope

The scope of this Working Group is to specify the format of the Lottie Animation Format, both
the allowed JSON structure, the semantics of that structure, and how such Lottie files are to be
rendered. The definition of the correct rendering will be specified by a combination of verbiage
in the written specification and by exemplar Lottie files and their desired renderings.


## CLA

Participation in this group requires signing the
[Contributor License Agreement](Notices.md), which you can
do by creating a pull request that adds your name, email address, and Community
Specification License version that you agree to be bound by.

Here is an [example of what that pull request should look like](https://github.com/lottie/lottie-spec/pull/9).


## Branching and Contribution Workflow

This repository uses a two-branch workflow to protect `main` from unstable or incomplete work:

- **`dev`** — The integration branch. All pull requests must target `dev`.
- **`main`** — The release branch. Only updated by merging `dev` into `main` when preparing a release.

### Contributing

1. Create a feature branch from `dev`.
2. Open a pull request targeting `dev`.
3. PRs are squash-merged into `dev` to keep the history clean.

### Releasing

When `dev` is stable and ready for release:

1. Merge `dev` into `main` using a **merge commit** to preserve a clear release boundary.
2. Update the schema `$id` in `root.json`.
3. Create and push a git tag (e.g., `1.0`).
4. Await GitHub Actions completion.
5. Trigger the tag-latest workflow if applicable.

See the [Building and Deploying](https://github.com/lottie/lottie-spec/wiki/Building-and-Deploying) wiki page for full details on versioning and deployment.

### Branch Protection

`main` is protected — direct pushes and PRs to `main` are not allowed. All changes flow through `dev` first.

