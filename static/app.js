function startResearch() {
    const topic = document.getElementById('topic').value.trim();
    if (!topic) return;

    document.getElementById('btn').disabled = true;
    document.getElementById('status').innerText = 'Researching... this takes about 30-60 seconds.';
    document.getElementById('report').style.display = 'none';

    fetch('/research', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({topic: topic})
    })
    .then(r => r.json())
    .then(data => pollStatus(data.job_id));
}

function pollStatus(jobId) {
    fetch('/status/' + jobId)
    .then(r => r.json())
    .then(data => {
        if (data.status === 'done') {
            showReport(data.result);
        } else if (data.status === 'error') {
            document.getElementById('status').innerText = 'Error: ' + data.error;
            document.getElementById('btn').disabled = false;
        } else {
            setTimeout(function() { pollStatus(jobId); }, 2000);
        }
    });
}

function showReport(result) {
    const r = result;
    let html = 'Topic: ' + r.topic + '\n\n';
    html += 'Summary:\n' + r.summary + '\n\n';
    html += 'Key Insights:\n' + r.key_insights.map(function(i) { return '• ' + i; }).join('\n') + '\n\n';
    html += 'Gaps:\n' + r.gaps.map(function(g) { return '• ' + g; }).join('\n') + '\n\n';
    html += 'Quality: ' + r.quality_score + ' | Eval: ' + r.eval_scores.overall + '\n';
    html += 'Critique: ' + r.eval_scores.critique;

    document.getElementById('status').innerText = '';
    document.getElementById('btn').disabled = false;
    const el = document.getElementById('report');
    el.innerText = html;
    el.style.display = 'block';
}