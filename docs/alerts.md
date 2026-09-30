# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1

- Tên: high_latency_p95
- Severity: warning
- Duration: 5m
- Kênh thông báo: Slack (#llmops-alerts)
- SLI/SLO liên quan: fast_successful_requests (latency <= 3000ms, target 99.5%)
- Điều kiện và thời gian duy trì: p95(latency_ms) > 3000ms duy trì liên tục trong 5 phút
- Ảnh hưởng tới người dùng: Người dùng cảm nhận hệ thống phản hồi chậm trễ, giảm trải nghiệm tương tác trực tiếp với trợ lý ảo
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel "Latency percentiles and TTFT" trên dashboard để xác định độ trễ tăng ở TTFT (LLM generation) hay sau TTFT (retrieval/tool).
  2. Lọc file log `data/logs.jsonl` tìm các event `response_sent` có `latency_ms > 3000` và trích xuất `correlation_id`.
  3. Mở trace trong Langfuse cá nhân bằng `correlation_id` để kiểm tra trace waterfall, định vị span gây chậm (retrieval hay generation).
- Mitigation tạm thời: Nếu nghẽn tại span retrieval (rag_slow), chuyển sang chế độ graceful degradation (giảm số document hoặc dùng cached context); nếu nghẽn tại LLM generation, xem xét route sang model nhẹ hơn.
- Owner: Tran Trong Chinh (2A202602720)

## Alert 2

- Tên: high_error_rate
- Severity: critical
- Duration: 3m
- Kênh thông báo: Slack (#llmops-alerts-urgent)
- SLI/SLO liên quan: Guardrail error_rate_pct_max (tỉ lệ lỗi tối đa 2%)
- Điều kiện và thời gian duy trì: error_rate_pct > 2% duy trì liên tục trong 3 phút
- Ảnh hưởng tới người dùng: Người dùng nhận mã lỗi 500, request bị fail hoàn toàn, gián đoạn dịch vụ hỏi đáp
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel "Error rate and retrieval success" trên dashboard để xem tỉ lệ lỗi tổng và phân bổ `error_type`.
  2. Lọc log `data/logs.jsonl` với `event == "request_failed"` để đọc thông điệp lỗi chi tiết trong `payload.detail`.
  3. Tìm trace Langfuse tương ứng với `correlation_id` của request lỗi để xác định span bị crash và stacktrace.
- Mitigation tạm thời: Kích hoạt circuit breaker cho tool/vector store bị lỗi (chuyển sang trả lời fallback tổng quát) hoặc rollback về prompt/version trước đó nếu lỗi do format prompt.
- Owner: Tran Trong Chinh (2A202602720)

## Alert 3

- Tên: degraded_retrieval_success
- Severity: warning
- Duration: 5m
- Kênh thông báo: Slack (#llmops-alerts)
- SLI/SLO liên quan: Guardrail retrieval_success_rate_pct_min (tỉ lệ retrieval thành công >= 90%)
- Điều kiện và thời gian duy trì: tool_success_rate_pct < 90% duy trì liên tục trong 5 phút
- Ảnh hưởng tới người dùng: Thiếu ngữ cảnh bổ trợ dẫn tới câu trả lời kém chính xác, chất lượng phản hồi suy giảm (quality_score giảm)
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel "Error rate and retrieval success" và panel "Quality proxy" trên dashboard.
  2. Lọc log `data/logs.jsonl` tìm các request có `tool_success == false` hoặc exception từ retrieval service.
  3. Mở trace Langfuse kiểm tra span `retrieval` để xác định lỗi kết nối database hoặc timeout vector store.
- Mitigation tạm thời: Khởi động lại connection pool của retrieval store hoặc kích hoạt bộ nhớ đệm (fallback search) cho đến khi retrieval phục hồi.
- Owner: Tran Trong Chinh (2A202602720)
