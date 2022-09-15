# Tsukete_Camera

Repository for Team Yonyon Trigger2022

## Set UP

### 1. Setup venv
```bash
python3 -m venv .venv
```
then
```bash
// actibate venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Copy image to tsukete_camrea/images from tsukete_camera/camera_images
```bash
cp tsukete_camera/camera_images/{picture_file}.* tsukete_camera/images/
```
※ tuskete_camera/images内の画像は必ず一枚にする


### 4. Run camera system
```bash
python3 tsukete_camera/detect_seated.py
```