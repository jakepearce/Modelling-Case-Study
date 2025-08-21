"""
Rate constants copied from the model (Excel file).
Line items will be NET in calculations, with GROSS derived at totals later.
"""

from decimal import Decimal

# --- HULL (from Excel file) ---
HULL_BASE_RATE = Decimal("0.06")  

WEIGHT_ADJUSTMENT = {
    "0 - 5kg": Decimal("1.00"),
    "5 - 10kg": Decimal("1.20"),
    "10 - 20kg": Decimal("1.60"),
}


# --- TPL (from Excel file) ---
TPL_BASE_RATE = Decimal("0.02") 


# ILF keyed by (limit, excess)
TPL_ILF = {
    (Decimal("1000000"), Decimal("0")): Decimal("1.00"),
    (Decimal("4000000"), Decimal("1000000")): Decimal("0.53"),
    (Decimal("5000000"), Decimal("5000000")): Decimal("0.31"),
}

# --- EXTENSIONS (from instructions file) ---
DRONE_INACTIVE_FLAT_PREMIUM = Decimal("150") 
CAMERA_INACTIVE_FLAT_PREMIUM = Decimal("50")