import os
import uuid
from typing import Optional
from pydantic import BaseModel, Field
from docxtpl import DocxTemplate


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


class Contract(BaseModel):
    number: Optional[int]
    personnel_name: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    personnel_short_name: Optional[str]
    service: Optional[str]
    salary: Optional[int]
    salary_text: Optional[str]


def docx_render(context: Contract):
    doc = DocxTemplate('modules/print_manager/tpl/contract.docx')
    doc.render(context.dict())
    temp_file = f'temp/contract_{uuid.uuid4()}.docx'
    doc.save(temp_file)
    return temp_file
