import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


def download_and_resample_yf_data(
    stock_symbol: str = "AAPL",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = "1d",
    fallback_to_higher: bool = False,
    include_resample_base_period: bool = False,
    data_dir: Optional[str] = None,  # New parameter for data directory
) -> None:
    """
    Download historical market data from Yahoo Finance, resample it to the desired period,
    and save the data to a CSV file.

    Parameters
    ----------
    stock_symbol : str, optional
        Ticker symbol of the stock to download data for, by default "AAPL".
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format, by default the start of the last full year.
    end_date : str, optional
        End date in 'YYYY-MM-DD' format, by default the end of the last full year.
    period : str, optional
        Desired resampling period (e.g., '4m' for 4 minutes, '2h' for 2 hours), by default "1d".
    fallback_to_higher : bool, optional
        Whether to fall back to the next higher period if data for the current period is unavailable, by default False.
    include_resample_base_period : bool, optional
        Whether to include base period info in the filename if a fallback period is used, by default False.
    data_dir : str, optional
        Directory where the 'sttk-data' folder should be created. If None, the current working directory is used.

    Returns
    -------
    None
    """

    if start_date is None:
        start_date = f"{datetime.now().year - 1}-01-01"
    if end_date is None:
        end_date = f"{datetime.now().year - 1}-12-31"

    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    end_date_inclusive = (end_date_dt + timedelta(days=1)).strftime("%Y-%m-%d")

    original_period = period
    download_period = determine_download_period(period)

    try:
        data = yf.download(
            stock_symbol,
            start=start_date,
            end=end_date_inclusive,
            interval=download_period,
        )

        while data.empty and download_period:
            print(
                f"Data for period '{download_period}' not available. Trying next available period."
            )
            download_period = get_next_lower_period(download_period, fallback_to_higher)
            if download_period:
                data = yf.download(
                    stock_symbol,
                    start=start_date,
                    end=end_date_inclusive,
                    interval=download_period,
                )

        if data.empty:
            raise ValueError(
                f"Failed to download data for {stock_symbol} with the specified date range {start_date} to {end_date}."
            )

        if original_period != download_period:
            data = resample_data(data, original_period)

        save_to_csv(
            data,
            stock_symbol,
            start_date,
            end_date,
            original_period,
            download_period,
            include_resample_base_period,
            data_dir,  # Pass the data directory to save_to_csv
        )

    except Exception as e:
        print(
            f"Error: {e}. Please check the input parameters and your network connection."
        )


def determine_download_period(period: str) -> str:
    """
    Determines the appropriate download period based on the requested period.
    Matches the requested period to the closest available download period from yfinance.

    Parameters
    ----------
    period : str
        The requested period (e.g., '2m', '1h', '1d').

    Returns
    -------
    str
        The appropriate download period supported by yfinance.

    Raises
    ------
    ValueError
        If the period is not supported.
    """
    available_periods = [
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ]

    if period in available_periods:
        return period

    if period.endswith("m"):
        requested_minutes = int(period.replace("m", ""))
        for p in available_periods:
            if p.endswith("m") and int(p.replace("m", "")) >= requested_minutes:
                return p
        return "1m"

    elif period.endswith("h"):
        return "1h"

    elif period.endswith("d"):
        return "1d"
    elif period.endswith("wk"):
        return "1wk"
    elif period.endswith("mo"):
        return "1mo"
    elif period.endswith("mo"):
        return "3mo"
    else:
        raise ValueError(f"Unsupported period format: {period}")


def get_next_lower_period(
    current_period: str, fallback_to_higher: bool
) -> Optional[str]:
    """
    Returns the next lower available period if the current one is deprecated or unavailable.
    If fallback_to_higher is True, it will return the next higher available period.

    Parameters
    ----------
    current_period : str
        The current download period that needs to be adjusted.
    fallback_to_higher : bool
        Whether to fall back to a higher period if the current one is unavailable.

    Returns
    -------
    str or None
        The next available period, or None if no further fallback is possible.
    """
    available_periods = [
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ]

    current_index = available_periods.index(current_period)

    if fallback_to_higher:
        if current_index > 0:
            return available_periods[current_index - 1]
    else:
        if current_index < len(available_periods) - 1:
            return available_periods[current_index + 1]

    return None


def resample_data(data: pd.DataFrame, period: str) -> pd.DataFrame:
    """
    Resamples the data to the desired period using pandas' resample functionality.

    Parameters
    ----------
    data : pd.DataFrame
        The data to be resampled.
    period : str
        The desired resampling period (e.g., '2m', '1h', '2d').

    Returns
    -------
    pd.DataFrame
        The resampled data.
    """
    pandas_period = (
        period.replace("m", "min")
        .replace("h", "h")
        .replace("d", "D")
        .replace("wk", "W")
        .replace("mo", "M")
    )
    return (
        data.resample(pandas_period)
        .agg({"Open": "first", "High": "max", "Low": "min", "Close": "last"})
        .dropna()
    )


def save_to_csv(
    data: pd.DataFrame,
    stock_symbol: str,
    start_date: str,
    end_date: str,
    original_period: str,
    download_period: str,
    include_resample_base_period: bool,
    data_dir: Optional[str],  # New parameter for data directory
) -> None:
    """
    Saves the resampled data to a CSV file with a descriptive filename in the sttk-data directory.
    If the sttk-data directory does not exist, it will be created.

    Parameters
    ----------
    data : pd.DataFrame
        The resampled data to be saved.
    stock_symbol : str
        The stock symbol (e.g., 'AAPL').
    start_date : str
        The start date for the data range.
    end_date : str
        The end date for the data range.
    original_period : str
        The originally requested period (e.g., '2d').
    download_period : str
        The period actually used to download the data (e.g., '1d').
    include_resample_base_period : bool
        Whether to include base period info in the filename if a fallback period is used.
    data_dir : str, optional
        Directory where the 'sttk-data' folder should be created. If None, the current working directory is used.

    Returns
    -------
    None
    """
    # Determine the filename based on the include_resample_base_period flag
    if include_resample_base_period:
        if original_period != download_period:
            filename = f"{stock_symbol}_historical_{start_date}_{end_date}_{original_period}_from_{download_period}.csv"
        else:
            filename = f"{stock_symbol}_historical_{start_date}_{end_date}_{original_period}.csv"
    else:
        filename = (
            f"{stock_symbol}_historical_{start_date}_{end_date}_{original_period}.csv"
        )

    # If no data directory is specified, use the current working directory
    if data_dir is None:
        data_dir = os.getcwd()

    # Define the path for the sttk-data directory
    sttk_data_dir = os.path.join(data_dir, "sttk-data")

    # Check if the sttk-data directory exists, if not, create it
    if not os.path.exists(sttk_data_dir):
        os.makedirs(sttk_data_dir)

    # Define the full path for the CSV file
    csv_file_path = os.path.join(sttk_data_dir, filename)

    # Save the DataFrame to a CSV file
    data.index = data.index.strftime("%Y-%m-%d %H:%M:%S")
    data.to_csv(csv_file_path, index_label="Date")
    print(f"Data successfully saved to {csv_file_path}")


if __name__ == "__main__":
    download_and_resample_yf_data(
        "ABR",
        "2023-01-01",
        "2023-12-31",
        "1d",
        fallback_to_higher=False,
        include_resample_base_period=False,
        data_dir="../../",  # This will use the current working directory by default
    )
