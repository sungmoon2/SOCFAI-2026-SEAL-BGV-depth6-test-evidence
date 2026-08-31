# SOCFAI 2026 SEAL BGV Depth-6 Test Evidence

2026-08-25에 수행한 SOCFAI Microsoft SEAL BGV 기반 depth-6 덧셈·곱셈
시험의 고정 실행 증빙을 제공한다.

> 이 저장소는 시험 당일 실행 원자료의 공개 가능한 부분을 제공하는 증빙
> 패키지이다. ETRI가 발급한 최종 시험결과서·시험성적서가 아니며,
> 인제대학교 또는 ETRI의 공식 GitHub 저장소라고 주장하지 않는다.

## Test Scope

| 항목 | 내용 |
|---|---|
| 시험일 | 2026-08-25 |
| 구현 | C++ / Microsoft SEAL BGV |
| 덧셈 항목 | D6_APE, encrypted addition depth 6 |
| 곱셈 항목 | D6_MPE, encrypted multiplication depth 6 |
| 반복 | operation별 100회 |
| 입력 생성 | seed 42 + iteration index |
| 논리 입력 | m1 512bit + m2 512bit = 1024bit |
| poly modulus degree | 16384 |
| plain modulus | 65537 |
| 보안 설정 | 128-bit, SEAL `tc128` |
| batching | enabled |

고정 Run ID:

- ADD: `PACKAGE22_add_100_20260825_134055_850`
- MUL: `PACKAGE22_mul_100_20260825_142742_621`

이후 재실행 결과나 다른 Run의 수치를 이 저장소의 고정 증빙과 혼합하지 않는다.

## Judgement Criterion

판정 단위는 **step1부터 step6까지 각 단계의 100회 산술평균**이다.

- ADD: 각 step의 100회 평균이 `1.000000 ms` 이하
- MUL: 각 step의 100회 평균이 `20.000000 ms` 이하

P95·최솟값·최댓값은 분포를 설명하는 기술통계이며 PASS 판정 기준이 아니다.
`eval_chain_ms`는 연속 체인 시간의 참고값이며 공식 step별 평균 판정값이 아니다.

## Frozen Result Summary

| Step | ADD avg_ms | ADD limit | ADD | MUL avg_ms | MUL limit | MUL |
|---|---:|---:|---|---:|---:|---|
| step1 | 0.134355 | 1.000000 | PASS | 18.541602 | 20.000000 | PASS |
| step2 | 0.108307 | 1.000000 | PASS | 18.080207 | 20.000000 | PASS |
| step3 | 0.099714 | 1.000000 | PASS | 18.084798 | 20.000000 | PASS |
| step4 | 0.098049 | 1.000000 | PASS | 17.526507 | 20.000000 | PASS |
| step5 | 0.096314 | 1.000000 | PASS | 16.651580 | 20.000000 | PASS |
| step6 | 0.096734 | 1.000000 | PASS | 15.893276 | 20.000000 | PASS |

결과: ADD `6/6 within limit`, MUL `6/6 within limit`.

## Measurement Boundary

- ADD step timer: `Evaluator::add_inplace` only
- MUL step timer: operand alignment + multiply + relinearize + result mod-switch
- step timer 제외: 입력 암호화, 암호문 저장·재로딩, 복호화 정합성 확인,
  최종 결과 확인, 통계 계산, 터미널·파일 출력
- 단계 사이 복호화: 없음

상세 설명은 [`docs/02_measurement_and_judgement.md`](docs/02_measurement_and_judgement.md)를
참조한다.

## Evidence Files

```text
evidence/2026-08-25/
  README.md
  FILE_MANIFEST.csv
  SHA256SUMS.txt
  ADD/
    terminal_output.txt
    summary.csv
    raw_iterations.csv
  MUL/
    terminal_output.txt
    summary.csv
    raw_iterations.csv
```

회차별 열람용 파생본은 다음 위치에 둔다.

```text
derived/2026-08-25/
  README.md
  ITERATION_MANIFEST.csv
  ADD/iteration_001.txt ... iteration_100.txt
  MUL/iteration_001.txt ... iteration_100.txt
```

파일 역할:

1. `summary.csv`: step별 통계와 판정을 빠르게 확인한다.
2. `terminal_output.txt`: 1~100회 전체 터미널 출력과 최종 집계를 확인한다.
3. `raw_iterations.csv`: 100개 원시값으로 통계를 독립 재계산한다.
4. `FILE_MANIFEST.csv`·`SHA256SUMS.txt`: 공개 파일의 크기와 SHA-256을 확인한다.
5. `derived/`: 전체 터미널 로그에서 바이트 단위로 추출한 회차별 열람용 파생본이다.

## Verification

Windows PowerShell에서 파일 무결성을 확인한다.

```powershell
powershell -ExecutionPolicy Bypass -File tools/verify_hashes.ps1
```

Python 3 표준 라이브러리만 사용하여 해시·100회 통계·판정·검증 플래그를
확인한다.

```text
python tools/verify_evidence.py
python tools/split_iterations.py
```

두 명령은 원자료를 수정하지 않는다.

## Repository Guide

- [`docs/01_test_scope.md`](docs/01_test_scope.md): 시험 범위와 입력·암호 설정
- [`docs/02_measurement_and_judgement.md`](docs/02_measurement_and_judgement.md): 타이머와 판정 정의
- [`docs/03_data_dictionary.md`](docs/03_data_dictionary.md): CSV 핵심 필드
- [`docs/04_provenance_and_integrity.md`](docs/04_provenance_and_integrity.md): Run·ZIP·해시 추적성
- [`docs/05_publication_boundary.md`](docs/05_publication_boundary.md): 공개 포함·제외와 주장 한계

## Verification and Reproduction Boundary

이 저장소로 공개 파일 해시, 100회 통계, 평균 판정과 기록된 검증 플래그를
확인할 수 있다. 실행파일·소스코드·`.seal` artifact는 포함하지 않으므로 시험을
독립적으로 재실행하거나 암호문을 다시 로드하는 실행 재현 패키지는 아니다.

공개 입력은 `seed 42 + iteration index`로 생성한 시험 데이터이다. 실제 협력기관
물류 payload를 포함한다고 주장하지 않는다.

## License and Reuse

Public 열람 가능성과 재사용 허가는 별개이다. 이 저장소에는 권리 주체가
승인한 명시적 재사용 라이선스가 아직 포함되지 않았다. 라이선스가 추가되기
전까지 저장소 내용을 자유 재사용 가능한 오픈소스로 해석하지 않는다.

자세한 비보증·권리 경계는 [`NOTICE.md`](NOTICE.md)를 참조한다.
