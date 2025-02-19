# Bracket Generator

This Python script generates a March Madness bracket based on data from ESPN and FiveThirtyEight. It calculates the leverage of each team's probabilities and selects the most likely teams to advance through each round.

---

## Prerequisites

Before running the script, ensure you have the following installed:

- **Python 3.x**
- **pandas library**

You can install the required library using pip:

```bash
pip install pandas
```

## Installation

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```

2. **Navigate to the repository directory**

   ```bash
   cd your-repo-name
   ```

## Usage

1. **Download the required data files:**

- **Copy of 2023 March Madness Optimal Bracket - ESPN.csv**
- **FiveThirtyEight Data - 538.csv**

2. **Run the script:**

```bash
   python BracketGenerator2023.py
   ```

## Example Output

The script will print the bracket in the following format:

```bash
=== March Madness Bracket ===

 Champion:
 [Champion Team]

 Finals:
 [Team A, Team B]

 Final Four:
 [Team A, Team B, Team C, Team D]

 Elite Eight:
 [Team A, Team B, Team C, Team D, Team E, Team F, Team G, Team H]

 Sweet Sixteen:
 [Team A, Team B, Team C, Team D, Team E, Team F, Team G, Team H, Team I, Team J, Team K, Team L, Team M, Team N, Team O, Team P]

 Round of 32:
 [Team A, Team B, Team C, Team D, Team E, Team F, Team G, Team H, Team I, Team J, Team K, Team L, Team M, Team N, Team O, Team P, Team Q, Team R, Team S, Team T, Team U, Team V, Team W, Team X, Team Y, Team Z, Team AA, Team AB, Team AC, Team AD, Team AE, Team AF]
```

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request with your changes.
