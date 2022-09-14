import shutil
import os
import subprocess


# カレントディレクトリのパスを取得
current_path = os.getcwd()

# 仮想環境をアクティブにするためのコマンドのパス指定
venv_activate_path = os.path.join(current_path,'.venv/bin/activate')

# 推論に必要なパスの指定
detect_py_path = os.path.join(current_path,'yolov5/detect.py')

img_filename = 'restaurant_2_nohuman'

input_dir_path =os.path.join(current_path,f'tsukete_camera/images/{img_filename}.jpg')

output_dir_path = os.path.join(current_path,'tsukete_camera/results')

model_weight_path = os.path.join(current_path,'tsukete_camera/models/yolov5s.pt')

# 推論パラメータの指定

# 推論値の閾値
conf = '0.4'

# フィルターするクラス(オブジェクト)の指定 => 0: person
# yolov5/data/coco.yamlに詳細が書いてある
filter_class = "0"


# ラベル結果ファイルのパス
label_txt_path = os.path.join(output_dir_path, 'labels', img_filename + '.txt')

# 毎回推論前にtsukete_camera/resultsの中身を空にする
shutil.rmtree(output_dir_path)
os.mkdir(output_dir_path)


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

# 推論の実行
cmd = " ".join(commands)
result = subprocess.run(cmd, shell=True)

if (os.path.isfile(label_txt_path)):
  print("Human is Detected!!")
else: print("No human detected...")