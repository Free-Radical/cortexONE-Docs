# Seven Habits Module

Role:
- Implement your personal organizing framework based on the "7 Habits" / big rocks approach.

Inputs:
- Task lists from TaskModule.
- Weekly and Daily context:
  - Weekly Compass.
  - Roles.
  - Big Rocks.
  - Daily Mission inputs.

Key behaviors:
- Weekly planning:
  - Map key tasks to roles and weekly priorities.
- Daily planning:
  - Select tasks for the Daily Mission from:
    - Weekly Compass.
    - Inbox tasks.
    - Email-derived tasks.
- Keep the Seven Habits logic separate from TaskModule:
  - TaskModule = generic engine.
  - SevenHabitsModule = how tasks are organized and chosen.

Outputs:
- Structured Weekly Compass representation.
- Structured Daily Mission representation.
- Data for the Output Bundle:
  - Markdown sections for roles, big rocks, today/tomorrow tasks.

Notes:
- This module is optional in the sense that:
  - Other users could disable it and plug in another org system module.
