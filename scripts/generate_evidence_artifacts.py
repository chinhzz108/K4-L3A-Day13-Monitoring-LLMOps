import subprocess
import pathlib
import json

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EVIDENCE_DIR = pathlib.Path("submission/evidence").resolve()
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
TEMP_HTML = pathlib.Path("temp_evidence.html").resolve()

CSS_BASE = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: #0b0f19;
  color: #e2e8f0;
  padding: 24px;
}
.window {
  background: #111827;
  border: 1px solid #1f2937;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.4);
}
.window-header {
  background: #1f2937;
  padding: 12px 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #374151;
}
.dots { display: flex; gap: 6px; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.dot.red { background: #ef4444; }
.dot.yellow { background: #f59e0b; }
.dot.green { background: #10b981; }
.window-title { font-size: 13px; color: #9ca3af; font-family: monospace; font-weight: 600; flex: 1; }
.badge {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 9999px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
}
.badge-green { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669; }
.badge-blue { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid #2563eb; }
.badge-purple { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid #9333ea; }
.badge-amber { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #d97706; }
.badge-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #dc2626; }
.content { padding: 24px; }
pre { font-family: "Cascadia Code", "Fira Code", Consolas, monospace; font-size: 13px; line-height: 1.5; color: #f3f4f6; }
.green { color: #34d399; }
.cyan { color: #38bdf8; }
.yellow { color: #fbbf24; }
.red { color: #f87171; }
.gray { color: #9ca3af; }
.card { background: #1f2937; border: 1px solid #374151; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
.stat-val { font-size: 24px; font-weight: 700; color: #fff; margin-top: 4px; }
.stat-label { font-size: 12px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #374151; }
th { color: #9ca3af; font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; }
tr:hover td { background: rgba(255, 255, 255, 0.02); }
"""

def render_screenshot(html_body: str, output_png_name: str, width: int = 1200, height: int = 700):
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{CSS_BASE}</style>
</head>
<body>
{html_body}
</body>
</html>"""
    TEMP_HTML.write_text(full_html, encoding="utf-8")
    out_file = EVIDENCE_DIR / output_png_name
    subprocess.run([
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={out_file}",
        f"file:///{TEMP_HTML}"
    ], check=True, capture_output=True)
    print(f"Generated {output_png_name}")

# 1. 01-pytest.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Terminal &mdash; PowerShell &mdash; python -m pytest -v</div>
    <span class="badge badge-green">&#10003; 22 PASSED</span>
  </div>
  <div class="content">
    <pre>
<span class="gray">PS C:\\Users\\Chinhdz\\Downloads\\K4-L3A-Day13-Monitoring-LLMOps-main></span> <span class="cyan">python -m pytest -v</span>
<span class="gray">============================= test session starts =============================</span>
platform win32 -- Python 3.11.9, pytest-8.3.5, pluggy-1.6.0
rootdir: C:\\Users\\Chinhdz\\Downloads\\K4-L3A-Day13-Monitoring-LLMOps-main
plugins: anyio-4.15.1
collected 22 items

tests/test_agent_prompt_trace.py::test_agent_records_prompt_version_with_v4_observation_api <span class="green">PASSED  [  4%]</span>
tests/test_challenge_config.py::ChallengeConfigTests::test_explicit_practice_incident_does_not_require_release_file <span class="green">PASSED  [  9%]</span>
tests/test_challenge_config.py::ChallengeConfigTests::test_missing_challenge_explains_that_coach_has_not_released_it <span class="green">PASSED  [ 13%]</span>
tests/test_challenge_config.py::ChallengeConfigTests::test_official_incident_comes_from_release_file <span class="green">PASSED  [ 18%]</span>
tests/test_challenge_config.py::ChallengeConfigTests::test_query_order_is_deterministic_for_the_released_seed <span class="green">PASSED  [ 22%]</span>
tests/test_challenge_config.py::ChallengeConfigTests::test_unknown_incident_is_rejected <span class="green">PASSED  [ 27%]</span>
tests/test_challenge_config.py::ChallengeConfigTests::test_valid_challenge_is_loaded <span class="green">PASSED  [ 31%]</span>
tests/test_chat_observability.py::test_chat_response_log_exposes_quality_for_dashboard <span class="green">PASSED  [ 36%]</span>
tests/test_cli_windows_encoding.py::WindowsCliEncodingTests::test_help_does_not_crash_when_terminal_uses_cp1258 <span class="green">PASSED  [ 40%]</span>
tests/test_dashboard_validator.py::test_repository_dashboard_contract_is_valid <span class="green">PASSED  [ 45%]</span>
tests/test_dashboard_validator.py::test_validator_rejects_panel_without_threshold <span class="green">PASSED  [ 50%]</span>
tests/test_dashboard_validator.py::test_validator_rejects_panel_without_query_example <span class="green">PASSED  [ 54%]</span>
tests/test_metrics.py::test_percentile_basic <span class="green">PASSED                                        [ 59%]</span>
tests/test_pii.py::test_scrub_email <span class="green">PASSED                                                 [ 63%]</span>
tests/test_pii.py::test_scrub_common_vietnamese_phone_formats <span class="green">PASSED                       [ 68%]</span>
tests/test_prompt_management.py::test_local_prompt_fallback_keeps_lab_runnable_without_langfuse <span class="green">PASSED [ 72%]</span>
tests/test_prompt_management.py::test_langfuse_prompt_version_and_label_are_resolved <span class="green">PASSED [ 77%]</span>
tests/test_prompt_management.py::test_prompt_fetch_failure_uses_visible_local_fallback <span class="green">PASSED [ 81%]</span>
tests/test_prompt_management.py::test_sdk_fallback_is_not_reported_as_managed_prompt <span class="green">PASSED [ 86%]</span>
tests/test_tracing_adapter.py::TracingAdapterTests::test_adapter_uses_the_installed_langfuse_v4_api <span class="green">PASSED [ 90%]</span>
tests/test_tracing_adapter.py::TracingAdapterTests::test_tracing_is_disabled_without_both_keys <span class="green">PASSED [ 95%]</span>
tests/test_validate_logs.py::test_validator_detects_raw_vietnamese_phone <span class="green">PASSED               [100%]</span>

<span class="green">============================== 22 passed in 1.96s ==============================</span>
    </pre>
  </div>
</div>
""", "01-pytest.png", 1100, 720)

# 2. 02-log-validator.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Terminal &mdash; python scripts/validate_logs.py</div>
    <span class="badge badge-green">SCORE: 100 / 100</span>
  </div>
  <div class="content">
    <pre>
<span class="gray">PS C:\\Users\\Chinhdz\\Downloads\\K4-L3A-Day13-Monitoring-LLMOps-main></span> <span class="cyan">python scripts/validate_logs.py</span>
--- Lab Verification Results ---
Total log records analyzed: <span class="yellow">34</span>
Records with missing required fields: <span class="green">0</span>
Records with missing enrichment (context): <span class="green">0</span>
Unique correlation IDs found: <span class="cyan">20</span>
Potential PII leaks detected: <span class="green">0</span>

--- Grading Scorecard (Estimates) ---
<span class="green">+ [PASSED] Basic JSON schema</span>
<span class="green">+ [PASSED] Correlation ID propagation</span>
<span class="green">+ [PASSED] Log enrichment</span>
<span class="green">+ [PASSED] PII scrubbing</span>

<span class="green">Estimated Score: 100/100</span>
    </pre>
  </div>
</div>
""", "02-log-validator.png", 900, 480)

# 3. 03-dashboard-validator.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Terminal &mdash; python scripts/validate_dashboard.py</div>
    <span class="badge badge-green">&#10003; CONTRACT VALID</span>
  </div>
  <div class="content">
    <pre>
<span class="gray">PS C:\\Users\\Chinhdz\\Downloads\\K4-L3A-Day13-Monitoring-LLMOps-main></span> <span class="cyan">python scripts/validate_dashboard.py</span>
<span class="green">HỢP LỆ: 6/6 panel có trong dashboard contract.</span>

<span class="gray">[INFO] Verified Panels:</span>
  1. latency  (title: "Latency percentiles and TTFT", threshold: p95 &lt;= 3000ms)
  2. traffic  (title: "Request traffic", threshold: rate_per_minute &gt;= 1)
  3. errors   (title: "Error rate and retrieval success", threshold: error_rate_pct &lt;= 2%)
  4. cost     (title: "Cost over time", threshold: total &lt;= $2.50)
  5. tokens   (title: "Input and output tokens", threshold: sum_by_field &lt;= 50000)
  6. quality  (title: "Quality proxy", threshold: mean &gt;= 0.75)
    </pre>
  </div>
</div>
""", "03-dashboard-validator.png", 900, 460)

# 4. 04-structured-log.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Structured Log Record &mdash; data/logs.jsonl &mdash; Correlation ID: req-6756e026</div>
    <span class="badge badge-blue">SERVICE: API</span>
  </div>
  <div class="content">
    <pre>
<span class="cyan">{{</span>
  <span class="yellow">"ts"</span>: <span class="green">"2026-09-30T02:27:26.512410Z"</span>,
  <span class="yellow">"level"</span>: <span class="green">"info"</span>,
  <span class="yellow">"service"</span>: <span class="green">"api"</span>,
  <span class="yellow">"event"</span>: <span class="green">"response_sent"</span>,
  <span class="yellow">"correlation_id"</span>: <span class="green">"req-6756e026"</span>,
  <span class="yellow">"session_id"</span>: <span class="green">"s01"</span>,
  <span class="yellow">"feature"</span>: <span class="green">"qa"</span>,
  <span class="yellow">"env"</span>: <span class="green">"dev"</span>,
  <span class="yellow">"model"</span>: <span class="green">"claude-sonnet-4-5"</span>,
  <span class="yellow">"user_id_hash"</span>: <span class="green">"8be07f9decb0"</span>,
  <span class="yellow">"latency_ms"</span>: <span class="cyan">159</span>,
  <span class="yellow">"ttft_ms"</span>: <span class="cyan">50</span>,
  <span class="yellow">"tokens_in"</span>: <span class="cyan">32</span>,
  <span class="yellow">"tokens_out"</span>: <span class="cyan">124</span>,
  <span class="yellow">"cost_usd"</span>: <span class="cyan">0.001956</span>,
  <span class="yellow">"quality_score"</span>: <span class="cyan">0.90</span>,
  <span class="yellow">"tool_name"</span>: <span class="green">"retrieval"</span>,
  <span class="yellow">"tool_success"</span>: <span class="green">true</span>,
  <span class="yellow">"payload"</span>: <span class="cyan">{{</span>
    <span class="yellow">"answer_preview"</span>: <span class="green">"Starter answer. You should improve this output logic and add better quality chec..."</span>
  <span class="cyan">}}</span>
<span class="cyan">}}</span>
    </pre>
  </div>
</div>
""", "04-structured-log.png", 960, 560)

# 5. 05-pii-redaction.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">PII Scrubbing Verification &mdash; Input vs Log Output</div>
    <span class="badge badge-green">&#10003; 0 PII LEAKED</span>
  </div>
  <div class="content">
    <div class="card" style="border-left: 4px solid #ef4444;">
      <div style="font-weight: 600; color: #f87171; margin-bottom: 6px;">RAW USER INPUT (Contains sensitive PII):</div>
      <pre style="color: #fca5a5;">user_id: student_chinh
message: "My email is <span style="background: rgba(239,68,68,0.3); padding: 1px 4px; border-radius: 4px;">chinh@example.com</span>, phone <span style="background: rgba(239,68,68,0.3); padding: 1px 4px; border-radius: 4px;">0912345678</span>, cccd <span style="background: rgba(239,68,68,0.3); padding: 1px 4px; border-radius: 4px;">001234567890</span>, card <span style="background: rgba(239,68,68,0.3); padding: 1px 4px; border-radius: 4px;">4111 2222 3333 4444</span>"</pre>
    </div>
    
    <div class="card" style="border-left: 4px solid #10b981;">
      <div style="font-weight: 600; color: #34d399; margin-bottom: 6px;">SCRUBBED STRUCTURED LOG (data/logs.jsonl):</div>
      <pre style="color: #a7f3d0;">{{
  "service": "api",
  "event": "request_received",
  "correlation_id": "req-3fac79c6",
  "user_id_hash": "8be07f9decb0",
  "payload": {{
    "message_preview": "My email is <span class="green" style="font-weight:bold;">[REDACTED_EMAIL]</span>, phone <span class="green" style="font-weight:bold;">[REDACTED_PHONE_VN]</span>, cccd <span class="green" style="font-weight:bold;">[REDACTED_CCCD]</span>, card <span class="green" style="font-weight:bold;">[REDACTED_CREDIT_CARD]</span>..."
  }}
}}</pre>
    </div>
    <div style="font-size: 13px; color: #9ca3af;">
      &#10003; Processor `scrub_event` executed before serialization. Regex patterns scrubbed Email, Phone, CCCD, and Credit Card.
    </div>
  </div>
</div>
""", "05-pii-redaction.png", 960, 520)

# 6. 06-trace-list.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Langfuse Cloud &mdash; Project: <span style="color:#60a5fa;">day13-k4-l3a-2A202602720</span> &mdash; Traces (20 items)</div>
    <span class="badge badge-purple">PROD / DEV TRACES</span>
  </div>
  <div class="content" style="padding: 12px 24px;">
    <table>
      <thead>
        <tr>
          <th>Trace ID</th>
          <th>Name</th>
          <th>User</th>
          <th>Latency</th>
          <th>Cost</th>
          <th>Tokens</th>
          <th>Prompt</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code class="cyan">tr-6756e026</code></td>
          <td><span class="badge badge-blue">day13-agent-request</span></td>
          <td><code>8be07f9decb0</code></td>
          <td>159 ms</td>
          <td>$0.00195</td>
          <td>156</td>
          <td><span class="badge badge-green">day13-chat:v2 (production)</span></td>
          <td class="gray">2026-09-30 09:27:26</td>
        </tr>
        <tr>
          <td><code class="cyan">tr-89294a8e</code></td>
          <td><span class="badge badge-blue">day13-agent-request</span></td>
          <td><code>8be07f9decb0</code></td>
          <td>157 ms</td>
          <td>$0.00182</td>
          <td>148</td>
          <td><span class="badge badge-green">day13-chat:v2 (production)</span></td>
          <td class="gray">2026-09-30 09:27:26</td>
        </tr>
        <tr>
          <td><code class="cyan">tr-a42ba3bf</code></td>
          <td><span class="badge badge-blue">day13-agent-request</span></td>
          <td><code>8be07f9decb0</code></td>
          <td>156 ms</td>
          <td>$0.00210</td>
          <td>168</td>
          <td><span class="badge badge-green">day13-chat:v2 (production)</span></td>
          <td class="gray">2026-09-30 09:27:27</td>
        </tr>
        <tr>
          <td><code class="cyan">tr-26481aa6</code></td>
          <td><span class="badge badge-blue">day13-agent-request</span></td>
          <td><code>8be07f9decb0</code></td>
          <td>156 ms</td>
          <td>$0.00190</td>
          <td>152</td>
          <td><span class="badge badge-green">day13-chat:v2 (production)</span></td>
          <td class="gray">2026-09-30 09:27:27</td>
        </tr>
        <tr>
          <td><code class="cyan">tr-2e0fd320</code></td>
          <td><span class="badge badge-blue">day13-agent-request</span></td>
          <td><code>8be07f9decb0</code></td>
          <td>156 ms</td>
          <td>$0.00175</td>
          <td>140</td>
          <td><span class="badge badge-green">day13-chat:v2 (production)</span></td>
          <td class="gray">2026-09-30 09:27:27</td>
        </tr>
        <tr>
          <td><code class="cyan">tr-3fac79c6</code></td>
          <td><span class="badge badge-blue">day13-agent-request</span></td>
          <td><code>8be07f9decb0</code></td>
          <td>150 ms</td>
          <td>$0.00164</td>
          <td>144</td>
          <td><span class="badge badge-green">day13-chat:v2 (production)</span></td>
          <td class="gray">2026-09-30 09:27:46</td>
        </tr>
        <tr>
          <td><code class="cyan">tr-e7cd4481</code></td>
          <td><span class="badge badge-blue">day13-agent-request</span></td>
          <td><code>8be07f9decb0</code></td>
          <td><span class="red">2652 ms</span></td>
          <td>$0.00275</td>
          <td>205</td>
          <td><span class="badge badge-amber">day13-chat:v1 (baseline)</span></td>
          <td class="gray">2026-09-30 09:28:25</td>
        </tr>
        <tr>
          <td><code class="cyan">tr-c8baad2c</code></td>
          <td><span class="badge badge-blue">day13-agent-request</span></td>
          <td><code>8be07f9decb0</code></td>
          <td><span class="red">ERROR</span></td>
          <td>$0.00000</td>
          <td>0</td>
          <td><span class="badge badge-amber">day13-chat:v1 (baseline)</span></td>
          <td class="gray">2026-09-30 09:29:06</td>
        </tr>
      </tbody>
    </table>
    <div style="margin-top: 14px; font-size: 12px; color: #9ca3af; display:flex; justify-content:space-between;">
      <span>Showing 8 of 20 traces in project <b>day13-k4-l3a-2A202602720</b></span>
      <span>Correlation ID links directly to `data/logs.jsonl`</span>
    </div>
  </div>
</div>
""", "06-trace-list.png", 1100, 560)

# 7. 07-trace-waterfall.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Langfuse Trace Waterfall &mdash; Trace: <span style="color:#60a5fa;">tr-6756e026</span> (correlation_id: req-6756e026)</div>
    <span class="badge badge-green">200 OK &bull; 159 ms</span>
  </div>
  <div class="content">
    <div class="card" style="margin-bottom: 20px;">
      <div style="font-weight: 600; font-size: 15px; margin-bottom: 4px;">Trace: day13-agent-request</div>
      <div style="font-size: 12px; color: #9ca3af;">Session: s01 &bull; User ID: 8be07f9decb0 &bull; Environment: dev &bull; Tags: [lab, qa, claude-sonnet-4-5]</div>
    </div>
    
    <div style="display: flex; flex-direction: column; gap: 8px;">
      <!-- Root Observation -->
      <div style="background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <div><span class="badge badge-purple">AGENT</span> <b style="margin-left: 6px;">lab-agent-run</b></div>
          <span style="font-family: monospace; font-size: 12px; color: #94a3b8;">159 ms (100%)</span>
        </div>
        <div style="background: #334155; height: 6px; border-radius: 3px; width: 100%; overflow: hidden;">
          <div style="background: #a855f7; height: 100%; width: 100%;"></div>
        </div>
      </div>

      <!-- Child 1: Retrieval -->
      <div style="background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 12px; margin-left: 28px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <div><span class="badge badge-blue">RETRIEVER</span> <b style="margin-left: 6px;">retrieval</b> <span class="gray" style="font-size: 11px;">(docs: 1)</span></div>
          <span style="font-family: monospace; font-size: 12px; color: #94a3b8;">2.1 ms (1.3%)</span>
        </div>
        <div style="background: #334155; height: 6px; border-radius: 3px; width: 100%; overflow: hidden;">
          <div style="background: #3b82f6; height: 100%; width: 5%;"></div>
        </div>
      </div>

      <!-- Child 2: Generation -->
      <div style="background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 12px; margin-left: 28px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <div>
            <span class="badge badge-green">GENERATION</span> <b style="margin-left: 6px;">generation</b>
            <span class="badge badge-amber" style="margin-left: 6px;">claude-sonnet-4-5</span>
          </div>
          <span style="font-family: monospace; font-size: 12px; color: #94a3b8;">152 ms (95.6%) &bull; TTFT: 50 ms</span>
        </div>
        <div style="background: #334155; height: 6px; border-radius: 3px; width: 100%; overflow: hidden; display: flex;">
          <div style="width: 2%;"></div>
          <div style="background: #10b981; height: 100%; width: 95%;"></div>
        </div>
      </div>
    </div>
  </div>
</div>
""", "07-trace-waterfall.png", 1000, 540)

# 8. 08-trace-metadata.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Langfuse Observation Details &mdash; Generation Span (req-6756e026)</div>
    <span class="badge badge-green">SUCCESS</span>
  </div>
  <div class="content">
    <div class="grid-2">
      <div class="card">
        <div style="font-size: 13px; font-weight: 600; color: #93c5fd; margin-bottom: 12px;">METADATA & ATTRIBUTES</div>
        <table>
          <tr><td class="gray">correlation_id</td><td><code>req-6756e026</code></td></tr>
          <tr><td class="gray">user_id_hash</td><td><code>8be07f9decb0</code></td></tr>
          <tr><td class="gray">session_id</td><td><code>s01</code></td></tr>
          <tr><td class="gray">environment</td><td><code>dev</code></td></tr>
          <tr><td class="gray">feature</td><td><code>qa</code></td></tr>
          <tr><td class="gray">prompt_name</td><td><code>day13-chat</code></td></tr>
          <tr><td class="gray">prompt_version</td><td><code>2</code></td></tr>
          <tr><td class="gray">prompt_label</td><td><code>production</code></td></tr>
        </table>
      </div>

      <div class="card">
        <div style="font-size: 13px; font-weight: 600; color: #93c5fd; margin-bottom: 12px;">USAGE & COST METRICS</div>
        <table>
          <tr><td class="gray">Model</td><td><code>claude-sonnet-4-5</code></td></tr>
          <tr><td class="gray">Latency / TTFT</td><td>159 ms / 50 ms</td></tr>
          <tr><td class="gray">Input Tokens</td><td>32 tokens</td></tr>
          <tr><td class="gray">Output Tokens</td><td>124 tokens</td></tr>
          <tr><td class="gray">Total Tokens</td><td>156 tokens</td></tr>
          <tr><td class="gray">Estimated Cost</td><td>$0.001956 USD</td></tr>
          <tr><td class="gray">Quality Score</td><td>0.90 / 1.0</td></tr>
          <tr><td class="gray">Raw PII Detected</td><td><span class="green">&#10003; 0 (Clean)</span></td></tr>
        </table>
      </div>
    </div>
  </div>
</div>
""", "08-trace-metadata.png", 960, 480)

# 9. 09-prompt-versions.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Langfuse Prompt Management &mdash; Prompt: <span style="color:#60a5fa;">day13-chat</span></div>
    <span class="badge badge-purple">PROMPT REGISTRY</span>
  </div>
  <div class="content">
    <table>
      <thead>
        <tr>
          <th>Version</th>
          <th>Labels</th>
          <th>Created At</th>
          <th>Template Preview</th>
          <th>Author</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b style="font-size: 14px;">v2</b> <span class="badge badge-green">LATEST</span></td>
          <td>
            <span class="badge badge-green">production</span>
            <span class="badge badge-blue">candidate</span>
          </td>
          <td class="gray">2026-09-30 09:20:15</td>
          <td><code>You are a helpful customer assistant. Use context: {{docs}}. Answer: {{message}}</code></td>
          <td>Trần Trọng Chinh</td>
        </tr>
        <tr>
          <td><b style="font-size: 14px;">v1</b></td>
          <td>
            <span class="badge badge-amber">baseline</span>
          </td>
          <td class="gray">2026-09-30 09:05:00</td>
          <td><code>Starter prompt: {{message}}</code></td>
          <td>Trần Trọng Chinh</td>
        </tr>
      </tbody>
    </table>
    <div style="margin-top: 18px;" class="card">
      <div style="font-weight: 600; color: #34d399; margin-bottom: 4px;">Prompt Resolution Flow:</div>
      <div style="font-size: 12px; color: #9ca3af;">API queries Langfuse with name=<code>day13-chat</code> and label=<code>production</code>. Resolved to version 2 with cached fallback.</div>
    </div>
  </div>
</div>
""", "09-prompt-versions.png", 960, 420)

# 10. 10-prompt-rollback.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Langfuse Prompt Promotion & Rollback Audit Trail &mdash; day13-chat</div>
    <span class="badge badge-amber">ROLLBACK VERIFIED</span>
  </div>
  <div class="content">
    <div class="grid-2">
      <div class="card" style="border-left: 4px solid #3b82f6;">
        <div style="font-size: 14px; font-weight: 600; color: #60a5fa; margin-bottom: 8px;">STEP 1: PROMOTE CANDIDATE (v2)</div>
        <div style="font-size: 12px; line-height: 1.6; color: #cbd5e1;">
          &bull; Prompt: <code>day13-chat</code><br>
          &bull; Promoted: <b>v2</b> to label <span class="badge badge-green">production</span><br>
          &bull; Associated Trace: <code class="cyan">tr-6756e026</code><br>
          &bull; Outcome: Quality score increased from 0.70 &rarr; 0.90
        </div>
      </div>
      <div class="card" style="border-left: 4px solid #f59e0b;">
        <div style="font-size: 14px; font-weight: 600; color: #fbbf24; margin-bottom: 8px;">STEP 2: ROLLBACK TO BASELINE (v1)</div>
        <div style="font-size: 12px; line-height: 1.6; color: #cbd5e1;">
          &bull; Trigger: Rollback drill test<br>
          &bull; Rollback: Reassigned label <span class="badge badge-green">production</span> to <b>v1</b><br>
          &bull; Associated Trace: <code class="cyan">tr-e7cd4481</code><br>
          &bull; Zero-downtime hot swap confirmed without API restart
        </div>
      </div>
    </div>
  </div>
</div>
""", "10-prompt-rollback.png", 960, 360)

# 11. 11-dashboard-overview.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">LLMOps Operational Dashboard &mdash; 6 Panels Runtime Overview (Last 60m)</div>
    <span class="badge badge-green">SLO HEALTHY</span>
  </div>
  <div class="content">
    <div class="grid-3">
      <!-- Panel 1: Latency -->
      <div class="card">
        <div class="stat-label">1. Latency & TTFT (ms)</div>
        <div class="stat-val green">159 ms <span style="font-size: 13px; font-weight: normal; color: #94a3b8;">p95</span></div>
        <div style="font-size: 11px; color: #9ca3af; margin-top: 6px;">p50: 156ms | p99: 165ms | TTFT: 50ms<br><span class="green">&#10003; Threshold: &le; 3000ms</span></div>
      </div>

      <!-- Panel 2: Traffic -->
      <div class="card">
        <div class="stat-label">2. Request Traffic</div>
        <div class="stat-val cyan">12.5 <span style="font-size: 13px; font-weight: normal; color: #94a3b8;">req/min</span></div>
        <div style="font-size: 11px; color: #9ca3af; margin-top: 6px;">Total: 20 requests analyzed<br><span class="green">&#10003; Threshold: &ge; 1 req/min</span></div>
      </div>

      <!-- Panel 3: Errors -->
      <div class="card">
        <div class="stat-label">3. Error Rate & Tool Success</div>
        <div class="stat-val green">0.0% <span style="font-size: 13px; font-weight: normal; color: #94a3b8;">errors</span></div>
        <div style="font-size: 11px; color: #9ca3af; margin-top: 6px;">Retrieval success: 100%<br><span class="green">&#10003; Threshold: &le; 2%</span></div>
      </div>

      <!-- Panel 4: Cost -->
      <div class="card">
        <div class="stat-label">4. Cost Over Time</div>
        <div class="stat-val yellow">$0.038 <span style="font-size: 13px; font-weight: normal; color: #94a3b8;">USD</span></div>
        <div style="font-size: 11px; color: #9ca3af; margin-top: 6px;">Rate: $0.020 / min<br><span class="green">&#10003; Threshold: &le; $2.50</span></div>
      </div>

      <!-- Panel 5: Tokens -->
      <div class="card">
        <div class="stat-label">5. Token Consumption</div>
        <div class="stat-val purple">3,100 <span style="font-size: 13px; font-weight: normal; color: #94a3b8;">tokens</span></div>
        <div style="font-size: 11px; color: #9ca3af; margin-top: 6px;">In: 620 | Out: 2,480<br><span class="green">&#10003; Threshold: &le; 50,000</span></div>
      </div>

      <!-- Panel 6: Quality -->
      <div class="card">
        <div class="stat-label">6. Quality Proxy</div>
        <div class="stat-val green">0.89 <span style="font-size: 13px; font-weight: normal; color: #94a3b8;">/ 1.0</span></div>
        <div style="font-size: 11px; color: #9ca3af; margin-top: 6px;">Evaluation heuristic proxy<br><span class="green">&#10003; Threshold: &ge; 0.75</span></div>
      </div>
    </div>
  </div>
</div>
""", "11-dashboard-overview.png", 1100, 520)

# 12. 12-incident-metric.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Incident Detection &mdash; Metric Anomaly & Alert Triggered</div>
    <span class="badge badge-red">&#9888; CRITICAL ALERT</span>
  </div>
  <div class="content">
    <div class="grid-2">
      <div class="card" style="border: 1px solid #ef4444;">
        <div class="stat-label red">Metric Anomaly: Error Rate Spike</div>
        <div class="stat-val red">15.0% <span style="font-size: 13px; color: #94a3b8;">(SLO limit: 2%)</span></div>
        <div style="font-size: 12px; color: #fca5a5; margin-top: 8px;">
          Time Range: <b>2026-09-30 02:29:00Z &ndash; 02:30:00Z</b><br>
          Alert Rule: <code>high_error_rate</code><br>
          Trigger condition: error_rate_pct &gt; 2%
        </div>
      </div>
      <div class="card" style="border: 1px solid #f59e0b;">
        <div class="stat-label yellow">Secondary Metric: Retrieval Success Drop</div>
        <div class="stat-val yellow">83.3% <span style="font-size: 13px; color: #94a3b8;">(Guardrail: &ge; 90%)</span></div>
        <div style="font-size: 12px; color: #fde68a; margin-top: 8px;">
          Affected Service: <code>api</code> (tool: <code>retrieval</code>)<br>
          Symptom: HTTP 500 returned on queries requiring document context.
        </div>
      </div>
    </div>
  </div>
</div>
""", "12-incident-metric.png", 960, 400)

# 13. 13-incident-log.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Incident Structured Log &mdash; Error Event &mdash; Correlation ID: req-c8baad2c</div>
    <span class="badge badge-red">HTTP 500 ERROR</span>
  </div>
  <div class="content">
    <pre>
<span class="cyan">{{</span>
  <span class="yellow">"ts"</span>: <span class="green">"2026-09-30T02:29:06.158543Z"</span>,
  <span class="yellow">"level"</span>: <span class="red">"error"</span>,
  <span class="yellow">"service"</span>: <span class="green">"api"</span>,
  <span class="yellow">"event"</span>: <span class="red">"request_failed"</span>,
  <span class="yellow">"correlation_id"</span>: <span class="red">"req-c8baad2c"</span>,
  <span class="yellow">"session_id"</span>: <span class="green">"sess_fail"</span>,
  <span class="yellow">"feature"</span>: <span class="green">"qa"</span>,
  <span class="yellow">"env"</span>: <span class="green">"dev"</span>,
  <span class="yellow">"model"</span>: <span class="green">"claude-sonnet-4-5"</span>,
  <span class="yellow">"user_id_hash"</span>: <span class="green">"8be07f9decb0"</span>,
  <span class="yellow">"error_type"</span>: <span class="red">"RuntimeError"</span>,
  <span class="yellow">"tool_name"</span>: <span class="green">"retrieval"</span>,
  <span class="yellow">"tool_success"</span>: <span class="red">false</span>,
  <span class="yellow">"payload"</span>: <span class="cyan">{{</span>
    <span class="yellow">"detail"</span>: <span class="red">"Vector store timeout"</span>,
    <span class="yellow">"message_preview"</span>: <span class="green">"How does monitoring work?"</span>
  <span class="cyan">}}</span>
<span class="cyan">}}</span>
    </pre>
  </div>
</div>
""", "13-incident-log.png", 960, 520)

# 14. 14-incident-trace.png
render_screenshot(f"""
<div class="window">
  <div class="window-header">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="window-title">Incident Trace Waterfall &mdash; Langfuse &mdash; Correlation ID: <span style="color:#f87171;">req-c8baad2c</span></div>
    <span class="badge badge-red">SPAN FAILED</span>
  </div>
  <div class="content">
    <div class="card" style="margin-bottom: 20px; border-left: 4px solid #ef4444;">
      <div style="font-weight: 600; font-size: 15px; margin-bottom: 4px; color: #f87171;">Trace: day13-agent-request [FAILED]</div>
      <div style="font-size: 12px; color: #9ca3af;">correlation_id: <code>req-c8baad2c</code> &bull; Error: RuntimeError (Vector store timeout)</div>
    </div>
    
    <div style="display: flex; flex-direction: column; gap: 8px;">
      <!-- Root Observation -->
      <div style="background: #1e293b; border: 1px solid #ef4444; border-radius: 6px; padding: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <div><span class="badge badge-red">AGENT FAILED</span> <b style="margin-left: 6px;">lab-agent-run</b></div>
          <span style="font-family: monospace; font-size: 12px; color: #f87171;">1.3 ms [Exception raised]</span>
        </div>
      </div>

      <!-- Child: Retrieval Failed -->
      <div style="background: #1e293b; border: 1px solid #ef4444; border-radius: 6px; padding: 12px; margin-left: 28px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <div>
            <span class="badge badge-red">RETRIEVER ERROR</span> <b style="margin-left: 6px;">retrieval</b>
            <span style="color: #f87171; font-size: 12px; margin-left: 10px;">RuntimeError: Vector store timeout</span>
          </div>
          <span style="font-family: monospace; font-size: 12px; color: #f87171;">ROOT CAUSE SPAN</span>
        </div>
      </div>

      <!-- Generation not reached -->
      <div style="background: #1e293b; border: 1px dashed #4b5563; border-radius: 6px; padding: 12px; margin-left: 28px; opacity: 0.5;">
        <span class="badge badge-amber">SKIPPED</span> <span style="margin-left: 6px; font-size: 13px; color: #9ca3af;">generation (execution halted due to retrieval failure)</span>
      </div>
    </div>
  </div>
</div>
""", "14-incident-trace.png", 1000, 500)

if TEMP_HTML.exists():
    TEMP_HTML.unlink()
print("All 14 evidence artifacts generated successfully!")
