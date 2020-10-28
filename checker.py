import time
import datetime
from typing import List

import requests
import simpleaudio
from bs4 import BeautifulSoup


def mugen(base_url: str, suffix: List[int]) -> None:
    while True:
        found = False
        for hour in suffix:
            res = requests.get(base_url + str(hour))
            if "～" in res.text:
                print(f"{hour}時台の空きを発見！")
                found = True
                wav_obj = simpleaudio.WaveObject.from_wave_file("発見の音.wav")
                play_obj = wav_obj.play()
                play_obj.wait_done()
        else:
            if not found:
                print("未発見", datetime.datetime.now())
        time.sleep(10)


def get_department_id(store_id: int) -> int:
    department_fetch_base_url = "https://epark.jp/receive_department/reserve_new_today/"
    res_text = requests.get(department_fetch_base_url + str(store_id)).text
    soup = BeautifulSoup(res_text, "html.parser")

    depart_id = soup.find("input", {"name": "receive[department_id]"}).attrs["value"]
    return depart_id


def calculate_epoch_time_of_the_day() -> int:
    current_jst_datetime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    date = datetime.datetime(year=current_jst_datetime.year,
                             month=current_jst_datetime.month,
                             day=current_jst_datetime.day,
                             hour=0, minute=0, second=0,
                             tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    return int(date.timestamp())


def base_url_generator(store_id: int, department_id: int, epoch_jst_of_the_day: int) -> str:
    return f"https://epark.jp/receive_department/wait/reserve_minute_select_ajax/{store_id}/depart/{department_id}" \
           f"?receive%5Breceipt_date%5D%5Bdate%5D={epoch_jst_of_the_day}&receive%5Breceipt_date%5D%5Bhour%5D="


def do_mugen (store_id, hours_to_search):
    epoch = calculate_epoch_time_of_the_day()

    base_url = base_url_generator(
        store_id=store_id,
        department_id=get_department_id(store_id_to_search),
        epoch_jst_of_the_day=epoch
    )

    try:
        mugen(base_url, hours_to_search)
    except:
        print("エラーが発生したので再起動しました。")
        print("日付変更以外でこれが表示された場合は、設定方法が間違っている可能性があります。")
        do_mugen(store_id, hours_to_search)


if __name__ == '__main__':
    # ここからの2行が設定
    hours = [18, 19, 20]  # 何時台を検索するかを指定します。
    store_id_to_search = 110202  # 店舗URLの末尾の数字を指定します。
    # 例；くら寿司品川駅前店（ https://epark.jp/detail/wait/479 ）の場合、「479」。

    # 設定ここまで

    do_mugen(store_id_to_search, hours)