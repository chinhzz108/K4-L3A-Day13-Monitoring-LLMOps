# Báo cáo cá nhân — K4-L3A Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** Trần Trọng Chinh
- **MSSV:** 2A202602720
- **Lớp:** K4-L3A
- **Repository URL:** https://github.com/chinhzz108/K4-L3A-Day13-Monitoring-LLMOps
- **Commit SHA cuối:** f6b9b12bb8f2d3c26824bf3e1114937401fce0d8
- **Challenge ID:** challenge-k4-l3a-2a202602720
- **Tên project Langfuse cá nhân:** `day13-k4-l3a-2A202602720`

## 2. Evidence index

Điền đúng đường dẫn tới evidence thực tế. Mọi đường dẫn đều là tương đối và có thể kiểm tra trực tiếp.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | [evidence/01-pytest.png](evidence/01-pytest.png) &bull; [evidence/01-pytest.txt](evidence/01-pytest.txt) |
| Log validator | [evidence/02-log-validator.png](evidence/02-log-validator.png) &bull; [evidence/02-log-validator.txt](evidence/02-log-validator.txt) |
| Dashboard validator | [evidence/03-dashboard-validator.png](evidence/03-dashboard-validator.png) &bull; [evidence/03-dashboard-validator.txt](evidence/03-dashboard-validator.txt) |
| Structured log | [evidence/04-structured-log.png](evidence/04-structured-log.png) &bull; [evidence/04-structured-log.txt](evidence/04-structured-log.txt) |
| PII redaction | [evidence/05-pii-redaction.png](evidence/05-pii-redaction.png) &bull; [evidence/05-pii-redaction.txt](evidence/05-pii-redaction.txt) |
| Trace list | [evidence/06-trace-list.png](evidence/06-trace-list.png) |
| Trace waterfall | [evidence/07-trace-waterfall.png](evidence/07-trace-waterfall.png) |
| Trace metadata | [evidence/08-trace-metadata.png](evidence/08-trace-metadata.png) |
| Prompt versions | [evidence/09-prompt-versions.png](evidence/09-prompt-versions.png) |
| Prompt rollback | [evidence/10-prompt-rollback.png](evidence/10-prompt-rollback.png) |
| Dashboard runtime | [evidence/11-dashboard-overview.png](evidence/11-dashboard-overview.png) |
| Incident metric | [evidence/12-incident-metric.png](evidence/12-incident-metric.png) |
| Incident log | [evidence/13-incident-log.png](evidence/13-incident-log.png) &bull; [evidence/13-incident-log.txt](evidence/13-incident-log.txt) |
| Incident trace | [evidence/14-incident-trace.png](evidence/14-incident-trace.png) |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` | 0/100 (chưa có log, thiếu correlation_id & enrichment) | 100/100 | Đạt toàn bộ 4 tiêu chí: JSON schema, propagation, enrichment, scrubbing |
| `validate_dashboard.py` | 6/6 panel | 6/6 panel | Đủ 6 panel chuẩn contract, có đầy đủ query, unit và threshold |
| `pytest` | 22 passed | 22 passed (100%) | Toàn bộ unit tests & integration tests đều vượt qua trơn tru |
| Số traces hợp lệ | 0 | 20+ traces | Traces được ghi nhận với đầy đủ quan hệ root, retrieval và generation |
| Số PII leak | Chưa xác định | 0 leak | Kiểm tra với email, sđt Việt Nam, CCCD 12 số, credit card |
| Latency P95 / TTFT P95 | N/A | 159 ms / 50 ms | Nằm sâu bên dưới ngưỡng SLO (<= 3000 ms) |
| Retrieval success rate | N/A | 100% (bình thường) / 83.3% (sự cố) | Phản ánh đúng trạng thái vận hành thực tế |

## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:**
  - Được triển khai thông qua `CorrelationIdMiddleware` (`app/middleware.py`).
  - Trước mỗi request, gọi `clear_contextvars()` để tránh hiện tượng rò rỉ context giữa các request bất đồng bộ trên cùng worker thread.
  - Trích xuất header `x-request-id` từ client; nếu client không truyền hoặc truyền sai định dạng, tự động sinh mã mới theo chuẩn `req-<8-char-hex>` bằng `uuid.uuid4().hex[:8]`.
  - Gán vào structlog contextvars thông qua `bind_contextvars(correlation_id=correlation_id)` và lưu vào `request.state.correlation_id`.
  - Trả về correlation ID và thời gian xử lý qua response headers: `x-request-id` và `x-response-time-ms`.
- **Các metadata được ghi vào structured log:**
  - Toàn cục (Global): `ts` (ISO timestamp UTC), `level`, `service` ("api" / "control"), `event`, `correlation_id`.
  - Request Context: `user_id_hash` (băm sha256 12 ký tự để ẩn danh PII), `session_id`, `feature`, `model`, `env`.
  - Observability Metrics trong `response_sent`: `latency_ms`, `ttft_ms`, `tokens_in`, `tokens_out`, `cost_usd`, `quality_score`, `tool_name`, `tool_success`.
- **Cách bảo đảm PII được scrub trước khi ghi:**
  - Processor `scrub_event` trong `app/logging_config.py` được đăng ký trong chuỗi xử lý structlog ngay trước `JsonlFileProcessor` và `JSONRenderer`.
  - Hàm `_scrub_recursive` duyệt qua toàn bộ cấu trúc dữ liệu của log event (nested dict, list, string) và thay thế các chuỗi khớp với biểu thức chính quy (`email`, `phone_vn`, `cccd`, `credit_card`, `passport`) thành các token che giấu: `[REDACTED_EMAIL]`, `[REDACTED_PHONE_VN]`, `[REDACTED_CCCD]`, `[REDACTED_CREDIT_CARD]`, `[REDACTED_PASSPORT]`.
  - Do việc scrub diễn ra ở cấp độ processor trong bộ nhớ trước khi file writer nhận chuỗi JSON, log ghi xuống đĩa tuyệt đối không chứa PII thô.
- **Cách kiểm chứng kết quả:**
  - Gửi request chứa email (`chinh@example.com`), số điện thoại (`0912345678`), CCCD (`001234567890`) và số thẻ (`4111 2222 3333 4444`).
  - Chạy `python scripts/validate_logs.py` kiểm tra độc lập bằng regex phát hiện PII: báo cáo 0 PII leaks, đạt điểm 100/100.

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:**
  - Project Langfuse Cloud được định danh riêng biệt theo MSSV: `day13-k4-l3a-2A202602720`.
  - Mọi trace đều gắn tag `["lab", feature, model]`, user ID băm duy nhất `8be07f9decb0` và `environment: dev`.
- **Cấu trúc root/retrieval/generation observations:**
  - Root observation: `lab-agent-run` (type `agent`), bao bọc toàn bộ chu trình xử lý của `LabAgent.run`.
  - Child observation 1: `retrieval` (type `retriever`), đo đạc thời gian tìm kiếm tài liệu từ vector database/corpus và số lượng tài liệu trích xuất (`doc_count`).
  - Child observation 2: `generation` (type `generation`), đo lường LLM inference, ghi nhận `model` (`claude-sonnet-4-5`), `ttft_ms` (Time To First Token), token sử dụng (`input`, `output`, `total`) và chi phí tính toán (`cost_usd`).
  - Mối quan hệ phân cấp cha-con được thể hiện chuẩn xác trên waterfall view của Langfuse.
- **Cách nối trace với log:**
  - `correlation_id` được gán vào metadata của trace Langfuse (`metadata={"correlation_id": correlation_id, ...}`) đồng thời xuất hiện trong mọi bản ghi structured log tại `data/logs.jsonl` của request tương ứng.
- **Prompt name:** `day13-chat`
- **Version/label baseline:** Version `v1` gắn label `baseline`.
- **Version/label candidate:** Version `v2` gắn label `candidate`, sau đó được promote lên `production`.
- **Trace ID của mỗi version:**
  - Trace ID sử dụng Prompt v2 (production): `tr-6756e026` (correlation_id: `req-6756e026`).
  - Trace ID sử dụng Prompt v1 (baseline / rollback): `tr-e7cd4481` (correlation_id: `req-e7cd4481`).
- **Cách promote và rollback `production`:**
  - Promotion: Trên giao diện Langfuse Prompt Management (hoặc SDK), gán nhãn `production` cho phiên bản `v2` sau khi kiểm chứng chất lượng vượt trội so với baseline. API tự động fetch prompt bản mới nhất mang label `production` mà không cần sửa code.
  - Rollback: Khi phát hiện dấu hiệu bất thường (hoặc trong bài tập diễn tập rollback), chỉ cần chuyển nhãn `production` quay trở lại phiên bản `v1`. Không cần restart container/server, hệ thống tự động tải lại phiên bản an toàn ngay trong request kế tiếp (zero downtime).

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:**
  1. *Latency percentiles and TTFT* (đơn vị: `ms`): p50, p95, p99 và TTFT p95 (ngưỡng p95 <= 3000ms).
  2. *Request traffic* (đơn vị: `requests_per_minute`): giám sát lưu lượng gọi API theo phút (ngưỡng >= 1 req/min).
  3. *Error rate and retrieval success* (đơn vị: `%`): theo dõi tỉ lệ lỗi tổng và tỉ lệ retrieval thành công (ngưỡng error <= 2%).
  4. *Cost over time* (đơn vị: `USD`): chi phí tích lũy theo phút và tổng chi phí trong khung giờ (ngưỡng <= $2.50).
  5. *Input and output tokens* (đơn vị: `tokens`): khối lượng token vào và ra (ngưỡng <= 50,000 tokens).
  6. *Quality proxy* (đơn vị: `score_0_to_1`): điểm số đánh giá chất lượng câu trả lời heuristic (ngưỡng >= 0.75).
- **SLO và lý do chọn:**
  - Primary SLO: `fast_successful_requests` với mục tiêu 99.5% request hoàn thành trong thời gian `<= 3000ms` trên chu kỳ đánh giá 28 ngày (`window: 28d`).
  - Lý do: Với hệ thống trợ lý ảo phục vụ hỏi đáp trực tiếp, phản hồi trễ quá 3 giây gây ức chế và làm gián đoạn dòng suy nghĩ của người dùng. Ngưỡng 3000ms đảm bảo độ tin cậy trải nghiệm người dùng cuối trong khi vẫn dung nạp được độ trễ mạng và token generation.
- **Cách tính error budget:**
  - Target SLO = 99.5%, do đó Error Budget = 100% - 99.5% = 0.5%.
  - Nếu trong 28 ngày có tổng số 1,000,000 requests, ngân sách lỗi cho phép là 5,000 requests bị chậm (> 3000ms) hoặc thất bại. Khi tốc độ đốt ngân sách (burn rate) vượt quá hạn mức, hệ thống phải đóng băng triển khai tính năng mới để tập trung tối ưu hiệu năng.
- **Ba alert và runbook tương ứng:**
  - Alert 1: `high_latency_p95` (Warning, p95 > 3000ms trong 5m) &rarr; Runbook: `docs/alerts.md#alert-1`.
  - Alert 2: `high_error_rate` (Critical, error_rate_pct > 2% trong 3m) &rarr; Runbook: `docs/alerts.md#alert-2`.
  - Alert 3: `degraded_retrieval_success` (Warning, tool_success_rate_pct < 90% trong 5m) &rarr; Runbook: `docs/alerts.md#alert-3`.

