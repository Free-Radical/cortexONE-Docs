# Task Module

Role:
- Provide a generic task engine for Cortex1 independent of any organizing framework.

Inputs:
- Task objects from:
  - EmailModule.
  - SevenHabitsModule (Daily/Weekly).
  - Manual entries or notes.
- Tags from Tagger:
  - @time, @energy, @deadline, @context, @owner.

Key behaviors:
- Normalize tasks into a uniform internal format.
- Score and categorize:
  - Today / Tomorrow / Later / Someday.
- Support basic prioritization based on:
  - Deadlines.
  - Energy and time slots.
  - User-configured rules.

Outputs:
- Lists of tasks grouped by time horizon.
- Data structures consumed by:
  - SevenHabitsModule (for roles and big rocks).
  - Daily Mission generation.
- Checklists for the Output Bundle.

Notes:
- This module does not enforce a specific productivity philosophy.
- It is meant to be reusable when swapping out Seven Habits for GTD or other systems.
