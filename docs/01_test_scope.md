# Test Scope

## Fixed Runs

| Operation | Item | Run ID | Iterations |
|---|---|---|---:|
| ADD | D6_APE addition depth 6 | `PACKAGE22_add_100_20260825_134055_850` | 100 |
| MUL | D6_MPE multiplication depth 6 | `PACKAGE22_mul_100_20260825_142742_621` | 100 |

시험일은 2026-08-25이다. 이 저장소의 수치와 파일은 위 두 Run만 사용한다.
후속 재실행이나 다른 Run을 혼합하지 않는다.

## Logical Input

- `m1`: 32 active slots x 16bit = 512bit
- `m2`: 32 active slots x 16bit = 512bit
- total logical payload: 1024bit
- input generation: seed 42 + iteration index
- distinct inputs: 100/100

입력은 시험을 위해 생성한 값이며 실제 물류 업무 데이터가 아니다.

## Cryptographic Configuration

터미널 원자료에 기록된 구성은 다음과 같다.

- implementation: C++ / Microsoft SEAL BGV
- `poly_modulus_degree`: 16384
- `plain_modulus`: 65537
- security: 128-bit, SEAL `tc128`
- batching: enabled

## Recorded Validation

각 operation의 100회 실행은 다음 항목을 기록한다.

- 입력 payload 1024bit 조건
- c1/c2 암호문 저장과 재로딩
- 저장본·재로딩본 바이트와 SHA-256 일치
- 재로딩된 입력의 암·복호화 roundtrip
- 최종 평문 기준값과 복호화 결과 일치
- 100회 단계별 시간과 최종 통계

공개 저장소에는 `.seal` artifact 자체를 포함하지 않는다. `raw_iterations.csv`에
기록된 artifact 파일명·크기·SHA-256·일치 플래그를 확인할 수 있지만, 공개 파일만
사용하여 암호문 재로딩을 독립 재현할 수는 없다.

## Host Context

시험 당일 장비의 상세 CPU·RAM·OS 정보는 시험절차서·시험결과서 검토 대상이다.
이 공개 증빙의 핵심 원자료 6개에는 완전한 하드웨어 식별정보가 포함되지 않으므로,
공식 문서 확정 전 이 저장소가 하드웨어 정보를 독립 입증한다고 주장하지 않는다.

