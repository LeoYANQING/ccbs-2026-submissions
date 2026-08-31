# Tools

`assemble_extension.py` — builds the skeleton of the week's extension-by-audience page
from the week folder's `*_ext.html` submissions (stdlib only).

```sh
python3 tools/assemble_extension.py week5
# -> week5/extension_skeleton.html
```

Then: hand the skeleton to an AI agent → "weave these into ONE coherent themed
long-form writeup; keep authors; keep conflicts visibly in conversation" → review →
publish to the main course site under `assets/ccbs/2026fall/lectureNN/extension/` and link
from `_pages/ccbs-2026.md` in `chemaoxfz/chemaoxfz.github.io`.

Quizzes are NOT assembled by the script — they are checked against the approval
checklist in `TEMPLATE_quiz.md` and used in class as-is.
