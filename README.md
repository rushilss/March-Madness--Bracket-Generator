# NCAA Bracket Generator

Welcome to the March Madness Bracket Generator 2023! This Python script is designed to generate a predictive bracket for the NCAA March Madness tournament using data from ESPN and FiveThirtyEight. By leveraging probability data from these sources, the script calculates the most likely teams to advance through each round of the tournament, from the Round of 64 all the way to the National Championship.

---

## Key Features

   - **Data Integration**: Combines data from ESPN and FiveThirtyEight to create a comprehensive dataset for analysis.

   - **Probability Calculation**: Uses advanced probability metrics to determine the likelihood of each team advancing through each round.

   - **Bracket Generation**: Automatically generates a full tournament bracket, including predictions for the Champion, Final Four, Elite Eight, Sweet Sixteen, and Round of 32.

   - **Customizable Output**: Provides a clear and structured output of the predicted bracket, making it easy to visualize the tournament progression.

---

## Key Features

   1. **Data Loading**: The script loads data from two CSV files:
      - **Copy of 2023 March Madness Optimal Bracket - ESPN.csv**
      - **FiveThirtyEight Data - 538.csv**

   2. **Data Cleaning**: The data is cleaned and standardized, ensuring that team names and probabilities are consistent across both datasets.

   3. **Data Merging**: The script calculates leverage scores for each team, which are used to determine the most likely teams to advance through each round.

   4. **Leverage Calculation**: Provides a clear and structured output of the predicted bracket, making it easy to visualize the tournament progression.
   
   5. **Bracket Generation**: Using the leverage scores, the script generates a full tournament bracket, including predictions for the Champion, Final Four, Elite Eight, Sweet Sixteen, and Round of 32.

   6. **Output**: The final bracket is printed in a structured format, making it easy to visualize the predicted tournament progression.

---

## Output

The script will print the bracket in the following format:

```bash
=== March Madness Bracket ===

 Champion:
Houston

 Finals:
Creighton, Houston

 Final Four:
Creighton, Gonzaga, Houston, Kentucky

 Elite Eight:
Creighton, Gonzaga, Houston, Iowa State, Kentucky, San Diego St, Tennessee, UConn

 Sweet Sixteen:
Arkansas, Boise St, Creighton, Drake, Gonzaga, Houston, Iowa State, Kentucky, Maryland, Memphis, Michigan St, San Diego St, Tennessee, Texas A&M, UConn, Utah State

 Round of 32:
Alabama, Arizona, Arizona State, Arkansas, Auburn, Boise St, Colgate, Creighton, Drake, Duke, Furman, Gonzaga, Houston, Iowa State, Kansas, Kennesaw St, Kent State, Kentucky, Maryland, Memphis, Michigan St, Montana St, Purdue, San Diego St, Tennessee, Texas A&M, UCLA, UCSB, UConn, Utah State, VCU, Vermont
```
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



## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request with your changes.
