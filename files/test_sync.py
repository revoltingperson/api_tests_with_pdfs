from files.pdf_reader import PDFReader
from files.headers import Headers
import pytest
import requests
import pandas as pd
import numpy as np


@pytest.fixture(scope='module')
def make_pdf():
    return PDFReader()


@pytest.fixture(scope='module')
def pdfs_ready(make_pdf):
    dates = make_pdf.no_start_date
    return dates


@pytest.fixture(scope='module')
def post_request(make_pdf):
    dates_for_requests = make_pdf.only_dates
    all_resps = []
    print("Collecting post requests...")
    for date in dates_for_requests:
        payload_post = {
            "type": "profit-and-loss",
            "marketplace_id": 3,
            "name": "MyRequest",
            "from": date[0],
            "to": date[1]
        }
        post = requests.post(Headers.URL,
                             headers=Headers.header_get,
                             json=payload_post)
        all_resps.append(post.text)
    return all_resps


@pytest.fixture(scope="module")
def collect_payloads(post_request):
    preparator = lambda x: x.strip('"')
    all_ints = list(map(preparator, post_request))
    """All payloads from the report list are filtered there"""
    list_of_final_payloads = []
    print('Waiting for the /completed/ status')
    while True:
        report = requests.get(Headers.URL,
                              headers=Headers.header_get,
                              params=Headers.payload_all_reports)
        # search in report for an item with id and check its status
        json_rep = report.json()
        for statuses in json_rep:
            if str(statuses['id']) in all_ints:
                if statuses['status'] == 'completed':
                    if statuses not in list_of_final_payloads:
                        list_of_final_payloads.append(statuses)
                        print(str(len(list_of_final_payloads)) + " " + statuses['status'])
                        if len(list_of_final_payloads) == len(all_ints):
                            return list_of_final_payloads


@pytest.fixture(scope='module')
def final_get_request(collect_payloads):
    all_reports = []
    for body in collect_payloads:
        grab_id = str(body['id'])
        Headers.header_get['Referer'] = f'http://54.218.163.142/reports/{grab_id}'
        body.pop('id')
        get_req = requests.get(Headers.URL + grab_id,
                               headers=Headers.header_get,
                               params=body)
        all_reports.append(get_req.json())

    return all_reports


#

@pytest.fixture(scope='module')
def process_api_reports(final_get_request):
    api_dictionaries = []
    for one_file in final_get_request:
        income = do_work_with_report(one_file, 'Income')
        expenses = do_work_with_report(one_file, 'Amazon Expenses')

        output_dict = {'date': one_file['columns'][0],
                       'income': income,
                       'expenses': expenses}

        api_dictionaries.append(output_dict)
    return api_dictionaries


def do_work_with_report(one_file, entry: str):
    collection = {'items': [], 'values': []}
    for key, value in one_file['marketplaces'][0]['data'][entry].items():
        collection['items'].append(key)
        for date, number in value.items():
            collection['values'].append(number)
    return collection


def compare_files(api_file, pdf_file, file_index: int):
    selected_api = api_file[file_index]
    date = selected_api['date']
    for pdf in pdf_file:
        if pdf['date'] == date:
            do_work(selected_api, pdf, 'income')
            do_work(selected_api, pdf, 'expenses')


def do_work(api, pdf, key: str):
    """Generate dataframes to display in the html report if a test fails"""
    assert all([item in api[key]['items'] for item in pdf[key]['items']])
    x = pd.DataFrame(api[key])
    y = pd.DataFrame(pdf[key]['values'], columns=['PDF'])
    final = pd.concat([x, y], axis=1)
    comparison = np.where(final['values'] == final['PDF'], True, False)
    final['equal'] = comparison
    assert final['values'].equals(final['PDF']), print(f"{key} {api['date']}\n{final}")


@pytest.mark.parametrize('file', [0, 1, 2, 3, 4, 5, 6])
def test_aggregate(process_api_reports, pdfs_ready, file):
    compare_files(process_api_reports, pdfs_ready, file)
