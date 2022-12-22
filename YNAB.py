from _private import API_SECRET, BUDGET_ID
import requests, json
from classes import YNABTransaction

BASE_URL = "https://api.youneedabudget.com/v1"
headers = {"Authorization": "Bearer " + API_SECRET}


def YNAB_post(trans_list):
    json_dict = YNABTransaction.json_list(trans_list)
    params = {"budget_id": BUDGET_ID}

    request_str = f"{BASE_URL}/budgets/{BUDGET_ID}/transactions"
    print("SENDING: ")
    print(request_str)
    print(json_dict)
    response = requests.post(
        request_str, headers=headers, json=json_dict, params=params
    )

    print("#################################################")
    print(response.content)


def _info():
    response = requests.get(
        f"{BASE_URL}/budgets/{BUDGET_ID}/transactions?since_date=2022-12-01",
        headers=headers,
    )
    with open("trans.txt", "wb") as f:
        f.write(response.content)
