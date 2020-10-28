import time
import datetime

import requests
import simpleaudio

base_url = "https://epark.jp/receive_department/wait/reserve_minute_select_ajax/172441/depart/21429?receive%5Breceipt_date%5D%5Bdate%5D=1603810800&receive%5Breceipt_date%5D%5Bhour%5D="
hours = [18, 19, 20]

while True:
    for hour in hours:
        res = requests.get(base_url + str(hour))
        if "～" in res.text:
            print(f"{hour}発見！")
            wav_obj = simpleaudio.WaveObject.from_wave_file("発見の音.wav")
            play_obj = wav_obj.play()
            play_obj.wait_done()
        else:
            print("未発見", datetime.datetime.now())
        time.sleep(10)
