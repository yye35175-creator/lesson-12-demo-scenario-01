# AI evidence for the classroom demo

Make an individual practice record for AI help you used. From the practice repository root, copy `templates/ai-evidence.md` to `evidence/ai-use/<student-id>.md` for each student who used AI. Keep `evidence/debug-log.md` for observed failures and fixes. Use fictional identifiers and omit private data.

For each material interaction, add an entry headed `## <student-id>-AI-01 — <task>` (then `-02`, and so on). Fill the template's Date, Contributor and tool/model, Task, Prompt excerpt, Reply excerpt, Decision, Verification and Evidence reference fields. Copy short excerpts from your **original** prompt and the **actual** reply. Mark any redaction `[REDACTED]` and state which facts still need verification.

Useful entries from this lesson include a PR workflow review, a lint rule you selected, a failed CI diagnosis or advice you rejected. For each, describe what *you* decided and cite the supporting file, commit, test result, pull request or CI run. A verification should name the command or action and its observed outcome. If you intentionally break a JS file, record the actual result of `npx --no-install eslint scripts` and the passing run after your fix. For the starter's full claim test, record the expected `501 SCENARIO_TODO` failure accurately.

Fill this ICE frame with details from your interaction and observations before sending a follow-up prompt.

> **Intention** — Help me check whether my evidence for [specific AI-assisted task] is accurate and traceable.
>
> **Context** — I asked [my original prompt excerpt] and received [actual reply excerpt]. I chose to [use, adapt or reject] the advice because [reason]. I ran [command or action] and observed [result].
>
> **Example** — A reader should be able to open [file, commit, test, pull request or CI run] and confirm [one specific claim]. Flag any claim that needs more evidence so I can verify it.

Compare every excerpt and result with the source conversation and the actual run before saving your evidence.
