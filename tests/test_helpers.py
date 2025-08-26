from decimal import Decimal

# Helpers for Consistent Rounding
Q2 = Decimal("0.01")  # 2 Decimal Places
Q4 = Decimal("0.0001")  # 4 Decimal Places

def D(x):
    """
    Helper to convert numbers to Decimal safely. 
    """
    return x if isinstance(x, Decimal) else Decimal(str(x))