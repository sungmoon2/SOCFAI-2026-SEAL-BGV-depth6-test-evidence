# CSV 필드 안내

## `summary.csv`

| 필드 | 내용 |
|---|---|
| `operation` | `ADD` 또는 `MUL` |
| `step` | `step1`~`step6` |
| `samples` | 단계별 측정 개수, 100 |
| `avg_ms` | 100개 측정값의 산술평균 |
| `p95_ms` | nearest-rank P95 |
| `min_ms` | 최솟값 |
| `max_ms` | 최댓값 |
| `limit_ms` | 평균 판정 기준 |
| `result` | 평균 기준 `PASS` 또는 `FAIL` |
| `timer_scope` | 단계별 시간에 포함된 연산 |
| `run_id` | 고정 실행 식별자 |
| `distinct_inputs` | 서로 다른 입력의 수 |
| `payload_pass` | 1024bit 입력 조건 통과 수 |
| `input_roundtrip_pass` | 입력 암·복호화 일치 확인 통과 수 |
| `final_correctness_pass` | 최종 결과 통과 수 |
| `excluded_from_step_timer` | 단계별 시간에서 제외한 작업 |

## `raw_iterations.csv`

연산별 100행을 포함한다. 주요 필드는 다음과 같이 나뉜다.

### 실행 식별과 시간

- `operation`, `iteration`, `run_id`, `field`
- `step1_total_ms`~`step6_total_ms`
- `eval_chain_ms`, `step_total_sum_ms`, `avg_step_ms`
- phase별 `_ms`와 `_tick_ns`

### 입력과 결과 확인

- `seed`, `engine_invocation_seed`
- `payload_bits`, `payload_bytes`, `payload_ok`
- `input_values`, `plaintext_result`, `decrypted_result`
- `correctness`, `result_verified_active_slots`

### 암호문 저장·재로딩 기록

- `c1_roundtrip_correct`, `c2_roundtrip_correct`
- `c1_roundtrip_verified_slots`, `c2_roundtrip_verified_slots`
- `c1_artifact_file`, `c2_artifact_file`
- 저장·재로딩 바이트 수와 SHA-256
- `c1_artifact_match`, `c2_artifact_match`
- `c1_artifact_load_success`, `c2_artifact_load_success`
- `chain_uses_loaded_inputs`

### 보조 측정값

- `encrypt_m1_ms`, `encrypt_m2_ms`, `encrypt_total_ms`
- alignment, operation, relinearize, mod-switch 시간
- `decrypt_ms`, `total_ms`, `noise_budget_bits`, `note`

## 해석 시 주의사항

- `total_ms`는 전체 시행의 보조 시간이며 단계별 평균 판정값이 아니다.
- `step_total_sum_ms`와 `eval_chain_ms`는 계산 범위가 다르다.
- ADD에 적용되지 않는 phase 값은 0 또는 빈 값일 수 있다.
- MUL의 단계별 판정에는 `stepX_total_ms`를 사용한다.
- CSV에 암호문 SHA-256이 있어도 `.seal` 파일 자체가 공개된 것은 아니다.
