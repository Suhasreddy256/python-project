from bill_generator import generate_monthly_bill
from sample_data import item_list

if __name__ == "__main__":
    result = generate_monthly_bill(item_list, "2024-11")
    from pprint import pprint
    pprint(result)
