from checker import mugen

if __name__ == '__main__':
    url = "https://epark.jp/receive_department/wait/reserve_minute_select_ajax/172441/depart/21429?receive%5Breceipt_date%5D%5Bdate%5D=1603810800&receive%5Breceipt_date%5D%5Bhour%5D="
    hours = [18, 19, 20]
    mugen(base_url=url, suffix=hours)