## 7. Điều tra challenge

- **Challenge ID:** `challenge-k4-l3a-2a202602720` (kịch bản diễn tập sự cố `tool_fail` / `rag_slow`)
- **Khoảng thời gian điều tra:** 2026-09-30 02:28:00Z &ndash; 02:31:00Z (múi giờ UTC)
- **Triệu chứng từ metrics:**
  - Panel "Error rate and retrieval success" trên dashboard ghi nhận tỉ lệ lỗi tăng đột biến từ 0% lên 15.0%, vượt xa ngưỡng SLO Guardrail (tối đa 2.0%).
  - Tỉ lệ retrieval thành công giảm xuống 83.3% (ngưỡng an toàn là >= 90%).
- **Log line và correlation ID liên quan:**
  - Correlation ID: `req-c8baad2c`
  - Log trích xuất:
    ```json
    {
      "service": "api",
      "event": "request_failed",
      "correlation_id": "req-c8baad2c",
      "session_id": "sess_fail",
      "error_type": "RuntimeError",
      "tool_name": "retrieval",
      "tool_success": false,
      "payload": {
        "detail": "Vector store timeout",
        "message_preview": "How does monitoring work?"
      }
    }
    ```
- **Trace ID và span gây ảnh hưởng:**
  - Trace ID trong Langfuse: `tr-c8baad2c`
  - Span gây ảnh hưởng: Child span `retrieval` (type: `retriever`) bị throw exception `RuntimeError("Vector store timeout")` tại thời điểm thực thi. Do bước retrieval gặp sự cố, luồng xử lý bị ngắt quãng, span `generation` của LLM không được kích hoạt.
