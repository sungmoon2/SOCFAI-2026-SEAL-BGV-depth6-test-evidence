# Data Dictionary

## `summary.csv`

| 필드 | 의미 |
|---|---|
| `operation` | `ADD` 또는 `MUL` |
| `step` | `step1`~`step6` |
| `samples` | 단계별 측정 개수, 100 |
| `avg_ms` | 100개 측정값의 산술평균 |
| `p95_ms` | nearest-rank P95 |
| `min_ms` | 최솟값 |
| `max_ms` | 최댓값 |
| `limit_ms` | 평균 판정 한계 |
| `result` | 평균 기준 `PASS` 또는 `FAIL` |
| `timer_scope` | 각 step에 포함된 연산 범위 |
| `run_id` | 고정 실행 식별자 |
| `distinct_inputs` | 서로 다른 입력 시행 수 |
| `payload_pass` | 1024bit payload 조건 통과 수 |
| `input_roundtrip_pass` | 입력 roundtrip 통과 수 |
| `final_correctness_pass` | 최종 결과 통과 수 |
| `excluded_from_step_timer` | 판정 타이머 제외 작업 |

## `raw_iterations.csv`

CSV는 operation별 100행을 포함한다. 필드는 다음 기능군으로 나뉜다.

### Identity and timing

- `operation`, `iteration`, `run_id`, `field`
- `step1_total_ms`~`step6_total_ms`
- `eval_chain_ms`, `step_total_sum_ms`, `avg_step_ms`
- phase별 `_ms`와 `_tick_ns`

### Input and correctness

- `seed`, `engine_invocation_seed`
- `payload_bits`, `payload_bytes`, `payload_ok`
- `input_values`, `plaintext_result`, `decrypted_result`
- `correctness`, `result_verified_active_slots`

### Ciphertext roundtrip trace

- `c1_roundtrip_correct`, `c2_roundtrip_correct`
- `c1_roundtrip_verified_slots`, `c2_roundtrip_verified_slots`
- `c1_artifact_file`, `c2_artifact_file`
- 저장·재로딩 byte 수와 SHA-256
- `c1_artifact_match`, `c2_artifact_match`
- `c1_artifact_load_success`, `c2_artifact_load_success`
- `chain_uses_loaded_inputs`

### Supporting measurements

- `encrypt_m1_ms`, `encrypt_m2_ms`, `encrypt_total_ms`
- phase별 alignment, operation, relinearize, mod-switch 시간
- `decrypt_ms`, `total_ms`, `noise_budget_bits`, `note`

## Interpretation Cautions

- `total_ms`는 전체 시행 보조 시간이며 step 평균 판정값이 아니다.
- `step_total_sum_ms`와 `eval_chain_ms`는 서로 다른 집계 의미를 가진다.
- ADD의 phase 중 적용되지 않는 항목은 0 또는 빈 값일 수 있다.
- MUL의 step 판정에는 phase 합성값인 `stepX_total_ms`를 사용한다.
- 원자료에 artifact SHA-256이 있어도 `.seal` 파일 자체가 공개됐다는 뜻은 아니다.

