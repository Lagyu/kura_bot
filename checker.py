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


def calculate_epoch_time_of_the_day(year: int, month: int, day: int) -> int:
    date = datetime.datetime(year=year, month=month, day=day, hour=0, minute=0, second=0,
                             tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    return int(date.timestamp())


def base_url_generator(store_id: int, department_id: int, epoch_JST_of_the_day: int) -> str:
    return f"https://epark.jp/receive_department/wait/reserve_minute_select_ajax/{store_id}/depart/{department_id}" \
           f"?receive%5Breceipt_date%5D%5Bdate%5D={epoch_JST_of_the_day}&receive%5Breceipt_date%5D%5Bhour%5D="


if __name__ == '__main__':
    # ここからの5行が設定
    year = 2020
    month = 10
    day = 28
    hours = [18, 19, 20]
    store_id_to_search = 110202  # 店舗URLの末尾の数字。
    # 例；くら寿司品川駅前店（ https://epark.jp/detail/wait/479 ）の場合、「479」。
    # 設定ここまで
    epoch = calculate_epoch_time_of_the_day(year=year, month=month, day=day)

    base_url = base_url_generator(
        store_id=store_id_to_search,
        department_id=get_department_id(store_id_to_search),
        epoch_JST_of_the_day=epoch
    )

    mugen(base_url, hours)
