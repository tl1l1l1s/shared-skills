# workspace (Obsidian vault)

raw 기록이 들어오는 Obsidian vault다. 이 폴더를 Obsidian에서 vault로 열어 쓴다.

개인 기록이라 내용물은 대부분 `.gitignore`로 제외된다(inbox, tasks, tasks-done, dashboard, standup-review, daily, weekly, sessions, estimates, portfolio). repo에는 이 README와 `.example` 파일, 구조만 올라간다.

## 구조

- `inbox.md` — 맨 위 오늘 할 일 칸과 그 아래 날짜별 자유 메모. 형식은 `templates/quick-record.md`
- `tasks.md` — 월간·주간 계획과 작업 상태의 원본. 형식은 `templates/planning.md`
- `tasks-done.md` — 끝난 작업과 지난 고정 일정. `/plan-daily`와 `/close-daily`가 옮긴다
- `dashboard.md` — `/plan-daily`와 `/log`가 쓰는 오늘 보드
- `standup-review.md` — `/plan-daily`가 날짜 전환 때 쌓는 회고 재료
- `daily/` — 날짜별 일지 (`YYYY-MM-DD.md`). 빠른 기록과 `/close-daily`의 상세 마감이 들어간다
- `weekly/` — `/review-weekly`가 만드는 주간 요약 (`YYYY-Www.md`)
- `sessions/` — Claude Code 세션 증류 노트 (월별 폴더)
- `estimates.md` — 시간 추정 누적 로그
- `portfolio/` — review-weekly가 만드는 Portfolio Seed 로컬 파일

## 처음 시작

```bash
cp workspace/inbox.example.md workspace/inbox.md
```

이것만 하면 된다. 오늘 할 일 칸은 첫 `/plan-daily`가 안내 문단 아래에 만들고, `tasks.md`를 비롯한 나머지 파일도 커맨드가 필요할 때 만든다. `tasks.example.md`는 `tasks.md`가 채워진 모습을 보여 주는 예시이며 복사하지 않는다.

아래는 `/plan-daily`를 돌린 뒤 `inbox.md`가 어떤 모습인지 보여 주는 예시다. 실제 데이터가 아니다.

```md
# Inbox

(안내 문단)

<!-- todo: 2025-03-14 -->
## 오늘 할 일 (2025-03-14)

- [ ] 13:00 안경점 (일정)
- [x] 분기 보고서 초안, 예상 90m (T2)
  - 10:00~10:40, 11:00~11:30
- [ ] 통계 교재 2장 읽고 정리 (T3)
<!-- /todo -->

## 2025-03-14

보고서는 부서별로 나누지 않고 월별 순서로 정리했다. 지난 분기에 월별 추이를 묻는 질문이 많았기 때문이다.
다음 주 금요일 15시에 독서 모임이 생겼다.
```
