# air-01-web

You have been assigned to create an interactive data visualization based on the developers salary data from JetBrains Developer Ecosystem Survey 2024. 

Use the following [Figma design ](https://www.figma.com/design/pmxb4N3i62YgFVzE5Nq74b/IT-Salary-Calculator?node-id=0-1&p=f) (password AirRPP_homework2025) and this [reference page](https://www.jetbrains.com/lp/devecosystem-it-salary-calculator/) to implement this visualization with working filters. Use `calculatorData.json` as data for visualization. You can use any frontend framework for this task. The data can be either stored as a static file, or served via your own API (or via any other method).

---

## Tech Stack
- **Python 3.12+**
- **Streamlit** for interactive web app
- **pandas** for data processing

## Setup & Run

1. **Install dependencies:**

   ```bash
   pip install streamlit pandas
   ```

2. **Run the app:**

   ```bash
   streamlit run main.py
   ```

3. **Open in browser:**
   - The app will open automatically, or visit [http://localhost:8501](http://localhost:8501)

## Usage
- Use the sidebar filters to interactively filter the salary data.
- The main area displays the filtered data and a salary distribution chart.
- Data is loaded from `calculatorData.json`.

## References
- [Figma design](https://www.figma.com/design/pmxb4N3i62YgFVzE5Nq74b/IT-Salary-Calculator?node-id=0-1&p=f) (password: AirRPP_homework2025)
- [Reference page](https://www.jetbrains.com/lp/devecosystem-it-salary-calculator/)