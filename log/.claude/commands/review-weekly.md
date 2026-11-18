주간 계획을 검토하고 다음 주 실행 범위를 정한다. `templates/planning.md`와 `templates/weekly-adjust.md`를 읽는다. standup(`/plan-daily`)의 짧은 조정과 주차별 상태를 공유한다. 일요일에도 기본 대상은 다음 주이며, 사용자가 지정한 주가 있으면 그 주를 우선한다. 날짜는 `CLAUDE.md`의 하루 경계를 따른다.

## 실행 모드

- 기본 `/review-weekly`: 로컬 작업 목록·일지·inbox를 근거로 `templates/planning.md`의 주간 재계획을 수행하고 주간 요약을 로컬에 저장한다. Notion 게시는 선택이며 같은 문서의 게시 절차를 따른다. 아래 Career Review는 실행하지 않는다.
- `/review-weekly career`: 아래 기존 경험 정리 절차를 수행한다. 주간 계획 변경과 별개이며 자동으로 재계획을 실행하지 않는다.

## Career Review

주간 Career Review를 수행하고 Portfolio Seed 후보를 추출한다.

이 명령은 개발 경험 정리 명령이다.

## Input Sources

다음 순서로 데이터를 읽는다. WHY(의사결정 이유·문제 원인·성과)는 Obsidian이 1순위다. 주 범위는 실행일이 속한 주(월~일, ISO 주)로 잡고 GitHub·estimates 필터에 일관되게 적용한다.

**WHY 1순위 — Obsidian:** `workspace/inbox.md`(미마감 당일치만), `workspace/sessions`의 세션 증류 노트(한 주를 지탱하는 지속 출처), `workspace/daily`.

1. 최근 Daily Logs — 한 주간의 기록 원문
2. 로컬 Daily Log의 Work Item 후보와 기존 Notion Work Items — 게시된 항목은 중복 생성하지 않고 연결한다
3. Trouble Records — 문제 해결 기록
4. GitHub (수집 규칙 → `collectors/github.md`, 미설정이면 건너뛰고 Evidence 없음으로 표시)
   - 이번 주 머지/생성된 PR
   - 이번 주 변경된 Issue
   - 이번 주 Commit 목록

## 작업

### 1. Work Item 정리

흩어진 Daily 기록을 Work Item 기준으로 통합한다.

### 2. Evidence 연결

각 Work Item에 아래 Evidence를 가능한 한 모두 연결한다.
- GitHub PR 링크
- GitHub Issue 번호
- 설계 문서 링크
- Trouble Record

Evidence가 없는 항목은 "Evidence 없음"으로 표시한다.

### 3. Portfolio Seed 후보 추출

아래 구조를 기준으로 후보를 만든다. 완성 후보는 넷이 다 찬 것이다.

Portfolio Seed 필수 항목:
- Problem: 어떤 문제 또는 과제가 있었나
- Action: 내가 한 행동 (의사결정 포함)
- Result: 결과 또는 배운 점
- Evidence: PR / Issue / 문서 중 하나 이상

Evidence(PR/Issue/문서 중 하나 이상)는 후보 생성의 하드 게이트다. Evidence가 없으면 후보로 만들지 않고 Review Needed로 남긴다. Evidence는 있지만 Problem/Action/Result 중 일부가 비면 후보는 만들되 Status를 Draft 또는 Review Needed로 두고 빈 섹션을 `(추후 보완)`으로 채운다. 넷이 다 차면 Ready로 승격한다.

## 규칙

- GitHub는 Evidence로만 사용한다. 의도, 원인, 성과를 추측하는 근거로 쓰지 않는다.
- Obsidian(inbox·세션 증류)·Daily Log·Notion Work Item에 없는 내용은 만들지 않는다.
- 부족한 정보는 구체적인 질문으로 남긴다.
- 사용자 미리보기 승인 없이 Notion에 쓰지 않는다(`collectors/notion.md`).

## 출력 형식

# Weekly Review — {날짜 범위}

## 시간 추정 정확도

통계에 쓸 행은 아래 기준으로 고른다(`templates/time-recording.md`에서 옮김).
- 숫자로 확인되는 직접 작업 소요와 비교 가능한 작업 범위가 있는 기록만 수치 통계·예측의 근거로 쓴다. 기존 행도 비고와 원본 근거로 이를 확인할 수 있을 때만 사용한다.
- 미진행·미측정·병렬 배분 불명·세션/AI 경과 시간·중복 총계·범위 불일치는 제외한다. 합산 금지로 표시된 기록은 합하지 않는다. 정정 행이 있으면 원본과 이중 집계하지 않는다.
- “약 40분”, “1~2시간” 같은 추정은 참고 범위로만 표시한다. 정확한 평균·편차 계산에 섞지 않는다. AI 예상과 사용자 예상의 정확도를 분리한다.
- 표본 수와 제외 이유를 짧게 밝힌다. 적합한 기록이 없으면 “비교 가능한 실측 없음”으로 표시하고 예측을 새 추정으로 명시한다. 완료 건수와 실제 투입 시간은 별개다.
이번 주 `workspace/estimates.md`(시간 추정 누적 로그)에서 이번 주 날짜 행을 추려 대략적인 카테고리로 묶어 요약한다.
예: "개발 작업은 평균 1.5배 과소 추정, 회의는 비교적 정확"
카테고리는 고정 목록이 아니라 그 주 데이터를 보고 자연스럽게 묶는다.
데이터가 적으면 통계적 정확성을 가장하지 않고 서술형으로만 요약한다.
이번 기록이 없는 주는 이 섹션을 생략한다.

