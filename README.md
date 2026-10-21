# A/B Testing Without a Statistics Degree: companion files

Free practice files for the book **A/B Testing Without a Statistics Degree: Sample Sizes, Significance and the Traps That Fool Smart Teams, Explained Through Worked Examples** by Mathew Kariuki.

Every example in the book uses Larkspur Outdoor, a fictional online outdoor-gear retailer, and its experiments: a delivery banner, a bundle offer, a search redesign, a product page and an express checkout. This repository holds those datasets, an Excel calculator that does the book's calculations without code, the test plan and result templates, and every code example from the book, so you can follow along.

## Download

Click the green **Code** button above, then **Download ZIP**. Unzip it somewhere sensible, such as your Documents folder.

## What's here

| Path | What it is |
| --- | --- |
| `ab_test_calculator.xlsx` | Excel calculator: sample size, conversion test, revenue test, SRM check, CUPED (Appendix B) |
| `data/delivery_banner.csv` | 48,230 users in the free-delivery banner test (Chapters 1, 3, 5, 8) |
| `data/bundle_offer.csv` | 30,000 users and their revenue in the bundle test (Chapters 2, 6) |
| `data/search_redesign.csv` | A search test with a sample ratio mismatch (Chapter 9) |
| `data/hero_daily.csv` | Daily visitors and clicks in a homepage test (Chapter 9) |
| `data/product_page.csv` | Spend before and during a product page test (Chapter 10) |
| `data/express_checkout.csv` | 64,400 users in the full case study (Chapters 2, 12) |
| `data/weekly_conversion.csv` | Six months of weekly conversion rates (Chapter 1) |
| `data/larkspur.db` | SQLite copy of the banner and checkout tables (Chapter 2) |
| `book_code/` | Every Python example, chapter by chapter, as `.py` files |
| `templates/` | Test plan and test result templates (`.md` and `.docx`, Chapter 11) |
| `scripts/make_data.py` | The script that generated the practice data |

## Quick start

1. Install Python, then run:

   ```
   pip install pandas numpy scipy statsmodels openpyxl jupyter
   ```

2. In VS Code, choose **File > Open Folder** and open this folder.
3. Create a notebook here (**File > New File > Jupyter Notebook**) and run:

   ```python
   import pandas as pd
   from statsmodels.stats.proportion import proportions_ztest

   banner = pd.read_csv("data/delivery_banner.csv")
   g = banner.groupby("group")["converted"].agg(["sum", "count"])
   print(g)
   print(proportions_ztest(g["sum"][::-1], g["count"][::-1]))
   ```

Paths such as `data/delivery_banner.csv` assume this folder is your working directory. No Python? Open `ab_test_calculator.xlsx` in Excel; yellow cells are inputs.

Tested with Python 3.13, pandas 3.0, SciPy 1.18 and statsmodels 0.15.

## Get the book

- **Book + Excel calculator + practice data (PDF bundle):** [mathewkariuki.gumroad.com/l/ab-testing-without-a-statistics-degree](https://mathewkariuki.gumroad.com/l/ab-testing-without-a-statistics-degree)
- **Paperback:** [Amazon.com](https://www.amazon.com/dp/B0HNKLWZ7G) · [Amazon.com.au](https://www.amazon.com.au/dp/B0HNKLWZ7G)
- **Kindle:** [Amazon.com](https://www.amazon.com/dp/B0HNK5KSC2) · [Amazon.com.au](https://www.amazon.com.au/dp/B0HNK5KSC2)

## About

Larkspur Outdoor and every person and business in its data are fictional, and the data is simulated. The data, calculator, templates and code are free to use for learning. The book itself is © 2026 Mathew Kariuki.

Spotted a problem with an example or the data? Please open an issue.
