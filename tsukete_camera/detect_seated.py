import shutil
import os
import subprocess
import datetime
import schedule
from seat_log import SeatLog
import pathlib

STATE_SEATED = 'seated'
STATE_VACANT = 'vacant'

def detect():
  # シートログデータ用のタイムゾーンを設定
  timezone_jst = datetime.timezone(datetime.timedelta(hours=9))

  # カレントディレクトリのパスを取得
  current_path = os.getcwd()

  # 座席ログファイル(seat_log.txt)のパス
  seat_logs_path = os.path.join(current_path,'tsukete_camera/seat_logs.txt')

  # APIに送るstateのログファイル
  seat_state_logs_path = os.path.join(current_path,'tsukete_camera/seat_state_logs.txt')

  # 仮想環境をアクティブにするためのコマンドのパス指定
  venv_activate_path = os.path.join(current_path,'.venv/bin/activate')

  # 推論に必要なパスの指定
  detect_py_path = os.path.join(current_path,'yolov5/detect.py')

  img_filename = os.listdir(os.path.join(current_path, 'tsukete_camera/images'))[-1].split('.')[0]
  input_dir_path =os.path.join(current_path,f'tsukete_camera/images/{img_filename}.jpg')

  output_dir_path = os.path.join(current_path,'tsukete_camera/results')

  model_weight_path = os.path.join(current_path,'tsukete_camera/models/yolov5s.pt')

  # 推論パラメータの指定

  # 推論値の閾値
  conf = '0.4'

  # フィルターするクラス(オブジェクト)の指定 => 0: person
  # yolov5/data/coco.yamlに詳細が書いてある
  filter_class = '0'


  # ラベル結果ファイルのパス
  label_txt_path = os.path.join(output_dir_path, 'labels', img_filename + '.txt')

  # サブコマンド用のコマンドを定義する
  commands = [
    '.', venv_activate_path,
    '&',
    'python', detect_py_path,
    '--source', input_dir_path,
    '--name', output_dir_path,
    '--weights', model_weight_path,
    '--exist-ok', '--save-txt',
    '--classes', filter_class,
    '--conf', conf
  ]

  # 毎回推論前にtsukete_camera/resultsの中身を空にする
  shutil.rmtree(output_dir_path)
  os.mkdir(output_dir_path)

  # 推論の実行
  cmd = ' '.join(commands)
  result = subprocess.run(cmd, shell=True)


  """
  1.seat_logを読み込んで、着席の判定をする

  #seat_logs.txtは最初に必要なのでなければ空のファイル作る
  """
  #ログを扱うためのクラスのインスタンス
  seatlog = SeatLog()
  # seat_logs.txtを一行ずつ読み込む
  log_lines = seatlog.read_log_lines(seat_logs_path)

  if (os.path.isfile(seat_logs_path)):
    pass
  else:
    pathlib.Path(seat_logs_path).touch()

  if (os.path.isfile(seat_state_logs_path)):
    pass
  else:
    seatlog.write_log(seat_state_logs_path,STATE_VACANT,timezone_jst)

  recent_seat_state = seatlog.read_log_lines(seat_state_logs_path)[-1].split()[-1]

  # 判定結果をログデータに書き込む
  if (os.path.isfile(label_txt_path)):
    print('Human is Detected!!')
    current_state = STATE_SEATED
    if(len(log_lines) >= 10):
      # 現在の状態をログに書き込む前に、前の10分間の状態の判定をする
      recent_states = seatlog.get_recent_states(log_lines,10)
      """
      10分間、空席状態(vacant)が続いている状態 
      かつ 
      人物が検出されていたら着席APIを叩く
      """
      if(all(x == STATE_VACANT for x in recent_states) and (recent_seat_state == STATE_VACANT)):
        print('空席 -> 着席')
        seatlog.write_log(seat_state_logs_path,STATE_SEATED,timezone_jst)
      else:
        print(f'席の状態: {recent_seat_state}')
    else:
      print('経過時間10分未満')

  else: 
    """
      離席 -> 席に人を検知していないが、その席に客はまだいる状態
      空席 -> 7分以上離席状態が続いている状態
    """
    print("Don't detect any human...")
    current_state = STATE_VACANT
    if(len(log_lines) >= 10):
      recent_states = seatlog.get_recent_states(log_lines,6)
      """
      離席が7分以上続く 
      かつ 
      現在の座席状態が着席(seat_state_logs.txtの最後の行が着席)であれば空席APIを叩く
      """
      if(all(x == STATE_VACANT for x in recent_states)):
        if(recent_seat_state == STATE_SEATED):
          print('離席 -> 空席')
          seatlog.write_log(seat_state_logs_path,STATE_VACANT,timezone_jst)
        else:
          print(f'席の状態: {recent_seat_state}')
      else:
        vacant_duration = recent_states.count(STATE_VACANT)
        print(f'離席: {vacant_duration + 1}分経過')
    else:
      print('経過時間10分未満')
  seatlog.write_log(file_path=seat_logs_path,state=current_state,timezone=timezone_jst)


  """
  2. バックエンドとの通信処理を書く
  """


# 定期実行のための処理
schedule.every(1).minutes.do(detect)

while True:
  schedule.run_pending()