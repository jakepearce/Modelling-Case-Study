"""
Starter data for the UAV rating model. 
- All line-item premiums will be stored as NET (as in the spreadsheet).
- Gross will be derived at totals later. 
- tpl_limit and tpl_excess manually added so the file runs. 
"""

from rating_constants import HULL_BASE_RATE, WEIGHT_ADJUSTMENT, TPL_BASE_RATE, TPL_ILF 
from decimal import Decimal, ROUND_HALF_UP

def get_example_data():
    """
    Return an example data structure containing the inputs and placeholder outputs for the drone pricing model
    """
    example_data = {
        "insured": "Drones R Us",
        "underwriter": "Michael",
        "broker": "AON",
        "brokerage": 0.3,
        "max_drones_in_air": 2,
        "drones": [
            {
                "serial_number": "AAA-111",
                "value": 10000,
                "weight": "0 - 5kg",
                "has_detachable_camera": True,
                "tpl_limit": 1000000,
                "tpl_excess": 0,
                "hull_base_rate": None,
                "hull_weight_adjustment": None,
                "hull_final_rate": None,
                "hull_premium": None,
                "tpl_base_rate": None,
                "tpl_base_layer_premium": None,
                "tpl_ilf": None,
                "tpl_layer_premium": None
            },
            {
                "serial_number": "BBB-222",
                "value": 12000,
                "weight": "10 - 20kg",
                "has_detachable_camera": False,
                "tpl_limit": 4000000,
                "tpl_excess": 1000000,
                "hull_base_rate": None,
                "hull_weight_adjustment": None,
                "hull_final_rate": None,
                "hull_premium": None,
                "tpl_base_rate": None,
                "tpl_base_layer_premium": None,
                "tpl_ilf": None,
                "tpl_layer_premium": None
            },
            {
                "serial_number": "AAA-123",
                "value": 15000,
                "weight": "5 - 10kg",
                "has_detachable_camera": True,
                "tpl_limit": 5000000,
                "tpl_excess": 5000000,
                "hull_base_rate": None,
                "hull_weight_adjustment": None,
                "hull_final_rate": None,
                "hull_premium": None,
                "tpl_base_rate": None,
                "tpl_base_layer_premium": None,
                "tpl_ilf": None,
                "tpl_layer_premium": None
            }
        ],
        "detachable_cameras": [
            {
                "serial_number": "ZZZ-999",
                "value": 5000,
                "hull_rate": None,
                "hull_premium": None
            },
            {
                "serial_number": "YYY-888",
                "value": 2500,
                "hull_rate": None,
                "hull_premium": None
            },
            {
                "serial_number": "XXX-777",
                "value": 1500,
                "hull_rate": None,
                "hull_premium": None
            },
            {
                "serial_number": "WWW-666",
                "value": 2000,
                "hull_rate": None,
                "hull_premium": None
            }

        ],
        "gross_prem": {
            "drones_hull": None,
            "drones_tpl": None,
            "cameras_hull": None,
            "total": None
        },
        "net_prem": {
            "drones_hull": None,
            "drones_tpl": None,
            "cameras_hull": None,
            "total": None
        }
    }

    return example_data


def main():
    """ 
    Perform the rating calculations replicating. 
    """
    model_data = get_example_data()

    # --- HULL & TPL for drones ---
    for drone in model_data["drones"]:
        rate_hull_for_drone(drone)
        rate_tpl_for_drone(drone)
    
    # --- CAMERAS ---
    rate_cameras(model_data)

    return model_data
    


def _money(x: Decimal) -> float:
    """
    Round a Decimla to 2 dp and return as float (JSON-friendly).
    """
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def rate_hull_for_drone(drone: dict) -> dict:
    """
    Fill HULL fields for a single drone (NET at line level).
    final_rate = base_rate * weight_adjustment
    hull_premium = value * final_rate
    """

    # 1) Base + Adjustment
    base = HULL_BASE_RATE
    adj = WEIGHT_ADJUSTMENT[drone["weight"]]

    # 2) Final Rate & Premium (as Decimal)
    final_rate = base * adj
    premium = Decimal(drone["value"]) * final_rate

    # 3) Store (round to 2 dp)
    drone["hull_base_rate"] = float(base)
    drone["hull_weight_adjustment"] = float(adj)
    drone["hull_final_rate"] = float(final_rate)
    drone["hull_premium"] = _money(premium)

    return drone


def rate_tpl_for_drone(drone: dict) -> dict:
    """
    Fill TPL fields for a single drone (NET at line level).
    base_layer_premium = value * TPL_BASE_RATE
    layer_premium = base_layer_premium * ILF(limit, excess)
    """
    
    # 1) Base Rate & Base Layer Premium
    base_rate = TPL_BASE_RATE 
    base_layer_premium = Decimal(drone["value"]) * base_rate

    # 2) ILF lookup (limit, excess)
    limit_dec = Decimal(drone["tpl_limit"])
    excess_dec = Decimal(drone["tpl_excess"])
    ilf = TPL_ILF[(limit_dec, excess_dec)]

    # 3) Layer Premium (NET) & Store (round to 2 dp)
    layer_prem = base_layer_premium * ilf

    drone["tpl_base_rate"] = float(base_rate)
    drone["tpl_base_layer_premium"] = _money(base_layer_premium)
    drone["tpl_ilf"] = float(ilf)
    drone["tpl_layer_premium"] = _money(layer_prem)

    return drone


def rate_cameras(model_data: dict) -> None:
    """
    Set camera hull_rate to the highest eligible drone hull_final_rate.
    (Consider only drones where has_detachable_camera = True).
    Then compuye each camera's hull_premium (NET). 
    """

    drones = model_data["drones"]

    # Eligible drones for camera attachment
    eligible = [d for d in drones if d.get("has_detachable_camera")]

    # If no eligible drones, no camera rate to apply
    if not eligible:
        for cam in model_data["detachable_cameras"]:
            cam["hull_rate"] = 0.0
            cam["hull_premium"] = 0.0
        return
    
    # Max hull_final_rate among eligible drones
    max_rate = max(d["hull_final_rate"] for d in eligible)

    # Apply to each camera
    for cam in model_data["detachable_cameras"]:
        cam["hull_rate"] = float(max_rate)
        prem = Decimal(cam["value"]) * Decimal(str(max_rate))
        cam["hull_premium"] = _money(prem)