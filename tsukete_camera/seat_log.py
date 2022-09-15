import os
import datetime
from typing import Tuple

timezone_jst = datetime.timezone(datetime.timedelta(hours=9))

class SeatLog:

  def write_log(self, file_path:str, state: str, timezone:str) -> None:
    dt_now_jst = datetime.datetime.now(timezone).strftime('%Y/%m/%d %H:%M:%S')
    with open(file_path, 'a') as f:
      f.write(dt_now_jst + ' ' + f'{state}\n')
      f.close()

  def read_log_lines(self,file_path:str) -> list:
    try:
      with open(file_path, 'r') as f:
        seat_log_lines = f.readlines()
        f.close()
      return seat_log_lines

    except FileNotFoundError as fe:
      print('読み込むファイルが存在しません')
      print(fe)
  
  def get_recent_states(self,seat_log_lines: list, line_num:int) -> list:
    previous_states = list(map(lambda log_line: log_line.split()[-1], seat_log_lines[-line_num:]))
    return previous_states