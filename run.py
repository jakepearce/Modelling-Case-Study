"""
Simple runner to print out the current model data.
"""

import json
from modelling_case_study import main

if __name__ == "__main__":
    model_data = main()
    print(json.dumps(model_data, indent = 2))