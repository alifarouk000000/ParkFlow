# ParkFlow — Smart Parking Management System

Final graduation project for the **Samsung Innovation Campus (SIC 8) Coding & Programming** track, built by a team of four.

ParkFlow is a Streamlit application that runs a parking lot end to end: vehicles enter, get a slot or join a waiting queue, exit with an automatic fee, and the next waiting vehicle is served. A separate analytics view explores a historical IIoT smart-parking dataset.

> Team repository: [Arwa245-coder/ParkFlow1](https://github.com/Arwa245-coder/ParkFlow1). This copy keeps the full commit history.

## Team

| Member | Role | Files |
|---|---|---|
| **Ali Farouk** | Core system + integration | `core.py`, `main.py`, `tests/`, `demo_core.py` |
| Ibrahim | Data structures + algorithms | `structures_and_algorithms.py` |
| Arwa Emad | Dataset + data analysis | `analytics.py`, `analytics.ipynb`, `data/` |
| Ziad Hamdy | Streamlit UI + dashboard | `dashboard.py` |

## Features

- **Live parking map** of the simulated lot, grouped into zones (Zone A, Zone B, ...)
- **Vehicle entry and exit** with plate validation, duplicate detection and an automatic fee (with a fee quote before exit)
- **FIFO waiting queue** when the lot is full; the first waiting vehicle that fits a freed slot is parked automatically
- **Three user roles**: Driver, Gate Operator and Admin, each seeing only the controls it may use
- **Search** by plate, slot, vehicle type, status or zone
- **History, undo and CSV export** of every operation
- **Historical analytics tab**: cleaning and analysis of 1,000 IIoT parking records with filters, KPIs and six charts

## How it works

```
arrival → validate plate → reject duplicates → choose slot (greedy) → park
                                                      └─ no slot → waiting queue
exit → duration + fee → release slot → serve waiting queue
```

**Fees:** first 15 minutes free, then each started hour at the vehicle rate (Car 10, Motorcycle 5, Truck 20 EGP; electric vehicles add 5 EGP/h for charging), capped at 10 billable hours per day.

## Technical highlights

**Object-oriented design (`core.py`)**
- `Vehicle` → `Car`, `Motorcycle`, `Truck`; `ElectricVehicle` extends `Car` and overrides `calculate_fee()` (polymorphism)
- `User` → `Driver`, `GateOperator`, `Admin` with permission sets
- `ParkingSlot` (Compact / Standard / Oversized), a 2D grid of slots, and custom exceptions with a `_safe` decorator so the UI never crashes on bad input
- Regex plate validation that accepts Latin and Arabic plates (`abc-1234` → `ABC 1234`)

**Data structures and algorithms**

| Used for | Structure / algorithm | Why |
|---|---|---|
| Plate lookup at the gate | Hash table | O(1) average on every entry and exit |
| Waiting list | Queue | First come, first served |
| Undo | Stack | Undo reverses the latest action |
| Slot choice | Greedy | Smallest fitting slot, nearest the gate; keeps large slots free for trucks |
| Find by vehicle ID | Binary search | IDs are created in order, so records are already sorted |
| Partial plate search | Sequential search | Substring matching needs a full scan |
| Sorting records | Merge sort | O(n log n) and stable; built-in sort not allowed |

**Integration (`main.py`)**: keeps one `ParkingSystem` in `st.session_state` so data survives every rerun, connects the four dashboard tabs, and `core.py` self-tests the team's data structures at startup (the sidebar shows which implementation is active).

## Run it

```bash
pip install -r requirements.txt
streamlit run main.py
```

Other commands:

```bash
python demo_core.py                      # console demo of the core system
python -m unittest discover -s tests -v  # 11 unit tests
```

## Project structure

```
├── main.py                       # Streamlit entry point and integration
├── core.py                       # ParkingSystem, vehicles, users, slots, fees, validation
├── structures_and_algorithms.py  # stack, queue, hash table, searches, merge sort, greedy
├── analytics.py                  # load, clean, validate and analyze the dataset
├── analytics.ipynb               # analysis notebook
├── dashboard.py                  # Streamlit screens and charts
├── data/                         # IIoT smart parking dataset (CSV)
├── tests/test_core.py            # unit tests for the core
├── demo_core.py                  # console demo
└── CORE_API.md                   # core API reference for the team
```
