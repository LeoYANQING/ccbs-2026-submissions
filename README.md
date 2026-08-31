# CCBS 2026 — submissions

Course: **CST 5034 — Control and Computation in Biological Systems, Fall 2026**
(Westlake University). Course site: <https://chemaoxfz.github.io/ccbs/2026fall/>

This repository is where the weekly artifacts are collected. The TAs assemble them into
the course site's three weekly artifacts (core / exposition / extension-by-audience).

## Who submits what, when

| What | Who | Filename | Due |
|---|---|---|---|
| Extension micro-essay | every student **not** teaching that week | `weekN_<name>_ext.html` | Wed 23:59 before the lecture |
| Session quiz (+ answer key) | each teaching student, **TA-approved** | `weekN_<name>_quiz.md` | Wed 23:59 (with the digest/outline) |
| Exposition (teaching material) | each teaching student | `weekN_<name>_exposition.html` (or `.pdf`/`.pptx`) | Fri after the lecture |

`<name>`: your Latin name in lowercase without spaces (e.g. `week5_liwei_ext.html`).
Week numbers: week2 = 2026-09-10, week3 = 09-17, week4 = 09-24, week5 = 10-08,
week6 = 10-15, week7 = 10-22, week8 = 10-29 (week1 = lecturer-taught, no submissions;
week of 10-01 = National Day holiday).

## How to submit

1. **Preferred:** you are added as a write collaborator (the TAs add your GitHub
   username), then `git add week5/liwei_ext.html` → commit → push. No review needed;
   the TAs read everything anyway.
2. **Fork + PR:** if you are not a collaborator, fork the repo, add your file on your
   branch, open a pull request to `main`. We merge within days.
3. **Fallback:** email the file to both TAs — Wenqin Zhou (zhouwenqin@westlake.edu.cn)
   and Xinyu Wang (wangxinyu@westlake.edu.cn) — with the same filename.

Rules of thumb: the extension micro-essay uses `TEMPLATE_ext.html` as its skeleton (any
HTML is fine, but keep it a *single self-contained file*); the quiz uses
`TEMPLATE_quiz.md` and must be approved by the TA pair before the lecture.

## For the TAs: how the week gets assembled

1. Move/confirm all submissions in `weekN/` (names checked against the roster).
2. Quizzes: check approval (tests the session's core point, ~30 s to solve for anyone
   who got the material, no tricks); fix or reject privately with the author.
3. Extension page: run `python3 tools/assemble_extension.py weekN` → it emits
   `weekN/extension_skeleton.html` with every micro-essay placed in order. Hand the
   skeleton to an AI agent with the instruction to weave the essays into **one coherent
   themed long-form writeup** (keep the authors and keep conflicts and opposing views
   visibly in conversation), then review the result yourself. That HTML is the week's
   **extension-by-audience** page.
4. Push the assembled pages to the main site repo:
   `chemaoxfz/chemaoxfz.github.io` → `assets/ccbs/2026fall/weekN/extension/index.html`,
   and link from `_pages/ccbs-2026.md`.

Templates: [`TEMPLATE_ext.html`](TEMPLATE_ext.html) (extension micro-essay skeleton),
[`TEMPLATE_quiz.md`](TEMPLATE_quiz.md) (quiz skeleton + approval checklist).
