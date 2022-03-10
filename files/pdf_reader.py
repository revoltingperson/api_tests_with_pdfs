from datetime import datetime
from pathlib import Path
import pdfplumber
import copy


class PDFReader:
    def __init__(self):
        self.directory = "reports"
        self.all_sorted_tables = []
        self.no_start_date = []
        self.only_dates = []
        self.pdf_iterator()
        self.no_start_dates()

    def no_start_dates(self):
        new = copy.deepcopy(self.all_sorted_tables)
        for item in new:
            save = item['date'][1]
            item['date'] = save
        self.no_start_date = new

    def pdf_iterator(self):
        all_pdfs = Path(self.directory).glob('*')
        print('These are all the PDF files in the directory:')
        for file in all_pdfs:
            print(file)
            raw = self.raw_extractor(file)
            final = self.format_the_table(raw)
            self.all_sorted_tables.append(final)

    def raw_extractor(self, pdf):
        raw_data = []
        pdf = pdfplumber.open(pdf)
        page = pdf.pages[0]
        """Slice the page into small images to process only needed parts"""
        """Numbers are just page coordinates"""
        date = page.crop((0, 60, page.width / 2, 75))
        income = page.crop((0, 220, page.width / 2, page.height * 0.7))
        expenses = page.crop((page.width / 2, 215, page.width, page.height * 0.68))

        date_text = date.extract_text()
        slicer = date_text.rsplit(" ", 5)
        slicer[2] = slicer[2].replace(",", '')
        end_date = datetime.strptime(f'{slicer[3]} {slicer[1]} {slicer[2]}', '%Y %b %d')

        slicer = date_text.split(' ', 6)
        slicer[4] = slicer[4].replace(",", '')
        start_date = datetime.strptime(f'{slicer[5]} {slicer[3]} {slicer[4]}', '%Y %b %d')

        text_income = income.extract_text()
        text_outcome = expenses.extract_text()

        raw_data.append([[str(start_date.date()), str(end_date.date())], [text_income], [text_outcome]])
        return raw_data

    def format_the_table(self, raw_input) -> dict:
        income = self.arrange_nice_columns(raw_input[0][1][0])
        expenses = self.arrange_nice_columns(raw_input[0][2][0])
        date = raw_input[0][0]

        final_output = {'date': date, "income": income, "expenses": expenses}
        self.only_dates.append(date)

        return final_output

    def arrange_nice_columns(self, raw_text) -> dict:
        output = {'items': [],
                  'values': []}
        for row in raw_text.split("\n"):
            splitter = row.rsplit(' ', 1)
            output['items'].append(splitter[0])
            output['values'].append(splitter[1])

        good_floats = list(map(self.convert_to_float, output['values']))
        output['values'].clear()
        output['values'] += good_floats
        return output

    def convert_to_float(self, num):
        try:
            return float(num.replace(',', ''))
        except:
            return 0
