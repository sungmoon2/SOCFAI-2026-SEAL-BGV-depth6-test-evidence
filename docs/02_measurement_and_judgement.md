# Measurement and Judgement

## Judgement Unit

step1부터 step6까지 각 단계에서 100개 측정값의 산술평균을 계산한다. 각 step의
평균을 operation별 한계값과 비교한다.

- ADD: 모든 step 평균이 `1.000000 ms` 이하
- MUL: 모든 step 평균이 `20.000000 ms` 이하

6개 step이 모두 한계 이내일 때 `6/6 within limit`으로 기록한다.

## Descriptive Statistics

각 step에 대해 다음 값을 기록한다.

- Average: 100개 값의 산술평균
- Minimum: 100개 값 중 최솟값
- Maximum: 100개 값 중 최댓값
- P95: 오름차순 정렬한 100개 값 중 95번째 값, nearest-rank 방식

P95·Minimum·Maximum은 분포를 설명하는 기술통계이다. PASS 판정은 Average만
사용한다. 따라서 개별 측정의 `max_ms`가 한계값을 넘는 것만으로 평균 기준
판정이 실패하지 않는다.

## ADD Timer Scope

ADD의 각 step 타이머는 `Evaluator::add_inplace`만 측정한다.

제외 항목:

- 입력 암호화
- 암호문 저장·재로딩
- 입력 roundtrip 확인
- 최종 평문 계산과 복호화 결과 확인
- 통계 계산과 tick 변환
- 터미널·CSV 파일 출력

단계 사이 복호화는 수행하지 않는다.

## MUL Timer Scope

MUL의 각 step `total_ms`는 다음 phase의 합성 측정 범위다.

1. operand alignment
2. multiply
3. relinearize
4. result mod-switch

입력 암호화, 암호문 저장·재로딩, 입력·최종 정합성 검증, 통계 및 출력은 각
step 타이머 밖이다. 단계 사이 복호화는 수행하지 않는다.

## Reference Chain Time

`eval_chain_ms`는 step1 시작부터 step6 종료까지의 연속 경과시간을 나타내는
참고값이다. step별 100회 평균 판정과 교체하거나 합산 판정값으로 사용하지 않는다.

## Source Fields

- 판정 표: `summary.csv`의 `avg_ms`, `limit_ms`, `result`
- 원시 재계산: `raw_iterations.csv`의 `step1_total_ms`부터 `step6_total_ms`
- 화면 기록: `terminal_output.txt`의 final 100-run statistical summary

