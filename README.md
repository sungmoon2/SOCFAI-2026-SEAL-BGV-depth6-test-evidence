# SOCFAI 2026 SEAL BGV Depth-6 Test Evidence

2026-08-25에 수행한 Microsoft SEAL BGV 기반 depth-6 덧셈·곱셈 시험의
공개 가능한 실행 기록을 정리한 저장소다.

> 이 저장소는 시험 당일 실행 기록을 확인하기 위한 자료다. ETRI가 발급한
> 시험결과서·시험성적서가 아니며, 인제대학교 또는 ETRI의 공식 저장소도 아니다.

## 빠르게 확인하기

| 확인할 내용 | ADD | MUL |
|---|---|---|
| 단계별 통계와 판정 | [summary.csv](evidence/2026-08-25/ADD/summary.csv) | [summary.csv](evidence/2026-08-25/MUL/summary.csv) |
| 1~100회 전체 터미널 로그 | [terminal_output.txt](evidence/2026-08-25/ADD/terminal_output.txt) | [terminal_output.txt](evidence/2026-08-25/MUL/terminal_output.txt) |
| 100회 원시 측정값 | [raw_iterations.csv](evidence/2026-08-25/ADD/raw_iterations.csv) | [raw_iterations.csv](evidence/2026-08-25/MUL/raw_iterations.csv) |
| 회차별 터미널 로그 | [iteration_views/](evidence/2026-08-25/ADD/iteration_views/) | [iteration_views/](evidence/2026-08-25/MUL/iteration_views/) |

회차별 TXT는 별도로 실행한 결과가 아니다. 각 `terminal_output.txt`에서
해당 회차의 `BEGIN ... ITERATION`부터 `END ... ITERATION`까지를 바이트 단위로
그대로 추출한 열람용 파일이다.

## 시험 개요

| 항목 | 내용 |
|---|---|
| 시험일 | 2026-08-25 |
| 구현 | C++ / Microsoft SEAL BGV |
| 덧셈 | D6_APE, encrypted addition depth 6 |
| 곱셈 | D6_MPE, encrypted multiplication depth 6 |
| 반복 횟수 | 연산별 100회 |
| 입력 생성 | seed 42 + iteration index |
| 논리 입력 | m1 512bit + m2 512bit = 1024bit |
| `poly_modulus_degree` | 16384 |
| `plain_modulus` | 65537 |
| 보안 설정 | 128-bit, SEAL `tc128` |
| batching | enabled |

고정 실행 식별자:

- ADD: `PACKAGE22_add_100_20260825_134055_850`
- MUL: `PACKAGE22_mul_100_20260825_142742_621`

이 저장소의 수치와 파일은 위 두 실행만을 기준으로 한다. 이후 재실행 결과를
섞거나 기존 값을 교체하지 않는다.

## 판정 기준

판정 단위는 step1부터 step6까지 **각 단계의 100회 산술평균**이다.

- ADD: 각 단계의 평균이 `1.000000 ms` 이하
- MUL: 각 단계의 평균이 `20.000000 ms` 이하

P95·최솟값·최댓값은 분포를 확인하기 위한 통계이며 판정 기준이 아니다.
`eval_chain_ms`도 전체 연속 실행 시간의 참고값으로만 사용한다.

## 결과 요약

| Step | ADD avg_ms | ADD 기준 | 판정 | MUL avg_ms | MUL 기준 | 판정 |
|---|---:|---:|---|---:|---:|---|
| step1 | 0.134355 | 1.000000 | PASS | 18.541602 | 20.000000 | PASS |
| step2 | 0.108307 | 1.000000 | PASS | 18.080207 | 20.000000 | PASS |
| step3 | 0.099714 | 1.000000 | PASS | 18.084798 | 20.000000 | PASS |
| step4 | 0.098049 | 1.000000 | PASS | 17.526507 | 20.000000 | PASS |
| step5 | 0.096314 | 1.000000 | PASS | 16.651580 | 20.000000 | PASS |
| step6 | 0.096734 | 1.000000 | PASS | 15.893276 | 20.000000 | PASS |

ADD와 MUL 모두 6개 단계의 평균이 기준 이내다.

## 측정 범위

