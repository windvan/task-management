from sqlmodel import SQLModel
from pydantic import field_validator
from dateutil.parser import parse
from datetime import datetime,timezone
import json


class DateTest(SQLModel):
    start_date: datetime
    end_date: datetime

    @field_validator('start_date', 'end_date',mode='before')
    @classmethod
    def JS_date_to_python_date(cls, v):
        return parse(v).astimezone(timezone.utc)


jsonstr = json.dumps({"start_date": "Tue Mar 25 2025 14:00:37 GMT+0800",
                     "end_date": "Tue Mar 25 2026 14:00:37 GMT+0600"})

mymode = DateTest.model_validate_json(jsonstr)

print(mymode.start_date)
print(mymode.end_date)
