# Lesson 12 student guide — Campus Lost Property Desk

## 1. Set up your practice repository

1. Clone your practice GitHub repository and open it in your editor. Use Git Bash on Windows. Switch to `main` if the branch already exists. If you cloned an empty repository, run `git branch -m main` to name your first branch.

2. Copy the contents of [starter-code/](starter-code/) into the repository root. Include hidden files such as `.github/` and `.gitattributes`.

3. Check that `docker-compose.yml`, `backend/`, `frontend/` and `tests/` are at the root. Run these commands to save the starter on GitHub.

   ```sh
   git add .
   git commit -m "Add Lesson 12 starter"
   git push -u origin main
   ```

4. Start Docker. Run these commands from the repository root, one at a time. The smoke test should report three passing checks.

   ```sh
   docker compose up --build -d --wait
   bash tests/run.sh --smoke
   docker compose down
   ```

5. Create a branch for your workflow files.

   ```sh
   git switch -c lesson-12-ci
   ```

## 2. Create the backend pull request workflow

1. Create the `.github/workflows/` folder if needed. In it, create `backend-pr.yml`. Start with this YAML. Keep the indentation and fill in each `FILL_IN` value.

   ```yaml
   name: Backend PR
   on:
     pull_request:
       branches: [FILL_IN_BRANCH]

   permissions:
     contents: read

   jobs:
     check:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v7
         - uses: actions/setup-python@v7
           with:
             python-version: 'FILL_IN_VERSION'
         - name: Compile Python
           run: FILL_IN_COMPILE_COMMAND
         - name: Build backend image
           run: FILL_IN_BUILD_COMMAND
   ```

2. Use `main` as the target branch and `3.14` as the Python version. `on` tells GitHub when to run the workflow. A step uses `uses` for a reusable action or `run` for a terminal command.

3. Fill in the compile command with `python -m compileall -q backend/app`. Fill in the build command with `docker compose build backend`. Keep them as separate steps. GitHub skips the build step if compilation fails.

4. Draft an **ICE prompt** in your own words. ICE stands for **Intention, Context, Example**. Fill each bracket with details from your file, then ask AI to review your steps.

   > **Intention** — Check whether my backend build runs only after [the check that must pass].
   >
   > **Context** — Here are my [two YAML steps]. My Python files are in [folder].
   >
   > **Example** — If [specific syntax error] occurs, I expect [step name] to fail and [step name] to be skipped.

## 3. Create the frontend pull request workflow

1. Use Node.js 22.13 or later within version 22. From the repository root, run these commands once to create the frontend package and lockfile. The module setting lets Node check JavaScript files that use `import`.

   ```sh
   cd frontend
   npm init -y
   npm pkg set type=module
   npm install --save-dev htmlhint eslint @eslint/js globals
   ```

2. Create `frontend/eslint.config.mjs` in your editor. Use these rules for the browser scripts.

   ```js
   import js from '@eslint/js';
   import globals from 'globals';

   export default [
     {
       files: ['scripts/**/*.js'],
       languageOptions: { globals: globals.browser },
       rules: js.configs.recommended.rules,
     },
   ];
   ```

3. Run these commands in the `frontend/` folder. A successful `test -f` or `node --check` usually prints nothing.

   ```sh
   npm ci
   test -f index.html
   test -f scripts/index.js
   test -f scripts/http.js
   node --check scripts/index.js
   node --check scripts/http.js
   npx --no-install htmlhint index.html
   npx --no-install eslint scripts
   ```

4. Run `cd ..` to return to the root. Create `.github/workflows/frontend-pr.yml` using the backend file as a starting point. Name it **Frontend PR** and keep the `pull_request` trigger for `main`.

5. Replace the Python setup step with `uses: actions/setup-node@v7`. Under `with:`, set `node-version: '22'`.

6. Replace **Compile Python** with **Check frontend**. Put the eight commands from step 3 where the comment is. Keep the same indentation.

   ```yaml
   - name: Check frontend
     working-directory: frontend
     run: |
       # Add the eight commands from step 3 here.
   ```