- ADD: 각 단계에서 `Evaluator::add_inplace` 실행 시간만 측정
- MUL: operand alignment, multiply, relinearize, result mod-switch를 합산
- 단계별 시간에서 제외: 입력 암호화, 암호문 저장·재로딩, 입력 암·복호화 일치 확인,
  최종 결과 확인, 통계 계산, 터미널·파일 출력
- 단계 사이 복호화: 없음

자세한 내용은 [측정 및 판정 기준](docs/02_measurement_and_judgement.md)에 정리했다.

## 저장소 구조

```text
evidence/2026-08-25/
  README.md
  FILE_MANIFEST.csv
  SHA256SUMS.txt
  ITERATION_MANIFEST.csv
  ADD/
    summary.csv
    terminal_output.txt
    raw_iterations.csv
    iteration_views/
      iteration_001.txt ... iteration_100.txt
  MUL/
    summary.csv
    terminal_output.txt
    raw_iterations.csv
    iteration_views/
      iteration_001.txt ... iteration_100.txt

docs/
  01_test_scope.md
  02_measurement_and_judgement.md
  03_data_dictionary.md
  04_provenance_and_integrity.md
  05_publication_boundary.md

tools/
  verify_hashes.ps1
  verify_evidence.py
  split_iterations.py
```

최상위 폴더의 역할은 다음과 같다.

- `evidence/`: 시험 당일 동결 파일과 그 파일에서 추출한 회차별 열람본
- `docs/`: 시험 범위, 판정 방법, CSV 필드, 출처와 공개 범위
- `tools/`: 해시·통계 검증과 회차별 열람본 생성 도구

## 파일 설명

- `summary.csv`: 단계별 평균·P95·최소·최대와 판정
- `terminal_output.txt`: 1~100회 전체 터미널 출력과 최종 집계
- `raw_iterations.csv`: 100회 입력값, 정합성 결과와 단계별 원시 측정값
- `FILE_MANIFEST.csv`: 동결 파일 6개의 경로·크기·SHA-256
- `SHA256SUMS.txt`: 동결 파일 6개의 표준 SHA-256 목록
- `ITERATION_MANIFEST.csv`: 회차별 TXT의 원본 경로, 바이트 구간, 크기와 SHA-256

## 검증 방법

저장소 루트에서 다음 명령을 실행한다.

```powershell
powershell -ExecutionPolicy Bypass -File tools/verify_hashes.ps1
python tools/verify_evidence.py
```

두 명령은 파일을 수정하지 않는다. 첫 번째 명령은 동결 파일 6개의 크기와
SHA-256을 확인한다. 두 번째 명령은 동결 파일, 회차별 TXT 200개, 100회 통계,
판정과 기록된 정합성 값을 함께 확인한다.

회차별 TXT와 `ITERATION_MANIFEST.csv`를 다시 만들 때에만 다음 명령을 사용한다.

```powershell
python tools/split_iterations.py
```

이 명령은 `iteration_views/`와 `ITERATION_MANIFEST.csv`만 다시 생성하며,
동결 파일 6개는 수정하지 않는다. 실행 후 `verify_evidence.py`로 일치 여부를
다시 확인한다.

## 세부 문서

- [시험 범위](docs/01_test_scope.md)
- [측정 및 판정 기준](docs/02_measurement_and_judgement.md)
- [CSV 필드 안내](docs/03_data_dictionary.md)
- [출처 및 무결성](docs/04_provenance_and_integrity.md)
- [공개 범위](docs/05_publication_boundary.md)

## 공개 범위와 한계

이 저장소에서는 공개 파일의 해시, 100회 통계, 평균 기준 판정, 기록된 정합성
값과 회차별 TXT의 원본 일치 여부를 확인할 수 있다.

시험 구현 실행파일·소스코드와 `.seal` 암호문 파일은 포함하지 않는다. 따라서
시험을 독립적으로 다시 실행하거나 암호문을 다시 로드하는 재현 패키지는 아니다.
공개 입력은 시험용으로 생성한 값이며 실제 협력기관의 물류 데이터를 포함하지 않는다.

## 이용 범위

저장소를 공개한 것과 자료의 복제·수정·재배포를 허용하는 것은 별개다.
현재 별도의 재사용 라이선스는 부여하지 않았다. 자세한 내용은
[NOTICE.md](NOTICE.md)를 확인한다.
