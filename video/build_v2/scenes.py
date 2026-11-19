# 바이브 코딩 프로젝트 수업 — 숏폼 v3 (1080x1920)
# 앞부분(도입 3장면)만 AI 이미지(Higgsfield · Nano Banana 2.1), 나머지는 실제 서비스 화면.
#   kind="img"    → assets/img/<img>.png  (AI 생성 이미지, 켄번스)
#   kind="screen" → assets/screens/<screen>.png  (rec/capture.mjs 로 찍은 실제 모바일 화면, 폰 목업 안에서 스크롤)
#   kind="wall"   → 실제 화면들을 모은 벽
#   kind="cta"    → 엔딩 안내
# narr = 내레이션(읽기용 표기), cap = 자막(**강조**, | 줄바꿈), tag = 상단 라벨, url = 실제 주소 표시

SCENES = [
    # ---------- 도입: AI 이미지 ----------
    dict(id="s01", kind="img", img="s01",
         narr="에이아이가 정답을 몇 초 만에 알려 주는 시대. 아직도 외우기만 하나요?",
         cap="AI가 **정답**을 알려 주는 시대|아직도 외우기만 하나요?"),
    dict(id="s02", kind="img", img="s03", tag="그래서 필요한 것",
         narr="이제 필요한 건, 내가 문제를 찾고 끝까지 만들어 보는 경험이에요.",
         cap="내가 문제를 찾고|**끝까지 만들어 보는 경험**"),
    dict(id="s03", kind="img", img="s04", tag="바이브 코딩",
         narr="바이브 코딩은 문법을 외우지 않아요. 말로 설명하면, 에이아이가 코드를 써요.",
         cap="말로 설명하면|**AI가 코드를 써요**"),

    # ---------- 실제 화면 ----------
    dict(id="s04", kind="screen", screen="aimakerlab", tag="AI Maker Lab", url="aimakerlab.com",
         narr="안녕하세요, 프로젝트 에이아이 코디네이터 김종필입니다. 지금 바이브 에이아이 코딩 과정을 운영하고 있어요.",
         cap="프로젝트 AI 코디네이터 **김종필**|바이브 AI 코딩 과정 운영"),
    dict(id="s05", kind="screen", screen="lingopang", tag="01 · LingoPang", url="lingopang.com",
         narr="제가 직접 만들어 출시한 링고팡. 아이들이 하루 십오 분, 한글과 영어를 배우는 서비스예요.",
         cap="직접 만들어 출시한|**링고팡** · 한글·영어 학습"),
    dict(id="s06", kind="screen", screen="playstore", tag="Google Play 출시", url="play.google.com",
         narr="웹으로 시작해서, 구글 플레이 앱까지 직접 출시했어요.",
         cap="웹에서 시작해|**구글 플레이 앱**까지 출시"),
    dict(id="s07", kind="screen", screen="readingclue", tag="02 · ReadingClue", url="readingclue.com",
         narr="책을 읽고 질문을 만드는 독서 플랫폼, 리딩클루.",
         cap="책에서 **질문**을 찾는|리딩클루"),
    dict(id="s08", kind="screen", screen="teenspark", tag="teensparkai", url="teenspark.vercel.app",
         narr="아이디어를 기획서로 키우는, 틴스파크.",
         cap="아이디어를 **기획서**로 키우는|틴스파크"),
    dict(id="s09", kind="screen", screen="zzingong", tag="03 · 찐공AI", url="zzingongai.vercel.app",
         narr="카메라로 진짜 공부 시간만 재는, 찐공 에이아이.",
         cap="**진짜 공부 시간**만 재는|찐공AI"),
    dict(id="s10", kind="screen", screen="deepq", tag="DeepQ 딥큐", url="deepq-omega.vercel.app",
         narr="객관식 문제를 서술형으로 바꿔 주는, 딥큐.",
         cap="객관식을 **서술형**으로|딥큐"),
    dict(id="s11", kind="screen", screen="maum", tag="마음씬", url="teen-dramaro.vercel.app",
         narr="에이아이와 상황극을 하며 마음을 말하는, 마음씬.",
         cap="AI와 상황극으로|**마음을 말하는** 마음씬"),
    dict(id="s12", kind="screen", screen="stock", tag="파도를 타라", url="stock-simulation-delta.vercel.app",
         narr="실제 차트로 투자 타이밍을 연습하는, 파도를 타라.",
         cap="실제 차트로 **투자**를 배우는|파도를 타라"),
    dict(id="s13", kind="wall",
         screens=["lingopang", "playstore", "readingclue", "teenspark", "zzingong", "deepq", "maum", "stock"],
         narr="전부 바이브 코딩으로 직접 만들고, 지금도 운영 중인 서비스예요.",
         cap="전부 **바이브 코딩**으로|직접 만들어 운영 중"),

    # ---------- 엔딩 ----------
    dict(id="s14", kind="cta",
         narr="코딩 몰라도 괜찮아요. 기초반은 첫 작품, 심화반은 출시까지. 수업에서 만나요!",
         cap=None),
]