- **Root cause:**
  - Dịch vụ Vector Database gặp tình trạng nghẽn kết nối hoặc quá tải timeout trong quá trình truy vấn tài liệu ngữ cảnh, dẫn đến việc hàm `retrieve()` văng ngoại lệ `RuntimeError`.
- **Fix action:**
  - Kích hoạt cơ chế Circuit Breaker và Graceful Degradation: khi vector store timeout hoặc fail quá số lần quy định, tự động chuyển sang chế độ trả lời tổng quát không có RAG thay vì ném lỗi HTTP 500 ra người dùng.
- **Preventive measure:**
  - Bổ sung connection pooling và exponential backoff retry có jitter cho các truy vấn retrieval.
  - Tích hợp caching cho các tài liệu/câu hỏi thường gặp (semantic cache) để giảm tải trực tiếp cho vector store.
  - Thiết lập alert cảnh báo sớm khi latency của vector store vượt quá 1500ms.

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:**
  - Quyết định: Đặt processor lọc PII (`scrub_event`) ở tầng structlog pipeline trước `JsonlFileProcessor` và `JSONRenderer`, kết hợp duyệt đệ quy toàn bộ cấu trúc dữ liệu payload thay vì chỉ lọc một số trường cố định.
  - Lý do: Đảm bảo nguyên tắc "Security by Design" — không có bất kỳ dữ liệu nhạy cảm nào được tuần tự hóa hoặc lưu xuống ổ cứng/stdout. Việc lọc đệ quy giúp hệ thống an toàn ngay cả khi các module trong tương lai bổ sung thêm các trường dữ liệu tùy biến mới.
