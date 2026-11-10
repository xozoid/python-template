---
name: update-from-template
description: >-
  Updates a project adopted from xozoid/python-template while preserving
  project-specific code, configuration, and intentional deviations.
---

# Update from template

Template-Source: `xozoid/python-template`

Template-Revision: `<full-upstream-commit-sha>`

The `Template-Revision` value records the upstream template commit last fully applied to
this project. During adoption, set it to the upstream commit used to create the project.
For later updates, advance it only after the applicable migration is complete and
validation succeeds. Do not record a target repository commit SHA here.

## Update workflow

1. Read `Template-Revision` above and confirm it is a full commit SHA. Resolve the
   template repository's default branch and its current full commit SHA. Fetch the
   upstream template and verify that the recorded revision exists there.
2. Compare the recorded revision with the current default-branch revision. If they are
   identical, report that no update is needed. If the target revision does not descend
   from the recorded revision, report divergence and stop before applying changes.
3. Review the template changes between the recorded and target revisions. Compare the
   affected files with the project, then apply relevant changes in context. Preserve
   project-specific code, metadata, dependencies, configuration, CI customizations, and
   intentional deviations. Never overwrite uncommitted changes or discard local edits.
4. For intentionally skipped changes, add the affected paths and reasons under
   `Skipped template changes` at the end of this skill. Reuse that persistent record
   during later updates so the same change is not proposed repeatedly.
5. Run relevant tests, linting, formatting, dependency locking, and pre-commit
   synchronization checks. Review generated changes and resolve conflicts with the
   project's conventions.
6. Only after the applicable migration is complete and checks succeed, replace
   `Template-Revision` above with the full target template SHA. Do not automatically
   commit changes unless the user explicitly requests a commit.

## Finding an initial revision

If `Template-Revision` is unset or still contains the placeholder, compare the project's
initial state with the template's history and use file contents and timestamps only as
supporting evidence. Do not select a revision solely because it looks like the closest
match. If the origin cannot be identified confidently, describe the candidate revisions
and ask the user to confirm before updating.

## Skipped template changes

Add one bullet per intentional skip. Include the affected path and reason. Remove or
revise an entry if a later template change makes the skipped update relevant again.

- None recorded.

## Report

Report the target template revision, applied changes, skipped changes and reasons,
conflicts, and validation results. State clearly when no update was needed or when
divergence or an ambiguous starting revision prevented an update. If a commit is
requested, use a clear summary and leave the revision recorded in this skill as the
source of template tracking.
