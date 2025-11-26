---
description: "Tasks for 001-s-parameter-viewer"
---

# Tasks: S-Parameter Viewer

**Input**: Design documents from `/specs/001-s-parameter-viewer/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure (src/core, src/gui, src/models, tests/unit)
- [ ] T002 Create requirements.txt with scikit-rf, matplotlib, PyQt6, pytest
- [ ] T003 [P] Configure pytest and create conftest.py in tests/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create ViewportConfig model in src/models/view_config.py
- [ ] T005 Create SParameterDataset model in src/models/dataset.py
- [ ] T006 Implement core.loader.load_touchstone_file using scikit-rf in src/core/loader.py
- [ ] T007 [P] Create unit tests for dataset model in tests/unit/test_models.py
- [ ] T008 [P] Create unit tests for loader logic in tests/unit/test_loader.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Import and View S-Parameters (Priority: P1) 🎯 MVP

**Goal**: Load Touchstone files, display plot tabs (Mag/Phase/Smith), and render data

**Independent Test**: Load a standard .s2p file and verify graph renders lines.

### Implementation for User Story 1

- [ ] T009 [US1] Create PlotWidget embedding Matplotlib in src/gui/plot_widget.py
- [ ] T010 [US1] Implement plot_magnitude_db method in src/gui/plot_widget.py
- [ ] T011 [P] [US1] Implement plot_phase_deg method in src/gui/plot_widget.py
- [ ] T012 [P] [US1] Implement plot_smith method in src/gui/plot_widget.py
- [ ] T013 [US1] Create TabManager widget to handle multiple files in src/gui/tabs.py
- [ ] T014 [US1] Implement MainWindow with Menu Bar and File Dialog in src/gui/main_window.py
- [ ] T015 [US1] Connect File Open action to Loader and TabManager in src/gui/main_window.py
- [ ] T016 [US1] Create entry point in src/app.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Toggle S-Parameter Visibility (Priority: P2)

**Goal**: Show/Hide specific traces using checkboxes

**Independent Test**: Toggle checkboxes and verify traces appear/disappear.

### Implementation for User Story 2

- [ ] T017 [US2] Create ControlPanel widget with layout for checkboxes in src/gui/control_panel.py
- [ ] T018 [US2] Implement logic to update ViewportConfig visibility in src/gui/control_panel.py
- [ ] T019 [US2] Update PlotWidget to respect visible_traces config in src/gui/plot_widget.py
- [ ] T020 [US2] Integrate ControlPanel into MainWindow layout in src/gui/main_window.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 4 - Adjust Frequency Range (Priority: P3)

**Goal**: Manually set start/stop frequencies

**Independent Test**: Enter new frequency limits and verify x-axis updates.

### Implementation for User Story 4

- [ ] T021 [US4] Add Min/Max frequency inputs to ControlPanel in src/gui/control_panel.py
- [ ] T022 [US4] Implement validation logic (Min < Max) in src/gui/control_panel.py
- [ ] T023 [US4] Update PlotWidget to update axes limits on signal in src/gui/plot_widget.py

**Checkpoint**: All previous stories functional + Frequency adjustment

---

## Phase 6: User Story 3 - Inspect Data Points (Priority: P3)

**Goal**: Click on trace to see data values

**Independent Test**: Click trace, verify tooltip/marker shows correct data.

### Implementation for User Story 3

- [ ] T024 [US3] Implement matplotlib pick_event handler in src/gui/plot_widget.py
- [ ] T025 [US3] Create annotation/tooltip logic for clicked points in src/gui/plot_widget.py
- [ ] T026 [US3] Implement data lookup from Dataset based on clicked frequency in src/models/dataset.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T027 Polish GUI layout and spacing in src/gui/main_window.py
- [ ] T028 Add error handling dialogs for invalid file loads in src/gui/main_window.py
- [ ] T029 Update documentation and README.md
- [ ] T030 Final manual testing of mixed-mode v2.0 files

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3+)**: Depend on Foundational
  - US1 is MVP (required for others)
  - US2 depends on US1 (needs plot to toggle)
  - US3 and US4 depend on US1 (need plot to interact with)

### Parallel Opportunities

- T007/T008 (Unit tests) can run parallel to T004/T005/T006 (Core impl)
- T010/T011/T012 (Plot methods) can run in parallel
- US3 and US4 can technically run in parallel after US1 is complete

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup & Foundational
2. Build basic PlotWidget and MainWindow
3. Verify loading .s2p files works
4. **STOP and VALIDATE**

### Incremental Delivery

1. Add Checkboxes (US2) -> Validate
2. Add Frequency Inputs (US4) -> Validate
3. Add Markers (US3) -> Validate
