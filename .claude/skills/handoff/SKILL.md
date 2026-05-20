---
name: handoff
description: Write a session state document so work can resume in a fresh session without context loss.
---

# Role
You are a Senior Technical Lead. Create a comprehensive "Session State & Handoff" document from our current conversation.

# Objective
Write a Markdown file to ./session-summary/ (append to today's file if one exists) detailed enough that a fresh Claude session could read ONLY this file and immediately resume.

# Guidelines
- Be specific: not "fixed the bug" but "fixed NullReference in auth.ts by initializing user object"
- Include exact file paths, commands, variable names
- Capture gotchas and environment quirks
- Next steps must be executable tasks
- If a section has nothing, say so — a gap is better than plausible-sounding fiction

# Output Format

## 1. Goal
- High-level goal of the project
- What this session specifically tried to achieve

## 2. Current State
### ✅ Completed
### ⚠️ In Progress (where exactly did we stop?)
### ❌ Blocking Issues (paste relevant errors/logs)

## 3. Technical Learnings
- Discoveries made this session
- Important file locations

## 4. Next Steps (prioritized)
1. Exact first action for next session
2. ...

## 5. Restoration Procedure
- How to get the environment running again
