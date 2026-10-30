# Datheon Python Programming Internship

## Task 1: Stock Portfolio Tracker

`task1_portfolio/portfolio.py` calculates position values and gains or losses,
prints a portfolio summary, and exports the results as CSV. It supports default
holdings, a single ticker, or interactive input.

```powershell
python task1_portfolio/portfolio.py
python task1_portfolio/portfolio.py --ticker AAPL --buy-price 150 --shares 10
python task1_portfolio/portfolio.py --interactive
```

The script uses Yahoo Finance market data for symbols not in its built-in
fallback price list. The included `portfolio_summary.csv` is a sample output,
not a live quote.

## Task 2: Hangman

`task2_hangman/hangman.py` is a command-line Hangman game with input
validation, duplicate-guess handling, a six-mistake limit, and replay support.

```powershell
python task2_hangman/hangman.py
```

## Task 3: File Organiser

`task3_file_organiser/organizer.py` sorts files into category folders based on
their extensions. It supports a dry run, optional recursive scanning,
collision-safe file names, and logging for permission and filesystem errors.

### Requirements

- Python 3.9 or newer
- No third-party packages

### Usage

Preview the changes first:

```powershell
python task3_file_organiser/organizer.py "$HOME\Downloads" --dry-run
```

Organize files directly inside a directory:

```powershell
python task3_file_organiser/organizer.py "$HOME\Downloads"
```

To also scan nested directories and move their files into category folders at
the selected directory's root:

```powershell
python task3_file_organiser/organizer.py "$HOME\Downloads" --recursive
```

Files are sorted into `Documents`, `Images`, `Videos`, `Audio`, `Archives`,
`Code`, or `Others`. Existing files are never overwritten; a numbered suffix
is added to colliding names. Symbolic links are skipped.

## Project status

All three task deliverables are included. The internship submission instructions
request at least two completed tasks before evaluation.
