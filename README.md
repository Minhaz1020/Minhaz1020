# GitHub ASCII Profile

This project creates a terminal-style ASCII portrait from the GitHub user's avatar and displays basic public GitHub statistics.

## Setup

1. Create a repository with the **same name as your GitHub username**.
2. Put these files in the repository:
   - `generate.py`
   - `.github/workflows/update.yml`
3. Enable GitHub Actions.
4. Run **Actions → Update ASCII Profile → Run workflow**.
5. After the workflow finishes, `profile.svg` will be generated.

## Add it to README.md

```html
<img src="./profile.svg" alt="GitHub ASCII profile">
```

## Important

This is an independent implementation inspired by the same general idea. It does not copy Andrew6rant's source code.

The reference repository contains `today.py`, `dark_mode.svg`, `light_mode.svg`, and a GitHub Actions workflow; its README describes the project as calculating repositories, commits, stars, followers and contributed lines of code.