- **Một lỗi/blocker đã gặp:**
  - Blocker: Khi mới chạy `validate_logs.py`, các bản ghi cũ từ trước khi sửa code còn lưu trong `data/logs.jsonl` khiến script báo lỗi thiếu metadata và context enrichment.
- **Cách tìm nguyên nhân và xử lý:**
  - Nguyên nhân: `validate_logs.py` đọc toàn bộ file `data/logs.jsonl` từ đầu đến cuối chứ không chỉ đọc các dòng mới.
  - Xử lý: Xóa sạch file `data/logs.jsonl`, khởi động lại server API và chạy lại workload test (`load_test.py`), qua đó toàn bộ log mới đều chuẩn schema và đạt 100/100 điểm.
- **Cách hiểu luồng Metrics → Logs → Traces:**
  - *Metrics*: Lớp phát hiện (Detection) &mdash; Giúp phát hiện triệu chứng ở tầm vĩ mô nhanh nhất (ví dụ: error rate tăng, latency p95 vượt ngưỡng) và kích hoạt cảnh báo on-call.
  - *Logs*: Lớp định vị (Localization) &mdash; Cho biết cụ thể sự kiện gì xảy ra trong khoảng thời gian đó, lọc ra các request bị lỗi và trích xuất mã định danh `correlation_id`.
  - *Traces*: Lớp căn nguyên (Root Cause Analysis) &mdash; Sử dụng `correlation_id` để mở biểu đồ phân rã thời gian (waterfall) của request đó, kiểm tra chi tiết từng span (retrieval, prompt resolution, generation) để tìm chính xác dòng code, câu lệnh hoặc dịch vụ bên thứ ba gây ra sự cố.
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:**
  - Prompt Versioning cho phép quản lý vòng đời prompt như mã nguồn phần mềm, tách biệt code logic với nội dung hướng dẫn prompt, cho phép A/B testing và canary release.
  - Giám sát Token & Cost bảo vệ ngân sách vận hành, phát hiện kịp thời các tình huống bùng nổ chi phí (cost spike) do prompt injection, lặp vô tận hoặc output quá dài.
  - Rollback đảm bảo tính khả dụng (high availability): khi phiên bản prompt mới gây ảo giác (hallucination) hoặc suy giảm điểm chất lượng, đội ngũ vận hành có thể hoàn tác ngay lập tức mà không cần quy trình build/deploy phức tạp.
- **Điều quan trọng nhất đã học:**
  - Khả năng kết nối chặt chẽ giữa 3 trụ cột của Observability (Metrics, Logs, Traces) thông qua `correlation_id` là chìa khóa để vận hành một hệ thống AI/LLM production ổn định, đáng tin cậy và minh bạch.
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:**
  - Hệ thống hiện tại sử dụng mock LLM và mock vector store phục vụ môi trường lab thực hành. Khi đưa lên môi trường sản xuất thực tế, cần tích hợp semantic caching nâng cao (Redis/Qdrant) và áp dụng distributed tracing liên service qua OpenTelemetry Collector.

## 9. Checklist trước khi nộp

- [x] Kết quả và evidence thuộc commit SHA cuối.
- [x] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [x] Incident evidence nối đúng metric → log → trace.
- [x] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [x] Repository chạy lại được theo README.
- [x] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [x] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.
