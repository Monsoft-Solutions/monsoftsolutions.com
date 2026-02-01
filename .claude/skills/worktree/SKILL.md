---
name: worktree
description: Manage git worktrees for parallel development. Use when creating feature branches in separate directories, setting up worktrees for AI agents, cleaning up merged worktrees, or when the user mentions "worktree", "parallel development", or "multiple branches".
allowed-tools: Bash(git *) Bash(npm *) Bash(ls *) Bash(cd *)
---

# Git Worktree Management

Manage git worktrees for parallel feature development. For full documentation, see [docs/GIT-WORKTREE.md](../../docs/GIT-WORKTREE.md).

## Project Paths

- **Main repo:** `~/.openclaw/workspace/monsoftsolutions.com/`
- **Worktrees directory:** `~/.openclaw/workspace/monsoftsolutions.com-worktrees/`

## Quick Commands

### Create New Worktree

```bash
git worktree add ../monsoftsolutions.com-worktrees/<folder-name> -b <branch-name>
```

### List Worktrees

```bash
git worktree list
```

### Remove Worktree

```bash
git worktree remove ../monsoftsolutions.com-worktrees/<folder-name>
```

### Prune Stale References

```bash
git worktree prune
```

## Workflow: Create Feature Worktree

When the user wants to create a new worktree:

1. **Create the worktree**

   ```bash
   git worktree add ../monsoftsolutions.com-worktrees/feat-<name> -b feat/<feature-name>
   ```

2. **Navigate and install dependencies**

   ```bash
   cd ../monsoftsolutions.com-worktrees/feat-<name> && npm install
   ```

3. **Start dev server** (use alternate port if main is running)

   ```bash
   npm run dev -- --port 4322
   ```

4. **After work is complete, push and create PR**
   ```bash
   git push -u origin feat/<feature-name>
   gh pr create --title "<Title>" --body "<Description>"
   ```

## Workflow: Cleanup After Merge

1. **Switch back to main repo**

   ```bash
   cd ~/.openclaw/workspace/monsoftsolutions.com
   ```

2. **Remove the worktree**

   ```bash
   git worktree remove ../monsoftsolutions.com-worktrees/feat-<name>
   ```

3. **Delete the branch locally** (optional)
   ```bash
   git branch -d feat/<feature-name>
   ```

## Naming Conventions

| Type    | Folder Pattern  | Branch Pattern |
| ------- | --------------- | -------------- |
| Feature | `feat-<name>/`  | `feat/<name>`  |
| Fix     | `fix-<issue>/`  | `fix/<issue>`  |
| Docs    | `docs-<topic>/` | `docs/<topic>` |

## Port Assignments

| Worktree        | Suggested Port |
| --------------- | -------------- |
| Main repo       | 4321 (default) |
| First worktree  | 4322           |
| Second worktree | 4323           |
| Third worktree  | 4324           |

## Troubleshooting

- **Branch already checked out**: Remove existing worktree first
- **Missing node_modules**: Run `npm install` in the worktree
- **Port in use**: Use `--port` flag with different port number
- **Stale worktrees**: Run `git worktree prune`
