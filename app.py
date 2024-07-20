# app.py
from flask import Flask, Response, render_template
from functions.stream import get_stream
from functions.tracking import track_objects

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(track_objects(get_stream()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5025, debug=True)





# from flask import Flask, Response, render_template
# from video_processing.stream import VideoStream

# app = Flask(__name__)
# video_stream = VideoStream()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(video_stream.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5025, debug=True)
