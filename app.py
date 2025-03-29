# app.py
import jmcomic
from flask import Flask, request, send_file, abort, send_from_directory
import os
import shutil
import logging
import schedule
import time
import threading
from dotenv import load_dotenv
import sys
from threading import Event, Lock

# 加载环境变量
load_dotenv()

# --------------------------
# Flask 初始化
# --------------------------
app = Flask(__name__)

# --------------------------
# 全局配置与变量
# --------------------------
JM_BASE_DIR = os.getenv('JM_BASE_DIR', 'C:/a/b/your/path')
EXCLUDE_FOLDER = os.getenv('JM_EXCLUDE_FOLDER', 'long')
EXCLUDE_FOLDER_PDF = os.getenv('JM_EXCLUDE_FOLDER_PDF', 'pdf')
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', '8000'))
CLEANUP_INTERVAL = int(os.getenv('CLEANUP_HOURS', '1'))

# 推导路径
IMAGE_FOLDER = os.path.join(JM_BASE_DIR, 'long')
PDF_FOLDER = os.path.join(JM_BASE_DIR, 'pdf')
OPTION_YML_PATH = os.path.join(JM_BASE_DIR, 'option.yml')

# 新增全局配置
DOWNLOAD_RETRY_MAX = 3
download_restart_flag = Event()
download_lock = Lock()

# --------------------------
# 日志配置
# --------------------------
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

# --------------------------
# 安全下载函数
# --------------------------
def safe_download_album(jm_id, option):
    """带异常捕获和自动重启的下载函数"""
    retry = 0
    while retry < DOWNLOAD_RETRY_MAX:
        try:
            with download_lock:
                logging.info(f"开始下载专辑 {jm_id} (尝试 {retry+1}/{DOWNLOAD_RETRY_MAX})")
                jmcomic.download_album(jm_id, option)
                return True
        except Exception as e:
            logging.error(f"下载失败: {str(e)}")
            retry += 1
            time.sleep(5)
    
    logging.critical(f"专辑 {jm_id} 下载失败，已达最大重试次数")
    download_restart_flag.set()
    return False

# --------------------------
# 文件夹清理函数
# --------------------------
def delete_folders_except_imgandpdf(target_dir, exclude_folder_img, exclude_folder_pdf):
    """带锁的清理函数"""
    with download_lock:
        if not os.path.exists(target_dir):
            logging.warning(f"目录不存在: {target_dir}")
            return

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if os.path.isdir(item_path) and item not in [exclude_folder_img, exclude_folder_pdf]:
                try:
                    shutil.rmtree(item_path)
                    logging.info(f"已删除: {item_path}")
                except Exception as e:
                    logging.error(f"删除失败: {item_path} - {str(e)}")

# --------------------------
# 定时任务
# --------------------------
def cleanup_job():
    logging.info(f"开始清理 {JM_BASE_DIR}...")
    delete_folders_except_imgandpdf(JM_BASE_DIR, EXCLUDE_FOLDER, EXCLUDE_FOLDER_PDF)

def schedule_loop():
    try:
        schedule.every(CLEANUP_INTERVAL).hours.do(cleanup_job)
        while True:
            schedule.run_pending()
            time.sleep(60)
    except Exception as e:
        logging.error(f"定时任务异常: {str(e)}")
        download_restart_flag.set()

# --------------------------
# 路由处理
# --------------------------
@app.route('/jmd', methods=['GET'])
def get_image():
    try:
        jm_id = request.args.get('jm', type=int)
        if not jm_id or jm_id <= 0:
            abort(400, description="参数 jm 必须为正整数")

        option = jmcomic.create_option_by_file(OPTION_YML_PATH)
        image_path = os.path.join(IMAGE_FOLDER, f"{jm_id}.png")

        if not os.path.exists(image_path):
            if not safe_download_album(jm_id, option):
                abort(503, description="服务暂时不可用，正在自动恢复")

            if not os.path.exists(image_path):
                abort(404, description="资源下载后仍未找到")

        return send_file(image_path, mimetype='image/png')

    except Exception as e:
        logging.error(f"全局异常捕获: {str(e)}")
        if download_restart_flag.is_set():
            restart_application()
        abort(500, description=f"服务器错误: {str(e)}")

@app.route('/jmdp', methods=['GET'])
def get_pdf():
    try:
        jm_id = request.args.get('jm', type=int)
        if not jm_id or jm_id <= 0:
            abort(400, description="参数 jm 必须为正整数")

        option = jmcomic.create_option_by_file(OPTION_YML_PATH)
        pdf_path = os.path.join(PDF_FOLDER, f"{jm_id}.pdf")

        if not os.path.exists(pdf_path):
            if not safe_download_album(jm_id, option):
                abort(503, description="服务暂时不可用，正在自动恢复")

            if not os.path.exists(pdf_path):
                abort(404, description="资源下载后仍未找到")

        return send_from_directory(
            PDF_FOLDER,
            f"{jm_id}.pdf",
            as_attachment=True
        )

    except Exception as e:
        logging.error(f"请求处理失败: {str(e)}")
        if download_restart_flag.is_set():
            restart_application()
        abort(500, description=f"服务器错误: {str(e)}")

# --------------------------
# 进程管理
# --------------------------
def restart_application():
    """安全重启应用"""
    logging.critical("执行安全重启...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

# --------------------------
# 主程序
# --------------------------
if __name__ == '__main__':
    configure_logging()
    logging.info("执行首次清理...")
    delete_folders_except_imgandpdf(JM_BASE_DIR, EXCLUDE_FOLDER, EXCLUDE_FOLDER_PDF)
    
    threading.Thread(target=schedule_loop, daemon=True).start()
    
    # 守护循环
    while True:
        try:
            app.run(
                host=FLASK_HOST,
                port=FLASK_PORT,
                debug=False,
                use_reloader=False
            )
        except Exception as e:
            logging.critical(f"主进程崩溃: {str(e)}")
            time.sleep(10)
            continue
        break