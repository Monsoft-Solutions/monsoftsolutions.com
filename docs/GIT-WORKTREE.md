# Git Worktree Guidelines

Guidelines for parallel development using git worktrees, enabling multiple AI agents or developers to work on separate features simultaneously.

**Related:** [CLAUDE.md](../CLAUDE.md)

## Overview

Git worktrees allow you to check out multiple branches simultaneously in separate directories. This is particularly useful for:

- Running multiple AI agents on different features in parallel
- Quick context switching without stashing changes
- Testing changes in one branch while developing in another
- Reviewing PRs while keeping your work-in-progress intact

## Directory Structure

Recommended layout for this project:

```
~/.openclaw/workspace/
├── monsoftsolutions.com/           # Main repository (main branch)
└── monsoftsolutions.com-worktrees/ # Worktrees directory
    ├── feat-new-feature/
    ├── fix-bug-123/
    └── docs-update/
```

**Important:** Keep worktrees adjacent to (not inside) the main repo to avoid git tracking issues.

## Essential Commands Reference

| Command               | Purpose                   |
| --------------------- | ------------------------- |
| `git worktree add`    | Create new worktree       |
| `git worktree list`   | Show all worktrees        |
| `git worktree remove` | Delete worktree           |
| `git worktree prune`  | Clean up stale references |

## Workflow for AI Agents

### Step-by-Step Process

1. **Create worktree**

   ```bash
   git worktree add ../monsoftsolutions.com-worktrees/feat-name -b feat/feature-name
   ```

2. **Navigate to worktree**

   ```bash
   cd ../monsoftsolutions.com-worktrees/feat-name
   ```

3. **Install dependencies**

   ```bash
   npm install
   ```

4. **Start dev server** (use alternate port if needed)

   ```bash
   npm run dev
   # Or with custom port:
   npm run dev -- --port 4322
   ```

5. **Work on feature** — Make changes, test locally

6. **Commit and push** — Regular git workflow

   ```bash
   git add .
   git commit -m "feat: add feature description"
   git push -u origin feat/feature-name
   ```

7. **Create PR**

   ```bash
   gh pr create --title "Feature title" --body "Description"
   ```

8. **Clean up after merge**

   ```bash
   cd ~/.openclaw/workspace/monsoftsolutions.com
   git worktree remove ../monsoftsolutions.com-worktrees/feat-name
   ```

## Running the Project in Worktrees

Critical setup for each worktree:

### Dependencies

Each worktree needs its own `node_modules`:

```bash
npm install
```

### Environment Variables

Copy `.env` file if needed, or create a new one with required variables:

```bash
cp ../monsoftsolutions.com/.env .env
```

### Port Conflicts

When running multiple dev servers simultaneously, use different ports:

```bash
npm run dev -- --port 4322  # Second worktree
npm run dev -- --port 4323  # Third worktree
```

### Build Validation

Always run a full build before pushing:

```bash
npm run build
```

## Best Practices

### Naming Convention

Use branch naming pattern for worktree folders:

- `feat-descriptive-name/` for features
- `fix-issue-number/` for fixes
- `docs-topic/` for documentation

### Regular Sync

Pull main branch updates frequently to avoid drift:

```bash
git fetch origin
git rebase origin/main
```

### Commit Often

Keep atomic commits in each worktree for easier review and potential rollback.

### Clean Up Promptly

Remove worktrees after PR merge to avoid clutter:

```bash
git worktree list              # See all worktrees
git worktree remove <path>     # Remove specific worktree
git worktree prune             # Clean stale references
```

### Test Before Merge

Run full validation in worktree before merging:

```bash
npm run build
npm run check
npm run typecheck
```

## Parallel Development with Multiple Agents

Guidelines for running multiple AI agents:

- Each agent works in its own worktree
- Use different terminal sessions/windows per worktree
- Run dev servers on different ports if testing simultaneously
- Coordinate via PR descriptions to avoid conflicting changes
- Keep worktree names descriptive to identify which agent is working where

## Troubleshooting

### Branch Already Checked Out

**Problem:** `fatal: 'branch-name' is already checked out`

**Solution:** A branch can only be in one worktree at a time. Either:

- Remove the existing worktree: `git worktree remove <path>`
- Create a new branch with a different name

### Stale Worktrees

**Problem:** Worktree references point to deleted directories

**Solution:** Clean up stale references:

```bash
git worktree prune
```

### Missing node_modules

**Problem:** Commands fail with module not found errors

**Solution:** Run `npm install` in the worktree directory

### Port Already in Use

**Problem:** `Error: listen EADDRINUSE: address already in use :::4321`

**Solution:**

1. Find and stop the running dev server, or
2. Use a different port: `npm run dev -- --port 4322`

### Worktree Not Tracking Remote

**Problem:** Push fails with no upstream branch

**Solution:** Push with upstream tracking:

```bash
git push -u origin branch-name
```

## Quick Reference Card

Condensed commands for copy-paste:

```bash
# Create new feature worktree
git worktree add ../monsoftsolutions.com-worktrees/feat-name -b feat/feature-name

# Setup worktree
cd ../monsoftsolutions.com-worktrees/feat-name && npm install

# Run dev server on alternate port
npm run dev -- --port 4322

# List all worktrees
git worktree list

# Clean up after merge
git worktree remove ../monsoftsolutions.com-worktrees/feat-name

# Prune stale references
git worktree prune
```
