from sqlmodel import SQLModel
from pydantic import field_validator
from dateutil.parser import parse
from datetime import datetime,timezone
import json
from ..schemas.note import Note
from ..schemas.enums import NoteSeverityEnum
from sqlmodel import Session
from ..database.database import engine

# note=Note( content="test",task_id=1,severity=NoteSeverityEnum.Info,tags='["test","test2"]')
# session=Session(engine)
# session.add(note)
# session.commit()    
# print('note',note)
# print('id',note.id)


class DateTest(SQLModel):
    # start_date: datetime
    # end_date: datetime
    title: str
    content: str

#     @field_validator('start_date', 'end_date',mode='before')
#     @classmethod
#     def JS_date_to_python_date(cls, v):
#         return parse(v).astimezone(timezone.utc)


# jsonstr = json.dumps({"start_date": "Tue Mar 25 2025 14:00:37 GMT+0800",
#                      "end_date": "Tue Mar 25 2026 14:00:37 GMT+0600"})

jsonstr = json.dumps({"title": "test"})
mymode = DateTest.model_validate_json(jsonstr)

print(mymode)
