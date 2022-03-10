class Headers:
    URL = "https://sellermetrix.com/api/v2/cached-reports/"

    header_post = {'Connection': 'keep-alive',
                   'Accept': 'application/json, text/plain, */*',
                   'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
                                    '.eyJ1c2VybmFtZSI6InBlcm9sYS5lcmljc3NvbkBnbWFpbC5jb20iLCJpYXQiOjE2N'
                                    'DQyOTkxMzgsImV4cCI6MTY0Njg5MTEzOCwianRpIjoiNDUwYTMyZGUtMTVkNi00Nj'
                                    'I4LTkzMDctYzFkZjQ0MGRlNDAwIiwidXNlcl9pZCI6MTUsInVzZXJfcHJvZmlsZV9pZC'
                                    'I6WzEzXSwib3JpZ19pYXQiOjE2NDQyOTkxMzh9.FxLSD2CWgGePZ1a-kpm6-QBM2spUV85UPiGSN8fVG-I',
                   'Content-Type': 'application/json;charset=UTF-8',
                   'Origin': 'http://54.218.163.142',
                   'Referer': 'http://54.218.163.142/reports'
                   }
    header_get = {'Connection': 'keep-alive',
                  'Accept': 'application/json, text/plain, */*',
                  'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
                                   '.eyJ1c2VybmFtZSI6InBlcm9sYS5lcmljc3NvbkBnbWFpbC5jb20iLCJpYXQiOjE2N'
                                   'DQyOTkxMzgsImV4cCI6MTY0Njg5MTEzOCwianRpIjoiNDUwYTMyZGUtMTVkNi00Nj'
                                   'I4LTkzMDctYzFkZjQ0MGRlNDAwIiwidXNlcl9pZCI6MTUsInVzZXJfcHJvZmlsZV9pZC'
                                   'I6WzEzXSwib3JpZ19pYXQiOjE2NDQyOTkxMzh9.FxLSD2CWgGePZ1a-kpm6-QBM2spUV85UPiGSN8fVG-I',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/96.0.4664.93 Safari/537.36',
                  'Referer': 'http://54.218.163.142/reports/',
                  'Accept-Language': 'en-US,en;q=0.9',
                  'Cookie': 'fid=6c05f5e7-4cbe-4055-a6c8-9040da3b6e6b; __test=1; '
                            'RememberMe=-770982921^1#7422198782369332562; '
                            'csrftoken=ZJfv6M1HfrXwSmcekH9evEp5tmwab8a2UNKOuqxx2KtAvyMv1Mq1WLxmam4c3jzR'
                  }

    payload_all_reports = {
        "id": 0,
        "name": "MyRequest",
        "marketplace_id": 3,
        "type": "profit-and-loss",
    }
