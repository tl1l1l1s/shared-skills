# log

Claude Code로 개발 성장을 기록하는 프레임워크.

매일 흩어지는 개발 기록(inbox 메모, Claude Code 세션, GitHub 활동)을 로컬 파일에 구조화해 쌓고, 남길 경험만 Notion에 게시한다.

- **개발 기록**: 아침 `/plan-daily`(standup)가 오늘 할 일 칸과 보드를 쓰고, 하루 중 `/log`가 일정·완료·시간을 바로 기록한다. `/close-daily`가 하루 기록을 상세히 마감하고 주간 `/review-weekly`가 다음 주 계획과 Portfolio Seed를 정리한다.

---

## 어떻게 연결되나

계획과 일상 기록의 원본은 로컬 파일이고 Notion은 게시 저장소다. 흐름은 이렇다.

```text
Obsidian (workspace/)   원본 기록과 계획 (inbox, tasks, daily, sessions)
        +
GitHub                  Evidence (구현 사실, 작업 흐름)
        ↓
Claude Code             이 repo의 커맨드로 분석하고 구조화
        ↓
Notion                  주간 요약 / Work Item / Trouble Record / Portfolio Seed
```

- `/plan-daily`와 `/log`는 로컬 파일만 읽고 쓴다. Notion과 GitHub를 조회하지 않는다.
- `/close-daily`는 로컬 기록과 Claude Code 세션, GitHub Evidence로 마감하고 결과를 로컬에 저장한다. Notion에는 쓰지 않는다.
- Notion은 `/review-weekly`에서만 쓴다. 주간 요약 게시는 선택이고 `/review-weekly career`가 Work Item, Trouble Record, Portfolio Seed를 승인받아 게시한다.
- 왜 했는지는 Obsidian이 1순위다. GitHub는 Evidence로만 쓰고, 그것만 보고 이유나 성과를 지어내지 않는다.
- Notion DB 구조와 collection ID는 `config/notion.md` 한 곳에서 관리한다(`config/notion.example.md`를 복사해 만든다).

---

## 설치

필요한 것: Claude Code. `/close-daily`와 `/review-weekly`에는 `gh` CLI와 `jq`가 더 필요하다. Notion 게시에는 claude.ai 로그인(`claude.ai Notion` 커넥터용)이, GitHub MCP fallback에만 Node.js(`npx`)가 필요하다.

1. **클론하고 Claude Code로 연다.**
   ```bash
   git clone https://github.com/tl1l1l1s/shared-skills.git && cd shared-skills/log && claude
   ```
   커맨드(`/plan-daily` 등)가 repo의 `.claude/`에 있어서 이 폴더에서 바로 잡힌다.

2. **Obsidian vault를 연다.** `workspace/`를 Obsidian vault로 열고, `workspace/README.md`대로 `inbox.md`를 만든다. 여기까지 하면 `/plan-daily`와 `/log`를 쓸 수 있다.

3. **프로필을 세팅한다.** `config/profile.example.md`를 복사해 `config/<본인>.md`로 만들고 본인 맥락(지금 하는 것, GitHub login, 레포 좌표)을 채운다. `config/current.example.md`를 `config/current.md`로 복사해 그 파일을 가리키게 한다.

4. **GitHub를 연결한다.** `/close-daily`와 `/review-weekly`가 Evidence를 찾을 때 쓴다. `gh auth login`으로 gh CLI를 인증한다(기본 경로, 빠르다). MCP fallback을 쓰려면 `.mcp.json.example`을 `.mcp.json`으로 복사하고 본인 GitHub 토큰을 채운다(`.mcp.json`은 gitignore라 커밋되지 않는다).

5. **Notion을 연결한다.** `/review-weekly`로 Notion에 게시할 때만 필요하다.
   - `config/notion.example.md`를 `config/notion.md`로 복사한다.
   - 그 파일의 Schema Summary대로 Work Item / Trouble Record / Portfolio Seed / Goal DB를 본인 Notion에 만들고, Relations 절의 relation(Trouble Record→Work Item)도 건다. 여기가 손이 제일 많이 가는 단계다(DB 4개, relation 1개).
   - Claude Code에서 `/mcp`로 `claude.ai Notion` 커넥터를 인증한다(최초 한 번).
   - `config/notion.md`의 표를 채운다. URL 칸에는 각 DB를 풀 페이지로 연 뒤 우측 상단 `...`에서 `Copy link`로 얻은 링크를 적는다.

3~5단계를 건너뛰어도 된다. 설정하지 않은 소스는 커맨드가 미설정이라고 알리고 로컬 기록만으로 진행한다. 각 소스의 수집 규칙은 `collectors/`의 해당 파일을 본다.

---

## Commands

| 커맨드 | 언제 | 하는 일 |
|--------|------|---------|
| `/plan-daily` | 매일 아침 | standup. 새 메모 정리, 오늘 할 일 칸과 보드 쓰기, 그 주 첫 실행의 짧은 주간 조정 |
| `/log` | 하루 중 | 보드를 보여 주고 말한 일정·할 일·완료·시간을 바로 기록 |
| `/close-daily` | 필요할 때 | 지정한 날의 상세 마감(세션 증류, GitHub Evidence 연결, 시간 추정 비교) |
| `/review-weekly` | 매주 | 주간 재계획과 주간 요약. `career`를 붙이면 한 주 기록 정리와 Portfolio Seed 후보 추출 |

하루 중에는 `workspace/inbox.md`에 자유롭게 적어 두거나 `/log`에 말로 남긴다. inbox에 적은 메모는 다음 `/plan-daily`가 처리한다.

---

## cover-letter 스킬

자소서 스킬은 이 폴더가 아니라 형제 폴더 `../cover-letter`에 있다. 자세한 내용은 거기 README를 참고한다.

---

## 개인 데이터

`workspace/`의 실제 기록(inbox, tasks, dashboard, daily, weekly, sessions, estimates, portfolio)과 본인이 채운 설정(`config/current.md`, `config/notion.md`, `config/<본인>.md`, `.mcp.json`)은 gitignore로 빠진다. repo에는 프레임워크(커맨드, 템플릿, config 예시, collector 규칙)만 올라간다.
