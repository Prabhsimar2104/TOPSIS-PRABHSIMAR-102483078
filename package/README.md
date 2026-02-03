# Topsis-Prabhsimar-102483078

## 📌 Description

This package implements the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method, a popular **multi-criteria decision-making (MCDM)** technique.

TOPSIS is used to rank alternatives based on their relative distance from:
- an **ideal best solution**
- an **ideal worst solution**

It helps decision-makers choose the best option among multiple alternatives.

---

## 🧠 Applications of TOPSIS

TOPSIS is widely used in:
- Product selection and comparison  
- Supplier evaluation  
- Project prioritization  
- Performance assessment  
- Resource allocation  
- Investment analysis  

---

## ⚙️ Installation

Install the package using pip:

```bash
pip install Topsis-Prabhsimar-102483078
```

## 🚀 Usage

After installation, the topsis command becomes available in the terminal.

### Basic Syntax

```
topsis <input_csv> <weights> <impacts> <output_csv>
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| input_csv | Path to the CSV file containing the decision matrix |
| weights | Comma-separated numerical weights for each criterion |
| impacts | Comma-separated impacts (+ for benefit, - for cost) |
| output_csv | Path where the output CSV file will be saved |

---

## 📊 Example

### Input File (sample.csv)

```
Model,Storage(in GB),Camera(in MP),Price(in $),Rating
M1,16,12,250,5
M2,16,8,200,3
M3,32,16,300,4
M4,32,8,275,4
M5,16,16,225,2
```

### Decision Criteria

**Weights Vector**
```
0.25,0.25,0.25,0.25
```

**Impacts Vector**
```
+,+,-,+
```

- Storage → Benefit (+)
- Camera → Benefit (+)
- Price → Cost (-)
- Rating → Benefit (+)

### Command

```bash
topsis sample.csv "0.25,0.25,0.25,0.25" "+,+,-,+" output.csv
```

---

## 📈 Output

The output CSV file will contain two additional columns:
- Topsis Score (closeness coefficient)
- Rank

### Sample Output

| Model | Storage | Camera | Price | Rating | Topsis Score | Rank |
|-------|---------|--------|-------|--------|--------------|------|
| M3 | 32 | 16 | 300 | 4 | 0.69 | 1 |
| M4 | 32 | 8 | 275 | 4 | 0.53 | 2 |
| M1 | 16 | 12 | 250 | 5 | 0.53 | 3 |
| M5 | 16 | 16 | 225 | 2 | 0.40 | 4 |
| M2 | 16 | 8 | 200 | 3 | 0.30 | 5 |

---

## 📋 Input File Requirements

- CSV format only
- First column must contain alternative names
- Remaining columns must be numeric
- No missing values
- Minimum 2 criteria columns required

---

## ⚠️ Important Notes

- Number of weights must equal number of criteria columns
- Number of impacts must equal number of criteria columns
- Weights must be positive numbers
- Impacts must be either + or -
- All criterion values must be numeric

---

## 🔧 How TOPSIS Works

1. Normalize the decision matrix
2. Apply weights to normalized values
3. Determine ideal best and ideal worst solutions
4. Compute distances from ideal best and worst
5. Calculate closeness coefficient
6. Rank alternatives based on score

---

## 📝 License

This project is licensed under the MIT License.

---

## 👤 Author

**Prabhsimar Singh**  
Roll Number: 102483078

---

## 📚 Academic Note

This package was developed as part of an academic assignment for  
**UCS654 – Prescriptive Analytics**
