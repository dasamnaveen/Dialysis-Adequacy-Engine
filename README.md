# Dialysis-Adequacy-Engine
A high-performance clinical engine for monitoring dialysis treatment adequacy. Automates **Urea Reduction Ratio (URR)** and **Kt/V** (Daugirdas II) calculations across longitudinal patient records to identify sub-optimal sessions and prevent clinical complications through automated trend alerts.

## Dialysis Adequacy Monitor (NumPy-Powered)

This project demonstrates how to handle longitudinal medical data using **NumPy Structured Arrays** and **Vectorized Operations** for maximum speed and memory efficiency—without requiring the Pandas library.

##  Clinical Problem
In dialysis, "adequacy" is a measure of how much waste (urea) is removed from a patient's blood. 
* **Sub-optimal cleaning** leads to toxin buildup and poor patient outcomes.
* **Fluid removal** must be balanced to avoid heart strain.
* **Trends matter:** A slow decline in efficiency often signals a failing vascular access (clotting) before it becomes a clinical emergency.

## Key Features
* **Vectorized Calculations:** Processes an entire month of sessions in a single mathematical sweep.
* **Dual-Metric Analysis:** Calculates both the simple **URR %** and the gold-standard **Kt/V** (Single-pool Daugirdas).
* **Automated Clinical Alerts:**
    * **Low Dose:** Flags sessions falling below the $Kt/V < 1.2$ or $URR < 65\%$ threshold.
    * **Trend Detection:** Identifies 3+ sessions of declining efficiency (early warning for access failure).
    * **Fluid Safety:** Flags sessions where fluid removal exceeds 5% of body weight.
* **Zero-Pandas Dependency:** Uses lightweight NumPy structured arrays for tabular data management.

## The Math
The core of this engine uses the Daugirdas II formula:

$$Kt/V = -\ln(R - 0.008 \times T) + (4 - 3.5 \times R) \times \frac{W}{V}$$

Where:
* $R$ = Post-urea / Pre-urea ratio
* $T$ = Dialysis duration (hours)
* $W$ = Ultrafiltration (Weight loss)
* $V$ = Post-dialysis weight (Total body water)

## Installation & Usage

### Prerequisites
* Python 3.x
* NumPy

```bash
pip install numpy
```

### Quick Start
1. Clone the repository.
2. Run `dialysis_monitor.py` to see the demonstration report.
3. Modify the `patient_records` array to input your own clinical data.

## Tech Stack
* **Language:** Python 3
* **Library:** NumPy (Structured Arrays, Vectorization, Logarithmic functions)
* **Formatting:** Tabulate-style console output

## 📜 License
This project is for educational and clinical decision-support demonstration purposes. Always consult a certified nephrologist for actual medical prescriptions.
