# Vertical (1080x1920) v11-style short: generated photo + partial web capture + caption bubble.
# narr = TTS text (Hangul readings), cap = on-screen caption (**word** = yellow highlight, | = line break)
# bg: ("img", name)  -> assets/gen/<name>.png (Higgsfield-generated, 9:16)
#     ("clip", path) -> existing vertical clip
#     ("card", kind) -> drawn infographic card
# shot: (kind, file, side) -> partial web capture. kind: phone | browser ; side: left | right | center

LP = "/Users/jongphilkim/Documents/GitHub/lingopang-youtube/03_소재_AI/01_영상클립-숏폼"

STUDENT = ("a 15-year-old Korean middle school girl with a short black bob haircut, wearing a navy hoodie, "
           "natural Korean face, photorealistic, warm soft natural light, shallow depth of field, "
           "cinematic 35mm photo, vertical 9:16 composition, the person filling the upper two thirds of the frame")

PROMPTS = {
    "g01_memorize": f"{STUDENT}, sitting at a study desk at night under a lamp, highlighting a thick textbook full of yellow highlights, tired determined face, stacks of workbooks",
    "g02_forget": f"{STUDENT}, sitting in a classroom after an exam, holding a test paper, blank confused face, pastel question-mark doodles floating around her head, soft daylight",
    "g03_made": f"{STUDENT}, proudly showing her own smartphone app to a laughing Korean boy classmate in a bright classroom, both excited, laptop open on the desk with code and app preview",
    "g04_coordinator": "over-the-shoulder view of a Korean male teacher in his 40s seen from behind, pointing at a big screen showing app wireframes, a small group of Korean teenagers with laptops looking at the screen, bright modern maker classroom, photorealistic, warm light, vertical 9:16, empty space at bottom third",
    "g05_zzingong": f"{STUDENT}, studying at a desk with a small webcam on the monitor, her smartphone turned face-down beside her, a soft glowing timer and fire-combo icon floating in the air, focused, cozy bedroom at evening",
    "g06_deepq": f"{STUDENT}, writing a long essay answer by hand on lined paper, a multiple-choice worksheet with circled answers beside it, thinking hard with pen near chin, library background",
    "g07_maum": f"{STUDENT}, standing alone on a small school theater stage under a warm spotlight, holding a script, a gentle brave expression, empty audience seats in soft shadow",
    "g08_stock": f"{STUDENT}, holding a smartphone showing a green rising stock chart, surprised and excited face, sitting on a sofa, soft afternoon light",
    "g09_reading": "three Korean middle school students (one girl with a short black bob in a navy hoodie) around a library table, each holding a different book, debating with sticky notes and question marks on the table, photorealistic, warm light, vertical 9:16, empty space at the bottom third",
    "g10_career": f"{STUDENT}, looking up at a glowing holographic map of career paths with small icons (doctor, designer, engineer, chef) connected by dotted lines, wonder on her face, dark blue evening room",
    "g11_spark": f"{STUDENT}, in front of a wall covered with colorful sticky notes and arrows, sticking a new note that says idea with a light-bulb doodle, sparks of light, energetic smile",
    "g12_demo": f"{STUDENT}, presenting her own app on a big screen at a school demo day, holding a microphone, classmates and parents clapping in the foreground, confetti, joyful",
}

# Keep the person clear of the phone mockup placed on the other side.
COMPOSE = {"g10_career": "left", "g09_reading": "right", "g11_spark": "left", "g05_zzingong": "right",
           "g06_deepq": "left", "g07_maum": "right", "g08_stock": "left"}
def full_prompt(name):
    p = PROMPTS[name]
    if name in COMPOSE:
        p += f", the person placed on the {COMPOSE[name]} half of the frame, the other half calmer background"
    return p + ", no text, no logos, no watermark"

