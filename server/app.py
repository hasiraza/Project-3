from flask import Flask, render_template, request, jsonify
from performance import PerformanceBenchmark, make_track_performance
from chatbot import generate_linkedin_reply
from datetime import datetime
import os

app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)

benchmark = PerformanceBenchmark()
track_performance = make_track_performance(benchmark)
generate_linkedin_reply = track_performance(generate_linkedin_reply)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/api/generate-reply', methods=['POST'])
def api_generate_reply():
    try:
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()

        comment = data.get('comment', '')
        context = data.get('context', 'professional')

        if not comment or not comment.strip():
            return jsonify({'error': 'Comment is required'}), 400

        reply = generate_linkedin_reply(comment, context)

        return jsonify({
            'success': True,
            'reply': reply,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    try:
        data = request.json
        satisfaction = int(data.get('satisfaction', 0))

        metrics = {
            'user_satisfaction': satisfaction,
            'quality_score': satisfaction,
            'response_time': 0,
            'api_call_time': 0,
            'tokens_used': 0
        }

        benchmark.log_performance(metrics)
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/benchmark-targets')
def api_benchmark_targets():
    PERFORMANCE_TARGETS = {
        'response_time': {'excellent': 1.0, 'good': 2.0, 'acceptable': 5.0, 'poor': float('inf')},
        'api_call_time': {'excellent': 0.5, 'good': 1.0, 'acceptable': 2.0, 'poor': float('inf')},
        'quality_score': {'excellent': 9.0, 'good': 7.0, 'acceptable': 5.0, 'poor': 0},
        'error_rate': {'excellent': 0.1, 'good': 1.0, 'acceptable': 5.0, 'poor': float('inf')}
    }
    return jsonify(PERFORMANCE_TARGETS)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
