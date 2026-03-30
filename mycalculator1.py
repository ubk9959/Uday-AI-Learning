import http.server
import socketserver
import json
from urllib.parse import urlparse

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Calculator</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background: #0a0a0f;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Share Tech Mono', monospace;
            background-image:
                radial-gradient(ellipse at 20% 50%, rgba(0, 255, 180, 0.05) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(0, 180, 255, 0.05) 0%, transparent 50%);
        }

        .calculator {
            background: #10101a;
            border: 1px solid rgba(0, 255, 180, 0.2);
            border-radius: 16px;
            padding: 36px 32px;
            width: 520px;
            box-shadow: 0 0 60px rgba(0, 255, 180, 0.06), 0 0 0 1px rgba(255,255,255,0.03) inset;
        }

        h1 {
            font-family: 'Orbitron', sans-serif;
            color: #00ffb4;
            font-size: 13px;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 28px;
            opacity: 0.7;
        }

        .number-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }

        .num-btn {
            background: #1a1a2e;
            border: 1px solid rgba(0, 255, 180, 0.15);
            border-radius: 8px;
            color: #00ffb4;
            font-family: 'Orbitron', sans-serif;
            font-size: 15px;
            font-weight: 700;
            padding: 14px 0;
            cursor: pointer;
            transition: all 0.15s ease;
            text-align: center;
        }

        .num-btn:hover {
            background: rgba(0, 255, 180, 0.12);
            border-color: rgba(0, 255, 180, 0.5);
            box-shadow: 0 0 14px rgba(0, 255, 180, 0.2);
            transform: translateY(-1px);
        }

        .num-btn.active {
            background: rgba(0, 255, 180, 0.2);
            border-color: #00ffb4;
        }

        .ops-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 24px;
        }

        .op-btn {
            background: #0f0f1e;
            border: 1px solid rgba(0, 180, 255, 0.25);
            border-radius: 8px;
            color: #00b4ff;
            font-family: 'Orbitron', sans-serif;
            font-size: 18px;
            font-weight: 900;
            padding: 14px 0;
            cursor: pointer;
            transition: all 0.15s ease;
            text-align: center;
        }

        .op-btn:hover {
            background: rgba(0, 180, 255, 0.12);
            border-color: rgba(0, 180, 255, 0.6);
            box-shadow: 0 0 14px rgba(0, 180, 255, 0.25);
            transform: translateY(-1px);
        }

        .op-btn.selected {
            background: rgba(0, 180, 255, 0.2);
            border-color: #00b4ff;
            box-shadow: 0 0 20px rgba(0, 180, 255, 0.3);
        }

        .display-area {
            background: #070710;
            border: 1px solid rgba(0, 255, 180, 0.12);
            border-radius: 10px;
            padding: 18px 20px;
            margin-bottom: 16px;
        }

        .display-label {
            font-size: 10px;
            letter-spacing: 0.2em;
            color: rgba(0, 255, 180, 0.4);
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        .expression-box {
            font-size: 14px;
            color: rgba(0, 255, 180, 0.6);
            min-height: 22px;
            letter-spacing: 0.05em;
        }

        .result-box {
            font-family: 'Orbitron', sans-serif;
            font-size: 32px;
            font-weight: 900;
            color: #00ffb4;
            min-height: 46px;
            text-shadow: 0 0 20px rgba(0, 255, 180, 0.5);
            letter-spacing: 0.05em;
            margin-top: 4px;
        }

        .result-box.error {
            color: #ff4d6d;
            font-size: 18px;
            text-shadow: 0 0 14px rgba(255, 77, 109, 0.4);
        }

        .action-row {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 10px;
        }

        .clear-btn {
            background: #1a0a10;
            border: 1px solid rgba(255, 77, 109, 0.3);
            border-radius: 8px;
            color: #ff4d6d;
            font-family: 'Orbitron', sans-serif;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.1em;
            padding: 14px;
            cursor: pointer;
            transition: all 0.15s ease;
            text-transform: uppercase;
        }

        .clear-btn:hover {
            background: rgba(255, 77, 109, 0.12);
            border-color: #ff4d6d;
            box-shadow: 0 0 14px rgba(255, 77, 109, 0.25);
        }

        .calc-btn {
            background: linear-gradient(135deg, #00ffb4, #00b4ff);
            border: none;
            border-radius: 8px;
            color: #0a0a0f;
            font-family: 'Orbitron', sans-serif;
            font-size: 13px;
            font-weight: 900;
            letter-spacing: 0.15em;
            padding: 14px;
            cursor: pointer;
            text-transform: uppercase;
            transition: all 0.15s ease;
        }

        .calc-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 24px rgba(0, 255, 180, 0.35);
        }

        .divider {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.05);
            margin: 20px 0;
        }
    </style>
