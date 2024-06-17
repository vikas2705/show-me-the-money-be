from pydantic import BaseModel, Field
from typing import List, Optional, Union


class Attribute(BaseModel):
    Value: str
    Id: str


class Cell(BaseModel):
    Value: Union[str, float]
    Attributes: Optional[List[Attribute]] = None


class Row(BaseModel):
    RowType: str
    Cells: Optional[List[Cell]] = None
    Title: Optional[str] = None
    Rows: Optional[List["Row"]] = None

    class Config:
        # This allows for recursive models in Pydantic
        arbitrary_types_allowed = True


class Report(BaseModel):
    ReportID: str
    ReportName: str
    ReportType: str
    ReportTitles: List[str]
    ReportDate: str
    UpdatedDateUTC: str
    Fields: List
    Rows: List[Row]


class BalanceSheetResponse(BaseModel):
    Status: str
    Reports: List[Report]


# Ensure correct typing for recursive Rows
Row.update_forward_refs()