## Work Item 정리

### {Work Item 이름}
- 상태:
- 관련 PR:
- 요약:

## Trouble 보강 후보

기존 Trouble Record 중 보강이 필요한 항목.
- {제목}: 부족한 부분

## Portfolio Seed 후보

### {제목}
- Problem:
- Action:
- Result:
- Evidence:

## Evidence 연결

Evidence가 없거나 약한 Work Item 목록.

## 부족한 정보 / 질문

Portfolio Seed 생성을 위해 필요한 질문 목록.
- {Work Item}: {질문}

## Notion 저장

Notion 접근·인증·relation 규칙은 `collectors/notion.md`, collection ID는 `config/notion.md`를 따른다. 저장 전에 저장 대상(Portfolio Seed 후보, 갱신할 Work Item, Trouble 항목)을 미리보기로 보여주고 사용자 승인을 받는다. Notion이 미설정이면 `collectors/notion.md`대로 건너뛰고 아래 로컬 포트폴리오 저장만 한 뒤 미게시로 알린다.

### Portfolio Seed DB (collection ID → `config/notion.md`)

| Property | 값 |
|---|---|
| Title (title) | Portfolio Seed 제목 |
| Status | Draft / Review Needed / Ready |
| Date | 해당 작업 날짜 |
| Evidence URL (url) | 대표 PR / Issue 링크 |

본문:
```
## Problem
## Action
## Result
```

### Work Item 생성·갱신 (collection ID → `config/notion.md`)

일상 마감에서 로컬 일지에 남긴 경험 후보도 검토한다. 기존 항목이 있으면 연결·보강하고, 없으면 사용자 승인 후 Name, Status, Type, Date와 근거가 있는 PR/Issue/Repository만 설정해 생성한다. 본문은 `## Evidence`, `## WHY`로 구성하고 없는 WHY는 만들지 않는다. 생성된 URL은 원본 로컬 일지에 남겨 재실행 시 중복을 방지한다.

기존 Work Item 갱신 시 property만 업데이트한다.
본문(Evidence, WHY)은 페이지를 열어 직접 보강한다.

### Trouble Record DB (collection ID → `config/notion.md`)

기본은 기존 Trouble Record 보강(본문 갱신)이다. 주간 집계만으로 신규 Trouble을 만들지 않는다. 신규 생성이 꼭 필요하면 Obsidian·세션 WHY와 연결하고(GitHub 단독 근거 금지) 사용자 승인 후 Detected From을 Review로 두어 만든다.

| Property | 값 |
|---|---|
| Title (title) | 트러블 제목 |
| Status | In Progress / Resolved / Review Needed |
| Date | 발생일 |
| Detected From | Manual / GitHub / Production / Review |
| Related PR (url) | 관련 PR (있으면) |
| Related Issue (url) | 관련 Issue (있으면) |
| Work Item (relation) | 연결 Work Item (있으면) |

본문:
```
## Problem
## Action
## Result
```

## 로컬 포트폴리오 저장

Portfolio Seed 후보를 먼저 로컬 파일로 저장한다. Notion 승인을 기다리거나 게시가 실패해도 로컬 초안은 보존한다. 게시 성공 후에만 notion URL을 갱신한다. `workspace/portfolio/` 디렉터리가 없으면 먼저 만든다.

### workspace/portfolio/{slug}.md (upsert)

파일명: `{slug}.md`
slug = Portfolio Seed 제목 핵심어 2~3단어, 공백→하이픈, 한글 그대로
예: `목록-조회-페이지네이션-설계.md`

같은 slug 파일이 이미 존재하면 내용을 갱신한다 (upsert).
새 파일이면 생성한다.

```md
---
date: YYYY-MM-DD (최초 작성일)
updated: YYYY-MM-DD (이번 갱신일)
notion: {게시된 Notion Portfolio Seed 페이지 URL, 미게시이면 빈 값}
status: Draft | Review Needed | Ready
---

# {Portfolio Seed 제목}

## Problem
{내용}

## Action
{내용}

## Result
{내용}

## Evidence
{PR / Issue / 문서 링크}
```

"추후 보완" 항목은 해당 섹션에 `(추후 보완)` 으로 채운다.

### workspace/portfolio/index.md 갱신

파일이 없으면 헤더와 함께 신규 생성한다.
있으면 새 행을 추가하거나 기존 행을 갱신한다.

```md
| 날짜 | 제목 | 파일 | 상태 |
|---|---|---|---|
| YYYY-MM-DD | {제목} | [{slug}.md]({slug}.md) | Draft |
```
