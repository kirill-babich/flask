from flask import Flask, render_template, Response, request, url_for
import cv2
import os

app = Flask(__name__)
url=0
camera = cv2.VideoCapture(url)

database = {'admin' : 'admin', 'babich' : 'babich'}


def generate_frames():
    while True:
        name, frame = camera.read()
        if not name:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
        return Response(generate_frames(),
            mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    print(url_for('index'))
    return render_template('login.html')

@app.route('/form_index', methods=['POST', 'GET'])
def login():
    name = request.form['username']
    password = request.form['password']
    print(name,password)
    if name not in database:
        return render_template('login.html', info='Неверный логин')
    else:
        if database[name]!=password:
            return render_template('login.html', info='Неверный пароль')
        else:
            return render_template('index.html', name=name)

@app.route('/login.html')
def log():
    print(url_for('log'))
    return render_template('login.html')


@app.route('/restart')
def restart():
    print(url_for('/restart'))
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)