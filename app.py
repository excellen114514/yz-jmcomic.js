import jmcomic
from flask import Flask, request, send_file, abort
import os
import shutil
import logging
import schedule
import time
import threading

app = Flask(__name__)

# 指定图片存储的文件夹路径
IMAGE_FOLDER = "C:/a/b/your/path"  # 替换为你的图片存储路径
EXCLUDE_FOLDER = "long"  # 替换为要保留的文件夹名称

# 定义删除文件夹的函数（保留特定文件夹）
def delete_folders_except_one(target_dir, exclude_folder):
    """
    删除指定目录下的所有文件夹，但保留一个特定的文件夹。
    :param target_dir: 目标目录路径
    :param exclude_folder: 要保留的文件夹名称
    """
    if not os.path.exists(target_dir):
        logging.info(f"目标目录 {target_dir} 不存在。")
        return

    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isdir(item_path) and item != exclude_folder:  # 检查是否为文件夹且不是要保留的文件夹
            try:
                shutil.rmtree(item_path)  # 删除文件夹及其内容
                logging.info(f"已删除文件夹: {item_path}")
            except Exception as e:
                logging.error(f"删除文件夹 {item_path} 时出错: {e}")

# 定时任务函数
def job():
    logging.info(f"开始删除 {IMAGE_FOLDER} 下的文件夹...")
    delete_folders_except_one(IMAGE_FOLDER, EXCLUDE_FOLDER)
    logging.info("删除完成。")

# 在后台运行定时任务
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 设置定时任务，例如每小时执行一次
schedule.every().hour.do(job)

@app.route('/jmd', methods=['GET'])
def get_image():
    # 获取参数 jm
    option = jmcomic.create_option_by_file('C:/a/b/your/path/option.yml')
    jm = request.args.get('jm', type=int)
  
    # 检查参数是否存在且为整数
    if jm is None or not str(jm).isdigit():
        abort(400, description="Missing parameter 'jm' or it is not a positive integer")
    
    # 构造图片文件的完整路径
    image_name = f"{jm}.png"  
    image_path = os.path.join(IMAGE_FOLDER, 'long', image_name)
    
    # 检查图片是否存在
    if not os.path.exists(image_path):
        jmcomic.download_album(jm, option)
    
    # 返回图片
    logging.info(f"Returning image: {image_path}")
    response = send_file(image_path, mimetype='image/png')
    
    return response

if __name__ == '__main__':
    # 首次执行删除操作
    logging.basicConfig(level=logging.INFO)
    logging.info("首次删除操作开始...")
    delete_folders_except_one(IMAGE_FOLDER, EXCLUDE_FOLDER)
    logging.info("首次删除操作完成。")

    # 启动定时任务线程
    threading.Thread(target=run_schedule, daemon=True).start()

    # 启动 Flask 应用
    app.run(host='0.0.0.0', port=8000)
