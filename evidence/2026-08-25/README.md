# 2026-08-25 시험 증빙

이 폴더에는 다음 두 고정 실행의 공개 가능한 파일을 보관한다.

- ADD: `PACKAGE22_add_100_20260825_134055_850`
- MUL: `PACKAGE22_mul_100_20260825_142742_621`

## 확인 순서

| 순서 | 확인 내용 | ADD | MUL |
|---:|---|---|---|
| 1 | 단계별 통계와 판정 | [summary.csv](ADD/summary.csv) | [summary.csv](MUL/summary.csv) |
| 2 | 1~100회 전체 로그 | [terminal_output.txt](ADD/terminal_output.txt) | [terminal_output.txt](MUL/terminal_output.txt) |
| 3 | 100회 원시 측정값 | [raw_iterations.csv](ADD/raw_iterations.csv) | [raw_iterations.csv](MUL/raw_iterations.csv) |
| 4 | 회차별 로그 | [iteration_views/](ADD/iteration_views/) | [iteration_views/](MUL/iteration_views/) |

## 원자료와 회차별 열람본

`ADD/`와 `MUL/` 바로 아래의 `summary.csv`, `terminal_output.txt`,
`raw_iterations.csv`는 시험 당일 동결 ZIP에서 바이트 변경 없이 추출한 파일이다.

`iteration_views/`의 TXT는 별도 실행 결과가 아니다. 각 `terminal_output.txt`에서
해당 회차의 시작부터 끝까지를 바이트 단위로 추출한 열람용 파일이다.
`ITERATION_MANIFEST.csv`에서 원본 경로, 바이트 구간, 크기와 SHA-256을 확인할 수 있다.

## 무결성 파일

- `FILE_MANIFEST.csv`: 동결 파일 6개의 경로·크기·SHA-256
- `SHA256SUMS.txt`: 동결 파일 6개의 표준 SHA-256 목록
- `ITERATION_MANIFEST.csv`: 회차별 TXT 200개의 원본 연결과 SHA-256

판정은 step1부터 step6까지 각 단계의 100회 평균을 사용한다. P95·최소·최대와
`eval_chain_ms`는 참고 통계다.

이 폴더의 파일은 ETRI가 발급한 시험결과서·시험성적서가 아니다. 동결 파일을
후속 재실행값으로 교체하지 않는다.
