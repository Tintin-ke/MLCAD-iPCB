import paddlex as pdx
import cv2
from PIL import Image

def angle_identify(img_path):
    print('\n')
    print(img_path)
    print("Loading model...")
    model = pdx.load_model(
        '../PaddleX/P0002/P0002-T0002_export_model/inference_model/inference_model')
    print("Model loaded.")

    im = cv2.imread(img_path)
    im = im.astype('float32')

    result = model.predict(im)
    print('result:', result)

    # 输出分类结果
    if model.model_type == "classifier":
        #print(result)
        result = result[0]
        print('result[0]:', result)
        angle = result['category']
        score = result['score']
        print(result['category'])

    if angle == '0':
        return
    elif angle == '90' and score >= 0.8:
        img = Image.open(img_path)
        img = img.transpose(Image.ROTATE_90)  # 旋转90度
        img.save(img_path)
        #im = img
        return
    elif angle == '180' and score >= 0.8:
        img = Image.open(img_path)
        img = img.transpose(Image.ROTATE_180)  # 旋转180度
        img.save(img_path)
        #im = img
        return
    elif angle == '270' and score >= 0.8:
        img = Image.open(img_path)
        img = img.transpose(Image.ROTATE_270)  # 旋转90度
        img.save(img_path)
        #im = img
        return

