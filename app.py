# app.py
import jmcomic
from flask import Flask, request, send_file, abort
import os
import shutil
import logging
import schedule
import time
import threading
from dotenv import load_dotenv  # 类似 Node.js 的 dotenv 包

# 加载环境变量（类似 Node.js 的 process.env）
load_dotenv()  # 默认加载 .env 文件

# --------------------------
# Flask 初始化
# --------------------------
app = Flask(__name__)

# --------------------------
# 配置项（环境变量优先 + 默认值）
# --------------------------
# 注意：Python 中推荐使用大写命名环境变量
JM_BASE_DIR = os.getenv('JM_BASE_DIR', 'C:/a/b/your/path')  # 基础目录
EXCLUDE_FOLDER = os.getenv('JM_EXCLUDE_FOLDER', 'long')     # 保留文件夹名
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')             # 监听地址
FLASK_PORT = int(os.getenv('FLASK_PORT', '8000'))           # 端口需要转为整数
CLEANUP_INTERVAL = int(os.getenv('CLEANUP_HOURS', '1'))     # 清理间隔（小时）

# 推导路径（避免硬编码，类似 Node.js 的 path.join）
IMAGE_FOLDER = os.path.join(JM_BASE_DIR, 'long')       # 图片目录
OPTION_YML_PATH = os.path.join(JM_BASE_DIR, 'option.yml')  # 配置文件路径

# --------------------------
# 日志配置（类似 Node.js 的 winston/morgan）
# --------------------------
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),  # 文件日志
            logging.StreamHandler()         # 控制台日志
        ]
    )

# --------------------------
# 文件夹清理函数
# --------------------------
def delete_folders_except_one(target_dir, exclude_folder):
    """删除目标目录下除指定文件夹外的所有内容"""
    if not os.path.exists(target_dir):
        logging.warning(f"目录不存在: {target_dir}")
        return

    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isdir(item_path) and item != exclude_folder:
            try:
                shutil.rmtree(item_path)
                logging.info(f"已删除: {item_path}")
            except Exception as e:
                logging.error(f"删除失败: {item_path} - {str(e)}")

# --------------------------
# 定时任务（类似 Node.js 的 node-schedule）
# --------------------------
def cleanup_job():
    logging.info(f"开始清理 {JM_BASE_DIR}...")
    delete_folders_except_one(JM_BASE_DIR, EXCLUDE_FOLDER)

def schedule_loop():
    # 动态设置间隔（比 Node.js 的 setInterval 更灵活）
    schedule.every(CLEANUP_INTERVAL).hours.do(cleanup_job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次（比 Node.js 的 cron 表达式更易读）

# --------------------------
# Flask 路由（类似 Express 的路由）
# --------------------------
@app.route('/jmd', methods=['GET'])
def get_image():
    try:
        # 参数验证（类似 Express 的 req.query）
        jm_id = request.args.get('jm', type=int)
        if not jm_id or jm_id <= 0:
            abort(400, description="参数 jm 必须为正整数")

        # 初始化配置（类似 Node.js 的 config 模块）
        option = jmcomic.create_option_by_file(OPTION_YML_PATH)
        
        # 构建图片路径
        image_path = os.path.join(IMAGE_FOLDER, f"{jm_id}.png")

        # 下载逻辑
        if not os.path.exists(image_path):
            logging.info(f"下载新专辑: {jm_id}")
            jmcomic.download_album(jm_id, option)
            
            # 二次验证（防御性编程）
            if not os.path.exists(image_path):
                abort(404, description="资源下载后仍未找到")

        # 返回图片（类似 Express 的 res.sendFile）
        return send_file(image_path, mimetype='image/png')

    except Exception as e:
        logging.error(f"请求处理失败: {str(e)}")
        abort(500, description=f"服务器错误: {str(e)}")

# --------------------------
# 主程序（类似 Node.js 的 app.listen()）
# --------------------------
if __name__ == '__main__':
    # 初始化日志
    configure_logging()
    
    # 首次清理
    logging.info("执行首次清理...")
    delete_folders_except_one(JM_BASE_DIR, EXCLUDE_FOLDER)
    
    # 启动定时任务（类似 Node.js 的 worker_threads）
    threading.Thread(target=schedule_loop, daemon=True).start()
    
    # 启动 Flask（生产环境建议用 Gunicorn，类似 PM2）
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=False  # 生产环境务必关闭 debug 模式
    )