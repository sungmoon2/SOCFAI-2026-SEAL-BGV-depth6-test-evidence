# 출처 및 무결성

## 동결 원본

- 시험일: 2026-08-25
- 원본 ZIP: `인제대학교_ETRI_공인인증시험_실행원자료_260825.zip`
- 크기: `339,295바이트`
- SHA-256: `D9EED4CC6351C489F3971CA7C8147FDE261A9B0491A5C2C6B4D4A1778F07D402`
- MD5: `465AA5662AF109331DE433C44C672387`

원본 ZIP은 공개하지 않는다. ZIP 안에서 다음 두 실행의
`terminal_output.txt`, `summary.csv`, `raw_iterations.csv`만 바이트 변경 없이
추출했다.

- ADD: `PACKAGE22_add_100_20260825_134055_850`
- MUL: `PACKAGE22_mul_100_20260825_142742_621`

## 무결성 확인 파일과 도구

- `evidence/2026-08-25/FILE_MANIFEST.csv`: 동결 파일 6개의 실행 식별자,
  경로, 크기와 SHA-256
- `evidence/2026-08-25/SHA256SUMS.txt`: 동결 파일 6개의 표준 SHA-256 목록
- `evidence/2026-08-25/ITERATION_MANIFEST.csv`: 회차별 TXT 200개의 원본 경로,
  원본 SHA-256, 바이트 구간, 크기와 개별 SHA-256
- `tools/verify_hashes.ps1`: 동결 파일 6개의 크기와 SHA-256 확인
- `tools/verify_evidence.py`: 동결 파일, 회차별 TXT, 통계, 판정과 정합성 확인
- `tools/split_iterations.py`: 전체 터미널 로그에서 회차별 TXT 생성

## 원자료와 회차별 열람본

`ADD/`와 `MUL/` 바로 아래의 동결 파일 6개는 수정하거나 후속 재실행값으로
교체하지 않는다.

각 `iteration_views/`의 TXT는 원본 `terminal_output.txt`의 연속 바이트 구간과
정확히 일치해야 한다. 이 파일들은 탐색을 돕기 위한 열람본이며 원자료를
대체하지 않는다.

오류 정정이나 새 자료 추가가 필요한 경우에는 기존 원자료와 태그를 유지하고,
새 리비전 또는 날짜로 구분한다. 공식 문서에서 참조하는 커밋 SHA와 태그는
검증 없이 바꾸지 않는다.

## 로그에 남은 경로

ADD·MUL `terminal_output.txt`의 마지막에는
`C:\SOCFAI_2026_CERT_TEST\...` 형식의 결과 경로가 한 줄 남아 있다.
사용자 프로필, 계정명 또는 인증정보는 포함하지 않는다. 원본 바이트를 보존하기
위해 해당 경로를 삭제하거나 바꾸지 않았다.
