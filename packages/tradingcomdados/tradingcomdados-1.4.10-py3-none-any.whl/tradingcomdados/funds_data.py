import time
import pandas as pd
import datetime

import functools
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def _logging_error(func):
    """
    A decorator that wraps the function execution with logging for debugging purposes. 
    Logs function arguments and exceptions if any occur.
    
    Parameters:
    -----------
    func : function
        The function to be wrapped by the decorator.

    Returns:
    --------
    wrapper : function
        The wrapped function with additional logging functionality.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper


@_logging_error
def create_interval(start_date: str, end_date: str):
    """
    Generates a list of dates in 'YYYYMM' format between the start and end dates provided.

    Parameters:
    -----------
    start_date : str
        The start date in 'YYYY-MM-DD' format.
    
    end_date : str
        The end date in 'YYYY-MM-DD' format.

    Returns:
    --------
    list : 
        A list of strings representing months between the start and end dates in 'YYYYMM' format.
    """
    
    b = list()
    end = str(datetime.datetime.strptime(end_date, '%Y-%m-%d').year) + '{:02d}'.format(datetime.datetime.strptime(end_date, '%Y-%m-%d').month + 1)

    for year in range(int(datetime.datetime.strptime(start_date, '%Y-%m-%d').year), int(datetime.datetime.strptime(end_date, '%Y-%m-%d').year) + 1):
        for month in range(1, 13):
            a = '{:02d}{:02d}'.format(year, month)
            if a == end:
                break
            b.append(a)
        if a == end:
            break
        year += 1

    return b


@_logging_error
def extract_fund_data(dates_list: list, verbose: bool = False):
    """
    Fetches and combines data from CVM for a list of specified dates.

    Parameters:
    -----------
    dates_list : list
        A list of strings representing dates in 'YYYYMM' format for which the data will be fetched.
    
    verbose : bool, optional
        If True, prints progress information during data extraction. Default is False.

    Returns:
    --------
    pandas.DataFrame :
        A DataFrame containing the combined data from all specified dates.
    """
    
    start_time = time.time()
    dataframes = []

    for i in dates_list:
        url_pre = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{i}.zip'
        df_loc = pd.read_csv(url_pre, sep=';', compression='zip')
        s = datetime.datetime.strptime(i, "%Y%m")
        date = s.strftime('%B %Y')
        
        if verbose:
            print("Extraction of month", date, "finished")

        dataframes.append(df_loc)

    combined_df = pd.concat(dataframes, ignore_index=True)

    if verbose:
        print("Process took %s seconds" % (time.time() - start_time))

    return combined_df


@_logging_error
def get_fund_data(start: str, end: str, cnpj: str = None, verbose: bool = False):
    """
    
    Fetches and filters fund data by date and CNPJ.

    Parameters:
    -----------
    start : str
        Start date in 'YYYY-MM-DD' format.
    
    end : str
        End date in 'YYYY-MM-DD' format.
    
    cnpj : str, optional
        The CNPJ of the specific fund to retrieve data for. If not provided, returns data for all funds.
    
    verbose : bool, optional
        If True, prints progress information during data extraction. Default is False.

    Returns:
    --------
    pandas.DataFrame :
        A DataFrame containing the filtered fund data for the specified date range and CNPJ.

    """
    
    interval = create_interval(start, end)
    data_fund = extract_fund_data(interval, verbose)
    data_fund['DT_COMPTC'] = pd.to_datetime(data_fund['DT_COMPTC'])
    mask = (data_fund['DT_COMPTC'] >= start) & (data_fund['DT_COMPTC'] <= end)
    data_fund = data_fund.loc[mask]

    if cnpj:
        data_fund = data_fund[data_fund['CNPJ_FUNDO'] == cnpj]

    return data_fund.reset_index(drop=True)


@_logging_error
def get_funds_info(cnpj: str = None):
    """
    Fetches the registration data of investment funds from the Brazilian Securities and Exchange Commission (CVM).

    Parameters:
    -----------
    cnpj : str, optional
        CNPJ (National Registry of Legal Entities) of the specific fund to retrieve information for. 
        If not provided, information for all funds is returned.

    Returns:
    --------
    pandas.DataFrame :
        A DataFrame containing the registration data of investment funds. Columns may include:
        - CNPJ_FUNDO: National Registry of Legal Entities.
        - DENOM_SOCIAL: Legal name of the company.
        - SIT: Status of the fund registration with the CVM.
        - GESTOR: Name of the fund manager.
        - ... (other relevant information)
    """
    
    url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
    info = pd.read_csv(url, sep=';', encoding='ISO-8859-1', low_memory=False)

    if cnpj:
        info = info[info['CNPJ_FUNDO'] == cnpj]

    return info.reset_index(drop=True)
