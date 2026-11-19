"""v4 전용 HTML 장면들 (1080x1920). drawn.py(이전 숏폼의 그림 카드)와 같은 스타일로 새 카드를 추가하고,
키네틱 타이포 · AI 빌더 재연 · 사진 스토리 · 엔딩을 만든다. 시간 값은 초 단위(장면 길이 D 기준으로 계산)."""
import os, sys, html, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "build"))
from drawn import DRAWN, box, chip, txt, emo, arrow, stripe, big_num, GRN, YEL, INK, BLUE, ORG, PUR, PINK  # noqa: E402

RED = "#E53935"
A = f"{HERE}/assets"

def cnt(n, fmt=""):
    return f'<i class="cnt" data-to="{n}" data-fmt="{fmt}">{n:,}</i>' if fmt == "comma" else f'<i class="cnt" data-to="{n}">{n}</i>'

# ───────────── 새 그림 카드 ─────────────
def d_record():
    b = txt(f'대입에서 <span style="color:{RED}">사라진 것들</span>', 70, 262, 80)
    rows = [("🏆", "수상경력"), ("📚", "독서활동"), ("🤝", "자율동아리"), ("🙋", "개인봉사")]
    for i, (e, t) in enumerate(rows):
        b += box(f'<div style="display:flex;align-items:center;gap:22px"><span style="font-size:62px">{e}</span>'
                 f'<span style="font-size:52px;flex:1;color:#9E9E9E;text-decoration:line-through;text-decoration-color:{RED};text-decoration-thickness:6px">{t}</span>'
                 f'<span style="font-size:36px;color:#fff;background:{RED};border-radius:999px;padding:8px 26px">미반영</span></div>',
                 70, 420 + i * 165, 940, border="#F5B5B5", pad=22)
    b += box(f'<div style="font-size:42px;color:#2e7d00">⭐ 학생을 설명하는 건</div><div style="font-size:72px;margin-top:6px">교과 세특</div>'
             '<div style="font-size:32px;color:#555;margin-top:10px">왜 시작했고 · 어떻게 탐구했고 · 무엇을 배웠나</div>', 70, 1110, 940, border=GRN, pad=30, bg="#F4FFE9")
    return b, stripe("#fff3f3", "#ffe9e9")

def d_seven():
    b = txt(f'문제에서 출시까지 <span style="color:{GRN}">7단계</span>', 70, 262, 64)
    steps = [("🔎", "문제 발견", "문제 정의서", ORG), ("📚", "리서치", "선행 사례 정리", BLUE), ("📐", "기획·설계", "기획서·와이어프레임", PUR),
             ("🛠️", "프로토타입", "작동하는 시제품", PINK), ("🧪", "테스트·개선", "사용자 5명 테스트", "#00B8A9"), ("🚀", "출시", "배포 URL·시연 영상", GRN),
             ("🎤", "보고·발표", "소논문·발표 자료", "#FF6B35")]
    for i, (e, t, o, c) in enumerate(steps):
        b += box(f'<div style="display:flex;align-items:center;gap:18px"><span style="font-size:32px;color:#fff;background:{c};border-radius:50%;width:56px;height:56px;'
                 f'display:flex;align-items:center;justify-content:center">{i+1}</span><span style="font-size:54px">{e}</span>'
                 f'<span style="font-size:44px;flex:1">{t}</span><span style="font-size:30px;color:{c};background:#fff;border:4px solid {c};border-radius:999px;padding:6px 20px;white-space:nowrap">{o}</span></div>',
                 70, 380 + i * 160, 940, border="#E5E5E5" if i < 6 else GRN, pad=16)
    return b, stripe("#f6fbef", "#eef7e4")

