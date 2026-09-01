# Publication Boundary

## Included Claims

이 공개 증빙으로 주장할 수 있는 범위는 다음과 같다.

- 지정된 두 Run이 각각 100회 기록을 포함함
- 기록된 입력 payload와 roundtrip·최종 결과 검증 상태
- step1~step6의 원시 시간과 재계산 통계
- 각 step의 100회 평균이 지정 한계 이내인지 여부
- 공개 파일이 동결 원본과 동일한지 여부
- 회차별 파생 TXT가 전체 터미널 로그의 해당 byte 구간과 동일한지 여부

## Excluded Claims

다음을 주장하지 않는다.

- 이 저장소 자체가 ETRI 공인시험 성적서 또는 인증서임
- ETRI가 저장소 내용 전체를 승인·보증·추천함
- 개인 GitHub 계정이 인제대학교 또는 ETRI 공식 계정임
- 공개 파일만으로 원 시험 실행을 완전 재현할 수 있음
- 회차별 파생 TXT가 별도의 실행 또는 추가 측정 결과임
- 공개 입력이 실제 항만·물류 협력기관 업무 데이터임
- 이 시험이 SOCFAI 운영 시스템 전체의 현재 실행 상태를 증명함
- 최댓값, P95 또는 전체 체인 시간이 공식 평균 판정 단위임

## Excluded Files

- `.seal` ciphertext artifacts
- test implementation executable, source, build products and runtime scripts
- credentials, certificates, keys, wallets and tokens
- private endpoints and deployment configuration
- HWP/HWPX/PDF/PPTX reports and administrative documents
- actual partner payloads and partner-specific mapping rules
- internal handoff prompts and private file-system provenance records

Public evidence verification and derived-file generation tools are included under `tools/`.

## Relationship to Official Documents

시험절차서·시험결과서·시험성적서는 별도의 문서 수명주기와 승인 절차를 가진다.
공개 저장소 링크를 공식 문서에 넣을 때에는 최종 공개 commit 전체 SHA와 tag를
기록하고, 문서의 판정 문구와 저장소 README가 일치하는지 다시 확인한다.
