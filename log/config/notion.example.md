# Notion Database Config

> **설치 시 세팅 필요.** 이 파일을 `config/notion.md`로 복사하고 아래 표의 URL과 Data Source ID를 본인 Notion으로 채운다. Notion에서 각 DB를 만들고(아래 Schema Summary 참고), 각 DB의 Data Source ID를 채운다. 스킬은 ID를 하드코딩하지 않고 이름으로 참조하며, 데이터소스는 `collection://{Data Source ID}`로 연다. 접근 규칙은 `collectors/notion.md` 참조.
>
> URL 칸에는 DB를 풀 페이지로 열어 복사한 링크를 적는다.

## Databases

이 표가 collection ID(Data Source ID)의 **단일 출처(SSOT)**다.

| Name | URL | Data Source ID |
|------|-----|----------------|
| Work Item | `<your Work Item DB URL>` | `<your Work Item data source id>` |
| Trouble Record | `<your Trouble Record DB URL>` | `<your Trouble Record data source id>` |
| Portfolio Seed | `<your Portfolio Seed DB URL>` | `<your Portfolio Seed data source id>` |
| Goal | `<your Goal DB URL>` | `<your Goal data source id>` |

## Relations

- Trouble Record → Work Item (Work Item 컬럼)

## Schema Summary

### Work Item
- Name (title), Status (Todo/In Progress/Done/Blocked), Type (Feature/Bug/Docs/Infra/Chore)
- GitHub PR (url), GitHub Issue (url), Repository (url), Date, Work ID (auto)
- 본문: Evidence, WHY

### Trouble Record
- Title (title), Status (In Progress/Resolved/Review Needed), Date
- Detected From (Manual/GitHub/Production/Review), Related PR (url), Related Issue (url), Work Item (relation)
- 본문: Problem, Action, Result

### Portfolio Seed
- Title (title), Status (Draft/Review Needed/Ready), Date, Evidence URL (url)
- 본문: Problem, Action, Result

### Goal
- Title (title), Period (select: Weekly/Monthly), Status (select: Active/Closed), Start Date, End Date
- 본문: 목표 체크리스트 (`- [ ]`/`- [x]`/`- [-]`, 상태 변경 시 인라인 사유)
- 항목은 삭제·재배열하지 않고 상태만 변경, 신규 항목은 리스트 끝에 추가
