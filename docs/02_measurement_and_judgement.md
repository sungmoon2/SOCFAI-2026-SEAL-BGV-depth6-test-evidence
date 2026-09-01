# 측정 및 판정 기준

## 판정 단위

step1부터 step6까지 각 단계에서 100개 측정값의 산술평균을 계산하고,
연산별 기준과 비교한다.

- ADD: 6개 단계의 평균이 각각 `1.000000 ms` 이하
- MUL: 6개 단계의 평균이 각각 `20.000000 ms` 이하

6개 단계가 모두 기준 이내이면 `6/6 within limit`으로 기록한다.

## 통계값

각 단계에는 다음 통계가 기록된다.

- `avg_ms`: 100개 값의 산술평균
- `min_ms`: 최솟값
- `max_ms`: 최댓값
- `p95_ms`: 오름차순으로 정렬한 100개 값 중 95번째 값(nearest-rank)

판정에는 `avg_ms`만 사용한다. P95·최소·최대는 측정값의 분포를 확인하기
위한 값이다. 따라서 개별 최댓값이 기준을 넘더라도 평균이 기준 이내이면
평균 기준 판정은 PASS다.

## ADD 측정 범위

ADD의 각 단계에서는 `Evaluator::add_inplace` 실행 시간만 측정한다.

다음 작업은 단계별 시간에 포함하지 않는다.

- 입력 암호화
- 암호문 저장·재로딩
- 입력 암·복호화 일치 확인
- 평문 기준값 계산과 최종 복호화 결과 확인
- 통계 계산과 tick 변환
- 터미널·CSV 출력

단계 사이에 복호화를 수행하지 않는다.

## MUL 측정 범위

MUL의 각 단계별 `total_ms`는 다음 작업을 합한 시간이다.

1. operand alignment
2. multiply
3. relinearize
4. result mod-switch

입력 암호화, 암호문 저장·재로딩, 입력·최종 결과 확인, 통계 계산과 출력은
단계별 시간에 포함하지 않는다. 단계 사이에 복호화를 수행하지 않는다.

## 전체 체인 시간

`eval_chain_ms`는 step1 시작부터 step6 종료까지의 연속 경과시간이다.
단계별 100회 평균을 판정하는 값이 아니며, 단계별 평균과 합산해 판정하지 않는다.

## 확인할 필드

- 단계별 판정: `summary.csv`의 `avg_ms`, `limit_ms`, `result`
- 원시값 재계산: `raw_iterations.csv`의 `step1_total_ms`~`step6_total_ms`
- 터미널 표시: `terminal_output.txt`의 final 100-run statistical summary
