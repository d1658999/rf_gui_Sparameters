# Feature Specification: S-Parameter Viewer

**Feature Branch**: `001-s-parameter-viewer`  
**Created**: 2025-11-26  
**Status**: Draft  
**Input**: User description: "being a RF engineer, we need to review and watch the performance and S-parameters like S11/S12/S21/S22 etc and we can easily check the checked botton to see if we open or close the S-paramenters. we also need load or import the existed .snp file like .s1p/.s2p/.s3p/.s4p etc. we also can change the frequency range for the x-axis. we also can mark the specific point to see all the information on the plot."

## Clarifications

### Session 2025-11-26 (Implementation Updates)
- Q: How should markers behave? → A: Support multiple persistent markers; Right-click to clear all.
- Q: How should Smith Chart handle frequency range? → A: Filter displayed data points to match the selected frequency band.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Import and View S-Parameters (Priority: P1)

As an RF Engineer, I want to load Touchstone (.snp) files (v1.0 and v2.0) so that I can visualize the frequency response of my DUT (Device Under Test).

**Why this priority**: This is the fundamental capability of the application. Without loading and plotting data, no other features matter.

**Independent Test**: Can be fully tested by loading a standard .s2p file and verifying that the graph renders lines corresponding to the data points.

**Acceptance Scenarios**:

1. **Given** the application is open, **When** I select an `.s2p` file from the file dialog, **Then** the application parses the file and displays a plot with frequency on the x-axis.
2. **Given** a file is loaded, **Then** the plot defaults to showing Magnitude (dB) for all available S-parameters, but allows switching to Phase or Smith Chart views via **plot type tabs**.
3. **Given** a file is already open, **When** I load a second file, **Then** it opens in a **new file tab**, keeping the first file open and accessible.
4. **Given** an invalid or corrupted file is selected, **When** I attempt to load it, **Then** the system displays an error message and does not crash.
5. **Given** a Touchstone v2.0 file with mixed-mode parameters, **When** loaded, **Then** the system correctly parses and displays the data.

---

### User Story 2 - Toggle S-Parameter Visibility (Priority: P2)

As an RF Engineer, I want to show or hide specific S-parameter traces using checkboxes so that I can focus on specific performance metrics (e.g., only looking at Return Loss S11).

**Why this priority**: RF plots can get cluttered, especially with 4-port devices (16 traces). Filtering is essential for analysis.

**Independent Test**: Load a file, then toggle the checkboxes for specific traces and verify they appear/disappear from the plot.

**Acceptance Scenarios**:

1. **Given** a loaded file with multiple parameters (S11, S21), **When** I uncheck the checkbox for "S21", **Then** the S21 trace is removed from the plot view immediately.
2. **Given** a trace is hidden, **When** I check the checkbox for "S21", **Then** the S21 trace reappears with its original color/style.
3. **Given** a new file is loaded, **Then** the controls dynamically update to list only the S-parameters available in that file (e.g., only S11 for .s1p).

---

### User Story 3 - Inspect Data Points (Priority: P3)

As an RF Engineer, I want to mark specific points on the trace so that I can read the exact frequency and magnitude values at critical frequencies.

**Why this priority**: Visual trends are good, but engineers need precise numbers for reporting and verification.

**Independent Test**: Click on a plotted line and verify a marker/tooltip appears with the correct numerical data.

**Acceptance Scenarios**:

1. **Given** a visible trace, **When** I click on a specific point on the line, **Then** a **persistent marker** is placed at that location.
2. **Given** a marker is placed, **Then** a label next to the marker shows the exact Frequency and Value (dB, Deg, or Z) of that point.
3. **Given** existing markers, **When** I click another point, **Then** a **new additional marker** is added (previous markers remain).
4. **Given** markers exist on the plot, **When** I **right-click** anywhere on the plot area, **Then** all markers are cleared.

---

### User Story 4 - Adjust Frequency Range (Priority: P3)

As an RF Engineer, I want to manually set the start and stop frequencies of the x-axis so that I can zoom in on a specific band of interest.

**Why this priority**: Analyzing narrow-band performance often requires excluding out-of-band data.

**Independent Test**: Manually enter start/stop frequencies and verify the plot x-axis limits change.

**Acceptance Scenarios**:

1. **Given** a plot covering 1GHz to 10GHz, **When** I enter "2GHz" as Start and "3GHz" as Stop, **Then** the plot redraws showing only the 2-3GHz range.
2. **Given** the frequency range inputs, **When** I enter a Start frequency higher than the Stop frequency, **Then** the system prevents the change or warns the user.
3. **Given** a Smith Chart view, **When** I adjust the frequency range, **Then** the chart updates to display **only the data points** within that frequency band.

### Edge Cases

- What happens when a file has non-monotonic frequency points? (Assume standard behavior or error).
- How does the system handle extremely large files (e.g., >100MB .snp files)?
- What happens if the file format version (Touchstone 1.0 vs 2.0) varies?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load Touchstone files with extensions .s1p, .s2p, .s3p, .s4p, supporting **both v1.0 and v2.0 standards**.
- **FR-002**: System MUST parse Frequency and S-parameter (Real/Imaginary or Mag/Angle) data from the file.
- **FR-003**: System MUST calculate and plot S-parameter Magnitude (dB), Phase (degrees), and Smith Charts.
- **FR-004**: System MUST generate a control panel with a labeled checkbox for every S-parameter present in the file (e.g., S11, S12...).
- **FR-005**: System MUST update the plot in real-time (or near real-time) when checkboxes are toggled.
- **FR-006**: System MUST provide input fields to define the Minimum and Maximum frequency for the plot's x-axis.
- **FR-007**: System MUST allow the user to select a point on the plot and display the coordinate values (Frequency, dB, or Phase/Impedance based on view) textually.
- **FR-008**: System MUST automatically scale the y-axis to fit the visible traces.
- **FR-009**: System MUST provide a **tabbed interface** to switch between Magnitude, Phase, and Smith Chart views within a file's display.
- **FR-010**: System MUST support **multiple open files**, with each file displayed in its own independent tab or window container.

### Key Entities

- **SParameterDataset**: Represents the loaded file data. Contains:
    - `frequencies`: List[Float]
    - `matrix`: Map<String, List[Complex]> (e.g., "S11" -> data)
    - `port_count`: Integer
    - `filename`: String
    - `version`: String (v1.0/v2.0)
- **ViewportConfig**: Represents current view state for a specific file tab. Contains:
    - `visible_traces`: Set<String>
    - `freq_min`: Float
    - `freq_max`: Float
    - `active_plot_type`: Enum (Magnitude, Phase, Smith)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can load a standard 1000-point .s2p file and see the plot rendered in under 1 second.
- **SC-002**: Toggling a trace visibility checkbox updates the plot in under 100ms.
- **SC-003**: User can read the exact dB value of a resonance peak using the marker tool with <1% error relative to the file data.
- **SC-004**: System successfully parses 100% of valid standard Touchstone v1.0 files provided for testing.
- **SC-005**: System successfully parses valid Touchstone v2.0 files with mixed-mode parameters.