7. Rename the final step **Build frontend image** and set `run: docker compose build frontend`. Leave this step at the repository root by setting `working-directory` only on **Check frontend**.

8. Fill in this **ICE prompt** before you ask AI for feedback.

   > **Intention** — Review my frontend checks for [actual files].
   >
   > **Context** — Here is my [check step]. It runs from [folder]. My Compose build runs from [folder].
   >
   > **Example** — If I remove or break [file], I expect [command] to fail and [step name] to be skipped.

## 4. Create the integration workflow

1. Create `.github/workflows/integration.yml`. Reuse the backend workflow structure. Name it **Integration**. Change `pull_request` to `push` and keep `branches: [main]`. A merge updates `main` and triggers this workflow. A direct push to `main` also triggers it.
2. Keep checkout and Python setup. Replace the compile and build steps with the numbered steps below. Make each one a separate YAML entry under `steps:` with a `name` and a `run`.

   1. **Build images** — `docker compose build backend frontend`
   2. **Start services** — `docker compose up -d --no-build --wait`
   3. **Run smoke tests** — `bash tests/run.sh --smoke`
   4. **Run full suite** — `bash tests/run.sh`
   5. **Print service logs** — `docker compose logs --no-color`. Add `if: failure()` beside `run`.
   6. **Stop services** — `docker compose down --volumes --remove-orphans`. Add `if: always()` beside `run` so cleanup runs after failures too.

3. Fill in this **ICE prompt** using your integration steps. Ask AI to explain any change it suggests before you apply it.

   > **Intention** — Check the order of my integration steps after [event and branch].
   >
   > **Context** — Here are my [test, log and cleanup steps]. The full test reaches an unfinished claim endpoint.
   >
   > **Example** — If [test step] fails, I expect [log step] followed by [cleanup step]. The final run status should be [status].

## 5. Run the workflows on GitHub

1. Run `git status`. Check that the three YAML files, `frontend/package.json`, `frontend/package-lock.json` and `frontend/eslint.config.mjs` are ready to commit. Commit and push your branch.

   ```sh
   git add .github/workflows frontend/package.json frontend/package-lock.json frontend/eslint.config.mjs
   git commit -m "Add Lesson 12 workflows"
   git push -u origin lesson-12-ci
   ```

2. On GitHub, select **Pull requests → New pull request**. Set the base to `main` and choose `lesson-12-ci` as the compare branch. Create the pull request. Open **Checks** and confirm **Backend PR** and **Frontend PR** both build their images.

3. On your practice branch, add `def broken(:` at the end of `backend/app/main.py` and `const = ;` at the end of `frontend/scripts/index.js`. Put each on its own line. Stage the two files, commit, then run `git push`. In **Checks**, confirm both check steps fail and both builds are skipped. Save the run links.

4. Remove the two temporary lines. Stage the files again, commit, then run `git push`. Wait for both checks to pass and save the new run links.

5. Merge the pull request. Click **Actions → Integration** and open the run for the new `main` commit. Confirm both images built and the smoke tests passed.

6. Open **Run full suite**. Expect `501 SCENARIO_TODO` from the unfinished claim feature. Check that **Print service logs** and **Stop services** ran. The workflow should report a failure until the claim feature is implemented.

## 6. Record your evidence

1. Open `evidence/debug-log.md`. Record the failing step, the key error, what you changed and the run link that shows the fix.

2. Read [AI-EVIDENCE.md](AI-EVIDENCE.md). Create `evidence/ai-use/` if needed. Copy `templates/ai-evidence.md` to `evidence/ai-use/<student-id>.md`. Replace `<student-id>` with your practice ID.

3. Save a short excerpt from your completed ICE prompt and a short excerpt from the AI reply. Record which suggestion you used, changed or rejected. Write down the command you ran or link to the file or run that shows how you checked it.

