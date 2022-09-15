# Tsukete_Camera

Repository for Team Yonyon Trigger2022

## Set UP

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Copy image to tsukete_camrea/images from tsukete_camera/camera_images
```bash
cp tsukete_camera/camera_images/{picture_file}.* tsukete_camera/images/
```
※ tuskete_camera/images内の画像は必ず一枚にする

### 3. Activate venv
```bash
source .venv/bin/activate
```

### 4. Run camera system
```bash
python3 tsukete_camera/detect_seated.py
```