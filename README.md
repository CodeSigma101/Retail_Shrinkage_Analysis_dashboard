# Naivas Kahawa Sukari Shrinkage Analysis system

## 📌 Project Overview
Project **Naivas Shrinkage Intelligence (NSI)** is an enterprise-grade retail command center specifically engineered for the 24-hour operations at the Naivas Kahawa Sukari branch. 

Traditional supermarket auditing relies on static, trailing monthly percentages. This project transitions operations into a predictive loss prevention model by mapping margin leakage across three core tactical vectors:
1. **WHAT** is walking out (Isolated via horizontal Pareto distributions).
2. **WHEN** the branch is vulnerable (Isolated via high-contrast 24-hour green-on-black heatmaps).
3. **WHY** the variance occurs (Isolated via hierarchical treemaps and predictive value indexes).

---

## 🛠️ System Features & Analytics Portfolio
* **Total Branch View Integration**: Seamlessly aggregates and joins dataset metrics across **GM** (General Merchandise/Liquor), **FMCG** (Daily Commodities), and **FRESH** (Perishables/Butchery).
* **Corporate Visual Palette**: Fully styled with official corporate branding—utilizing high-contrast **Naivas Dark Green (`#1b4d3e`)** and **Naivas Orange (`#e67e22`)**.
* **Model A (Operational Value Loss Index)**: Automatically groups, counts, and costs historical ledger rows to rank root causes by their average transaction impact. Includes a dynamic, localized **SKU Deep-Dive Explorer**.
* **Model B (Tactical LP Schedule Matrix)**: Evaluates all 168 hours of the weekly cycle to extract the top 5 high-bleed windows. Outputs an automated plain-text guard placement directive.
* **Strategic ROI Simulation Engine**: Allows interactive, real-time tracking of capital expenses against targeted margin contractions, instantly plotting payback horizons in months.
* **1-Based Indexing Compliance**: Data frame indices are adjusted to run strictly from **1, 2, 3...**, removing default developer zero-padding (`0, 1, 2...`) for clear management scanning.

---

## 🚀 Deployment & Installation Guide

### 1. Repository Setup & Dependencies
Clone or create your local workspace folder, drop your code into a script named `dashboard.py`, and install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Corporate Logo Local Integration (Offline Safety Mode)
To ensure the dashboard displays the corporate logo without relying on network hotlinks or facing internet drops during meetings:
1. Download a transparent Naivas logo graphic file (`.png`).
2. Drop the asset directly into your project root directory.
3. Name the file exactly **`naivas_logo.png`**.
*(The application features built-in fallback rules that dynamically source the file locally first).*

### 3. Initialize the Web Application Server
Run the localized Streamlit engine directly from your command terminal box:
```bash
streamlit run dashboard.py
```

### 4. Local Node Viewport
Open your web browser and navigate to the live operational interface at:
👉 **`http://localhost:8501`**

---

## 📂 System Directory Mapping
Your active production workspace directory folder should be structured as follows:
```text
naivas-sukari-lp/
│
├── dashboard.py         # Main analytics and Streamlit UI engine
├── naivas_logo.png      # Local corporate brand graphic emblem asset
├── README.md            # System operational documentation manual
└── requirements.txt     # Python project deployment dependency ledger
```

---

## 🛡️ Operational Taxonomy Reference
To connect your live ERP database or spreadsheet log to this workspace later, map your dataset columns to match these system expectations:
* `sku`: Product nomenclature labels (e.g., `Brookside_Milk_500ml`).
* `kes_value`: The actual financial value in KES of the lost inventory.
* `classification`: Categorical parameters strictly labeled as `GM`, `FMCG`, or `FRESH`.
* `cause`: Root cause tags classified as `Theft`, `Receiving_Error`, `Supplier_Short`, `Spoilage`, or `Damage`.
* `hour`: Time of day logged as an integer from `0` to `23`.
* `day`: Day of the week string (e.g., `Monday`, `Friday`).
