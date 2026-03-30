# 📋 GitHub Issue Templates & Commit Messages

Use the templates below to populate your GitHub Issues. Copy the **Title** and **Description** into GitHub, then use the **Commit Sequence** to build the branch or push to main.

---

## Issue #1: Project Foundation & Environment Setup
**Title**: `Setup: Repository Scaffolding, Documentation & Dependency Configuration`

**Description**:
### Objective
Initialize the repository with professional standards to ensure team collaboration and environment reproducibility.

### Key Tasks
- [ ] Initialize directory structure for `/src`, `/data`, and `/tests`.
- [ ] Create a comprehensive `README.md` with the technical architecture (Mermaid) and project features.
- [ ] Configure `.gitignore` to prevent tracking of binary files, caches, and virtual environments.
- [ ] Define the industrial-grade environment in `requirements.txt`.

### Deliverables
- Project structure initialized.
- Technical documentation established.
- Dependency management configured.

**Commit Sequence**:
1. `git commit -m "chore: initial project scaffold and folder structure"`
2. `git commit -m "docs: add comprehensive README with architecture diagram"`
3. `git commit -m "chore: configure .gitignore for python, pycache, and env"`
4. `git commit -m "build: define project dependencies in requirements.txt"`

---

## Issue #2: Data Engineering & ETL Logic
**Title**: `Feature: Implement Attendance Processor Engine (ETL)`

**Description**:
### Objective
Build the core data ingestion engine to transform raw attendance logs into clean, numerical features for the ML model.

### Key Tasks
- [ ] Implement `AttendanceProcessor` class.
- [ ] Develop `time_to_minutes` utility to normalize logout/login times.
- [ ] Add logic for handling cross-midnight shifts (e.g., login at 10 PM, logout at 6 AM).
- [ ] Calculate deviations from standard 9 AM login and 9-hour shift durations.

### Deliverables
- Functioning ETL pipeline in `src/processing.py`.
- Automated feature engineering for ML ready-data.

**Commit Sequence**:
5. `git commit -m "feat(data): add sample data generation script and CSV"`
6. `git commit -m "feat(processing): implement time-to-minutes conversion logic"`
7. `git commit -m "feat(processing): handle cross-midnight logout shifts"`
8. `git commit -m "feat(processing): add login and duration deviation feature engineering"`

---

## Issue #3: Anomaly Detection Model implementation
**Title**: `ML: Isolation Forest Model & Reason Generator Implementation`

**Description**:
### Objective
Deploy an unsupervised machine learning model to identify pattern outliers without requiring labeled data.

### Key Tasks
- [ ] Implement `AttendanceAnomalyDetector` using Scikit-Learn's `IsolationForest`.
- [ ] Configure `StandardScaler` for preprocessing numerical features.
- [ ] Develop a "Reason Generator" logic to interpret model decisions into human-readable text.
- [ ] Support adjustable contamination rates for sensitivity tuning.

### Deliverables
- ML model class in `src/model.py`.
- Automated explanation logic for anomalies.

**Commit Sequence**:
9. `git commit -m "feat(model): implement Isolation Forest detector with standard scaling"`
10. `git commit -m "feat(model): implement fit_predict pipeline for numerical features"`
11. `git commit -m "feat(model): add automated 'Reason Generator' for detected anomalies"`

---

## Issue #4: Streamlit Analytics Dashboard
**Title**: `UI: Build Interactive Attendance Anomaly Dashboard`

**Description**:
### Objective
Create a professional web interface for HR/Operation teams to analyze logs and manage detected anomalies.

### Key Tasks
- [ ] Develop multi-tab dashboard layout (Distribution, Details, Trends).
- [ ] Implement secure CSV file uploader and sample data loader.
- [ ] Integrate Plotly for interactive data visualization.
- [ ] Add CSV export functionality for reporting.

### Deliverables
- Main app script `app.py`.
- Interactive visualization suite.

**Commit Sequence**:
12. `git commit -m "feat(ui): initialize streamlit layout with sidebar and headers"`
13. `git commit -m "feat(ui): add CSV upload and sample data loading integration"`
14. `git commit -m "feat(ui): implement model training control and anomaly metrics"`
15. `git commit -m "feat(ui): add Plotly visualizations and anomaly density heatmap"`
16. `git commit -m "feat(ui): implement anomaly report table with CSV export"`

---

## Issue #5: Testing & Project Polishing
**Title**: `QA: Automated Test Suite & Final Project Documentation`

**Description**:
### Objective
Ensure industrial reliability through automated unit testing and finalize delivery assets.

### Key Tasks
- [ ] Implement 13+ unit tests covering processing edge cases.
- [ ] Verify model stability across different contamination rates.
- [ ] Clean up docstrings and finalize final report documentation.

### Deliverables
- Comprehensive unit test suite in `/tests`.
- Finalized project documentation.

**Commit Sequence**:
17. `git commit -m "test(processing): add unit tests for time logic and feature math"`
18. `git commit -m "test(model): add unit tests for prediction stability and explanations"`
19. `git commit -m "docs: add presentation.md with slide scripts for delivery"`
20. `git commit -m "chore: final code cleanup and docstring updates"`
