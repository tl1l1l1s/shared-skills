# GitHub Collector

## 역할

GitHub는 Evidence Source다.
구현 사실을 확인하는 데 쓴다. 의도와 맥락은 Obsidian에서 가져온다.

## 접근 방법

- **`gh` CLI를 기본 경로로 쓴다** (빠르다). 예: `gh api "repos/{owner}/{repo}/commits?author={GitHub login}&since=...&until=..."`, `gh pr list --author {GitHub login}`, `gh search`.
- `.mcp.json`의 github MCP 서버는 fallback으로 둔다. 두 경로를 한 작업에서 섞지 않는다.
- 레포 좌표와 GitHub login은 현재 프로필 config(`config/current.md`가 가리키는 파일)에서 확인한다. 레포 좌표가 여러 개면 레포마다 조회한다.
- Commit과 PR은 프로필의 GitHub login이 작성한 것만 사용자의 Evidence로 쓴다. 팀 레포에서 다른 사람의 Commit을 가져오지 않는다.
- 날짜 범위는 `CLAUDE.md`의 하루 경계로 정한 현지 시각을 UTC로 바꿔 `since`/`until`에 넣는다.
- **미설정이면 건너뛴다.** `config/current.md`나 프로필 config가 없거나 레포 좌표·GitHub login이 `<...>` 자리표시로 남아 있을 때, `gh`가 없거나 인증되지 않았을 때는 GitHub를 조회하지 않는다. `GitHub 미설정`이라고 한 줄로 알리고 로컬 기록만으로 계속한다.

## 수집 대상

| 대상 | 수집 내용 |
|---|---|
| Pull Request | 제목, 상태(open/merged/closed), 브랜치, 머지 날짜, 리뷰어 |
| Issue | 제목, 상태, 라벨, 연결된 PR |
| Commit | 메시지, 날짜, 변경 파일 목록 |
| Changed Files | 수정된 파일 경로 (내용 분석 아님) |

## 사용 목적

- **Work Item 근거 연결** — Notion Work Item의 `GitHub PR`, `GitHub Issue` 필드에 연결
- **Trouble Record 근거 연결** — Notion Trouble Record의 `Related PR`, `Related Issue` 필드에 연결
- **Portfolio Seed Evidence** — STAR 구조의 Evidence 항목으로 사용

## 금지

- Commit message만 보고 문제 원인을 추측하지 않는다.
- Commit message만 보고 성과나 성능 개선 결과를 추측하지 않는다.
- Commit message만 보고 의사결정 이유를 추측하지 않는다.
- PR description이 없으면 구현 의도를 만들어내지 않는다.

부족한 정보는 Review Needed로 표시하고 질문을 남긴다.

## 우선순위

GitHub 단독으로 Work Item이나 Portfolio Seed를 완성하지 않는다.
반드시 Obsidian(WHY) 또는 Daily Log와 함께 사용한다.
