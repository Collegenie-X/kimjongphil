"""Hand-drawn (HTML/SVG) illustration backgrounds for scenes without a generated photo.
Canvas 1080x1920. Free areas: top band y≈260-780 (full width) and the column opposite the phone
(phone sits at x 50-430 for 'left' or x 650-1030 for 'right', y 800-1580). Caption covers y>1550.
Each function returns (body_html, background_css)."""

GRN, YEL, INK, BLUE, ORG, PUR, PINK = "#58CC02", "#FFD900", "#2B2B2B", "#1CB0F6", "#FF9600", "#CE82FF", "#FF4B4B"

def stripe(a, b): return f"repeating-linear-gradient(135deg,{a} 0 40px,{b} 40px 80px)"
def box(inner, x, y, w, border="#E5E5E5", rot=0, pad=28, bg="#fff", extra=""):
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;padding:{pad}px;background:{bg};border:5px solid {border};'
            f'border-bottom-width:12px;border-radius:36px;transform:rotate({rot}deg);box-shadow:0 14px 30px rgba(0,0,0,.08);{extra}">{inner}</div>')
def emo(e, x, y, size, rot=0):
    return f'<div class="abs" style="left:{x}px;top:{y}px;font-size:{size}px;line-height:1;transform:rotate({rot}deg)">{e}</div>'
def chip(t, col, x, y, size=40, rot=0):
    return (f'<div class="abs" style="left:{x}px;top:{y}px;white-space:nowrap;font-size:{size}px;color:#fff;background:{col};padding:12px 26px;'
            f'border-radius:999px;border-bottom:7px solid rgba(0,0,0,.18);transform:rotate({rot}deg)">{t}</div>')
def txt(t, x, y, size, col=INK, w=None, align="left"):
    ww = f"width:{w}px;" if w else ""
    return f'<div class="abs" style="left:{x}px;top:{y}px;{ww}font-size:{size}px;color:{col};text-align:{align};line-height:1.25">{t}</div>'
def arrow(x, y, size=80, rot=0, col="#BDBDBD"):
    return f'<div class="abs" style="left:{x}px;top:{y}px;font-size:{size}px;color:{col};transform:rotate({rot}deg)">➜</div>'

