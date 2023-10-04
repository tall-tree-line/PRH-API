import requests
from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.orm import sessionmaker
from decouple import config

from prh.logging_config import my_project_logger
from prh.helpers import is_valid_company_number

BASE_URL = "https://avoindata.prh.fi/bis/v1/{}"

def get_response(company_number:str|None) -> dict|None:
    """Get's the API response for the company number provided.

    Args:
        company_number (str): Finnish company's "y-tunnus". Example "1234567-8". Length should always be 9 chars and no letters.

    Returns:
        dict: JSON response from the API
    """
    if is_valid_company_number(company_number) is False:
        my_project_logger.warning(f"Company number is not in correct format: '{company_number}' won't fetch data for it.")
        return None

    search_url = BASE_URL.format(company_number)

    response = requests.get(search_url)

    if response.status_code != 200:
        my_project_logger.warning(f"Couldn't get a response for company_number: '{company_number}', response status code: {response.status_code}")
        return None

    return response.json()

def get_data(company_numbers:list[dict[str,str]]|None) -> list[dict[str, str|None ,str|dict|None]]:
    """
    Get data for a list of company numbers.
    
    Args:
        company_numbers (list[dict[str,str]]|None): List of dictionaries containing company numbers and company UIDs. Format [{company_number:str, company_uid:str}].
    
    Returns:
        list[tuple[str,str|None,dict]]: List of tuples containing company number, company UID, and data.
    """

    if not company_numbers:
        return None
    
    data_list = []
    for item in company_numbers:
        number = item.get("company_number")
        company_uid = item.get("company_uid")

        data = get_response(number)
        if not data:
            my_project_logger.info(f"No data returned for company: {number}")
            continue

        data = data.get("results")
        if not data:
            my_project_logger.info(f"No data returned for company: {number}")
            continue
        # When requesting the API with the company number, it won't return more than one result.
        data = data[0]
        data_list.append({"company_number":number, "company_uid":company_uid, "data":data})

    return data_list


def query_all_company_nums(query_statement=None) -> list[dict]:
    input_db_uri = config("POSTGRES_INPUT_DB")
    engine = create_engine(input_db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = MetaData()
    metadata.reflect(bind=engine)
    company = metadata.tables["company"]

    if query_statement:
        stmt = query_statement
    else:
        
        stmt = select(company.c.company_number, company.c.pk).where(company.c.country_code == "FI")
    
    try:
        result = session.execute(stmt).fetchall()
        return [{"company_number": row.company_number, "company_uid": row.pk} for row in result]
    
    except Exception as e:
        my_project_logger.error(f"Error querying db address: {input_db_uri}, error message: {str(e)}", exc_info=True)
        return None
    
    finally:
        session.close()
