# LeetCode Solutions

Portfolio of accepted LeetCode solutions, synchronized automatically with [LeetSync](https://github.com/LeetSync/LeetSync).

## Progress

<!-- LEETCODE_STATS_START -->
| Metric | Value |
|---|---:|
| Problems solved | **0** |
| Languages | **0** |
| Last synced | 2026-09-24 09:15 UTC |
| Easy | 0 |
| Medium | 0 |
| Hard | 0 |
<!-- LEETCODE_STATS_END -->

## Repository structure

LeetSync creates one directory per problem:

```text
leetcode-solutions/
├── 0001-two-sum/
│   ├── README.md       # problem statement and difficulty
│   └── two-sum.py      # accepted solution
├── 0020-valid-parentheses/
│   ├── README.md
│   └── valid-parentheses.cpp
└── README.md
```

Each problem directory can also contain `Notes.md` when notes are added in LeetSync.

## How it works

1. Solve and submit a problem on LeetCode.
2. LeetSync waits for an accepted submission and pushes it through the GitHub API.
3. GitHub Actions recalculates the statistics shown above.

The workflow updates only the marked block in this file, so its manual content is preserved.

## LeetSync configuration

- **Repository:** `kkonstantin08/leetcode-solutions`
- **Subdirectory:** leave empty (repository root)
- **Branch:** `main`
- **Push:** automatic after an accepted submission
