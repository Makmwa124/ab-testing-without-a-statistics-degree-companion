A/B Testing Without a Statistics Degree - companion files
Mathew Kariuki, 2026

ab_test_calculator.xlsx        Excel calculator: sample size, conversion test, revenue test,
                               SRM check, CUPED (Appendix B). Yellow cells are inputs.
data/                          Larkspur Outdoor experiment datasets (CSV) and larkspur.db (SQLite)
book_code/                     Every Python example, chapter by chapter, as .py files
templates/                     Test plan and test result templates (.md and .docx)
scripts/make_data.py           The script that generated the practice data

How to use: open this folder in VS Code (File > Open Folder), create a notebook here,
and run the examples. Paths such as "data/delivery_banner.csv" assume this folder is the
working directory.

Install: pip install pandas numpy scipy statsmodels openpyxl jupyter
Tested with Python 3.13, pandas 3.0, SciPy 1.18 and statsmodels 0.15.

Larkspur Outdoor and all people and businesses in the data are fictional; the data is simulated.
