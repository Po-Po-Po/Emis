import uuid
from openpyxl.styles import Font, Border, Side, Alignment, PatternFill
from .report_card import ReportCartPrint, get_month
from common.utils import convert_full_name


class FundPrint(ReportCartPrint):
    table_row = 4
    template: str = 'modules/print_manager/tpl/fund_table.xlsx'
    tmp_file: str = f'temp/fund_table_{uuid.uuid4()}.xlsx'

    def header(self):
        period = self.queryset.period.split('.')
        month = period[0]
        year = period[1]

        self.document.cell(row=1, column=1).value = f'{get_month(month)} {year}'

    def get_rows(self, field):
        return {
                1: {
                    'value': field.contract_number,
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': Alignment(horizontal="left", vertical="center")
                },
                2: {
                    'value': field.personnel.name,
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': Alignment(horizontal="left", vertical="center")
                },
                3: {
                    'value': field.personnel.birthday.strftime('%d.%m.%Y') if field.personnel.birthday else '',
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': Alignment(horizontal="left", vertical="center")
                },
                4: {
                    'value': field.start_date.strftime('%d.%m'),
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': self.style['alignment']
                },
                5: {
                    'value': field.end_date.strftime('%d.%m'),
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': self.style['alignment']
                },
                6: {
                    'value': field.accrued,
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': self.style['alignment']
                },
                7: {
                    'value': field.personnel.position,
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': Alignment(horizontal="left", vertical="center")
                },
                8: {
                    'value': field.personnel.code.name if field.personnel.code else '',
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': self.style['alignment']
                },
                9: {
                    'value': field.report_card.entity.directorate,
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': Alignment(horizontal="left", vertical="center")
                },
                10: {
                    'value': convert_full_name(field.report_card.customer.name) if field.report_card.customer else '',
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': Alignment(horizontal="left", vertical="center")
                },
                11: {
                    'value': field.description,
                    'border': self.style['border'],
                    'font': self.style['font'],
                    'alignment': self.style['alignment'],
                }
            }

    def get_addon_field(self, row, field):
        return row

    def build(self):
        self.fields = self.queryset
        self.table()
        return self.save()
