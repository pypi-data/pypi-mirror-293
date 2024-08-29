import pandas as pd
from IPython import get_ipython
from IPython.display import display as ipy_display
from typing import Optional


def csvinspector(
    csv_file_path: str, rows_to_display: Optional[int] = 5, show_info: bool = True
) -> None:
    """
    Display a CSV file as a table, using Jupyter's display function if available,
    or print otherwise. Optionally, show basic DataFrame info.

    Parameters
    ----------
    csv_file_path : str
        The path to the CSV file.
    rows_to_display : int, optional
        The number of rows to display. If None, all rows are displayed. Default is None.
    show_info : bool, optional
        If True, display DataFrame info such as number of rows, columns, and data types.
        Default is True.

    Returns
    -------
    pd.DataFrame
        The loaded DataFrame.

    Raises
    ------
    ValueError
        If the file does not exist, is empty, or cannot be read as a CSV.
    """
    # Load the data into a pandas DataFrame with error handling
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        raise ValueError(f"The file '{csv_file_path}' does not exist.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file '{csv_file_path}' is empty or not a valid CSV.")
    except Exception as e:
        raise ValueError(f"An error occurred while reading '{csv_file_path}': {e}")

    # Determine if we are in a Jupyter environment
    is_jupyter = "IPKernelApp" in get_ipython().config if get_ipython() else False

    # Display DataFrame info if requested
    if show_info:
        if is_jupyter:
            df.info()  # Outputs directly in Jupyter
        else:
            print(df.info())  # print info explicitly when not in Jupyter

    # Display or print the DataFrame
    if rows_to_display is None:
        rows_to_display = len(df)

    if is_jupyter:
        ipy_display(df.head(rows_to_display))
    else:
        print(df.head(rows_to_display))


if __name__ == "__main__":
    csvinspector("../../sttk-data/AAPL_historical_2023-01-01_2023-12-31_2d.csv")
