import subprocess
from sys import stdout

from flask import Flask, render_template, send_from_directory,send_file,abort
from datetime import datetime
import os
import platform

from werkzeug.utils import append_slash_redirect

#导入日志配置
from log import dir_test,setup_flask_logging
#检查文件夹是否建立
dir_test()


app = Flask(__name__)

# 设置 Flask 日志
log_path = setup_flask_logging(app)  # 调用日志设置函数
print(f"Log file path:{log_path}")  # 打印日志文件路径

# 音乐文件目录
app.config['UPLOAD_FOLDER'] = 'static/music' 
# 获取音乐文件列表
def get_music_files():
    music_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
# 显示播放器
@app.route('/music')
def index():
    songs = get_music_files()
    return render_template('music.html', songs=songs)
# 提供音乐文件播放
@app.route('/music/<filename>')
def stream_music(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#资源文件目录
app.config['RESOURCE_FOLDER'] = 'static/resource'
# 获取资源文件，获取文件详细信息
def get_file_info():
    files = []
    for filename in os.listdir(app.config['RESOURCE_FOLDER']):
        filepath = os.path.join(app.config['RESOURCE_FOLDER'], filename)
        if os.path.isfile(filepath):
            stat = os.stat(filepath)
            files.append({
                'name': filename,
                'size': round(stat.st_size / 1024, 2),  # KB
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'type': filename.split('.')[-1] if '.' in filename else '未知'
            })
    return files
#显示资源页
@app.route('/resource')
def notice():
    files = get_file_info()
    return render_template('notice.html', files=files)
#提供文件的下载
@app.route('/download/<filename>')

def download_file(filename):
    try:
        # 安全检查，防止目录遍历攻击
        if '..' in filename or filename.startswith('/'):
            abort(400)
        return send_from_directory(
            app.config['RESOURCE_FOLDER'], 
            filename, 
            as_attachment=True
        )
    except FileNotFoundError:
        abort(404)

'''
#这是一段简单的示例代码：
@app.route('/example') #自定义路径
def about():
    return render_template('example.html') #引用文件
'''
#定义主页的路径
@app.route('/')
def home():
    return render_template('index.html')

#爬虫君子协议
@app.route('/Robots.txt')
def robots():
    return render_template('Robots.txt')

@app.route('/map')
def map():
    return render_template('map.html')
#404错误页重定向
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

#403错误页重定向
@app.errorhandler(403)
def page_refuse_access(e):
    return render_template('403.html')

if __name__ == '__main__':
    app.run(debug=True)
