# Flask Text To Audio Code by Sandro Putraa
from flask import Flask, request, jsonify, send_from_directory, render_template
from gtts import gTTS, langs
from flask_apscheduler import APScheduler
import os
import time


app = Flask(__name__, template_folder="template")
scheduler = APScheduler()

def scheduleTask():
    directory = os.getcwd() + "/tmp/"
    for list_file in os.listdir(directory):
        os.remove(os.path.join(directory, list_file))
        print(" * [ CronJobs ] File " + list_file + " Deleted")

@app.route("/")
def home():
    language_pack = langs._main_langs()
    return render_template("index.html", option_language=language_pack)


@app.route("/tmp/<path:path>")
def static_dir(path):
    return send_from_directory("tmp", path)


@app.route("/api", methods=['POST'])
def api():
    languages = request.form["language"]
    text = request.form["text"]

    if (languages and text) == '':
        return jsonify({
            "status": False,
            "msg": "Fill all form !"
        })

    try:

        random_name = "audio-" + str(time.time())
        audio = gTTS(text=text, lang=languages, tld="com")
        audio.save(os.getcwd() + '/tmp/' + str(random_name) + '.mp3')

    except ValueError as e:

        return jsonify({
            "status": False,
            "msg": str(e),
        })

    return jsonify({
        "status": True,
        "msg": "success",
        "url": "/tmp/" + str(random_name) + ".mp3"
    })


if __name__ == '__main__':
    scheduler.add_job(id='Scheduled Task', func=scheduleTask, trigger="interval", seconds=180)
    scheduler.start()
    app.run(debug=False, threaded=True, host='0.0.0.0')
