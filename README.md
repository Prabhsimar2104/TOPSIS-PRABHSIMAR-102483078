# TOPSIS Web Service & Python Package

Multi-Criteria Decision Making using TOPSIS

This project implements the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) algorithm and provides:

1. A Python CLI tool published on PyPI
2. A deployed Web Service with a user-friendly interface

## 1. Methodology

The TOPSIS workflow followed in this project is shown below:

```
Data Collection
      ↓
Data Validation & Preprocessing
      ↓
Weight & Impact Assignment
      ↓
TOPSIS Computation
      ↓
Result Generation & Ranking
      ↓
Result Delivery (CSV / Email)
```

## 2. Description

- TOPSIS is a Multi-Criteria Decision Making (MCDM) technique.
- It ranks alternatives based on their distance from:
  - Ideal Best Solution
  - Ideal Worst Solution
- The alternative closest to the ideal solution gets Rank 1.

### Key Highlights

- Implemented fully in Python
- Available as a CLI tool via PyPI
- Extended into a Web Service
- Input validation for weights, impacts, and email
- Results generated in CSV format

## 3. Input / Output

### Input

- CSV file containing alternatives and criteria
- Weights (comma-separated, numeric)
- Impacts (comma-separated, `+` or `-`)

#### Example Input CSV

```
Model,Storage,Camera,Price,Rating
M1,16,12,250,5
M2,16,8,200,3
M3,32,16,300,4
M4,32,8,275,4
```

#### Weights

```
0.25,0.25,0.25,0.25
```

#### Impacts

```
+,+,-,+
```

### Output

The output CSV file contains two additional columns:

- Topsis Score
- Rank

#### Example Output

| Model | Storage | Camera | Price | Rating | Topsis Score | Rank |
|-------|---------|--------|-------|--------|--------------|------|
| M3    | 32      | 16     | 300   | 4      | 0.69         | 1    |
| M4    | 32      | 8      | 275   | 4      | 0.53         | 2    |
| M1    | 16      | 12     | 250   | 5      | 0.53         | 3    |

## 4. Python Package (PyPI CLI Tool)

### Installation

```bash
pip install Topsis-Prabhsimar-102483078
```

### Usage

```bash
topsis <input_csv> <weights> <impacts> <output_csv>
```

### Example

```bash
topsis data.csv "1,1,1,1" "+,+,-,+" result.csv
```

PyPI Link: [https://pypi.org/project/Topsis-Prabhsimar-102483078/](https://pypi.org/project/Topsis-Prabhsimar-102483078/)

## 5. Web Service

The TOPSIS algorithm is also available as a web application.

### Features

- Upload CSV file
- Enter weights and impacts
- Email-based result delivery
- Fully validated inputs
- Clean and responsive UI

Live Web Service: [https://topsis-prabhsimar-102483078.streamlit.app/](https://topsis-prabhsimar-102483078.streamlit.app/)

## 6. Screenshot of the Interface

![TOPSIS Web Interface](https://github.com/Prabhsimar2104/TOPSIS-PRABHSIMAR-102483078/blob/main/Screenshot%202026-02-04%20074152.png)

The web interface allows users to:

- Upload a CSV file
- Enter weights and impacts
- Provide an email address
- Submit the form to perform TOPSIS analysis

## 7. Project Structure

```
TOPSIS-PRABHSIMAR-102483078/
│
├── package/
│   ├── dist/
│   ├── topsis_prabhsimar_102483078/
│   │   ├── __init__.py
│   │   └── topsis.py
│   ├── Topsis_Prabhsimar_102483078.egg-info/
│   ├── LICENSE
│   ├── README.md
│   └── setup.py
│
├── web-service/
│   ├── .streamlit/
│   │   └── secrets.toml
│   ├── README.md
│   ├── requirements.txt
│   └── streamlit_app.py
│
├── .gitignore
└── README.md
```

## 8. Academic Information

- **Course:** UCS654 – Predictive Analytics using Statistics
- **Student Name:** Prabhsimar Singh
- **Roll Number:** 102483078
- **Institute:** Thapar Institute of Engineering & Technology

## 9. License

This project is licensed under the MIT License.