from config import logger
from flask import Flask, render_template, jsonify
from werkzeug.utils import secure_filename
import request
import os
from intelhex import hex2bin

app = Flask(__name__)
app.debug = True
start = None
end = None
size = None
pad = None
header_data = [0x55, 0x00, 0x00, 0x20, 0x64, 0x00, 0x80, 0x46]
DEFAULT_STEP = 0x40
DEFAULT_TAIL = [0x20, ]
DEFAULT_READ_BIN_DATA_SIZE = 128
DEFAULT_BIN_FILE_TAIL = [0x51, 0x20]


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            logger.debug('No file part')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        if 'project' not in request.project:
            logger.debug('No file part')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No project part'})
        if 'version' not in request.version:
            logger.debug('No file part')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No version part'})

        f = request.files['file']
        project = request.form.get("project")
        version = request.form.get("version")
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(base_path, 'static', project, version)
        f.save(file_path, secure_filename(f.filename))
        get_hex_file_name(file_path)

        return "文件上传成功!!"
    return render_template('upload.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
