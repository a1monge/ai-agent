from flask import Flask, request, jsonify, render_template_string
from agent import run
import threading
import uuid

app = Flask(__name__)
jobs = {}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Research Agent</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 60px auto; padding: 0 20px; }
        h1 { font-size: 24px; }
        input { width: 100%; padding: 10px; font-size: 16px; margin: 10px 0; box-sizing: border-box; }
        button { padding: 10px 24px; font-size: 16px; background: #000; color: #fff; border: none; cursor: pointer; }
        button:disabled { background: #999; }
        #status { margin-top: 20px; color: #555; }
        #report { margin-top: 20px; white-space: pre-wrap; background: #f5f5f5; padding: 20px; display: none; }
        .score { font-weight: bold; }
    </style>
</head>
<body>
    <h1>Research Agent</h1>
    <input id="topic" type="text" placeholder="Enter a research topic..." />
    <button id="btn" onclick="startResearch()">Research</button>
    <div id="status"></div>
    <div id="report"></div>

    <script src="/static/app.js"></script>
</body>
</html>
"""

@app.route("/")
def index():
    return HTML

@app.route("/research", methods=["POST"])
def research():
    topic = request.json.get("topic")
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "running"}

    def run_job():
        try:
            result = run(topic)
            jobs[job_id] = {"status": "done", "result": result}
        except Exception as e:
            jobs[job_id] = {"status": "error", "error": str(e)}

    threading.Thread(target=run_job).start()
    return jsonify({"job_id": job_id})

@app.route("/status/<job_id>")
def status(job_id):
    return jsonify(jobs.get(job_id, {"status": "not found"}))

if __name__ == "__main__":
    app.run(debug=True, port=5000)