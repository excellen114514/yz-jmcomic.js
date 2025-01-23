import jmcomic
from flask import Flask, request, send_file, abort
import os
import shutil
import logging

app = Flask(__name__)

# 指定图片存储的文件夹路径
IMAGE_FOLDER = "C:/your/per/path"  # 替换为你的图片存储路径

@app.route('/jmd', methods=['GET'])
def get_image():
    # 获取参数 jm
    option = jmcomic.create_option_by_file('C:/your/per/path/option.yml')
    jm = request.args.get('jm', type=int)
  
    # 检查参数是否存在且为整数
    if jm is None or not str(jm).isdigit():
        abort(400, description="Missing parameter 'jm' or it is not a positive integer")
    
    # 构造图片文件的完整路径
    image_name = f"{jm}.png"  
    image_path = os.path.join(IMAGE_FOLDER, image_name)
    
    # 检查图片是否存在
    if not os.path.exists(image_path):
        jmcomic.download_album(jm, option)
    # 返回图片
    logging.info(f"Returning image: {image_path}")
    response = send_file(image_path, mimetype='image/png')
    
    # 清理下载文件
    shutil.rmtree(IMAGE_FOLDER, ignore_errors=True)
    
    return response

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=8000)
