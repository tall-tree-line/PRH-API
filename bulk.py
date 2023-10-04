from typing import Optional, Union

from ratelimit import sleep_and_retry, limits

from prh.models import Company
from prh.fetch import get_data, query_all_company_nums

@sleep_and_retry
@limits(calls=290, period=60)
def bulk_run(query_statement=None) -> Union[list[dict[str,str|bool]],False]:
    """
    This function performs a bulk run of data retrieval and upload to the PostgreSQL database.
    It retrieves a list of company numbers from the input database, fetches data for each company number,
    and uploads the data to the output database.
    Limiting the API calls to 290 per 60 seconds per API ratelimit.

    Arguments:
        query_statemnt (): Defaults to None. SQLalchemy query statemnt created with select() function. If not specified will use default query.

    Returns:
        upload_results (list[tuple[str,bool]]): A list of tuples containing the company number and the upload result.
    """
    
    input_company_nums: Optional[list[dict]] = query_all_company_nums(query_statement)
    if not input_company_nums:
        return False
    
    data_list = get_data(input_company_nums)

    upload_results = []
    for item in data_list:
        company_number = item.get("company_number")
        company_uid = item.get("company_uid")
        data = item.get("data")

        upload_result = Company(company_uid=company_uid, **data).update_postgres()
        upload_results.append({"company_number":company_number, "upload_result":upload_result})

    return upload_results

if __name__ == "__main__":
    upload_result = bulk_run()
    print(upload_result)

