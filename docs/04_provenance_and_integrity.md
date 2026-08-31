# Provenance and Integrity

## Frozen Source Package

- 시험일: 2026-08-25
- 원본명: `인제대학교_ETRI_공인인증시험_실행원자료_260825.zip`
- 크기: `339,295 bytes`
- SHA-256: `D9EED4CC6351C489F3971CA7C8147FDE261A9B0491A5C2C6B4D4A1778F07D402`
- MD5: `465AA5662AF109331DE433C44C672387`

원본 ZIP 자체는 이 공개 저장소에 포함하지 않는다. `evidence/2026-08-25/ADD`와
`MUL`의 6개 파일만 ZIP entry의 byte를 변경하지 않고 추출한다.

## Frozen Run IDs

- ADD: `PACKAGE22_add_100_20260825_134055_850`
- MUL: `PACKAGE22_mul_100_20260825_142742_621`

## Integrity Files

- `evidence/2026-08-25/FILE_MANIFEST.csv`: operation, Run ID, 경로, 크기, SHA-256
- `evidence/2026-08-25/SHA256SUMS.txt`: 표준 해시 점검용 목록
- `tools/verify_hashes.ps1`: 크기·SHA-256 확인
- `tools/verify_evidence.py`: 해시, Run ID, 행 수, 통계와 검증 플래그 확인

## Immutable Evidence Rule

최초 공개 commit 이후 `terminal_output.txt`, `summary.csv`,
`raw_iterations.csv`를 수정하거나 더 좋은 후속 수치로 교체하지 않는다.

오류 정정이나 추가 자료가 필요하면 다음을 따른다.

1. 기존 evidence와 tag를 유지한다.
2. 새 날짜 또는 revision 디렉터리에 새 자료를 추가한다.
3. 변경 이유와 원본 해시를 별도 문서에 기록한다.
4. 결과서가 참조하는 commit SHA와 tag를 임의로 바꾸지 않는다.

## Path Disclosure

ADD/MUL `terminal_output.txt` 마지막에는 각각
`C:\SOCFAI_2026_CERT_TEST\...` 결과 경로가 한 줄 기록되어 있다. 사용자 프로필,
계정명 또는 credential을 포함하지 않는다. 원본 무결성을 위해 삭제·치환하지 않는다.
