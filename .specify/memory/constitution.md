<!--
SYNC IMPACT REPORT
==================
Version: 1.0.0 (Initial Ratification)
Changes:
- Defined Project Name: rf_gui_Sparameters
- Defined Principles:
  1. High Quality & Testability (derived from user input)
  2. MVP & Simplicity (YAGNI) (derived from user input)
  3. Pythonic Standards (derived from user input)
- Removed undefined template principles (4 & 5) to adhere to "Simplicity" and avoid overdesign.
- Defined Governance:
  - Ratified: 2025-11-26
  - Version: 1.0.0
Templates Status:
- .specify/templates/plan-template.md: ✅ Compatible
- .specify/templates/spec-template.md: ✅ Compatible
- .specify/templates/tasks-template.md: ✅ Compatible
TODOs:
- None.
-->
# rf_gui_Sparameters Constitution

## Core Principles

### I. High Quality & Testability
Code must be high quality and testable. We adhere to a Test-Driven Development (TDD) mindset where possible. Unit tests are mandatory for logic to ensure robustness and prevent regression. Coverage should be maintained at a high level.

### II. MVP & Simplicity (YAGNI)
Build the Minimum Viable Product (MVP) first. Do not overdesign. Strictly follow "You Aren't Gonna Need It" (YAGNI) and "Keep It Simple, Stupid" (KISS). Avoid premature optimization and unnecessary abstraction. Implement only what is required for the current feature set.

### III. Pythonic Standards
Adhere strictly to Python best practices and PEP 8 style guidelines. Use idiomatic Python constructs (e.g., list comprehensions, context managers, correct type hinting). As the project is built in Python, consistency with the language's ecosystem is paramount.

## Technology Stack

**Language**: Python (Latest stable recommended)
**GUI Framework**: Python-based GUI libraries appropriate for the MVP (e.g., Tkinter, PyQt/PySide, or others as required).
**Testing**: Standard Python testing frameworks (e.g., pytest, unittest).

## Development Workflow

1.  **Test-First**: Changes should ideally be accompanied by tests.
2.  **Linting**: Code must pass standard Python linting (e.g., pylint, flake8, black).
3.  **Versioning**: Adhere to semantic versioning for releases.
4.  **Review**: Code reviews must ensure adherence to the Pythonic Standards and MVP principles.

## Governance

This constitution is the supreme source of truth for engineering decisions.

- **Amendments**: Require a pull request, team review, and a version bump of this document.
- **Compliance**: All code reviews must verify compliance with these principles. Complexity must be justified.
- **Runtime Guidance**: See `README.md` for getting started.

**Version**: 1.0.0 | **Ratified**: 2025-11-26 | **Last Amended**: 2025-11-26