</head>
<body>
<div class="calculator">
    <h1>&#9654; Python Calculator</h1>

    <div class="number-grid">
        <button class="num-btn" onclick="selectNumber(1, this)">1</button>
        <button class="num-btn" onclick="selectNumber(2, this)">2</button>
        <button class="num-btn" onclick="selectNumber(3, this)">3</button>
        <button class="num-btn" onclick="selectNumber(4, this)">4</button>
        <button class="num-btn" onclick="selectNumber(5, this)">5</button>
        <button class="num-btn" onclick="selectNumber(6, this)">6</button>
        <button class="num-btn" onclick="selectNumber(7, this)">7</button>
        <button class="num-btn" onclick="selectNumber(8, this)">8</button>
        <button class="num-btn" onclick="selectNumber(9, this)">9</button>
        <button class="num-btn" onclick="selectNumber(10, this)">10</button>
    </div>

    <hr class="divider">

    <div class="ops-grid">
        <button class="op-btn" onclick="selectOp('+', this)">+</button>
        <button class="op-btn" onclick="selectOp('-', this)">−</button>
        <button class="op-btn" onclick="selectOp('*', this)">×</button>
        <button class="op-btn" onclick="selectOp('/', this)">÷</button>
    </div>

    <div class="display-area">
        <div class="display-label">Expression</div>
        <div class="expression-box" id="expression">—</div>
        <div class="display-label" style="margin-top:10px;">Result</div>
        <div class="result-box" id="result">—</div>
    </div>

    <div class="action-row">
        <button class="clear-btn" onclick="clearAll()">Clear</button>
        <button class="calc-btn" onclick="calculate()">= Calculate</button>
    </div>
</div>

<script>
    let num1 = null, num2 = null, op = null, step = 'first';

    function selectNumber(n, btn) {
        if (step === 'first') {
            num1 = n;
        } else {
            num2 = n;
        }
        document.querySelectorAll('.num-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        updateExpression();
    }

    function selectOp(operation, btn) {
        op = operation;
        document.querySelectorAll('.op-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        if (num1 !== null) step = 'second';
        updateExpression();
    }

    function updateExpression() {
        const sym = { '+': '+', '-': '−', '*': '×', '/': '÷' };
        let expr = '';
        if (num1 !== null) expr += num1;
        if (op) expr += ' ' + (sym[op] || op);
        if (num2 !== null) expr += ' ' + num2;
        document.getElementById('expression').textContent = expr || '—';
    }

    function calculate() {
        if (num1 === null || num2 === null || op === null) {
            showResult('Select both numbers and an operation', true);
            return;
        }
        fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ num1, num2, op })
        })
        .then(r => r.json())
        .then(data => {
            if (data.error) showResult(data.error, true);
            else showResult(data.result, false);
        });
    }

    function showResult(value, isError) {
        const el = document.getElementById('result');
        el.textContent = value;
        el.className = 'result-box' + (isError ? ' error' : '');
    }

    function clearAll() {
        num1 = null; num2 = null; op = null; step = 'first';
        document.querySelectorAll('.num-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.op-btn').forEach(b => b.classList.remove('selected'));
        document.getElementById('expression').textContent = '—';
        document.getElementById('result').textContent = '—';
        document.getElementById('result').className = 'result-box';
    }
</script>
</body>
</html>
"""

class CalcHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Clean terminal output
        print(f"  {args[0]} {args[1]}")

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML.encode('utf-8'))

    def do_POST(self):
        if urlparse(self.path).path == '/calculate':
            length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(length))

            num1 = body.get('num1')
            num2 = body.get('num2')
            op   = body.get('op')

            try:
                if op == '+':
                    result = num1 + num2
                elif op == '-':
                    result = num1 - num2
                elif op == '*':
                    result = num1 * num2
                elif op == '/':
                    if num2 == 0:
                        self._send_json({'error': 'Cannot divide by zero'})
                        return
                    result = num1 / num2
                    result = int(result) if result == int(result) else round(result, 4)
                else:
                    self._send_json({'error': 'Unknown operation'})
                    return
                self._send_json({'result': result})
            except Exception as e:
                self._send_json({'error': str(e)})

    def _send_json(self, data):
        response = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)


PORT = 5000

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CalcHandler) as httpd:
        print(f"\n  ✅ Calculator running!")
        print(f"  👉 Open your browser: http://localhost:{PORT}")
        print(f"  🛑 Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Server stopped.")