# Scene list: (tts text, caption text). tts uses Hangul readings; caption uses display text.
# visual types: clips / scroll / still / phone

SCENES = [
    dict(id="01_open", visual=dict(type="clips", files=["ms_2dd2fa1c"]), dim=True,
         card=dict(kind="title", kicker="바이브 코딩 프로젝트 수업",
                   title="외우는 수업 말고,<br><em>만들어서 세상에 내놓는</em> 수업",
                   sub="프로젝트 AI 코디네이터 김종필"),
         lines=[("외우는 수업 말고, 직접 만들어서 세상에 내놓는 수업.", None),
                ("바이브 코딩 프로젝트 수업을 소개합니다.", None)]),

    dict(id="02_why", visual=dict(type="scroll", file="aimakerlab_t"), label="AI Maker Lab · 프로젝트 교육 허브",
         lines=[("안녕하세요, 프로젝트 에이아이 코디네이터 김종필입니다.", "안녕하세요, 프로젝트 AI 코디네이터 김종필입니다."),
                ("정답을 외우는 시대에서, 질문하고 만드는 시대로.", None),
                ("커리큘럼을 따라가는 수업보다, 내 프로젝트를 끝까지 완성하는 수업이 필요합니다.", None)]),

    dict(id="03_vibe", visual=dict(type="scroll", file="vibecoding_t"), label="바이브 코딩",
         lines=[("문법을 외우는 코딩이 아니라, 말로 설명하고 에이아이와 함께 만드는 바이브 코딩.",
                 "문법을 외우는 코딩이 아니라, 말로 설명하고 AI와 함께 만드는 바이브 코딩."),
                ("저는 이렇게 기획부터 출시까지 직접 해 봤습니다.", None),
                ("그동안 만든 작품들을 보여 드릴게요.", None)]),

    dict(id="04_ch1", visual=dict(type="clips", files=["lp_931d15c4", "lp_4a07518d"]), dim=True,
         card=dict(kind="chapter", num="01", kicker="상용화 서비스", title="LingoPang 링고팡",
                   sub="기획 → 출시 → 홍보 → 수익화"),
         lines=[("첫 번째는 상용화까지 간 서비스, 링고팡입니다.", None)]),

    dict(id="05_lp_clips", visual=dict(type="clips", files=["lp_645c1718", "lp_abe6c584", "lp_26cbb918", "lp_484e0736"]),
         label="LingoPang · 유아·초등 한글·영어 학습",
         lines=[("네 살 아이부터 초등학생까지, 게임처럼 배우는 한글과 영어.", "4세부터 초등학생까지, 게임처럼 배우는 한글과 영어"),
                ("낱말 카드, 따라 쓰기, 퍼즐과 퀴즈로 하루 십오 분 학습 루틴을 만듭니다.",
                 "낱말 카드 · 따라 쓰기 · 퍼즐 · 퀴즈로 하루 15분 학습 루틴")]),

    dict(id="06_lp_web", visual=dict(type="scroll", file="lingopang_t"), label="lingopang.com · 웹 서비스",
         lines=[("한글 만 오천 개, 영어 이만 개가 넘는 단어와 문장을 담았고,", "한글 15,000개+ · 영어 20,000개+ 단어와 문장"),
                ("로그인 없이, 아이의 개인정보는 하나도 모으지 않습니다.", "로그인 없이, 아이 개인정보는 수집하지 않습니다")]),

    dict(id="07_lp_play", visual=dict(type="still", file="playstore"), label="Google Play 앱 출시",
         lines=[("웹으로 시작해서, 구글 플레이 앱으로 출시했고,", "웹으로 시작해 Google Play 앱으로 출시하고,")]),

    dict(id="08_lp_yt", visual=dict(type="still", file="youtube"), label="YouTube 쇼츠 홍보",
         lines=[("유튜브 쇼츠로 직접 알리고, 광고 수익으로 서버비를 충당합니다.", "YouTube 쇼츠로 직접 알리고, 광고 수익으로 운영합니다")]),

    dict(id="09_lp_wrap", visual=dict(type="clips", files=["lp_02d53c96", "lp_53fd8331", "lp_2df81c9f"]), label="LingoPang",
         lines=[("기획, 개발, 출시, 홍보, 수익화까지. 혼자 에이아이와 함께 해낸 전 과정입니다.",
                 "기획 · 개발 · 출시 · 홍보 · 수익화 — 혼자 AI와 함께 해낸 전 과정"),
                ("바로 이 과정을, 수업에서 그대로 경험합니다.", None)]),

    dict(id="10_ch2", visual=dict(type="clips", files=["ms_ce4f5356"]), dim=True,
         card=dict(kind="chapter", num="02", kicker="교육 플랫폼", title="배움을 프로젝트로",
                   sub="CareerPath · ReadingClue · teensparkai · AI Maker Lab"),
         lines=[("두 번째는, 배움을 프로젝트로 이어 주는 교육 플랫폼입니다.", None)]),

    dict(id="11_career", visual=dict(type="still", file="careerpath"), label="AI CareerPath · AI 진로 설계",
         lines=[("에이아이 커리어패스는 적성 검사로 시작해, 이백 개가 넘는 직업을 탐색하고,",
                 "AI CareerPath — 적성 검사로 시작해 200개+ 직업을 탐색하고,"),
                ("학년별 활동과 프로젝트로 나만의 커리어 패스를 설계합니다.", None)]),

    dict(id="12_reading", visual=dict(type="still", file="readingclue"), label="ReadingClue · 질문 중심 독서",
         lines=[("리딩클루는 질문 중심 독서 플랫폼입니다.", "ReadingClue — 질문 중심 독서 플랫폼"),
                ("이천삼백 권이 넘는 책 중에서, 한 주제를 입장이 다른 세 권으로 함께 읽고,",
                 "등록 도서 2,327권 · 한 주제를 입장이 다른 책 3권으로 병렬 독서"),
                ("가지 치는 토론을 거쳐, 논문과 캠페인, 서비스 기획안으로 완성합니다.",
                 "가지 치는 토론 → 논문 · 캠페인 · 서비스 기획안으로 완성")]),

    dict(id="13_spark", visual=dict(type="still", file="teenspark"), label="teensparkai · 청소년 AI 기획 스튜디오",
         lines=[("틴스파크 에이아이는 답을 주지 않습니다.", "teensparkai는 답을 주지 않습니다"),
                ("열린 질문으로 문제를 발견하고, 넓히고, 기획서로 착륙시킵니다.", "발견 → 확장 → 착륙, 열린 질문으로 기획서까지"),
                ("아이디어에 불꽃, 설계는 내가.", "아이디어에 불꽃, 설계는 내가")]),

    dict(id="14_ch3", visual=dict(type="clips", files=["ms_015b7ae2"]), dim=True,
         card=dict(kind="chapter", num="03", kicker="학생 프로젝트용 서비스", title="나라면 무엇을 바꿀까?",
                   sub="찐공AI · DeepQ · 마음씬 · 파도를 타라"),
         lines=[("세 번째는, 학생들이 먼저 써 보고 나라면 무엇을 바꿀까를 고민하게 만든 서비스들입니다.",
                 "학생이 먼저 써 보고 \"나라면 무엇을 바꿀까\"를 고민하게 만든 서비스")]),

    dict(id="15_zzin", visual=dict(type="scroll", file="zzingong_t"), label="찐공AI · 컴퓨터 비전 집중력 측정",
         lines=[("찐공 에이아이는 카메라로 딴짓을 감지해, 진짜 공부 시간만 잽니다.",
                 "찐공AI — 카메라로 딴짓을 감지해 '진짜 순공 시간'만 측정"),
                ("영상은 기기 밖으로 나가지 않고, 숫자만 기록합니다.", None)]),

    dict(id="16_deepq", visual=dict(type="still", file="deepq"), label="DeepQ 딥큐 · 서술형 문제 생성",
         lines=[("딥큐는 객관식 문제 사진 한 장을,", "DeepQ — 객관식 문제 사진 한 장을"),
                ("서술형 문제와 모범답안, 채점 루브릭으로 바꿉니다.", "서술형 문제 + 모범답안 + 채점 루브릭으로")]),

    dict(id="17_maum", visual=dict(type="phone", file="dramaro_m", scroll=True), label="마음씬 · AI 상황극 · 감정 표현",
         lines=[("마음씬은 에이아이와 상황극을 하며, 내 마음을 들여다보는 무대입니다.",
                 "마음씬 — AI와 상황극을 하며 내 마음을 들여다보는 무대")]),

    dict(id="18_maum_clips", visual=dict(type="clips", files=["ms_7ba3552e", "ms_3f73e185", "ms_9bf30d42"]), label="마음씬",
         lines=[("장면을 멈추고, 속말을 하고, 자리를 바꿔 보며 나만의 이야기를 완성하고,",
                 "멈추기 · 속말 · 자리 바꾸기로 나만의 이야기 완성"),
                ("위험 신호가 보이면 즉시 멈추고, 상담 연락처를 안내합니다.",
                 "위험 신호엔 즉시 멈춤 · 109 · 1388 · 1577-0199 안내")]),

    dict(id="19_stock", visual=dict(type="still", file="stock_w"), label="파도를 타라 · 투자 교육 게임",
         lines=[("파도를 타라는 실제 일 년 차트로 매수와 매도를 연습하고,", "파도를 타라 — 실제 1년 차트로 매수·매도 타이밍 연습"),
                ("에이아이와 수익률을 겨루는 투자 게임입니다.", "AI와 8턴 수익률 대결 · 100% 무료")]),

    dict(id="20_you", visual=dict(type="clips", files=["ms_893b33f3", "ms_cfd8e2a0"]), label="이제 여러분 차례",
         lines=[("이 모든 작품, 바이브 코딩으로 만들었습니다.", None),
                ("코딩을 몰라도 괜찮아요. 아이디어 하나면 시작할 수 있습니다.", None),
                ("여러분도 할 수 있어요.", None)]),

    dict(id="21_class", visual=dict(type="clips", files=["lp_931d15c4", "ms_659e932f"]), dim=True,
         card=dict(kind="classes"),
         lines=[("기초반에서는 아이디어로 첫 작품을 만들고,", None),
                ("심화반에서는 내 프로젝트를 실제 출시와 상용화까지 이어 갑니다.", None),
                ("주말반과 야간반, 줌 온라인과 오프라인 공간에서 함께합니다.", "주말반 · 야간반 | 줌 온라인 · 오프라인 공간")]),

    dict(id="22_end", visual=dict(type="clips", files=["ms_7590aa10"]), dim=True,
         card=dict(kind="end"),
         lines=[("기초반, 심화반 수업에서 만나요!", None)]),
]