def d_five():
    b = box(f'<div style="font-size:34px;color:{PUR}">❓ 하나의 질문</div><div style="font-size:52px;margin-top:8px;word-break:keep-all">"우리 교실 공기, 왜 오후만 되면 답답할까?"</div>',
            70, 270, 940, border="#B9A8FF", pad=30)
    outs = [("📄", "논문", "CO₂ 농도와 집중도 소논문", BLUE), ("🔍", "리서치", "세 반 측정 데이터 분석", ORG), ("🎬", "캠페인", "환기 캠페인 AI 영상", PINK),
            ("🌐", "서비스", "환기 알림 웹앱", GRN), ("🔧", "제품", "아두이노 CO₂ 측정기", "#00B8A9")]
    for i, (e, t, s, c) in enumerate(outs):
        x = 70 + (i % 2) * 480; y = 590 + (i // 2) * 250
        b += box(f'<div style="display:flex;gap:16px;align-items:center"><span style="font-size:74px">{e}</span><div><div style="font-size:48px;color:{c}">{t}</div>'
                 f'<div style="font-size:30px;color:#555;margin-top:4px;word-break:keep-all">{s}</div></div></div>', x, y, 460, border=c, pad=22, rot=(-1, 1)[i % 2])
    b += box('<div style="font-size:38px;color:#fff">📝 그대로</div><div style="font-size:46px;color:#fff;margin-top:4px">세특 · 면접 재료</div>',
             550, 1090, 460, border="#3f9a00", pad=22, bg=GRN)
    return b, stripe("#f4f1ff", "#ece7ff")

def d_turn():
    b = txt(f'교육 현장에서 본<br><span style="color:{RED}">진짜 문제</span>', 70, 262, 74)
    rows = [("📖", "문법 암기 위주 코딩 수업", "코드는 쓸 줄 안다", "#9E9E9E", "✔"),
            ("❓", "무엇을, 왜 만들지", "모른다", RED, "✖"),
            ("🗑️", "수업이 끝나면", "남는 결과물이 없다", RED, "✖")]
    for i, (e, t, v, c, m) in enumerate(rows):
        b += box(f'<div style="display:flex;align-items:center;gap:22px"><span style="font-size:80px">{e}</span><div style="flex:1">'
                 f'<div style="font-size:38px;color:#777">{t}</div><div style="font-size:56px;color:{c};margin-top:6px">{v}</div></div>'
                 f'<span style="font-size:72px;color:{c}">{m}</span></div>', 70, 500 + i * 300, 940, border=c if i else "#E5E5E5", pad=30)
    return b, stripe("#f5f5f5", "#ececec")

def d_shift():
    b = txt(f'생성형 AI 이후,<br><span style="color:{BLUE}">만드는 일</span>은 AI에게', 70, 262, 72)
    pills = lambda items, c, bg: "".join(f'<span style="font-size:38px;color:{c};background:{bg};border-radius:999px;padding:10px 26px">{t}</span>' for t in items)
    b += box('<div style="font-size:46px;color:#777">🤖 AI가 하는 것</div><div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:20px">'
             + pills(["코드 작성", "디자인 구현", "콘텐츠 생성", "데이터 분석"], "#555", "#EEEEEE") + '</div>', 70, 500, 940, pad=32)
    b += arrow(500, 840, 90, 90, ORG)
    b += box(f'<div style="font-size:50px;color:{ORG}">🧑 사람이 해야 하는 것</div><div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:20px">'
             + pills(["진짜 문제 정의", "기획과 전략", "공감과 직관", "실행 의지"], "#fff", ORG) + '</div>', 70, 960, 940, border=ORG, pad=32, bg="#FFF8EE")
    return b, stripe("#eef6ff", "#e2efff")

def d_proof():
    b = txt(f'그래서 <span style="color:#FF6B35">제가 먼저</span><br>해 봤어요', 70, 262, 78)
    b += box(f'<div style="display:flex;align-items:center;gap:30px"><div style="font-size:170px;line-height:1;color:#FF6B35;letter-spacing:-4px">{cnt(10)}<span style="font-size:70px">개</span></div>'
             '<div style="font-size:44px;line-height:1.35">1년 동안<br>혼자 AI와 만든<br>서비스</div></div>', 70, 520, 940, border="#FF6B35", pad=34)
    b += box('<div style="font-size:42px">⏱️ 개발에 실제로 든 시간</div><div style="display:flex;margin-top:22px;height:96px;border-radius:20px;overflow:hidden;font-size:38px;color:#fff">'
             f'<div class="grow" style="flex:8;background:#FF6B35;display:flex;align-items:center;padding-left:26px">기획 · 화면 {cnt(80)}%</div>'
             '<div style="flex:2;background:#BDBDBD;display:flex;align-items:center;justify-content:center">코드</div></div>', 70, 900, 940, pad=32)
    b += ('<div class="abs" style="left:70px;right:70px;top:1250px;display:flex;gap:16px;justify-content:center">'
          + "".join(f'<span style="font-size:38px;color:#fff;background:{c};border-radius:999px;padding:12px 28px;border-bottom:7px solid rgba(0,0,0,.18)">{t}</span>'
                    for t, c in [("상용 서비스 1", GRN), ("교육 플랫폼 4", BLUE), ("학생 서비스 4", PUR)]) + '</div>')
    return b, stripe("#fff3ec", "#ffe9dd")

def d_lp():       # 폰은 오른쪽
    b = txt(f'우리 아이 첫<br><span style="color:{GRN}">한글</span> &amp; <span style="color:{BLUE}">영어</span>', 70, 262, 76)
    b += box(f'<div style="font-size:96px;line-height:1;color:{GRN};letter-spacing:-3px">{cnt(15000, "comma")}<span style="font-size:52px">+</span></div><div style="font-size:38px;margin-top:8px">🇰🇷 한글 단어·문장</div>', 60, 520, 520, border=GRN, pad=26)
    b += box(f'<div style="font-size:96px;line-height:1;color:{BLUE};letter-spacing:-3px">{cnt(20000, "comma")}<span style="font-size:52px">+</span></div><div style="font-size:38px;margin-top:8px">🇺🇸 영어 단어·문장</div>', 60, 790, 520, border=BLUE, pad=26)
    b += box('<div style="font-size:40px">⏱️ 하루 15분 루틴</div><div style="font-size:32px;color:#555;margin-top:8px">카드 → 타이핑 → 자모 → 쓰기</div>', 60, 1060, 520, border=ORG, pad=24)
    b += chip("🔓 가입 없이 · 완전 무료", "#3C3C3C", 60, 1290, 36, -2)
    return b, stripe("#f6fbef", "#eef7e4")

def d_lp_launch():  # 폰은 왼쪽
    b = txt(f'LingoPang<br><span style="color:#FF6B35">출시 과정</span>', 480, 262, 74, w=560)
    steps = [("🌐", "웹 출시", "lingopang.com", GRN), ("📱", "Google Play", "앱 출시", BLUE), ("🎬", "YouTube 쇼츠", "직접 홍보", PINK), ("💰", "광고 수익", "으로 운영", ORG)]
    for i, (e, t, s, c) in enumerate(steps):
        b += box(f'<div style="display:flex;gap:20px;align-items:center"><span style="font-size:72px">{e}</span><div><div style="font-size:46px;color:{c}">{t}</div>'
                 f'<div style="font-size:32px;color:#666">{s}</div></div></div>', 480, 510 + i * 255, 540, border=c, pad=22, rot=(-1, 1)[i % 2])
        if i < 3: b += f'<div class="abs" style="left:720px;top:{510 + i * 255 + 178}px;font-size:46px;color:#C8C8C8">▼</div>'
    return b, stripe("#fff3ec", "#ffe9dd")

def classes():
    bx = lambda c, e, t, lines: (f'<div style="background:#fff;border:6px solid {c};border-bottom-width:14px;border-radius:40px;padding:40px 46px">'
                                 f'<div style="font-size:70px;color:{c}">{e} {t}</div>'
                                 + "".join(f'<div style="font-size:44px;margin-top:16px;color:#444">· {l}</div>' for l in lines) + "</div>")
    b = ('<div class="abs" style="left:80px;right:80px;top:300px;display:flex;flex-direction:column;gap:40px">'
         + bx(GRN, "🌱", "기초반", ["코딩 경험 없어도 OK", "아이디어로 첫 작품 완성", "데모데이 시연"])
         + bx("#1CB0F6", "🚀", "심화반 (프로젝트)", ["7단계 프로젝트 프로세스", "실제 출시 · 상용화까지", "포트폴리오 · 세특 재료 완성"])
         + '<div style="display:flex;flex-wrap:wrap;gap:18px;justify-content:center">'
         + "".join(f'<span style="font-size:40px;background:#fff;border:4px solid #E5E5E5;border-bottom-width:9px;border-radius:999px;padding:12px 28px">{t}</span>'
                   for t in ["☀️ 주말반", "🌙 야간반", "💻 줌 온라인", "🏫 오프라인 공간"]) + "</div></div>")
    return b, stripe("#f6fbef", "#eef7e4")

CARDS = dict(DRAWN, d_record=d_record, d_seven=d_seven, d_five=d_five, d_turn=d_turn, d_shift=d_shift, d_proof=d_proof,
             d_lp=d_lp, d_lp_launch=d_lp_launch, classes=classes)

# ───────────── 공통: 파티클 ─────────────
def particles(n, cx, cy, t0, spread=520, seed=1, chars=None, colors=None, size=(18, 34), dur=1.3):
    rnd = random.Random(seed); out = ""
    colors = colors or [GRN, YEL, BLUE, PINK, ORG, PUR]
    for i in range(n):
        ang = rnd.uniform(0, 6.283); r = rnd.uniform(0.35, 1.0) * spread
        import math
        dx, dy = r * math.cos(ang), r * math.sin(ang) + rnd.uniform(120, 360)
        s = rnd.randint(*size); c = rnd.choice(colors); rot = rnd.randint(-540, 540)
        shape = (f'<span style="font-size:{s * 1.6:.0f}px;color:{c}">{rnd.choice(chars)}</span>' if chars
                 else f'<span style="display:block;width:{s}px;height:{s * 0.5:.0f}px;background:{c};border-radius:3px"></span>')
        out += (f'<div class="abs" style="left:{cx}px;top:{cy}px;--dx:{dx:.0f}px;--dy:{dy:.0f}px;--r:{rot}deg;'
                f'animation:burst {dur}s cubic-bezier(.15,.7,.3,1) {t0 + rnd.uniform(0, .12):.2f}s both">{shape}</div>')
    return out

# ───────────── 키네틱 타이포 ─────────────
def kinetic(s, D):
    st = s.get("style")
    if st == "qs":
        qs = s["qs"]; T = [0.08 * D + i * 0.26 * D for i in range(len(qs))]
        b = ('<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 30%,#2a0d10,#07080c 70%)"></div>'
             '<div class="abs grid"></div>'
             f'<div class="abs" style="left:0;right:0;top:300px;text-align:center;font-size:52px;color:{RED};letter-spacing:2px;animation:rise .5s .05s both">⚠ {html.escape(s["head"])}</div>')
        for i, q in enumerate(qs):
            b += (f'<div class="abs" style="left:70px;right:70px;top:{470 + i * 290}px;background:#14151b;border:3px solid #2a2c35;border-left:14px solid {RED};'
                  f'border-radius:28px;padding:40px 44px;font-size:56px;line-height:1.3;color:#e9e9ee;word-break:keep-all;animation:slam .5s cubic-bezier(.2,1.4,.4,1) {T[i]:.2f}s both,'
                  f'glitchx .35s steps(3) {T[i]:.2f}s 1">{q}</div>')
        b += f'<div class="abs" style="right:40px;top:1240px;font-size:360px;color:rgba(229,57,53,.13);line-height:1">?</div>'
        return b, "#07080c"
    if st == "chapter":
        b = ('<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 40%,#123d12,#061006 72%)"></div><div class="abs grid g2"></div>'
             '<div class="abs" style="left:0;right:0;top:560px;text-align:center;color:#cfe9c4;font-size:62px;animation:rise .6s .15s both">말로만이 아니라,</div>'
             f'<div class="abs" style="left:0;right:0;top:700px;text-align:center;color:#fff;font-size:118px;line-height:1.2;animation:pop .6s {0.32 * D:.2f}s both">'
             f'직접 만들어<br><span class="hl">운영 중입니다</span></div>'
             f'<div class="abs" style="left:0;right:0;top:1130px;display:flex;gap:16px;justify-content:center;animation:rise .5s {0.6 * D:.2f}s both">'
             + "".join(f'<span style="font-size:40px;color:#fff;background:{c};border-radius:999px;padding:12px 28px">{t}</span>' for t, c in [("상용 서비스", GRN), ("교육 플랫폼", BLUE), ("학생 서비스", PUR)])
             + '</div>')
        return b, "#061006"
    if st == "mission":
        b = ('<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 42%,#1f5c0c,#0a1f05 72%)"></div><div class="abs grid g2"></div>'
             '<div class="abs" style="left:0;right:0;top:420px;text-align:center;color:#d7f5c8;font-size:56px;animation:rise .55s .1s both">그래서 시작한</div>'
             f'<div class="abs" style="left:0;right:0;top:520px;text-align:center;color:#fff;font-size:100px;animation:pop .55s .35s both">프로젝트 수업</div>'
             f'<div class="abs" style="left:90px;right:90px;top:820px;text-align:center;color:#fff;font-size:76px;line-height:1.35;animation:rise .6s {0.42 * D:.2f}s both">'
             f'<span style="opacity:.6;text-decoration:line-through;text-decoration-color:{RED};text-decoration-thickness:7px">개발자</span>가 아니라<br>'
             f'<span class="hl" style="font-size:104px">실행자</span>를 키웁니다</div>'
             f'<div class="abs" style="left:0;right:0;top:1290px;text-align:center;color:#bfe3ad;font-size:40px;animation:rise .5s {0.62 * D:.2f}s both">— AI Maker Lab · 김종필</div>'
             + particles(26, 530, 900, 0.5 * D, 460, seed=7, chars=["✦", "✧", "★"], colors=[YEL, "#fff", GRN]))
        return b, "#0a1f05"
    if st == "choice":
        b = ('<div class="abs" style="inset:0;background:#07080c"></div>'
             f'<div class="abs" style="left:0;right:0;top:0;height:960px;background:radial-gradient(ellipse at 50% 60%,#16461a,#07080c 70%);animation:rise .5s .05s both"></div>'
             f'<div class="abs" style="left:0;right:0;top:960px;height:960px;background:radial-gradient(ellipse at 50% 40%,#4a1214,#07080c 70%);animation:rise .5s {0.3 * D:.2f}s both"></div>'
             f'<div class="abs" style="left:0;right:0;top:470px;text-align:center;color:#fff;font-size:96px;animation:pop .55s .1s both">AI를 <span style="color:#7CFF4F">부리는</span> 사람</div>'
             f'<div class="abs" style="left:0;right:0;top:600px;text-align:center;color:#a9e59a;font-size:44px;animation:rise .5s .4s both">문제를 정하고 · 만들고 · 검증한다</div>'
             f'<div class="abs" style="left:440px;top:900px;width:200px;height:120px;border-radius:60px;background:#fff;color:#111;font-size:64px;display:flex;align-items:center;justify-content:center;animation:pop .4s {0.25 * D:.2f}s both">VS</div>'
             f'<div class="abs" style="left:0;right:0;top:1150px;text-align:center;color:#fff;font-size:96px;animation:pop .55s {0.3 * D:.2f}s both,glitchx .4s steps(3) {0.3 * D:.2f}s 3">AI에 <span style="color:#FF5A5A">밀리는</span> 사람</div>'
             f'<div class="abs" style="left:0;right:0;top:1280px;text-align:center;color:#e7a3a3;font-size:44px;animation:rise .5s {0.36 * D:.2f}s both">답만 받아 적고 · 창을 닫는다</div>')
        return b, "#07080c"
    raise ValueError(st)

# ───────────── AI 빌더 재연 (Claude · v0 류 도구) ─────────────
def _hl_code(line):
    import re
    e = html.escape(line)
    e = re.sub(r"(&quot;.*?&quot;|&#x27;.*?&#x27;|'.*?')", r'<span style="color:#9ece6a">\1</span>', e)
    e = re.sub(r"(&lt;/?[A-Za-z]+)", r'<span style="color:#7aa2f7">\1</span>', e)
    e = re.sub(r"\b(export|default|function|return|use client)\b", r'<span style="color:#bb9af7">\1</span>', e)
    e = re.sub(r"\b(className|steps|brand)\b", r'<span style="color:#e0af68">\1</span>', e)
    return e

BUILD_PROMPT = "청소년이 아이디어를 기획서로 키우는 웹사이트 만들어 줘. 어두운 우주 테마, 제목은 '아이디어에 불꽃, 설계는 내가', 시작 버튼은 주황색으로."
FIX_PROMPT = "시작 버튼을 더 크게 하고, 아래에 단계 카드 3개 추가해 줘. 다 되면 배포!"
CODE = ["'use client'", "export default function Home() {", "  return (", '    <main className="min-h-screen bg-[#0b0b14]">',
        '      <Header brand="teensparkai" />', '      <p className="text-white/60">AI와 함께하는 청소년 기획 스튜디오</p>',
        '      <h1 className="text-5xl font-bold">', '        아이디어에 <span className="text-orange-500">불꽃</span>,',
        "        <br />설계는 내가.", "      </h1>", '      <Button className="bg-orange-500 rounded-xl">', "        🚀 시작하기",
        "      </Button>", "      <StepCards steps={['질문이 자라', '우주처럼 확장', '결과로 착륙']} />", "    </main>", "  )", "}"]
DIFF = [("-", '      <Button className="bg-orange-500">'), ("+", '      <Button size="xl" className="bg-orange-500">'),
        ("+", "      <StepCards steps={['질문이 자라', '우주처럼 확장', '결과로 착륙']} />"), (" ", "  배포: vercel --prod")]

def builder(s, D):
    step = s["step"]; shot = f"{A}/screens/teenspark.png"
    WX, WY, WW, WH = 36, 250, 1008, 1210           # 창
    PW, PH = 400, round(400 * 844 / 390)          # 미리보기 화면
    pX, pY = WX + 572, WY + 150                    # 미리보기 폰 화면 좌상단
    js_prompt = (BUILD_PROMPT if step == "build" else FIX_PROMPT).replace("'", "\\'")
    if step == "build":
        T = dict(type0=0.03 * D, type1=0.30 * D, code0=0.33 * D, code1=0.60 * D, skel0=0.36 * D, rev0=0.55 * D, rev1=0.80 * D, done=0.82 * D)
    else:
        T = dict(type0=0.03 * D, type1=0.26 * D, code0=0.28 * D, code1=0.42 * D, ring=0.30 * D, press=0.47 * D, prog0=0.50 * D, prog1=0.68 * D, done=0.70 * D)
    tool = ('<div class="abs" style="left:0;right:0;top:196px;text-align:center;font-size:28px;color:rgba(255,255,255,.75);font-weight:600">'
            'Claude · v0 같은 AI 코딩 도구로 수업에서 만드는 과정 (재연)</div>')
    win = (f'<div class="abs" style="left:{WX}px;top:{WY}px;width:{WW}px;height:{WH}px;border-radius:30px;background:#0f1117;border:2px solid #2a2d36;'
           f'box-shadow:0 40px 90px rgba(0,0,0,.6);overflow:hidden;animation:pop .5s .02s both">'
           '<div style="height:64px;background:#161922;display:flex;align-items:center;gap:12px;padding:0 24px;border-bottom:1px solid #23262f">'
           '<i style="width:16px;height:16px;border-radius:50%;background:#ff5f57"></i><i style="width:16px;height:16px;border-radius:50%;background:#febc2e"></i>'
           '<i style="width:16px;height:16px;border-radius:50%;background:#28c840"></i>'
           '<span style="margin-left:18px;font-size:26px;color:#c9cdd6;font-weight:600">✦ AI 빌더 — 새 프로젝트</span>'
           f'<span id="deploy" style="margin-left:auto;font-size:26px;color:#fff;background:#2f3340;border-radius:14px;padding:8px 22px;font-weight:600">▲ 배포하기</span></div></div>')
    # 채팅 영역
    cx, cy = WX + 24, WY + 90
    chat = ""
    if step == "deploy":
        chat += (f'<div class="abs" style="left:{cx + 50}px;top:{cy}px;width:470px;background:#3a3157;color:#d9d3f5;border-radius:24px 24px 6px 24px;'
                 f'padding:16px 22px;font-size:24px;line-height:1.4;opacity:.7">{html.escape(BUILD_PROMPT[:38])}…</div>'
                 f'<div class="abs" style="left:{cx}px;top:{cy + 120}px;font-size:24px;color:#8be9a8;opacity:.7">✦ AI · ✓ 첫 화면 완성</div>')
        uy = cy + 175
    else:
        uy = cy
    chat += (f'<div class="abs" style="left:{cx + 20}px;top:{uy}px;width:500px;background:#6E56CF;color:#fff;border-radius:26px 26px 6px 26px;'
             f'padding:22px 26px;font-size:29px;line-height:1.42;min-height:80px;animation:rise .35s {T["type0"]:.2f}s both"><span id="typed"></span>'
             f'<span class="caret">▍</span></div>')
    ay = uy + (270 if step == "build" else 200)
    chat += (f'<div class="abs" style="left:{cx}px;top:{ay}px;width:520px;animation:rise .35s {T["code0"]:.2f}s both">'
             f'<div style="font-size:26px;color:#8be9a8">✦ AI</div><div id="status" style="font-size:28px;color:#e6e6e6;margin-top:6px">코드를 쓰는 중…</div></div>')
    code_top = ay + 100; code_h = WY + WH - code_top - 60
    lines = (CODE if step == "build" else [l for _, l in DIFF])
    code_html = ""
    for i, l in enumerate(lines):
        if step == "build": code_html += f'<div class="cl" data-i="{i}">{_hl_code(l) or "&nbsp;"}</div>'
        else:
            sign = DIFF[i][0]; col = {"-": "rgba(229,57,53,.22)", "+": "rgba(88,204,2,.18)", " ": "transparent"}[sign]
            code_html += f'<div class="cl" data-i="{i}" style="background:{col}"><b style="color:#888;font-weight:400">{sign}</b>{_hl_code(l)}</div>'
    chat += (f'<div class="abs" style="left:{cx}px;top:{code_top}px;width:520px;height:{code_h}px;background:#0a0c10;border:1px solid #20232b;border-radius:18px;'
             f'padding:18px 16px;font-family:Menlo,monospace;font-size:{19 if step == "build" else 21}px;line-height:1.6;color:#c9d1d9;overflow:hidden;letter-spacing:0;'
             f'animation:rise .35s {T["code0"]:.2f}s both">{code_html}</div>')
    # 미리보기
    url0 = "localhost:3000 · 미리보기"
    prev = (f'<div class="abs" style="left:{pX - 12}px;top:{WY + 84}px;width:{PW + 24}px;height:46px;border-radius:23px;background:#1b1e26;'
            f'display:flex;align-items:center;justify-content:center;font-size:22px;color:#9aa0aa;font-family:Menlo,monospace;letter-spacing:0">'
            f'<span id="url0">🔒 {url0}</span><span id="url1" style="display:none;color:#7CFF4F">🔒 teenspark.vercel.app</span></div>'
            f'<div class="abs" style="left:{pX - 12}px;top:{pY - 12}px;width:{PW + 24}px;height:{PH + 24}px;border-radius:46px;background:#000;border:2px solid #2a2d36"></div>'
            f'<div class="abs" style="left:{pX}px;top:{pY}px;width:{PW}px;height:{PH}px;border-radius:34px;overflow:hidden;background:#0b0b14">')
    if step == "build":
        sk = "".join(f'<div class="sk" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>' for x, y, w, h in
                     [(24, 30, 140, 26), (24, 120, 300, 18), (24, 170, 340, 54), (24, 236, 260, 54), (24, 330, 352, 18), (24, 360, 300, 18),
                      (24, 430, 352, 64), (24, 515, 352, 64), (24, 620, 352, 110), (24, 750, 352, 110)])
        prev += (f'<div class="abs" style="inset:0;animation:fadeio {T["rev1"] - T["skel0"]:.2f}s linear {T["skel0"]:.2f}s both">{sk}</div>'
                 f'<img class="abs" src="file://{shot}" style="left:0;top:0;width:{PW}px;animation:reveal {T["rev1"] - T["rev0"]:.2f}s cubic-bezier(.5,0,.3,1) {T["rev0"]:.2f}s both">'
                 f'<div class="abs scanbar" style="animation:scan {T["rev1"] - T["rev0"]:.2f}s cubic-bezier(.5,0,.3,1) {T["rev0"]:.2f}s both"></div>')
    else:
        prev += f'<img class="abs" src="file://{shot}" style="left:0;top:0;width:{PW}px">'
        bt = round(450 * PW / 390)
        prev += (f'<div class="abs" style="left:14px;top:{bt - 30}px;width:{PW - 28}px;height:110px;border:6px solid #FFD900;border-radius:22px;'
                 f'box-shadow:0 0 30px #FFD900;animation:ring 1s ease-in-out {T["ring"]:.2f}s 3 both"></div>'
                 f'<div class="abs" style="right:16px;top:{bt - 74}px;font-size:24px;background:#FFD900;color:#111;border-radius:12px;padding:4px 14px;animation:pop .4s {T["ring"] + 0.2:.2f}s both">✦ 수정됨</div>')
    prev += '</div>'
    extra = ""
    if step == "build":
        extra += particles(22, pX + PW // 2, pY + PH // 2, T["rev1"] - 0.05, 340, seed=3, chars=["✦", "✧", "✨"], colors=[YEL, "#fff", "#B9A8FF"])
    else:
        extra += (f'<div class="abs" style="left:{cx}px;top:{ay + 60}px;width:520px;height:22px;border-radius:11px;background:#23262f;overflow:hidden;animation:rise .3s {T["prog0"]:.2f}s both">'
                  f'<div style="height:100%;background:linear-gradient(90deg,#58CC02,#7CFF4F);animation:prog {T["prog1"] - T["prog0"]:.2f}s linear {T["prog0"]:.2f}s both"></div></div>'
                  f'<div class="abs" style="left:{cx}px;top:{ay + 100}px;width:520px;font-size:30px;color:#7CFF4F;animation:pop .4s {T["done"]:.2f}s both">✓ 배포 완료!<br>'
                  f'<span style="font-family:Menlo,monospace;font-size:26px;color:#fff;letter-spacing:0">https://teenspark.vercel.app</span></div>'
                  + particles(46, pX + PW // 2, WY + 100, T["done"], 560, seed=5))
    js = f"""<script>
const P='{js_prompt}', T={T}, D={D};
const cls=[...document.querySelectorAll('.cl')];
window.seek2=function(t){{
  const k=Math.max(0,Math.min(1,(t-T.type0-0.2)/(T.type1-T.type0-0.2)));
  document.getElementById('typed').textContent=P.slice(0,Math.round(P.length*k));
  document.querySelector('.caret').style.opacity=(k<1&&Math.floor(t*3)%2==0)||k<1?1:0;
  const c=Math.max(0,Math.min(1,(t-T.code0)/(T.code1-T.code0)));
  cls.forEach((e,i)=>e.style.visibility=(i<Math.ceil(cls.length*c))?'visible':'hidden');
  const st=document.getElementById('status');
  if('{step}'=='build') st.textContent = t<T.code1?'코드를 쓰는 중…':(t<T.done?'화면을 만드는 중…':'✓ 완성! 미리보기를 확인하세요');
  else {{ st.textContent = t<T.code1?'수정하는 중…':(t<T.done?'배포 중…':'✓ 수정 반영 · 배포 완료');
    const d=document.getElementById('deploy'); const on=t>=T.press;
    d.style.background=on?'#58CC02':'#2f3340'; d.style.transform=(t>=T.press&&t<T.press+0.15)?'scale(.9)':'scale(1)'; d.style.boxShadow=on?'0 0 24px #58CC02':'none';
    document.getElementById('url0').style.display=t>=T.done?'none':'inline'; document.getElementById('url1').style.display=t>=T.done?'inline':'none'; }}
}};
</script>"""
    return tool + win + chat + prev + extra + js, "radial-gradient(ellipse at 50% 30%,#1d2240,#07080f 75%)"

# ───────────── 사진 스토리 (실제 전시·수업 사진) ─────────────
def photos(s, D):
    ph = s["photos"]; n = len(ph); rnd = random.Random(len(s["id"]) * 13)
    t0, span = 0.12, 0.78 * D
    T = [t0 + i * span / n for i in range(n)]
    out = ('<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 42%,#3a2f25,#14100c 75%)"></div>'
           '<div class="abs" style="inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.015) 0 2px,transparent 2px 9px)"></div>')
    for i, (f, label) in enumerate(ph):
        rot = rnd.uniform(-6, 6); dx = rnd.uniform(-46, 46); dy = rnd.uniform(-40, 40)
        dim = f",dim .45s linear {T[i + 1]:.2f}s forwards" if i + 1 < n else ""
        out += (f'<div class="abs pol" style="left:{90 + dx:.0f}px;top:{420 + dy + (i % 2) * 40:.0f}px;transform:rotate({rot:.1f}deg);'
                f'animation:land .55s cubic-bezier(.2,1.25,.4,1) {T[i]:.2f}s both{dim}">'
                f'<img src="file://{A}/photos/{f}.jpg"><div class="lab">📍 {html.escape(label)}</div></div>')
    return out, "#14100c", T

def photo_flash_times(s, D):
    n = len(s["photos"]); return [0.12 + i * 0.78 * D / n + 0.33 for i in range(n)]

# ───────────── 벽 · 엔딩 ─────────────
def wall(s, D):
    w, h = 236, 470; xs = [30, 290, 554, 814]; out = ""
    for i, n in enumerate(s["screens"]):
        c, r = i % 4, i // 4; rot = (-4, 3, -2, 4)[c] * (1 if r else -1)
        out += (f'<div class="abs" style="left:{xs[c]}px;top:{330 + r * 560 + (40 if c % 2 else 0)}px;width:{w}px;height:{h}px;border-radius:34px;background:#111;padding:9px;'
                f'box-shadow:0 18px 40px rgba(0,0,0,.35);transform:rotate({rot}deg);animation:land .5s cubic-bezier(.2,1.25,.4,1) {0.1 + i * 0.11:.2f}s both">'
                f'<div style="width:100%;height:100%;border-radius:26px;overflow:hidden;background:#fff"><img src="file://{A}/screens/{n}.png" style="width:100%;display:block"></div></div>')
    return out, stripe("#f6fbef", "#eef7e4")

def cta(s, D):
    b = ('<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 35%,#6BE01A,#46A800 75%)"></div>'
         '<div class="abs" style="left:0;right:0;top:330px;text-align:center;color:#fff">'
         '<div style="font-size:52px;opacity:.95;animation:rise .5s .1s both">아이디어에 불꽃, 설계는 내가</div>'
         '<div style="font-size:120px;line-height:1.2;margin-top:40px;text-shadow:0 8px 30px rgba(0,0,0,.18);animation:pop .6s .3s both">기초반 · 심화반<br>수업에서<br>만나요!</div></div>'
         '<div class="abs" style="left:90px;right:90px;top:1180px;background:#fff;border-radius:40px;border-bottom:12px solid #d9d9d9;padding:40px;text-align:center;animation:rise .5s .7s both">'
         f'<div style="font-size:54px">주말반 · 야간반</div><div style="font-size:46px;color:{GRN};margin-top:14px">줌 온라인 · 오프라인 공간</div></div>'
         '<div class="abs" style="left:0;right:0;top:1560px;text-align:center;color:#fff;font-size:44px;line-height:1.5;animation:rise .5s 1s both">프로젝트 AI 코디네이터 김종필<br>'
         '<span style="font-size:56px">aimakerlab.com</span></div>'
         + particles(60, 530, 700, 0.35, 620, seed=11, colors=["#fff", YEL, "#FF9600", "#1CB0F6", "#FF4B4B"]))
    return b, "#46A800"
