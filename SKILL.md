---
name: afterbuild
description: Inspects a finished codebase and guides AI agents or developers through generating publication-ready documentation, architecture overviews, developer guides, research reports, case studies, or engineering storytelling with automated factual verification.
---

# afterbuild Skill

Turn finished codebases into verified, production-ready documentation and technical narratives.

Follow this systematic workflow:

## 1. Analyze
Run `afterbuild analyze` in the repository root (or inspect the codebase structure directly):
- Read `.afterbuild/brief.md` and `.afterbuild/brief.json` to understand languages, entry points, test suites, git history, and existing README context.

## 2. Select Document Mode
Confirm with the user which documentation mode best fits their target audience:

- **`product-docs`** – End-user facing guides, feature overviews, and usage manuals.
- **`technical-docs`** – Deep-dive architectural blueprints, module designs, and developer APIs.
- **`research-report`** – Formal research reports, methodologies, and technical analyses with citations.
- **`storytelling`** – Narrative journey of building the project, challenges faced, and lessons learned.
- **`case-study`** – Retrospective analysis covering problem statement, engineering trade-offs, and outcomes.

*(See `skill/modes/<mode>.md` for structural outlines and section guidelines).*

## 3. Targeted Alignment Interview
Ask up to 3 to 5 targeted questions to clarify context:
1. What core problem does this codebase solve?
2. Who is the primary target audience (developers, users, stakeholders)?
3. What are the key architectural decisions or milestones?

## 4. Draft Document
Draft the requested documentation adhering strictly to the chosen mode's outline:
- Every technical claim must directly trace back to real code, commit history, or verified facts.
- Never invent benchmarks, fictional flags, or unverified symbols.

## 5. Automated Verification
Run the verification engine:
```bash
afterbuild verify <draft.md>
```
The verifier checks:
- Hyperlink reachability (HTTP status 200).
- Referenced file paths exist in the workspace.
- Referenced functions, classes, and symbols actually exist in code.
- Mentioned CLI flags match project configs (`pyproject.toml`, `package.json`, etc.).

Fix any hallucinated or broken references flagged by `verify`.

## 6. Multi-Format Export
Export the verified draft to the desired format:
```bash
afterbuild export <draft.md> --to [md|docx|pdf] --out docs/
```
Output is cleanly generated under `docs/`.
