import typing
import unicodedata

from bs4.element import ResultSet
from bs4 import BeautifulStoneSoup


def normalize(text: str) -> str:
    """
    Strips spaces from the beginning and the end of the text, and normalizes the text.
    This also replaces stuff like &nbsp; with a regular space.
    :param text: The text to normalize.
    :returns: The normalized text.
    """
    return unicodedata.normalize("NFKD", text.strip()).strip()


def get_cells(num_expected_cells: typing.Optional[int] = None, **kwargs) -> ResultSet:
    """
    Retrieves the cells from the html row being provided.
    If the number of actual cells does not match the expected number of cells, this method will raise an ValueError.
    :param num_expected_cells: The expected number of cells in the row (if not provided - no validations will occur).
    :param kwargs: A single keyword argument containing the row to process.
    :returns: a BeautifulSoup ResultSet containing the retrieved cells.
    """
    assert len(kwargs) == 1
    row_name, row = list(kwargs.items())[0]
    cells = row.find_all("td")
    if not cells and num_expected_cells != 0:
        raise ValueError(F"Expected {row_name} to have cells but it has none.")
    num_actual_cells = len(cells)
    if num_expected_cells is not None and num_actual_cells != num_expected_cells:
        raise ValueError(
            F"Expected {row_name} to have {num_expected_cells} cells but it has {num_actual_cells}.",
        )
    return cells
