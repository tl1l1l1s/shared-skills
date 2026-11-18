#!/usr/bin/env python3
"""check.py — 세는 일만 한다. 판정은 모델이 한다.

Stage 6.5 기계 점검(reference/final-gate.md 3번)에서 눈으로 세면 틀리기 쉬운 것을 기계로 옮겼다.

  check.py count <자소서.md>      문항 섹션별 As-Is/To-Be 글자 수, 금지어 후보, 짧은 문장이 연달아 나온 자리, 도입과 마무리 겹침
  check.py count -                stdin 전문 하나를 센다
  check.py refs                   스킬 문서끼리의 참조가 실제로 있는지 본다
  check.py selftest               활용형 매칭이 깨지지 않았는지 본다

글자 수 기준은 SKILL.md Stage 1과 같다. 공백 포함, 줄바꿈 제외.
"""
import re, sys, pathlib

SKILL = pathlib.Path(__file__).resolve().parent.parent

def body_only(text):
    """자소서 본문만 남긴다. 소제목은 본문이고 구분선은 아니다."""
    # ==하이라이트== 표시는 본문 글자가 아니다
    lines = [l for l in text.replace("==", "").splitlines() if l.strip() not in ("---", "***", "___")]
    return "\n".join(lines).strip()

def count_chars(text):
    return len(body_only(text).replace("\n", "").replace("\r", ""))

def banned_terms():
    """BANNED_WORDS.md에서 기계로 찾을 수 있는 항목만 뽑는다."""
    src = (SKILL / "BANNED_WORDS.md").read_text(encoding="utf-8")
    if "## 목록" not in src:
        sys.exit("BANNED_WORDS.md에 '## 목록' 제목이 없어 금지어를 읽지 못했다. 제목을 되돌린 뒤 다시 돌린다.")
    body = src.split("## 목록", 1)[1]
    mechanical, by_eye = [], []
    for line in body.splitlines():
        if not line.startswith("- "):
            continue
        item = line[2:].split(" (", 1)[0].split(" — ", 1)[0].strip()
        for term in [t.strip() for t in item.split(", ")]:
            if not term:
                continue
            # 부호나 구조를 가리키는 항목은 문자열 검색으로 못 잡는다
            if "`" in term or term in ("괄호 주석",):
                by_eye.append(term)
            else:
                mechanical.append(term.lstrip("~"))
    return mechanical, by_eye

# 활용형은 BANNED_WORDS.md 매칭 방식 절이 이름을 댄 것과, 목록에 기본형(~다)으로 적혀 활용형을 못 잡는 것만 넣는다.
# 어간을 깎아 만들지 않는다 — 통해에서 통을 뽑으면 통신 장비가 걸린다.
# 값은 그 항목 대신 셀 문자열 전부다. 활용·도출·수립은 부분 문자열로 활용형까지 잡히므로 적지 않는다(적으면 두 번 센다).
# 금지어 목록에 기본형 항목을 더하면 여기에 그 활용형을 함께 적는다.
# 값은 정규식이다. 소통한, 소통해는 통해가 아니라 뺀다. 패턴형(~를 넘어, ~에 직면하여)은 조사와 어미가 바뀐 꼴까지만 잡는다.
INFLECTIONS = {
    "통해": [r"(?<!소)통해", r"(?<!소)통하여", r"(?<!소)통한"],
    "를 넘어": [r"[을를] 넘어"],
    "에 직면하여": [r"에 직면(?:하여|해)"],
}

def variants(term):
    """목록에 적힌 형태 하나, 또는 INFLECTIONS가 그 대신 셀 정규식들."""
    return INFLECTIONS.get(term, [re.escape(term)])

def scan(text, terms):
    hits = []
    for term in terms:
        n = sum(len(re.findall(v, text)) for v in variants(term))
        if n:
            hits.append((term, n))
    return sorted(hits, key=lambda x: -x[1])

# 짧은 문장이 연달아 나온 자리. 사실만 한 문장씩 끊어 늘어놓은 곳을 찾는다.
SHORT, RUN = 50, 2

def short_runs(text):
    """문단마다 SHORT자 이하 문장이 RUN개 이상 이어진 자리를 문장 앞부분으로 돌려준다."""
    out = []
    for para in re.split(r"\n\s*\n", body_only(text)):
        if para.lstrip().startswith("["):  # 소제목 줄은 뺀다
            para = para.split("\n", 1)[1] if "\n" in para else ""
        sents = [x for x in re.split(r"(?<=다\.)\s+", para.replace("\n", " ").strip()) if x]
        i = 0
        while i < len(sents):
            j = i
            while j < len(sents) and len(sents[j]) <= SHORT:
                j += 1
            if j - i >= RUN:
                out.append([x[:20] for x in sents[i:j]])
            i = max(j, i + 1)
    return out

# 첫 문단과 마지막 문단에 글자 그대로 함께 나온 두 어절 이상 구절. 도입 구절을 마무리에서 되풀이한 자리를 찾는다.
# 흔한 서술어 구절(수 있습니다, 있다고 생각합니다)은 겹쳐도 되풀이로 읽히지 않아 그 낱말이 낀 구절은 뺀다.
# 두 어절 구절은 서술어로 끝날 때만 센다. 새 화면을, 한 달 안에 같은 두 어절 명사구는 겹쳐도 되풀이로 읽히지 않는다.
ECHO_STOP = {"수", "것", "것을", "것이", "있습니다", "있는", "있다고", "있었습니다", "생각합니다", "저는", "제가", "제",
             "더", "그", "이", "할", "하는", "하고", "했습니다", "합니다", "위해", "때", "때문입니다", "같은"}

