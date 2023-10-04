import argparse

from decouple import config

from prh.fetch import get_data
from prh.models import Company

def single_company(company_number:str, company_uid:str|None=None) -> tuple[str,bool]:
    input_packet = [{"company_number":company_number, "company_uid":company_uid}]
    data_list = get_data(input_packet)

    if not data_list:
        return {"company_number":company_number, "upload_result":False}
    company_number = data_list[0].get("company_number")
    company_uid = data_list[0].get("company_uid")
    data = data_list[0].get("data")

    upload_result = Company(company_uid=company_uid, **data).to_postgres()
    return {"company_number":company_number, "upload_result":upload_result}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("company_number", type=str, help="Company number")
    parser.add_argument("--company_uid", type=str, help="Company UID", default=None)
    args = parser.parse_args()

    upload_results = single_company(args.company_number, args.company_uid)
    print(upload_results)
    