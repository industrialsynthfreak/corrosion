import corrosion2 as corroder

from flask import Flask, render_template, url_for

app = Flask(__name__)


def generate():
    data = corroder.Constructor.construct()
    size = data.count('\n')
    return render_template('index.html', text=data, text_height=size)


@app.route('/', methods=['GET'])
def index():
    return generate()


if __name__ == '__main__':
    app.run()
