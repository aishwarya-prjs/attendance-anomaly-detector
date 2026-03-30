# 📋 GitHub Issues & Commit Plan

This document outlines the professional workflow for pushing the **Attendance Anomaly Detector** project to GitHub. Follow these sequential steps to establish a high-quality development history.

---

## 🛠️ Step 1: Initial Setup
### **Issue #1: Repository Scaffolding & Initial Documentation**
**Description**: 
Initialize the project structure, define python dependencies, and create a comprehensive README that documents the system architecture and key features.
- Setup `.gitignore` to prevent tracking of cache/env files.
- Document the technical architecture using Mermaid diagrams.
- Define requirements for the industrial-grade ML environment.

**Commit Messages**:
1. `git commit -m "chore: initial project scaffold and folder structure"`
2. `git commit -m "docs: add comprehensive README with architecture diagram"`
3. `git commit -m "chore: configure .gitignore for python, pycache, and env"`
4. `git commit -m "build: define project dependencies in requirements.txt"`

---

## 📂 Step 2: Core Data Engine
### **Issue #2: Implementation of Data Processing & ETL Logic**
**Description**: 
Develop the `AttendanceProcessor` engine responsible for sanitizing raw logs, converting human-readable time into numerical features, and handling edge cases like 24-hour shifts.
- Implement time-to-minutes logic.
- Handle "Next Day" logout normalization.
- Engineer login/duration deviation features.

**Commit Messages**:
5. `git commit -m "feat(data): add sample data generation script and CSV"`
6. `git commit -m "feat(processing): implement time-to-minutes conversion logic"`
7. `git commit -m "feat(processing): handle cross-midnight logout shifts"`
8. `git commit -m "feat(processing): add login and duration deviation feature engineering"`

---

## 🧠 Step 3: Machine Learning Logic
### **Issue #3: Anomaly Detection with Isolation Forest & Explanation Engine**
**Description**: 
Integrate Scikit-learn for unsupervised learning. Develop the ML pipeline to detect behavior outliers and implement an explanation generator to translate mathematical scores into HR-friendly insights.
- Feature scaling with StandardScaler.
- Isolation Forest model integration.
- Human-readable reason generation for anomalies.

**Commit Messages**:
9. `git commit -m "feat(model): implement Isolation Forest detector with standard scaling"`
10. `git commit -m "feat(model): implement fit_predict pipeline for numerical features"`
11. `git commit -m "feat(model): add automated 'Reason Generator' for detected anomalies"`

---

## 🎨 Step 4: Frontend Development
### **Issue #4: Interactive Streamlit Dashboard Development**
**Description**: 
Build the comprehensive Streamlit UI. Implement interactive components for model tuning (contamination slider), data visualization (Plotly), and anomaly reporting.
- Implement tabbed layout for visual vs tabular analysis.
- Create department-specific heatmaps.
- Implement "One-Click" training and report export.

**Commit Messages**:
12. `git commit -m "feat(ui): initialize streamlit layout with sidebar and headers"`
13. `git commit -m "feat(ui): add CSV upload and sample data loading integration"`
14. `git commit -m "feat(ui): implement model training control and anomaly metrics"`
15. `git commit -m "feat(ui): add Plotly visualizations and anomaly density heatmap"`
16. `git commit -m "feat(ui): implement anomaly report table with CSV export"`

---

## ✅ Step 5: QA & Documentation
### **Issue #5: Unit Testing Suite & Delivery Documentation**
**Description**: 
Verify system stability with 13+ automated industrial tests and finalize the presentation materials for project delivery.
- Test cross-midnight time handling.
- Verify model sensitivity to contamination rates.
- Finalize delivery scripts and logs.

**Commit Messages**:
17. `git commit -m "test(processing): add unit tests for time logic and feature math"`
18. `git commit -m "test(model): add unit tests for prediction stability and explanations"`
19. `git commit -m "docs: add presentation.md with slide scripts for delivery"`
20. `git commit -m "chore: final code cleanup and docstring updates"`

---

### 💡 Pro Workflow Tip:
When you push the final commit for an issue, use the syntax `Closes #1` in your commit description to automatically link and close the GitHub Issue!
