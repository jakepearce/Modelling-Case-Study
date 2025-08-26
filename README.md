# Modelling Case Study

This project replicates a simplified **UAV Exposure Rating Model**, originally built in an Excel spreadsheet. 
The Python implementation follows the same logic while making it testable and extendable. 

---

## Project Overview

The model calculates **insurance premiums** for drones and detachable cameras, applying rules from the case study spec:


- **Drone Hull Premiums**
    - Base rate: 6%
    - Weight band factors: 1.0 / 1.6 / 1.2
    - Premium = drone value x base x factor

- **Drone TPL Premiums**:
    - Base rate: 2%
    - Increased Limit Factors (ILFs) applied per drone
    - Premium = base layer x ILF

- **Camera Hull Premiums**:
    - Charged at the highest eligible drone hull rate (7.2%)
    - Premium = camera value x rate

- **Extensions**:
    - **Drones**: Only top-n drones (ordered by hull premium) at full rate, the rest fixed at £150. 
    - **Cameras**: If more cameras than drones, only top-n cameras (ordered by value) at full rate, the rest fixed at £50. 

- **Totals**: 
    - Net premium = sum of line totals. 
    - Gross premium = net / (1 - brokerage), where brokerage = 30%. 

- **Golden Example Totals (from Spreadsheet)**:
    - Drone Hull NET:      2832.00 / GROSS: 4045.71
    - Drone TPL NET:        420.20 / GROSS: 600.29
    - Camera Hull NET:      792.00 / GROSS: 1131.43
    - TOTAL NET:           4044.20 / GROSS: 5777.43

--- 

## Notes

All line-item values, final and intermediate, are calculated as NET as per the spreadsheet. 
Gross is then reverse engineered during the totals calculation. 

-

In the extensions, extension 2 follows on from extension 1 in my implementation. 
i.e. the amount of cameras charged at full premium is equal to the maximum number of drones in the air at one time. 
This only changes when the amount of drones is set to less than the maximum number of drones in the air at one time, 
in which case it calculates how many cameras are charged full premium based off of the amount of drones. 

- 

Decimal is used extensively to ensure precise and accurate calculations for financial values. 
Pythons built-in float type can introduce small rounding errors which can accumulate and cause inaccuracies, 
which would become problematic if this was scaled. 

---

## Running the program manually

python run.py

---

## Running the Tests

- **Run All Tests**:
python -m unittest discover -s tests -p "test_*.py" -v

- **Run a Single Test File**:
python -m unittest tests.test_30_cameras -v

- **Run a Single Test Method**:
python -m unittest tests.test_40_extensions.TestExtensions.test_drones_extensions -v