def d_coordinator():
    # badges from the scene sit at y 300-430; flow of the whole build in the middle
    b = emo("👨‍🏫", 430, 530, 200)
    steps = [("💡", "기획", ORG), ("💻", "바이브 코딩", BLUE), ("🚀", "출시", GRN), ("📈", "운영·수익화", PUR)]
    for i, (e, t, c) in enumerate(steps):
        x = 80 + (i % 2) * 480; y = 780 + (i // 2) * 330
        b += box(f'<div style="font-size:96px">{e}</div><div style="font-size:52px;color:{c};margin-top:8px">{t}</div>', x, y, 420,
                 border=c, rot=(-2, 2, 2, -2)[i], extra="text-align:center")
    b += arrow(495, 880, 70) + arrow(495, 1210, 70) + arrow(200, 1090, 70, 90)
    return b, stripe("#f6fbef", "#eef7e4")

def d_career():   # phone on the right
    b = txt('AI와 함께 그리는<br><span style="color:#7C5CFF">나만의 진로 지도</span>', 70, 270, 74)
    nodes = [("🧭", "적성 검사", "RIASEC + AI 리포트"), ("🔭", "직업 탐색", "200개+ 직업"), ("🗺️", "패스 설계", "학년별 활동·프로젝트"), ("📁", "포트폴리오", "자동 정리")]
    for i, (e, t, s) in enumerate(nodes):
        y = 520 + i * 250
        b += box(f'<div style="display:flex;gap:22px;align-items:center"><span style="font-size:80px">{e}</span>'
                 f'<div><div style="font-size:48px">{t}</div><div style="font-size:32px;color:#777">{s}</div></div></div>', 60, y, 540, border="#B9A8FF", pad=22)
        if i < 3: b += f'<div class="abs" style="left:150px;top:{y+178}px;width:8px;height:70px;background:repeating-linear-gradient(#B9A8FF 0 12px,transparent 12px 22px)"></div>'
    return b, stripe("#f4f1ff", "#ece7ff")

def d_reading():  # phone on the left
    b = txt('한 주제,<br><span style="color:#E8590C">세 권</span>으로 읽기', 470, 260, 76, w=560)
    books = [("📕", "찬성의 책", PINK), ("📗", "반대의 책", GRN), ("📘", "새 관점의 책", BLUE)]
    for i, (e, t, c) in enumerate(books):
        b += box(f'<div style="display:flex;gap:18px;align-items:center"><span style="font-size:78px">{e}</span><span style="font-size:46px">{t}</span></div>',
                 500, 570 + i * 180, 500, border=c, rot=(-2, 1, -1)[i], pad=20)
    b += arrow(700, 1105, 70, 90)
    b += box('<div style="font-size:44px">💬 근거 · 반론 · 새 문제</div><div style="font-size:52px;margin-top:10px;color:#E8590C">→ 📝 기획안 완성</div>',
             480, 1200, 540, border="#FFB38A", pad=24)
    b += chip("등록 도서 2,327권", ORG, 700, 470, 32, 3)
    return b, stripe("#fff6ee", "#ffeedd")

def d_spark():    # phone on the right
    notes = [("#FFF27A", -6, "급식 알레르기 앱?"), ("#FFC2E2", 4, "가방 무게 알림"), ("#B5F0FF", -3, "거북목 감시 웹캠"), ("#C9FFB5", 5, "위험 등굣길 지도")]
    b = ""
    for i, (c, r, t) in enumerate(notes):
        x = 70 + (i % 2) * 300; y = 280 + (i // 2) * 250
        b += f'<div class="abs" style="left:{x}px;top:{y}px;width:270px;height:210px;background:{c};transform:rotate({r}deg);box-shadow:0 10px 20px rgba(0,0,0,.12);padding:26px;font-size:36px;line-height:1.3;word-break:keep-all">{t}</div>'
    b += emo("💡", 700, 300, 230, 8)
    steps = [("🔍", "발견", "문제 찾기", ORG), ("🪐", "확장", "가능성 넓히기", PUR), ("🛬", "착륙", "기획서 완성", GRN)]
    for i, (e, t, s, c) in enumerate(steps):
        b += box(f'<div style="display:flex;gap:20px;align-items:center"><span style="font-size:76px">{e}</span><div><div style="font-size:50px;color:{c}">{t}</div>'
                 f'<div style="font-size:32px;color:#777">{s}</div></div></div>', 60, 830 + i * 240, 540, border=c, pad=20)
    return b, stripe("#fff9e6", "#fff2cc")

def d_zzingong():  # phone on the left
    b = txt('딴짓은 빼고<br><span style="color:#1CB0F6">진짜 공부만</span>', 470, 260, 76, w=560)
    b += box('<div style="font-size:34px;color:#777">오늘의 순공 시간</div><div style="font-size:92px;color:#1CB0F6;letter-spacing:-2px">2:47:12</div>'
             '<div style="font-size:34px;margin-top:6px">🔥 콤보 30분 · 무적 모드</div>', 480, 500, 540, border="#9AD8FF", extra="text-align:center")
    rows = [("📱", "핸드폰 보기", "−12분"), ("😶", "멍때리기", "−8분"), ("🚶", "자리 비움", "−5분")]
    for i, (e, t, m) in enumerate(rows):
        b += box(f'<div style="display:flex;align-items:center;gap:18px"><span style="font-size:60px">{e}</span><span style="font-size:42px;flex:1">{t}</span>'
                 f'<span style="font-size:42px;color:{PINK}">{m}</span></div>', 480, 860 + i * 165, 540, pad=18)
    b += chip("🔒 영상은 기기 밖으로 안 나가요", "#3C3C3C", 470, 1370, 32)
    return b, stripe("#eef8ff", "#e2f3ff")

def d_deepq():    # phone on the right
    b = txt('아는 것을,<br><span style="color:#7C5CFF">말할 수 있게</span>', 70, 260, 76)
    b += box('<div style="font-size:40px">Q. 광합성에 필요한 것은?</div><div style="font-size:40px;color:#777;margin-top:12px">① 물 ② 빛 ③ 이산화탄소 ④ 모두</div>',
             60, 520, 560, rot=-2, pad=24, extra="opacity:.85")
    b += emo("📸", 470, 470, 90, 10)
    b += arrow(290, 760, 80, 90, "#7C5CFF")
    b += box('<div style="font-size:42px;color:#7C5CFF">✍️ 서술형</div><div style="font-size:38px;margin-top:10px">광합성이 일어나는 과정을<br>근거를 들어 설명하시오.</div>',
             60, 880, 560, border="#B9A8FF", rot=1, pad=24)
    b += box('<div style="font-size:36px">📋 채점 루브릭 · 10점</div><div style="font-size:32px;color:#555;margin-top:8px">개념 3 · 근거 3 · 구성 2 · 표현 2</div>',
             60, 1180, 560, border="#E5E5E5", pad=22)
    b += chip("모범답안 포함", PUR, 360, 1130, 32, 4)
    return b, stripe("#f4f1ff", "#ece7ff")

def d_maum():     # phone on the left
    b = (f'<svg class="abs" style="left:470px;top:250px" width="580" height="560" viewBox="0 0 580 560">'
         '<defs><linearGradient id="sp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9A8" stop-opacity=".95"/><stop offset="1" stop-color="#FFE9A8" stop-opacity=".1"/></linearGradient></defs>'
         '<path d="M0 0 H580 V70 Q290 120 0 70 Z" fill="#B3263E"/><path d="M0 0 V500 Q40 320 60 70 Z" fill="#C8324D"/><path d="M580 0 V500 Q540 320 520 70 Z" fill="#C8324D"/>'
         '<polygon points="290,60 150,470 430,470" fill="url(#sp)"/><ellipse cx="290" cy="480" rx="210" ry="40" fill="#5A3B2E"/></svg>')
    b += emo("🧍‍♀️", 690, 420, 150) + emo("🎭", 850, 300, 90, 12)
    btns = [("⏸️", "멈추기"), ("💭", "속말 하기"), ("🔄", "자리 바꾸기")]
    for i, (e, t) in enumerate(btns):
        b += box(f'<div style="display:flex;align-items:center;gap:18px"><span style="font-size:62px">{e}</span><span style="font-size:46px">{t}</span></div>',
                 490, 860 + i * 165, 520, border="#F3A6C8", pad=18)
    b += box('<div style="font-size:30px;line-height:1.35">🛟 위험 신호엔 즉시 멈춤<br>109 · 1388 · 1577-0199 안내</div>', 490, 1360, 520, border="#9AD8FF", pad=18)
    return b, stripe("#fff0f6", "#ffe4ef")

def d_stock():    # phone on the right
    b = txt('차트로 배우는<br><span style="color:#2BB24C">실전 투자</span>', 70, 260, 76)
    pts = [(0, 300), (60, 280), (120, 310), (180, 240), (240, 260), (300, 190), (360, 210), (420, 130), (480, 150), (540, 60)]
    path = " ".join(f"{'M' if i == 0 else 'L'}{x + 20} {y + 20}" for i, (x, y) in enumerate(pts))
    b += (f'<div class="abs" style="left:60px;top:520px;width:580px;height:400px;background:#101820;border-radius:36px;box-shadow:0 14px 30px rgba(0,0,0,.2)">'
          f'<svg width="580" height="400" viewBox="0 0 580 380"><path d="{path}" fill="none" stroke="#3BE477" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"/>'
          '<circle cx="140" cy="330" r="18" fill="#1CB0F6"/><circle cx="500" cy="170" r="18" fill="#FF4B4B"/></svg></div>')
    b += chip("매수", BLUE, 110, 800, 34) + chip("매도", PINK, 470, 640, 34)
    b += box('<div style="display:flex;align-items:center;justify-content:space-between"><span style="font-size:80px">🙋</span><span style="font-size:52px">VS</span><span style="font-size:80px">🤖</span></div>'
             '<div style="font-size:40px;text-align:center;margin-top:8px">AI와 8턴 수익률 대결</div>', 60, 980, 560, border="#9BE7B0", pad=24)
    b += box('<div style="font-size:38px">📰 뉴스 쇼크 대응 · 투자 성향 분석</div>', 60, 1270, 560, pad=20)
    return b, stripe("#eefbf1", "#e1f7e7")

DRAWN_BASE = {"d_coordinator": d_coordinator, "d_career": d_career, "d_reading": d_reading, "d_spark": d_spark,
         "d_zzingong": d_zzingong, "d_deepq": d_deepq, "d_maum": d_maum, "d_stock": d_stock}

# ---------------- education spec ----------------
def big_num(n, unit, label, col, x, y, w=440):
    return box(f'<div style="font-size:150px;line-height:1;color:{col};letter-spacing:-4px">{n}<span style="font-size:64px">{unit}</span></div>'
               f'<div style="font-size:44px;margin-top:12px">{label}</div>', x, y, w, border=col, extra="text-align:center")

def d_years():
    b = big_num("14", "년", "💻 개발", BLUE, 70, 290, 450) + big_num("11", "년", "🧑‍🏫 코딩·AI 교육", ORG, 560, 320, 450)
    tl = [("2005", "군수항공 통신장비 개발", "#8A8A8A"), ("2014", "CAC 연구소장 · 코딩·메이커·AI 교육", BLUE),
          ("2019", "AI Maker Lab 대표", GRN), ("2020", "GPT 에세이 서비스 개발 리드", PUR), ("지금", "바이브 코딩 · 서비스 출시", ORG)]
    b += '<div class="abs" style="left:150px;top:760px;width:8px;height:740px;background:#E0E0E0;border-radius:4px"></div>'
    for i, (yr, t, c) in enumerate(tl):
        y = 740 + i * 150
        b += (f'<div class="abs" style="left:126px;top:{y+30}px;width:56px;height:56px;border-radius:50%;background:{c};border:8px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.15)"></div>'
              + txt(f'<span style="color:{c}">{yr}</span>', 210, y + 16, 50) + txt(t, 400, y + 24, 40, "#444", w=620))
    return b, stripe("#f2f8ff", "#e8f2ff")

def d_where():
    b = (chip("👩‍🎓 누적 3,000명+", ORG, 90, 270, 48, -3) + chip("📣 교육·연수 100회+", BLUE, 560, 300, 48, 3))
    groups = [("🏫", "학교 · 교육청", "인천·강화 130개 학교 · 세종시교육청 교사 연수 · SW 선도학교", GRN),
              ("🎓", "대학교", "가천대 AI 자율주행차 · 전북대 · 한양대 · 단국대 · 선문대", PUR),
              ("🏢", "기업 · 기관", "IBK시스템 · 현대해상 · 심텍 · 창업진흥원 · 창조경제혁신센터", BLUE)]
    for i, (e, t, s, c) in enumerate(groups):
        b += box(f'<div style="display:flex;gap:26px;align-items:center"><span style="font-size:110px">{e}</span><div>'
                 f'<div style="font-size:58px;color:{c}">{t}</div><div style="font-size:34px;color:#555;line-height:1.35;margin-top:8px;word-break:keep-all">{s}</div></div></div>',
                 70, 470 + i * 345, 940, border=c, rot=(-1, 1, -1)[i], pad=30)
    return b, stripe("#fff8ec", "#fff0d9")

def d_programs():
    tiles = [("🚗", "AI 자율주행차"), ("🌱", "스마트팜"), ("🤖", "AI 챗봇"), ("🥽", "VR 제작"), ("📡", "IoT 앱·웹"), ("🧠", "감성 분석 AI")]
    b = txt('직접 만든 <span style="color:#58CC02">교육 프로그램</span>', 70, 260, 66)
    for i, (e, t) in enumerate(tiles):
        x = 70 + (i % 3) * 320; y = 400 + (i // 3) * 330
        b += box(f'<div style="font-size:110px">{e}</div><div style="font-size:40px;margin-top:8px">{t}</div>', x, y, 290,
                 border=(GRN, BLUE, PUR, ORG, PINK, "#00B8A9")[i], rot=(-2, 1, -1, 2, -1, 1)[i], pad=24, extra="text-align:center")
    b += box('<div style="font-size:40px">📚 공동 저서</div><div style="font-size:46px;margin-top:10px">Maker Spirit CAR <span style="color:#999;font-size:36px">2016</span><br>SMART FARM <span style="color:#999;font-size:36px">2017</span></div>',
             70, 1100, 940, border=YEL, pad=30, bg="#FFFBE0")
    return b, stripe("#f6fbef", "#eef7e4")

def d_course():   # phone (curriculum page) on the left
    b = txt('<span style="color:#FF6B35">바이브 AI 코딩</span><br>과정 스펙', 470, 260, 72, w=580)
    rows = [("🎒", "초5 ~ 고3 · 교사 연수"), ("👥", "반당 최대 12명 · 3인 1팀"), ("⏱️", "3시간 · 6시간 · 16시간"), ("🧰", "v0 · Cursor · Claude · Vercel")]
    for i, (e, t) in enumerate(rows):
        b += box(f'<div style="display:flex;gap:18px;align-items:center"><span style="font-size:64px">{e}</span><span style="font-size:40px;word-break:keep-all">{t}</span></div>',
                 480, 500 + i * 190, 550, border="#FFB38A", pad=20)
    b += chip("📄 PDF 가이드 9종 · 템플릿 2종", "#FF6B35", 470, 1290, 32, -2)
    return b, stripe("#fff3ec", "#ffe9dd")

def d_dagachi():
    days = [("1일차", "🔎", "문제 찾기", "디자인 씽킹 · 아이디어 50선"), ("2일차", "🌱", "아이디어 키우기", "기획 워크시트 · 손그림"),
            ("3일차", "🍽️", "구조 이해 + 클론", "v0 → Vercel 공개 주소"), ("4일차", "🧰", "AI 도구 준비", "설치 · 안전 규칙"),
            ("5일차", "🖥️", "질문하며 완성", "Claude와 UI 완성")]
    b = txt('다가치학교 강남서초<br><span style="color:#FF6B35">「AI 발명품」 5일 과정</span>', 70, 260, 60)
    for i, (d, e, t, s) in enumerate(days):
        c = "#FF6B35" if i in (2, 4) else "#E5E5E5"
        b += box(f'<div style="display:flex;gap:20px;align-items:center"><span style="font-size:36px;color:#fff;background:{"#FF6B35" if i in (2,4) else "#9E9E9E"};border-radius:16px;padding:8px 16px">{d}</span>'
                 f'<span style="font-size:62px">{e}</span><div><div style="font-size:46px">{t}</div><div style="font-size:30px;color:#777">{s}</div></div></div>',
                 70, 470 + i * 205, 940, border=c, pad=20)
    return b, stripe("#fff3ec", "#ffe9dd")

# ---------------- vibe coding process ----------------
ME, AI = "#FF6B35", BLUE
def d_process():
    """One-page summary: talk -> see -> refine (loop) -> open, with who does each step (me = conductor, AI = player)."""
    steps = [("🗣️", "말한다", "손그림 + 주문서(프롬프트)", ORG, ("🧑‍🎓 나", ME)),
             ("👀", "본다", "AI가 화면·예시 데이터를 뚝딱", BLUE, ("🤖 AI", AI)),
             ("🔧", "다듬는다", "써 보고 \"버튼 더 크게!\"", PUR, ("🧑‍🎓 나", ME)),
             ("🌐", "오픈!", "Vercel 배포 → 내 서비스 주소", GRN, ("🎉 완성", GRN))]
    X, W_, Y0, STEP, BH = 60, 830, 280, 250, 190
    b = ""
    for i, (e, t, s, c, (role, rc)) in enumerate(steps):
        y = Y0 + i * STEP
        b += box(f'<div style="display:flex;align-items:center;gap:24px;height:{BH - 61}px">'
                 f'<span style="font-size:96px;line-height:1">{e}</span>'
                 f'<div style="flex:1"><div style="font-size:64px;color:{c};line-height:1.1">{t}</div>'
                 f'<div style="font-size:34px;color:#555;margin-top:8px;word-break:keep-all">{s}</div></div>'
                 f'<span style="font-size:34px;color:#fff;background:{rc};padding:10px 22px;border-radius:999px;white-space:nowrap;'
                 f'border-bottom:6px solid rgba(0,0,0,.18)">{role}</span></div>',
                 X, y, W_, border=c, pad=22, bg="#F4FFE9" if i == 3 else "#fff")
        b += (f'<div class="abs" style="left:{X - 18}px;top:{y - 18}px;width:62px;height:62px;border-radius:50%;background:{c};color:#fff;'
              f'font-size:38px;display:flex;align-items:center;justify-content:center;border:5px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.15)">{i + 1}</div>')
        if i < 3:
            b += f'<div class="abs" style="left:{X + 70}px;top:{y + BH + 4}px;font-size:46px;color:#C8C8C8;line-height:1">▼</div>'
    # loop: from 3 (refine) back up to 2 (see) until it feels right
    y2, y3 = Y0 + STEP + BH // 2, Y0 + 2 * STEP + BH // 2
    xr = X + W_
    b += (f'<svg class="abs" style="left:0;top:0" width="1080" height="1920"><defs><marker id="ah" viewBox="0 0 8 8" markerUnits="userSpaceOnUse" markerWidth="40" markerHeight="40" refX="7" refY="4" orient="auto">'
          f'<path d="M0,0 L8,4 L0,8 z" fill="{PUR}"/></marker></defs>'
          f'<path d="M{xr + 6},{y3} C{xr + 190},{y3} {xr + 190},{y2} {xr + 14},{y2}" fill="none" stroke="{PUR}" stroke-width="12" '
          f'stroke-dasharray="26 16" stroke-linecap="round" marker-end="url(#ah)"/></svg>')
    b += (f'<div class="abs" style="left:{xr + 72}px;top:{(y2 + y3) // 2 - 50}px;width:100px;height:100px;border-radius:50%;background:#fff;'
          f'border:5px solid {PUR};display:flex;align-items:center;justify-content:center;font-size:56px">🔁</div>')
    b += chip("마음에 들 때까지", PUR, xr - 236, (y2 + y3) // 2 - 34, 28)
    # who does what
    half = lambda e, t, s, c: (f'<div style="flex:1;text-align:center"><div style="font-size:46px;color:{c}">{e} {t}</div>'
                               f'<div style="font-size:32px;color:#666;margin-top:6px">{s}</div></div>')
    b += box('<div style="display:flex;align-items:center">' + half("🧑‍🎓", "나는 지휘자", "무엇을 · 왜 · 누구를 위해", ME)
             + '<div style="width:4px;height:90px;background:#E5E5E5;border-radius:2px"></div>' + half("🤖", "AI는 연주자", "코드를 쓰고 화면을 만든다", AI) + '</div>',
             X, Y0 + 4 * STEP - 10, 960, pad=24)
    return b, stripe("#fff8ec", "#fff0d9")

def d_speed():
    b = txt("작은 서비스 하나 만드는 시간", 70, 270, 54, w=940, align="center")
    b += box('<div style="font-size:46px">🐢 옛날 방식 · <b style="color:#FF4B4B">약 7시간</b></div>'
             '<div style="display:flex;gap:8px;margin-top:20px">' + "".join(f'<div style="flex:{f};height:70px;background:{c};border-radius:14px;color:#fff;font-size:28px;display:flex;align-items:center;justify-content:center">{t}</div>'
                                                               for f, c, t in [(2, "#FF8A80", "화면 2h"), (3, "#FF6F61", "서버 3h"), (1, "#FF5252", "오류 1h"), (1, "#E53935", "올리기")]) + '</div>',
             70, 400, 940, border="#FF8A80", pad=30)
    b += box('<div style="font-size:46px">🚀 바이브 코딩 · <b style="color:#58CC02">약 35분</b></div>'
             '<div style="display:flex;gap:8px;margin-top:20px;width:42%">' + "".join(f'<div style="flex:{f};height:70px;background:{c};border-radius:14px"></div>'
                                                                         for f, c in [(10, "#9BE15D"), (15, "#7ED957"), (5, "#58CC02"), (5, "#3FAE00")]) + '</div>'
             '<div style="font-size:30px;color:#666;margin-top:14px">v0 화면 10분 · 서버 15분 · 올리기 5분 · 테스트 5분</div>',
             70, 720, 940, border="#9BE7B0", pad=30)
    b += big_num("100", "회+", "AI에게 묻고 · 검증하고 · 책임지기", PUR, 70, 1060, 940)
    return b, stripe("#f4f1ff", "#ece7ff")

def d_url(mob):
    b = (f'<div class="browser" style="left:70px;top:280px;width:940px;transform:rotate(-1deg)"><div class="bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i>'
         f'<i style="background:#28c840"></i><span class="url" style="font-size:30px;color:#333">🔒 my-first-app.vercel.app</span></div>'
         f'<div style="height:520px;overflow:hidden"><img src="file://{mob}" style="width:100%"></div></div>')
    outs = [("🌐", "배포 URL"), ("🖼️", "Before / After"), ("🧾", "요청 기록"), ("📓", "디버거 성찰 일지")]
    for i, (e, t) in enumerate(outs):
        b += box(f'<div style="font-size:70px">{e}</div><div style="font-size:38px;margin-top:6px">{t}</div>', 70 + (i % 2) * 480, 940 + (i // 2) * 270, 460,
                 border=(GRN, BLUE, ORG, PUR)[i], pad=20, extra="text-align:center")
    return b, stripe("#f6fbef", "#eef7e4")

import os as _os
_MOB = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "assets", "mobile")
DRAWN = dict(DRAWN_BASE, d_years=d_years, d_where=d_where, d_programs=d_programs, d_course=d_course, d_dagachi=d_dagachi,
             d_process=d_process, d_speed=d_speed,
             d_url=lambda: d_url(f"{_MOB}/teenspark.png"))

# ---------------- motivation: why project classes (aimakerlab.com/why-project) ----------------
def d_why_now():
    b = txt('입시가 <span style="color:#FF6B35">바뀌었어요</span>', 70, 270, 84)
    rows = [("2025", "고교학점제 전면 시행", "과목별 탐구·프로젝트 수업 확대", BLUE),
            ("2028", "대입 개편 · 내신 5등급제", "등급 변별력↓ → 정성 평가 비중↑", PUR),
            ("세특", "학종 평가의 핵심 기록", "왜 시작했고 · 어떻게 탐구했나", ORG),
            ("논·서술", "평가 확대", "정답 고르기 → 근거로 논증하기", GRN)]
    for i, (k, t, s, c) in enumerate(rows):
        b += box(f'<div style="display:flex;gap:26px;align-items:center"><div style="min-width:220px;font-size:66px;color:{c};letter-spacing:-2px">{k}</div>'
                 f'<div><div style="font-size:46px">{t}</div><div style="font-size:32px;color:#666;margin-top:6px">{s}</div></div></div>',
                 70, 430 + i * 270, 940, border=c, pad=28)
    return b, stripe("#fff8ec", "#fff0d9")

def d_world():
    b = txt('세계의 교육은 이미<br><span style="color:#1CB0F6">프로젝트</span>로', 70, 270, 76)
    items = [("🌐", "IB 국제 바칼로레아", "4,000단어 소논문 · TOK"), ("🇬🇧", "영국 A-Level", "EPQ 자기 주도 프로젝트"), ("🇺🇸", "미국 AP Capstone", "연구 논문 · 발표"),
             ("🇫🇷", "프랑스 바칼로레아", "탐구 주제 구술시험"), ("🇫🇮", "핀란드", "현상 기반 학습"), ("🇸🇬", "싱가포르", "팀 Project Work 필수")]
    for i, (e, t, s) in enumerate(items):
        x = 70 + (i % 2) * 480; y = 520 + (i // 2) * 300
        b += box(f'<div style="font-size:70px">{e}</div><div style="font-size:42px;margin-top:6px">{t}</div><div style="font-size:30px;color:#666;margin-top:4px">{s}</div>',
                 x, y, 460, border=(BLUE, PUR, ORG, PINK, GRN, "#00B8A9")[i], rot=(-1, 1)[i % 2], pad=24)
    return b, stripe("#f2f8ff", "#e8f2ff")

def d_jobs():
    b = txt('취업도 <span style="color:#FF6B35">바뀌었어요</span>', 70, 270, 84)
    b += box('<div style="font-size:44px;color:#999">😮‍💨 과거의 채용</div>' + "".join(f'<div style="font-size:40px;color:#999;margin-top:14px;text-decoration:line-through">{t}</div>'
             for t in ["학점·자격증 스펙", "알고리즘 암기 코딩 테스트", "코드를 얼마나 빨리 치나"]), 70, 430, 940, pad=30, extra="opacity:.85")
    b += arrow(500, 790, 90, 90, "#FF6B35")
    b += box('<div style="font-size:48px;color:#FF6B35">🚀 AI 시대의 채용</div>' + "".join(f'<div style="font-size:42px;margin-top:14px">✔ {t}</div>'
             for t in ["직접 만든 결과물로 증명", "문제를 정의하고 설계", "AI에게 맡기고 검증"]), 70, 920, 940, border="#FF6B35", pad=30)
    return b, stripe("#fff3ec", "#ffe9dd")

def d_10vs150():
    b = box('<div style="font-size:150px;line-height:1;color:#AFAFAF">10<span style="font-size:60px">번</span></div>'
            '<div style="font-size:44px;color:#999;margin-top:12px">묻고 끝내는 아이</div><div style="font-size:32px;color:#AFAFAF;margin-top:12px">숙제 답 옮겨 적기<br>창을 닫으면 아무것도 안 남음</div>',
            70, 290, 450, pad=30, extra="text-align:center;opacity:.9")
    b += box('<div style="font-size:150px;line-height:1;color:#7C5CFF">150<span style="font-size:60px">번</span></div>'
             '<div style="font-size:44px;margin-top:12px">물고 늘어지는 아이</div><div style="font-size:32px;color:#555;margin-top:12px">실행하고 검증하고<br>작동하는 서비스가 남음</div>',
             560, 290, 450, border="#B9A8FF", pad=30, extra="text-align:center")
    qs = [("#1", "교실 공기질은 어떻게 측정해?"), ("#23", "이동평균을 쓰면 반응이 느려지지 않을까?"), ("#96", "세 반을 비교하는 대시보드 구조는?"), ("#150", "배포 후 피드백, 무엇부터 고칠까?")]
    for i, (n, q) in enumerate(qs):
        b += box(f'<div style="display:flex;gap:18px;align-items:center"><span style="font-size:34px;color:#fff;background:#7C5CFF;border-radius:14px;padding:6px 14px">{n}</span>'
                 f'<span style="font-size:36px;word-break:keep-all">{q}</span></div>', 70 + i * 20, 900 + i * 150, 900 - i * 20, border="#E5E5E5", pad=18)
    return b, stripe("#f4f1ff", "#ece7ff")

def d_need():
    b = txt('그래서<br><span style="color:#58CC02">프로젝트 수업</span>이 필요해요', 70, 270, 76)
    steps = [("🎯", "문제를 직접 정하고", "무엇을 왜 만들지 내가 정해요"), ("🛠️", "AI와 끝까지 만들고", "실제로 돌아가게"),
             ("🔧", "틀린 곳을 고치고", "찾고, 고치고, 다시 시험해요"), ("📁", "결과물로 남겨요", "세특 · 면접 · 포트폴리오")]
    for i, (e, t, s) in enumerate(steps):
        b += box(f'<div style="display:flex;gap:24px;align-items:center"><span style="font-size:40px;color:#fff;background:{GRN};border-radius:50%;width:64px;height:64px;display:flex;align-items:center;justify-content:center">{i+1}</span>'
                 f'<span style="font-size:76px">{e}</span><div><div style="font-size:48px">{t}</div><div style="font-size:32px;color:#666">{s}</div></div></div>',
                 70, 520 + i * 230, 940, border=GRN if i == 3 else "#E5E5E5", pad=24)
    return b, stripe("#f6fbef", "#eef7e4")

DRAWN.update(d_why_now=d_why_now, d_world=d_world, d_jobs=d_jobs, d_10vs150=d_10vs150, d_need=d_need)
