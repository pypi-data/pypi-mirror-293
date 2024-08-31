from __future__ import annotations

from typing import Literal, Optional, overload, List

from pyfastexcel.driver import ExcelDriver, WorkSheet
from pyfastexcel.utils import deprecated_warning

from pydantic import validate_call as pydantic_validate_call

from ._typing import CommentTextStructure, SetPanesSelection
from .utils import CommentText, Selection


class Workbook(ExcelDriver):
    """
    A base class for writing data to Excel files with custom styles.

    This class provides methods to set file properties, cell dimensions,
    merge cells, manipulate sheets, and more.

    Methods:
        remove_sheet(sheet: str) -> None:
            Removes a sheet from the Excel data.
        rename_sheet(self, old_sheet_name: str, new_sheet_name: str) -> None:
            Rename a sheet.
        create_sheet(sheet_name: str) -> None:
            Creates a new sheet.
        switch_sheet(sheet_name: str) -> None:
            Set current self.sheet to a different sheet.
        set_file_props(key: str, value: str) -> None:
            Sets a file property.
        set_cell_width(sheet: str, col: str | int, value: int) -> None:
            Sets the width of a cell.
        set_cell_height(sheet: str, row: int, value: int) -> None:
            Sets the height of a cell.
        set_merge_cell(sheet: str, top_left_cell: str, bottom_right_cell: str) -> None:
            Sets a merge cell range in the specified sheet.
    """

    def remove_sheet(self, sheet: str) -> None:
        """
        Removes a sheet from the Excel data.

        Args:
            sheet (str): The name of the sheet to remove.
        """
        if len(self.workbook) == 1:
            raise ValueError('Cannot remove the only sheet in the workbook.')
        if self.workbook.get(sheet) is None:
            raise IndexError(f'Sheet {sheet} does not exist.')
        self.workbook.pop(sheet)
        self._sheet_list = tuple(self.workbook.keys())
        self.sheet = self._sheet_list[0]

    def rename_sheet(self, old_sheet_name: str, new_sheet_name: str) -> None:
        """
        Renames a sheet in the Excel data.

        Args:
            old_sheet_name (str): The name of the sheet to rename.
            new_sheet_name (str): The new name for the sheet.
        """
        if self.workbook.get(old_sheet_name) is None:
            raise IndexError(f'Sheet {old_sheet_name} does not exist.')
        if self.workbook.get(new_sheet_name) is not None:
            raise ValueError(f'Sheet {new_sheet_name} already exists.')
        self.workbook[new_sheet_name] = self.workbook.pop(old_sheet_name)
        self._sheet_list = tuple(
            [new_sheet_name if x == old_sheet_name else x for x in self._sheet_list]
        )
        self.sheet = new_sheet_name

    def create_sheet(
        self,
        sheet_name: str,
        pre_allocate: dict[str, int] = None,
        plain_data: list[list] = None,
    ) -> None:
        """
        Creates a new sheet, and set it as current self.sheet.

        Args:
            sheet_name (str): The name of the new sheet.
            pre_allocate (dict[str, int], optional): A dictionary containing
                'n_rows' and 'n_cols' keys specifying the dimensions
                for pre-allocating data in new sheet.
            plain_data (list[list[str]], optional): A 2D list of strings
                representing initial data to populate new sheet.
        """
        if self.workbook.get(sheet_name) is not None:
            raise ValueError(f'Sheet {sheet_name} already exists.')
        self.workbook[sheet_name] = WorkSheet(pre_allocate=pre_allocate, plain_data=plain_data)
        self.sheet = sheet_name
        self._sheet_list = tuple([x for x in self._sheet_list] + [sheet_name])

    def switch_sheet(self, sheet_name: str) -> None:
        """
        Set current self.sheet to a different sheet. If sheet does not existed
        then raise error.

        Args:
            sheet_name (str): The name of the sheet to switch to.

        Raises:
            IndexError: If sheet does not exist.
        """
        self._check_if_sheet_exists(sheet_name)
        self.sheet = sheet_name

    @pydantic_validate_call
    def set_file_props(self, key: str, value: str) -> None:
        """
        Sets a file property.

        Args:
            key (str): The property key.
            value (str): The property value.

        Raises:
            ValueError: If the key is invalid.
        """
        if key not in self._FILE_PROPS:
            raise ValueError(f'Invalid file property: {key}')
        self.file_props[key] = value

    @pydantic_validate_call
    def protect_workbook(
        self,
        algorithm: str,
        password: str,
        lock_structure: bool = False,
        lock_windows: bool = False,
    ):
        if algorithm not in self._PROTECT_ALGORITHM:
            raise ValueError(
                f'Invalid algorithm, the options are {self._PROTECT_ALGORITHM}',
            )
        self.protection['algorithm'] = algorithm
        self.protection['password'] = password
        self.protection['lock_structure'] = lock_structure
        self.protection['lock_windows'] = lock_windows

    def set_cell_width(self, sheet: str, col: str | int, value: int) -> None:
        self._check_if_sheet_exists(sheet)
        self.workbook[sheet].set_cell_width(col, value)

    def set_cell_height(self, sheet: str, row: int, value: int) -> None:
        self._check_if_sheet_exists(sheet)
        self.workbook[sheet].set_cell_height(row, value)

    @overload
    def set_merge_cell(
        self,
        sheet: str,
        top_lef_cell: Optional[str],
        bottom_right_cell: Optional[str],
    ) -> None: ...

    @overload
    def set_merge_cell(
        self,
        sheet: str,
        cell_range: Optional[str],
    ) -> None: ...

    def set_merge_cell(self, sheet, *args) -> None:
        deprecated_warning(
            "wb.set_merge_cell is going to deprecated in v1.0.0. Please use 'wb.merge_cell' instead",
        )
        self.merge_cell(sheet, *args)

    @overload
    def merge_cell(
        self,
        sheet: str,
        top_lef_cell: Optional[str],
        bottom_right_cell: Optional[str],
    ) -> None: ...

    @overload
    def merge_cell(
        self,
        sheet: str,
        cell_range: Optional[str],
    ) -> None: ...

    def merge_cell(self, sheet: str, *args) -> None:
        self._check_if_sheet_exists(sheet)
        self.workbook[sheet].set_merge_cell(*args)

    def auto_filter(self, sheet: str, target_range: str) -> None:
        self._check_if_sheet_exists(sheet)
        self.workbook[sheet].auto_filter(target_range)

    def set_panes(
        self,
        sheet: str,
        freeze: bool = False,
        split: bool = False,
        x_split: int = 0,
        y_split: int = 0,
        top_left_cell: str = '',
        active_pane: Literal['bottomLeft', 'bottomRight', 'topLeft', 'topRight', ''] = '',
        selection: Optional[SetPanesSelection | list[Selection] | Selection] = None,
    ) -> None:
        self._check_if_sheet_exists(sheet)
        self.workbook[sheet].set_panes(
            freeze=freeze,
            split=split,
            x_split=x_split,
            y_split=y_split,
            top_left_cell=top_left_cell,
            active_pane=active_pane,
            selection=selection,
        )

    def set_data_validation(
        self,
        sheet: str,
        sq_ref: str = '',
        set_range: Optional[list[int | float]] = None,
        input_msg: Optional[list[str]] = None,
        drop_list: Optional[list[str | int | float] | str] = None,
        error_msg: Optional[list[str]] = None,
    ):
        self._check_if_sheet_exists(sheet)
        self.workbook[sheet].set_data_validation(
            sq_ref=sq_ref,
            set_range=set_range,
            input_msg=input_msg,
            drop_list=drop_list,
            error_msg=error_msg,
        )

    def add_comment(
        self,
        sheet: str,
        cell: str,
        author: str,
        text: CommentTextStructure | CommentText | List[CommentText],
    ) -> None:
        """
        Adds a comment to the specified cell.
        Args:
            sheet (str): The name of the sheet.
            cell (str): The cell location to add the comment.
            author (str): The author of the comment.
            text (str | dict[str, str] | list[str | dict[str, str]]): The text of the comment.
        Raises:
            ValueError: If the cell location is invalid.
        Returns:
            None
        """
        self._check_if_sheet_exists(sheet)
        self.workbook[sheet].add_comment(cell, author, text)

    def group_columns(
        self,
        sheet: str,
        start_col: str,
        end_col: Optional[str] = None,
        outline_level: int = 1,
        hidden: bool = False,
        engine: Literal['pyfastexcel', 'openpyxl'] = 'pyfastexcel',
    ):
        self._check_if_sheet_exists(sheet)
        self.workbook[sheet].group_columns(
            start_col,
            end_col,
            outline_level,
            hidden,
            engine,
        )

    def group_rows(
        self,
        sheet: str,
        start_row: int,
        end_row: Optional[int] = None,
        outline_level: int = 1,
        hidden: bool = False,
        engine: Literal['pyfastexcel', 'openpyxl'] = 'pyfastexcel',
    ):
        self._check_if_sheet_exists(sheet)
        self.workbook[sheet].group_rows(
            start_row,
            end_row,
            outline_level,
            hidden,
            engine,
        )

    def create_table(
        self,
        sheet: str,
        cell_range: str,
        name: str,
        style_name: str = '',
        show_first_column: bool = True,
        show_last_column: bool = True,
        show_row_stripes: bool = False,
        show_column_stripes: bool = True,
        validate_table: bool = True,
    ):
        self._check_if_sheet_exists(sheet)
        self.workbook[self.sheet].create_table(
            cell_range,
            name,
            style_name,
            show_first_column,
            show_last_column,
            show_row_stripes,
            show_column_stripes,
            validate_table,
        )
