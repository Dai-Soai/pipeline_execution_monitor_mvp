# Pipeline Execution Monitor MVP

Pipeline Execution Monitor MVP is a lightweight utility for observing pipeline execution status, execution timelines, node states, and runtime metrics within the RADAR Services pipeline ecosystem.

---

# Overview

This utility consumes pipeline execution logs and produces:

- Pipeline execution state
- Node execution state
- Execution timeline
- Runtime metrics
- JSON monitor reports

The generated monitor report can be consumed by downstream utilities such as:

- Pipeline Retry Controller
- Pipeline Notification
- Pipeline Audit Trail
- Pipeline Dashboard

---

# Features

- Load pipeline execution logs
- Build pipeline execution state
- Build node execution states
- Build execution timeline
- Calculate execution metrics
- Generate JSON monitor reports
- CLI interface
- Fully tested with pytest

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<your-account>/pipeline_execution_monitor_mvp.git
cd pipeline_execution_monitor_mvp
```

Create a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -e .
```

---

# CLI Usage

Monitor execution log.

```bash
pipeline-monitor monitor data/sample_execution_log.json
```

Verbose mode.

```bash
pipeline-monitor monitor data/sample_execution_log.json --verbose
```

Generate JSON monitor report.

```bash
pipeline-monitor monitor \
    data/sample_execution_log.json \
    --json \
    --output outputs/monitor_report.json
```

---

# Example Output

CLI

```text
Pipeline Execution Monitor

Pipeline ID: pipeline-demo-001

Status: running

Metrics

Timeline Summary
```

JSON

```json
{
  "pipeline_state": {},
  "nodes": [],
  "timeline": [],
  "metrics": {}
}
```

---

# JSON Monitor Report

Generated report includes:

- pipeline_state
- nodes
- timeline
- metrics

Example:

```text
outputs/
└── monitor_report.json
```

---

# Project Structure

```text
pipeline_execution_monitor_mvp/
│
├── pipeline_execution_monitor/
│   ├── cli.py
│   ├── contract.py
│   ├── loader.py
│   ├── metrics.py
│   ├── report.py
│   ├── state_builder.py
│   └── timeline.py
│
├── tests/
│
├── data/
│   └── sample_execution_log.json
│
├── outputs/
│   └── .gitkeep
│
├── README.md
├── pyproject.toml
└── .gitignore
```

---

# Development

Install editable package.

```bash
pip install -e .
```

Run tests.

```bash
pytest
```

---

# Build Package

Build source distribution and wheel.

```bash
python -m build
```

Install wheel.

```bash
pip install dist/*.whl
```

---

# Testing

Current status:

- Pytest
- CLI
- JSON Export
- Editable Install
- Wheel Build

---

# Architecture

```text
Execution Log
        │
        ▼
Loader
        │
        ▼
State Builder
        │
        ├────────────┐
        ▼            ▼
Timeline      Metrics
        │            │
        └──────┬─────┘
               ▼
        Monitor Report
               │
        ┌──────┴─────────┐
        ▼                ▼
      CLI          JSON Export
```

---

# Roadmap Position

```text
Pipeline Template Registry
        ↓
Pipeline Variable Resolver
        ↓
Pipeline Validator
        ↓
Pipeline Dependency Analyzer
        ↓
Pipeline Execution Planner
        ↓
Pipeline Execution Monitor   ← Current Utility
        ↓
Pipeline Orchestrator
        ↓
Workflow Runner
```

---

# License

MIT License.
