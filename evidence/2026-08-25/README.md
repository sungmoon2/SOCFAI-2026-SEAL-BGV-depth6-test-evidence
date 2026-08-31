# Frozen Evidence: 2026-08-25

이 디렉터리는 다음 두 고정 Run의 공개 원자료를 보존한다.

- ADD: `PACKAGE22_add_100_20260825_134055_850`
- MUL: `PACKAGE22_mul_100_20260825_142742_621`

`ADD/`와 `MUL/`의 파일은 시험 당일 동결 ZIP에서 byte 변경 없이 추출한다.

## Reading Order

1. `ADD/summary.csv`, `MUL/summary.csv`
2. `ADD/terminal_output.txt`, `MUL/terminal_output.txt`
3. `ADD/raw_iterations.csv`, `MUL/raw_iterations.csv`
4. `FILE_MANIFEST.csv`, `SHA256SUMS.txt`

## File Roles

- `terminal_output.txt`: 1~100회 전체 출력과 최종 통계
- `summary.csv`: step1~step6의 평균·P95·최소·최대·기준·판정
- `raw_iterations.csv`: 100회 입력·정합성·암호문 추적·원시 단계 시간

판정은 각 step의 100회 평균을 사용한다. P95·최소·최대 및 `eval_chain_ms`는
기술통계 또는 참고값이다.

이 파일들은 ETRI 최종 시험결과서·시험성적서가 아니다. 원본을 수정하거나 후속
재실행값으로 교체하지 않는다.
