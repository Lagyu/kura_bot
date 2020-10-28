import time
import datetime
from typing import List

import requests
import simpleaudio


def mugen (base_url: str, suffix: List[int]) -> None:
    while True:
        for hour in suffix:
            res = requests.get(base_url + str(hour))
            if "～" in res.text:
                print(f"{hour}時台の空きを発見！")
                wav_obj = simpleaudio.WaveObject.from_wave_file("発見の音.wav")
                play_obj = wav_obj.play()
                play_obj.wait_done()
            else:
                print("未発見", datetime.datetime.now())
            time.sleep(10)


if __name__ == '__main__':
    url = "https://epark.jp/receive_department/wait/reserve_minute_select_ajax/110202/depart/11768?receive" \
          "%5Breceipt_date%5D%5Bdate%5D=1603810800&receive%5Breceipt_date%5D%5Bhour%5D= "
    hours = [18, 19, 20]
    mugen(base_url=url, suffix=hours)
