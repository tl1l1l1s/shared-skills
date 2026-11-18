# Notion Collector

## 역할

Notion은 주간 요약과 Career Knowledge의 게시 저장소다. 개인 계획·작업 상태의 원본은 `workspace/tasks.md`이며, 일상 마감은 로컬에 저장한다. 계획 및 주간 요약 게시는 `templates/planning.md`를 따른다.
구조화된 Career Knowledge(Work Item / Trouble Record / Portfolio Seed / Goal)가 누적되는 곳이다.
읽기(기존 상태 확인)와 쓰기(생성·갱신)를 모두 한다.

## 접근 커넥터

- **`claude.ai Notion` 커넥터(`mcp__claude_ai_Notion__*`)를 쓴다.**
- 인증이 만료됐으면(401 또는 커넥터 미인증) 임의로 우회하지 말고, 사용자에게 `/mcp` → "claude.ai Notion" 선택으로 재인증을 요청한 뒤 진행한다.
- **미설정이면 건너뛴다.** `config/notion.md`가 없거나 쓰려는 DB의 Data Source ID가 `<...>` 자리표시로 남아 있을 때, 커넥터가 연결돼 있지 않을 때는 Notion을 조회하거나 쓰지 않는다. `Notion 미설정`이라고 한 줄로 알리고 로컬 기록만으로 계속한다.

## collection ID (단일 출처)

- 모든 데이터소스 ID는 **`config/notion.md`의 Databases 표가 단일 출처(SSOT)**다. 스킬 문서에 ID를 다시 하드코딩하지 않고 이름으로 참조한다.
- 데이터소스는 `collection://{Data Source ID}` 형태로 참조한다. 예: Goal DB → `config/notion.md`에서 ID를 찾아 `collection://{그 ID}`.

## 읽기·쓰기 규칙

- **조회**: 데이터소스를 Status/Period 등으로 필터해 필요한 페이지만 가져온다. 페이지 본문은 마크다운으로 읽는다.
- **relation 필드**: 연결 페이지를 **JSON 배열 문자열**로 넣는다(URL 또는 페이지 ID 배열). 단일 값이라도 배열로 감싼다.
- **429(rate limit)**: `retry_after`(보통 30초)만큼 쉬었다가 재시도한다. 실패를 성공으로 간주하지 않는다.
- **조회 한도**: 데이터소스 SQL 조회가 워크스페이스 사용 한도로 막히면 기다려도 바로 풀리지 않는다. DB의 뷰를 열어 뷰 조회로 바꾸고, 뷰에 걸리지 않은 조건은 결과를 받은 뒤 직접 거른다.
- **속성 갱신은 append가 아니라 replace다.** relation에 대상을 더할 때 기존 값을 함께 넣는다.
- **기존 페이지 갱신**: 본문 전체를 다시 생성하지 말고 대상 줄만 바꿔 쓴다. 특히 Goal 체크리스트는 기존 줄을 삭제·재배열하지 않고 상태 문자(`- [ ]`/`- [x]`/`- [-]`)와 인라인 사유만 바꾼다.

## 금지

- 인증 실패(401)를 방치한 채 "저장했다"고 보고하지 않는다. 재인증 후 저장하거나, 저장 못 했음을 명확히 알린다.
- 사용자 승인(각 명령의 미리보기 절차) 없이 Notion에 쓰지 않는다.
- Notion 데이터만 보고 WHY(의사결정 이유·문제 원인·성과)를 생성하지 않는다. WHY 출처는 Obsidian·세션 증류다.

## 우선순위

Notion은 구조화 저장소이자 기존 상태 확인용이다.
경험의 의미와 맥락(WHY)은 Obsidian(inbox·세션 증류)에서 가져오고, Evidence는 GitHub에서 붙인다.