SCENES = [
    # --- hook: why project classes (aimakerlab.com/why-project) ---
    dict(id="o01", bg=("img", "g01_memorize"), narr="에이아이가 정답을 몇 초 만에 알려 주는 시대. 외우기만 해서 될까요?",
         cap="AI가 **정답**을 알려 주는 시대|외우기만 해서 될까요?"),
    dict(id="o02", bg=("card", "d_why_now"), pill="왜 지금일까",
         narr="고교학점제, 이천이십팔 대입 개편. 입시는 이제 세특과 탐구 과정을 봐요.", cap="입시는 이제|**탐구 과정**을 봐요"),
    dict(id="o03", bg=("card", "d_world"), pill="세계는 이미",
         narr="세계의 교육도 이미 소논문과 프로젝트로 바뀌었어요.", cap="세계의 교육도|이미 **프로젝트**로"),
    dict(id="o04", bg=("card", "d_jobs"), pill="취업 시장",
         narr="취업도 마찬가지예요. 직접 만든 결과물로 실력을 증명해야 해요.", cap="취업도 **직접 만든 결과물**로|증명하는 시대"),
    dict(id="o05", bg=("card", "d_10vs150"), pill="같은 AI, 다른 아이",
         narr="에이아이에게 열 번 묻고 끝내는 아이와, 백오십 번 물고 늘어져 서비스를 만드는 아이.", cap="10번 묻고 끝내는 아이 vs|**150번** 물고 늘어지는 아이"),
    dict(id="o06", bg=("card", "d_need"), pill="그래서",
         narr="그래서 프로젝트 수업이 필요해요. 문제를 정하고, 끝까지 만들고, 고치며 배우는 수업.", cap="그래서 **프로젝트 수업**|정하고 · 만들고 · 고치며 배워요"),
    dict(id="o07", bg=("img", "g03_made"), badges=["세특", "면접 답변", "포트폴리오"],
         narr="직접 만든 결과물은, 세특도 되고 면접 답변도 돼요.", cap="직접 만든 결과물이|**세특 · 면접 · 포트폴리오**로"),
    dict(id="s05", bg=("card", "d_coordinator"), badges=["AI Maker Lab 대표", "프로젝트 코디네이터"],
         narr="안녕하세요, 프로젝트 에이아이 코디네이터 김종필입니다.", cap="프로젝트 AI 코디네이터|**김종필**입니다"),

    # --- education specs ---
    dict(id="e01", bg=("card", "d_years"), pill="교육 스펙",
         narr="개발 십사 년, 코딩과 에이아이 교육 십일 년.", cap="개발 **14년** · 교육 **11년**"),
    dict(id="e02", bg=("card", "d_where"), pill="교육 현장",
         narr="학교와 교육청, 대학, 기업에서 삼천 명 넘게 가르쳤어요.", cap="학교 · 대학 · 기업|**3,000명+** 수강생"),
    dict(id="e03", bg=("card", "d_programs"), pill="커리큘럼 개발",
         narr="자율주행, 스마트팜, 챗봇까지. 교육 프로그램과 책을 직접 만들었고,", cap="교육 프로그램과 **책**을|직접 만들었고"),
    dict(id="e04", bg=("card", "d_course"), pill="aimakerlab.com", shot=("phone", "curriculum", "left"),
         narr="지금은 바이브 에이아이 코딩 과정을 운영합니다.", cap="지금은 **바이브 AI 코딩**|과정을 운영합니다"),
    dict(id="e05", bg=("card", "d_dagachi"), pill="운영 사례 · 2026",
         narr="다가치학교에서는 문제 찾기부터 배포까지, 오 일 과정을 이끌었어요.", cap="문제 찾기부터 배포까지|**5일 과정** 운영"),

    # --- vibe coding process ---
    # one-page summary (was 3 cards: loop / conductor / 6 stairs)
    dict(id="v01", bg=("card", "d_process"), pill="바이브 코딩 프로세스",
         narr="바이브 코딩은 간단해요. 말하고, 보고, 다듬는다. 무엇을, 왜, 누구를 위해 만들지는 내가 정하고, 코드는 에이아이가 써요.",
         cap="**말한다 → 본다 → 다듬는다**|나는 지휘자, AI는 연주자"),
    dict(id="v04", bg=("card", "d_speed"), pill="왜 바이브 코딩인가",
         narr="칠 시간 걸리던 작은 서비스가, 수업에서는 삼십오 분.", cap="작은 서비스 하나|7시간 → **35분**"),
    dict(id="v05", bg=("card", "d_url"), pill="수업이 끝나면",
         narr="수업이 끝나면, 내 서비스 주소와 포트폴리오가 남아요.", cap="**내 서비스 주소**와|포트폴리오가 남아요"),

    # --- LingoPang (commercial) ---
    dict(id="s06", bg=("clip", f"{LP}/ai61.mp4"), pill="01 상용화 서비스", shot=("phone", "lingopang", "right"),
         narr="그리고 제가 직접 만들어 출시한, 링고팡.", cap="직접 만들어 출시한|**링고팡**"),
    dict(id="s07", bg=("card", "lp_launch"), pill="LingoPang 출시 과정",
         narr="웹으로 출시하고, 구글 플레이 앱, 유튜브 홍보까지.", cap="웹 → **구글 플레이** → 유튜브"),
    dict(id="s08", bg=("clip", f"{LP}/ai53.mp4"), pill="LingoPang", badges=["단어·문장 3만 개+", "완전 무료", "광고 수익 운영"],
         narr="광고 수익으로 운영하는, 진짜 서비스예요.", cap="광고 수익으로 운영하는|**진짜 서비스**"),

    # --- education platforms ---
    dict(id="s09", bg=("card", "d_career"), pill="02 AI CareerPath", shot=("phone", "careerpath", "right"),
         narr="에이아이와 진로 지도를 그리는 커리어패스.", cap="AI와 **진로 지도**를 그리는|커리어패스"),
    dict(id="s10", bg=("card", "d_reading"), pill="ReadingClue", shot=("phone", "readingclue", "left"),
         narr="한 주제를 세 권으로 읽고 토론하는 리딩클루.", cap="한 주제를 **세 권**으로 읽고 토론|리딩클루"),
    dict(id="s11", bg=("card", "d_spark"), pill="teensparkai", shot=("phone", "teenspark", "right"),
         narr="아이디어를 기획서로 키우는 틴스파크.", cap="아이디어를 **기획서**로 키우는|teensparkai"),

    # --- student services ---
    dict(id="s12", bg=("card", "d_zzingong"), pill="03 찐공AI", shot=("phone", "zzingong", "left"),
         narr="카메라가 딴짓을 잡아내는 찐공 에이아이.", cap="카메라가 **딴짓**을 잡아내는|찐공AI"),
    dict(id="s13", bg=("card", "d_deepq"), pill="DeepQ 딥큐", shot=("phone", "deepq", "right"),
         narr="객관식을 서술형으로 바꾸는 딥큐.", cap="객관식을 **서술형**으로|딥큐"),
    dict(id="s14", bg=("card", "d_maum"), pill="마음씬", shot=("phone", "dramaro", "left"),
         narr="에이아이와 상황극으로 마음을 말하는 마음씬.", cap="AI와 상황극으로 **마음을 말하는**|마음씬"),
    dict(id="s15", bg=("card", "d_stock"), pill="파도를 타라", shot=("phone", "stock", "right"),
         narr="차트로 투자를 배우는 파도를 타라.", cap="차트로 **투자**를 배우는|파도를 타라"),

    # --- payoff ---
    dict(id="s16", bg=("card", "wall"), narr="전부, 바이브 코딩으로 만들었어요.", cap="전부 **바이브 코딩**으로|만들었어요"),
    dict(id="s17", bg=("img", "g12_demo"), narr="코딩 몰라도 괜찮아요. 아이디어 하나면 돼요.", cap="코딩 몰라도 괜찮아요|**아이디어 하나면 돼요**"),
    dict(id="s18", bg=("img", "g03_made"), narr="여러분도 할 수 있어요.", cap="**여러분도** 할 수 있어요"),
    dict(id="s19", bg=("card", "classes"), narr="기초반은 첫 작품, 심화반은 출시까지.", cap="기초반은 **첫 작품**|심화반은 **출시까지**"),
    dict(id="s20", bg=("card", "cta"), narr="기초반, 심화반 수업에서 만나요!", cap=None),
]