def paragraphs(text):
    out = []
    for para in re.split(r"\n\s*\n", body_only(text)):
        if para.lstrip().startswith("["):  # 소제목 줄은 뺀다
            para = para.split("\n", 1)[1] if "\n" in para else ""
        if para.strip():
            out.append(para.replace("\n", " "))
    return out

def echo_phrases(text):
    """첫 문단과 마지막 문단에 함께 나온 구절을 첫 문단 순서대로 이어 붙여 돌려준다."""
    paras = paragraphs(text)
    if len(paras) < 2:
        return []
    words = lambda p: [w.strip(".,!?") for w in p.split()]
    head, tail = words(paras[0]), words(paras[-1])
    tail_pairs = set(zip(tail, tail[1:]))
    hit = [i for i in range(len(head) - 1)
           if (head[i], head[i + 1]) in tail_pairs and not {head[i], head[i + 1]} & ECHO_STOP]
    out, start = [], None
    for k, i in enumerate(hit):
        if start is None:
            start = i
        if k + 1 == len(hit) or hit[k + 1] != i + 1:
            phrase = head[start:i + 2]
            if len(phrase) >= 3 or phrase[-1].endswith("다"):
                out.append(" ".join(phrase))
            start = None
    return out

def report(label, text, mech, eye):
    hits = scan(text, mech)
    total = sum(n for _, n in hits)
    print(f"{label}: {count_chars(text)}자 (공백 포함, 줄바꿈 제외) / 금지어 후보 {total}건")
    for term, n in hits:
        print(f"    {term} × {n}")
    for run in short_runs(text):
        print(f"    짧은 문장 연속: {' / '.join(run)}")
    echoes = echo_phrases(text)
    if echoes:
        print(f"    도입과 마무리 겹침: {' / '.join(echoes)}")

def cmd_count(path):
    mech, eye = banned_terms()
    if path != "-" and not pathlib.Path(path).is_file():
        sys.exit(f"파일이 없다: {path}")
    raw = sys.stdin.read() if path == "-" else pathlib.Path(path).read_text(encoding="utf-8")
    if path == "-":
        report("입력", raw, mech, eye)
    else:
        # 문항 섹션(## …) 안의 ### As-Is / ### To-Be 를 각각 센다
        found = 0
        for q in re.split(r"^## ", raw, flags=re.M)[1:]:
            title = q.splitlines()[0].strip()
            for m in re.finditer(r"^### (As-Is|To-Be).*?\n(.*?)(?=^### |\Z)", q, re.M | re.S):
                found += 1
                report(f"{title} / {m.group(1)}", m.group(2).strip(), mech, eye)
        if not found:
            sys.exit("## 문항 절 안의 ### As-Is 나 ### To-Be 를 하나도 찾지 못했다. 파일 모양은 reference/revision-loop.md를 따른다.")
    print(f"\n눈으로 볼 것 ({len(eye)}건, 문자열 검색으로 못 잡음): {', '.join(eye)}")
    print("금지어 후보는 세기만 한 것이다. 문맥에 맞는지는 BANNED_WORDS.md 매칭 방식으로 판정한다.")
    print(f"짧은 문장 연속은 {SHORT}자 이하 문장이 {RUN}개 이상 이어진 자리다. 이을지는 STYLE_GUIDE.md 어투 절로 판정한다.")
    print("도입과 마무리 겹침은 첫 문단과 마지막 문단에 글자 그대로 함께 나온 구절이다. 고칠지는 STYLE_GUIDE.md 도입 절로 판정한다.")

def cmd_selftest():
    mech, _ = banned_terms()
    hits = dict(scan("통신 장비를 활용한 뒤 회의를 통하여 원인을 도출했습니다", mech))
    assert hits.get("활용") == 1 and hits.get("통해") == 1 and hits.get("도출") == 1, hits
    hits = dict(scan("통신 장비로 팀원과 소통한 뒤 한계를 넘어 문제에 직면해 ==고쳤습니다==", mech))
    assert "통해" not in hits and hits.get("를 넘어") == 1 and hits.get("에 직면하여") == 1, hits
    assert count_chars("==가나==") == 2
    echo = echo_phrases("저는 확인한 주문만 접수되게 개발할 수 있습니다.\n\n중간 문단입니다.\n\n앞으로도 확인한 주문만 접수되게 할 수 있습니다.")
    assert echo == ["확인한 주문만 접수되게"], echo
    assert echo_phrases("한 문단뿐입니다.") == [], "한 문단"
    assert echo_phrases("새 기술을 익혔고 서버와 화면을 함께 맡습니다.\n\n앞으로도 새 기술을 익혀 함께 맡습니다.") == ["함께 맡습니다"]
    print("selftest 통과")

def cmd_refs():
    bad = 0
    for md in sorted(SKILL.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for ref in set(re.findall(r"`((?:reference|prompts|scripts)/[\w.-]+)`", text)):
            if not (SKILL / ref).exists():
                print(f"[FAIL] {md.relative_to(SKILL)} → {ref} 없음")
                bad += 1
        for ref in set(re.findall(r"`([A-Z_]+\.md)`", text)):
            if not (SKILL / ref).exists():
                print(f"[FAIL] {md.relative_to(SKILL)} → {ref} 없음")
                bad += 1
    print("참조 이상 없음" if not bad else f"깨진 참조 {bad}건")
    return 1 if bad else 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["count"] and len(a) == 2:
        cmd_count(a[1])
    elif a[:1] == ["refs"]:
        sys.exit(cmd_refs())
    elif a[:1] == ["selftest"]:
        cmd_selftest()
    else:
        print(__doc__); sys.exit(1)
