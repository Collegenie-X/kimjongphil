"""바이브 코딩 프로젝트 수업 — 숏폼 v4 편집 (1080x1920 · 30fps)

레이어
  · 그림 카드/키네틱/AI 빌더/사진/엔딩 → HTML 애니메이션을 rec/frames.mjs 로 프레임 단위 렌더링
  · AI 이미지(Higgsfield Nano Banana 2.1) → ffmpeg 켄번스 + 투명 오버레이(자막·배지)
  · 실제 서비스 화면 → 그림 카드 위에 폰 목업이 슬라이드 인 + 실제 페이지 스크롤
특수효과: 글리치(RGB 분리+노이즈) · 도장 쾅(흔들림+플래시) · 사진 셔터 플래시 · 공포 구간 그레이딩(채도↓·비네팅·그레인) · 다양한 xfade 전환
사운드: edge-tts 한국어 내레이션(InJoon) · 긴장/희망 음악 2곡(Higgsfield ElevenLabs Music) 교차 · 합성 효과음(휙·쾅·글리치·셔터·타이핑·팝·딩·라이저)

사용법: python3 video/build_v2/build4.py [출력.mp4]
"""
import os, sys, re, json, html, hashlib, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from scenes4 import SCENES
import cards4
from PIL import Image, ImageDraw

A = f"{HERE}/assets"; OUT = f"{HERE}/out4"; TTS = f"{HERE}/out/tts"; SFX = f"{OUT}/sfx"
for d in (OUT, TTS, SFX): os.makedirs(d, exist_ok=True)
FONT_B = f"{A}/fonts/Pretendard-Bold.ttf"; FONT_S = f"{A}/fonts/Pretendard-SemiBold.ttf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
EDGE = f"{HERE}/.venv/bin/edge-tts"; VOICE = os.environ.get("NARR_VOICE", "ko-KR-InJoonNeural")
W, H, FPS = 1080, 1920, 30
XF, LEAD, TAIL = 0.4, 0.1, 0.2
EXTRA = dict(card=0.2, photos=0.6, screen=0.45, builder=0.9, cta=1.8, kinetic=0.35, img=0.25, wall=0.4)
FINAL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "바이브코딩_프로젝트수업_숏폼_v4.mp4")

# 실제 화면 장면의 폰 (이전 숏폼과 같은 자리: 왼쪽 x50 / 오른쪽 x650, y740)
SW, SH, BZ, SR = 380, round(380 * 844 / 390), 14, 44
PY = 740
def phone_x(side): return 50 if side == "left" else 650

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(map(str, cmd))[:1500]); print(r.stderr[-3000:]); sys.exit(1)
    return r.stdout
def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).strip())

GRN, YEL, INK, RED = "#58CC02", "#FFD900", "#2B2B2B", "#E53935"
CSS = f"""@font-face{{font-family:Pret;src:url("file://{FONT_B}");font-weight:700}}
@font-face{{font-family:Pret;src:url("file://{FONT_S}");font-weight:600}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:transparent;font-family:Pret,"Apple SD Gothic Neo",sans-serif;font-weight:700;color:{INK};letter-spacing:-1px}}
.abs{{position:absolute}} i{{font-style:normal}}
.brand{{position:absolute;top:54px;left:0;right:0;text-align:center;font-size:30px;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.45)}}
.pill{{position:absolute;top:120px;left:50%;transform:translateX(-50%);white-space:nowrap;background:{GRN};color:#fff;font-size:46px;
  padding:16px 38px;border-radius:999px;border-bottom:8px solid #3f9a00;box-shadow:0 10px 24px rgba(0,0,0,.18);animation:drop .45s cubic-bezier(.2,1.3,.4,1) .05s both}}
.cap{{position:absolute;left:70px;right:70px;bottom:150px;text-align:center;background:#fff;border:5px solid #E5E5E5;border-bottom-width:13px;
  border-radius:44px;padding:34px 30px;font-size:64px;line-height:1.3;word-break:keep-all;box-shadow:0 18px 40px rgba(0,0,0,.2);animation:popc .5s cubic-bezier(.2,1.35,.4,1) .18s both}}
.cap b{{font-weight:inherit;background:linear-gradient({YEL},{YEL}) no-repeat 0 88%/0% 42%;padding:0 4px;animation:sweep .45s ease-out .62s both}}
.badge{{position:absolute;white-space:nowrap;font-size:40px;color:#fff;padding:14px 28px;border-radius:999px;border-bottom:8px solid rgba(0,0,0,.18);box-shadow:0 8px 20px rgba(0,0,0,.18)}}
.url{{position:absolute;white-space:nowrap;background:rgba(255,255,255,.97);color:#333;font-weight:600;font-size:26px;letter-spacing:-.3px;padding:8px 20px;
  border-radius:999px;box-shadow:0 8px 20px rgba(0,0,0,.25);transform:translateX(-50%);animation:rise .45s .5s both}}
.stamp{{position:absolute;left:50%;transform:translateX(-50%) rotate(-8deg);white-space:nowrap;border:12px solid {RED};color:{RED};font-size:88px;padding:6px 44px;
  border-radius:22px;background:rgba(255,255,255,.88);letter-spacing:-2px;box-shadow:0 20px 50px rgba(0,0,0,.35)}}
.redvig{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 45%,rgba(150,0,0,.42));animation:pulse 1.8s ease-in-out infinite}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.04) 2px,transparent 2px);background-size:60px 60px}}
.g2{{background-image:linear-gradient(rgba(124,255,79,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(124,255,79,.06) 2px,transparent 2px)}}
.hl{{background:linear-gradient({YEL},{YEL}) no-repeat 0 90%/100% 34%;color:#fff;padding:0 8px}}
.caret{{color:#fff;opacity:.8}}
.sk{{position:absolute;border-radius:12px;background:linear-gradient(90deg,#1c1d29 0%,#2c2e40 50%,#1c1d29 100%);background-size:600px 100%;animation:shimmer 1.1s linear infinite}}
.scanbar{{left:0;right:0;height:8px;background:#fff;box-shadow:0 0 30px 12px rgba(185,168,255,.9),0 0 80px 30px rgba(124,92,255,.5)}}
.pol{{width:860px;background:#fff;padding:20px 20px 0;border-radius:6px;box-shadow:0 30px 60px rgba(0,0,0,.55)}}
.pol img{{width:820px;height:615px;object-fit:cover;display:block}}
.pol .lab{{height:86px;display:flex;align-items:center;font-size:36px;color:#333;padding-left:6px}}
@keyframes rise{{from{{opacity:0;translate:0 70px;scale:.94}}to{{opacity:1;translate:0 0;scale:1}}}}
@keyframes drop{{from{{opacity:0;translate:0 -60px}}to{{opacity:1;translate:0 0}}}}
@keyframes pop{{0%{{opacity:0;scale:.55}}60%{{opacity:1;scale:1.07}}100%{{opacity:1;scale:1}}}}
@keyframes popc{{0%{{opacity:0;scale:.82;translate:0 40px}}100%{{opacity:1;scale:1;translate:0 0}}}}
@keyframes slam{{0%{{opacity:0;scale:1.6;translate:0 -30px}}100%{{opacity:1;scale:1;translate:0 0}}}}
@keyframes sweep{{from{{background-size:0% 42%}}to{{background-size:100% 42%}}}}
@keyframes stampin{{0%{{opacity:0;scale:3.2}}50%{{opacity:1;scale:.9}}72%{{scale:1.06}}100%{{opacity:1;scale:1}}}}
@keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
@keyframes shimmer{{from{{background-position:-600px 0}}to{{background-position:600px 0}}}}
@keyframes glitchx{{0%{{text-shadow:7px 0 #ff2a2a,-7px 0 #00e5ff;translate:-6px 0}}33%{{text-shadow:-9px 2px #ff2a2a,9px -2px #00e5ff;translate:5px 2px}}66%{{text-shadow:4px -2px #ff2a2a,-4px 2px #00e5ff;translate:-2px -1px}}100%{{text-shadow:none;translate:0 0}}}}
@keyframes burst{{0%{{opacity:0;translate:0 0;rotate:0deg}}8%{{opacity:1}}100%{{opacity:0;translate:var(--dx) var(--dy);rotate:var(--r)}}}}
@keyframes land{{0%{{opacity:0;scale:1.45;translate:0 -140px;filter:blur(6px)}}70%{{opacity:1;scale:.97;filter:blur(0)}}100%{{opacity:1;scale:1;translate:0 0}}}}
@keyframes dim{{to{{filter:brightness(.55) saturate(.7)}}}}
@keyframes reveal{{from{{clip-path:inset(0 0 100% 0)}}to{{clip-path:inset(0 0 0 0)}}}}
@keyframes scan{{from{{top:0;opacity:1}}95%{{opacity:1}}to{{top:100%;opacity:0}}}}
@keyframes fadeio{{0%{{opacity:0}}10%{{opacity:1}}85%{{opacity:1}}100%{{opacity:0}}}}
@keyframes ring{{0%,100%{{opacity:.35;scale:1}}50%{{opacity:1;scale:1.04}}}}
@keyframes prog{{from{{width:0}}to{{width:100%}}}}
"""
SEEK = """<script>
window.seek=function(t){document.querySelectorAll('.cnt').forEach(e=>{const s=+(e.dataset.s||0.3);let p=Math.min(1,Math.max(0,(t-s)/1.1));p=1-Math.pow(1-p,3);
 const v=Math.round(+e.dataset.to*p); e.textContent=e.dataset.fmt=='comma'?v.toLocaleString('en-US'):v});
 if(window.seek2)window.seek2(t)};
</script>"""
def page(body, bg="transparent"):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:{bg}}}</style></head><body>{body}{SEEK}</body></html>'
BRAND = '<div class="brand">AI Maker Lab · 바이브 코딩 프로젝트 수업</div>'

def cap_html(c):
    if not c: return ""
    t = html.escape(c).replace("|", "<br>")
    return '<div class="cap">' + re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t) + "</div>"

BADGE_COLORS = [("#1CB0F6", -4), ("#FF9600", 3), ("#CE82FF", -2)]
def badges_html(items, top=300):
    out = ""
    for i, t in enumerate(items):
        col, rot = BADGE_COLORS[i % 3]; x = [70, 470, 160][i % 3]; y = top + [0, 30, 130][i % 3]
        out += f'<div class="badge" style="left:{x}px;top:{y}px;background:{col};transform:rotate({rot}deg);animation:pop .45s cubic-bezier(.2,1.4,.4,1) {0.35 + i * 0.28:.2f}s both">{t}</div>'
    return out

def stamp_html(s, D):
    if not s.get("stamp"): return ""
    text, frac = s["stamp"][:2]; y = s["stamp"][2] if len(s["stamp"]) > 2 else 1180
    return f'<div class="stamp" style="top:{y}px;animation:stampin .42s cubic-bezier(.3,1.5,.5,1) {frac * D:.2f}s both">{html.escape(text)}</div>'

def stagger_js(n_base, step):
    return f"""<script>
[...document.querySelectorAll('#stage > *')].forEach((el,i)=>{{const d={n_base}+i*{step};
 el.style.animation=`rise .6s cubic-bezier(.2,.9,.3,1.15) ${{d}}s both`; el.querySelectorAll('.cnt').forEach(c=>c.dataset.s=d+0.25)}});
</script>"""

def card_body(name, D, n_hint=None):
    body, bg = cards4.CARDS[name]()
    body = re.sub(r'(font-size:150px;line-height:1;color:[^"]+">)(\d+)(<span)', lambda m: m.group(1) + f'<i class="cnt" data-to="{m.group(2)}">{m.group(2)}</i>' + m.group(3), body)
    n = body.count('<div class="abs"') or 6
    step = min(0.17, 0.42 * D / max(1, n))
    return f'<div id="stage">{body}</div>' + stagger_js(0.12, round(step, 3)), bg, 0.12 + n * step + 1.4

# ---------- 장면별 HTML ----------
def scene_layers(s, D):
    """returns list of (name, html, alpha, hold)"""
    k, fear = s["kind"], s.get("act") == "fear"
    vig = '<div class="redvig"></div>' if fear else ""
    pill = f'<div class="pill">{html.escape(s["pill"])}</div>' if s.get("pill") else ""
    if k == "card":
        body, bg, settle = card_body(s["card"], D)
        badges = badges_html(s["badges"]) if s.get("badges") else ""
        hold = D if (fear or s.get("stamp")) else min(D, settle)
        return [("main", page(body + vig + BRAND + pill + badges + stamp_html(s, D) + cap_html(s["cap"]), bg), False, hold)]
    if k == "screen":
        body, bg, settle = card_body(s["card"], D)
        x = phone_x(s["side"]) + SW // 2
        ov = f'<div class="url" style="left:{x}px;top:{PY - BZ - 60}px">🔒 {html.escape(s["url"])}</div>' + cap_html(s["cap"])
        return [("main", page(body + BRAND + pill, bg), False, min(D, settle)), ("ov", page(ov), True, 1.3)]
    if k == "img":
        ov = ('<div class="abs" style="left:0;right:0;top:0;height:420px;background:linear-gradient(rgba(0,0,0,.5),rgba(0,0,0,0))"></div>' + vig + BRAND + pill
              + (badges_html(s["badges"]) if s.get("badges") else "") + cap_html(s["cap"]))
        return [("ov", page(ov), True, D if fear else 1.8)]
    if k == "kinetic":
        body, bg = cards4.kinetic(s, D)
        return [("main", page(body + vig + BRAND + stamp_html(s, D) + cap_html(s.get("cap")), bg), False, D)]
    if k == "builder":
        body, bg = cards4.builder(s, D)
        return [("main", page(body + BRAND + '<div class="pill">바이브 코딩 실제 과정</div>' + cap_html(s["cap"]), bg), False, D)]
    if k == "photos":
        body, bg, _ = cards4.photos(s, D)
        return [("main", page(body + BRAND + pill + cap_html(s["cap"]), bg), False, D)]
    if k == "wall":
        body, bg = cards4.wall(s, D)
        return [("main", page(body + BRAND + cap_html(s["cap"]), bg), False, min(D, 2.6))]
    if k == "cta":
        body, bg = cards4.cta(s, D)
        return [("main", page(body + '<div class="brand">AI Maker Lab · 바이브 코딩 프로젝트 수업</div>', bg), False, D)]
    raise ValueError(k)

# ---------- 내레이션 ----------
AF = ("silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
      "loudnorm=I=-15:TP=-1.5:LRA=7")
def narration(s):
    out = f"{OUT}/{s['id']}_v.wav"
    for ext in (".m4a", ".wav", ".mp3"):
        mine = f"{A}/voice_mine/{s['id']}{ext}"
        if os.path.exists(mine):
            run(["ffmpeg", "-v", "error", "-y", "-i", mine, "-af", AF, "-ar", "48000", "-ac", "2", out]); return out
    rate = "+16%" if s.get("act") == "fear" else "+20%"
    key = hashlib.md5(f"{VOICE}|{rate}|{s['narr']}".encode()).hexdigest()[:10]
    mp3 = f"{TTS}/{s['id']}_{key}.mp3"
    if not os.path.exists(mp3):
        for _ in range(4):
            r = subprocess.run([EDGE, "--voice", VOICE, f"--rate={rate}", "--text", s["narr"], "--write-media", mp3], capture_output=True, text=True, timeout=90)
            if r.returncode == 0 and os.path.exists(mp3) and os.path.getsize(mp3) > 1000: break
        else: sys.exit(f"edge-tts failed {s['id']}: {r.stderr[-300:]}")
    run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af", AF, "-ar", "48000", "-ac", "2", out]); return out

# ---------- 효과음 합성 ----------
SFX_DEF = {
    "whoosh": "anoisesrc=d=0.7:c=pink:a=0.7,highpass=f=350,lowpass=f=5000,afade=t=in:d=0.38:curve=exp,afade=t=out:st=0.38:d=0.32,volume=0.8",
    "impact": "aevalsrc='0.95*exp(-4.2*t)*sin(2*PI*(46+80*exp(-12*t))*t)+0.35*exp(-30*t)*(random(0)*2-1)':d=1.5,lowpass=f=1800",
    "glitch": "anoisesrc=d=0.34:c=white:a=0.55,acrusher=bits=4:samples=8,tremolo=f=26:d=1,highpass=f=700,afade=t=out:st=0.24:d=0.1",
    "riser": "aevalsrc='0.42*pow(t/2.2,2)*(sin(2*PI*(160+420*t)*t)*0.5+(random(0)*2-1)*0.5)':d=2.2,highpass=f=300",
    "pop": "aevalsrc='0.7*exp(-28*t)*sin(2*PI*(650+600*exp(-22*t))*t)':d=0.22",
    "ding": "aevalsrc='0.45*exp(-3*t)*(sin(2*PI*1318.5*t)+0.6*sin(2*PI*1975.5*t))':d=1.3",
    "sparkle": "aevalsrc='0.22*exp(-3.5*t)*(sin(2*PI*2637*t)+sin(2*PI*3520*t)+sin(2*PI*4186*t*(1+0.01*sin(30*t))))':d=1.1",
    "shutter": "aevalsrc='0.8*exp(-90*t)*(random(0)*2-1)+0.6*exp(-60*(t-0.07))*gt(t,0.07)*(random(0)*2-1)':d=0.2,highpass=f=1200",
    "type": "aevalsrc='0.45*exp(-260*mod(t,0.071))*sin(2*PI*2300*t)*(0.6+0.4*random(0))':d=2.2,highpass=f=900,afade=t=out:st=1.9:d=0.3",
    "thud": "aevalsrc='0.8*exp(-9*t)*sin(2*PI*(70+60*exp(-15*t))*t)':d=0.6",
}
def make_sfx():
    for n, f in SFX_DEF.items():
        p = f"{SFX}/{n}.wav"
        if not os.path.exists(p): run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f, "-ar", "48000", "-ac", "2", p])

# ---------- 렌더 ----------
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS)]
KB = [("1.0+0.10*on/{n}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"), ("1.10-0.10*on/{n}", "iw/2-iw/zoom/2", "ih*0.35-ih/zoom*0.35"),
      ("1.04+0.08*on/{n}", "(iw-iw/zoom)*(0.35+0.3*on/{n})", "ih/2-ih/zoom/2")]

def fx_chain(s, D):
    f = []
    if s.get("act") == "fear": f += ["eq=saturation=0.86:contrast=1.06", "vignette=angle=0.6", "noise=alls=7:allf=t"]
    if s.get("glitch"): f += ["rgbashift=rh=-24:bh=24:rv=5:bv=-5:enable='lt(t,0.3)'", "noise=alls=75:allf=t:enable='lt(t,0.3)'"]
    shakes = [s["stamp"][1] * D + 0.12] if s.get("stamp") else []
    flashes = [(ts, 0.30) for ts in shakes]
    if s["kind"] == "photos": flashes += [(t, 0.16) for t in cards4.photo_flash_times(s, D)]
    if s["kind"] == "builder" and s["step"] == "build": flashes += [(0.80 * D, 0.22)]
    if shakes:
        ex = "+".join(f"exp(-6*(t-{t:.2f}))*between(t,{t:.2f},{t + 0.7:.2f})" for t in shakes)
        f += [f"scale=1134:2016,crop=1080:1920:x='27+24*sin(91*t)*({ex})':y='48+20*cos(67*t)*({ex})'"]
    if flashes:
        ex = "+".join(f"{a}*exp(-12*(t-{t:.2f}))*gte(t,{t:.2f})" for t, a in flashes)
        f += [f"eq=brightness='{ex}':eval=frame"]
    return ",".join(f + ["format=yuv420p"])

def bezel_png(side):
    p = f"{OUT}/bezel_{side}.png"
    if not os.path.exists(p):
        x = phone_x(side)
        hp = p[:-4] + ".html"
        open(hp, "w").write(page(f'<div class="abs" style="left:{x - BZ}px;top:{PY - BZ}px;width:{SW + 2 * BZ}px;height:{SH + 2 * BZ}px;border-radius:{SR + BZ}px;'
                                 f'background:#111;box-shadow:0 30px 60px rgba(0,0,0,.35),inset 0 0 0 3px #2c2c30"></div>'
                                 f'<div class="abs" style="left:{x + SW // 2 - 50}px;top:{PY + 10}px;width:100px;height:28px;border-radius:16px;background:#111;z-index:2"></div>'))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", f"--window-size={W},{H}",
                        "--default-background-color=00000000", f"--screenshot={p}", "file://" + hp], capture_output=True, timeout=60)
    m = f"{OUT}/mask.png"
    if not os.path.exists(m):
        im = Image.new("L", (SW, SH), 0); ImageDraw.Draw(im).rounded_rectangle([0, 0, SW - 1, SH - 1], radius=SR, fill=255); im.save(m)
    return p, m

def seq(d, alpha):  # 프레임 시퀀스 입력
    return ["-framerate", str(FPS), "-i", f"{d}/f%05d.{'png' if alpha else 'jpg'}"]

def compose(args):
    i, s, D, layers = args; sid, k = s["id"], s["kind"]; out = f"{OUT}/{sid}.mp4"
    L = {name: f"{OUT}/fr_{sid}_{name}" for name, *_ in layers}
    hold = lambda: f"tpad=stop_mode=clone:stop_duration={D + 1:.2f},trim=duration={D:.3f},setpts=PTS-STARTPTS"
    fx = fx_chain(s, D)
    if k == "img":
        n = int(D * FPS) + 2; z, x, y = (m.format(n=n) for m in KB[i % len(KB)])
        fc = (f"[0]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS},setsar=1[bg];"
              f"[1]format=rgba,{hold()}[o];[bg][o]overlay=0:0:shortest=1,{fx}[v]")
        cmd = ["-loop", "1", "-framerate", str(FPS), "-t", f"{D + 0.5:.2f}", "-i", f"{A}/img/{s['img']}.png", *seq(L['ov'], True)]
    elif k == "screen":
        bez, mask = bezel_png(s["side"]); px = phone_x(s["side"]); sgn = -1 if s["side"] == "left" else 1
        iw, ih = Image.open(f"{A}/screens/{s['screen']}.png").size; sh = round(ih * SW / iw)
        Ls = max(0, min(sh - SH, int(110 * D))); a, b = 1.5, max(0.5, D - 2.1); p = f"clip((t-{a})/{b},0,1)"
        slide = f"{sgn}*820*pow(1-min(t/0.65,1),3)"
        fc = (f"[0]{hold()}[c];[2]scale={SW}:-2,crop={SW}:{SH}:0:'{Ls}*(3*pow({p},2)-2*pow({p},3))'[s0];[s0][3]alphamerge[s];"
              f"[c][1]overlay=x='{slide}':y=0[c1];[c1][s]overlay=x='{px}+{slide}':y={PY}[c2];[4]format=rgba,{hold()}[o];[c2][o]overlay=0:0,{fx}[v]")
        cmd = [*seq(L['main'], False), "-loop", "1", "-framerate", str(FPS), "-i", bez, "-loop", "1", "-framerate", str(FPS), "-i", f"{A}/screens/{s['screen']}.png",
               "-loop", "1", "-framerate", str(FPS), "-i", mask, *seq(L['ov'], True)]
    else:
        fc = f"[0]{hold()},{fx}[v]"
        cmd = [*seq(L['main'], False)]
    run(["ffmpeg", "-v", "error", "-y", *cmd, "-filter_complex", fc, "-map", "[v]", "-t", f"{D:.3f}", *ENC, out])
    print(f"{sid:5s} {k:8s} {D:5.2f}s", flush=True)
    return out

def main():
    make_sfx()
    with ThreadPoolExecutor(6) as ex: wavs = list(ex.map(narration, SCENES))
    Ds = []
    for s, w in zip(SCENES, wavs):
        Ds.append(round(LEAD + dur(w) + TAIL + XF + EXTRA[s["kind"]], 3))
    # 1) HTML 레이어 → 프레임
    jobs, all_layers = [], []
    for s, D in zip(SCENES, Ds):
        layers = scene_layers(s, D); all_layers.append(layers)
        for name, htm, alpha, hold in layers:
            d = f"{OUT}/fr_{s['id']}_{name}"; hp = d + ".html"
            key = hashlib.md5((htm + f"{D}{hold}").encode()).hexdigest()
            stamp = d + "/.key"
            if os.path.exists(stamp) and open(stamp).read() == key: continue
            if os.path.isdir(d): shutil.rmtree(d)
            open(hp, "w").write(htm)
            jobs.append(dict(html=hp, out=d, dur=D, hold=hold, alpha=alpha, key=key))
    if jobs:
        jf = f"{OUT}/jobs.json"; json.dump(jobs, open(jf, "w"))
        print(f"rendering {len(jobs)} layers …", flush=True)
        r = subprocess.run(["node", f"{HERE}/rec/frames.mjs", jf], capture_output=True, text=True)
        if r.returncode: print(r.stdout[-2000:], r.stderr[-3000:]); sys.exit(1)
        for j in jobs: open(j["out"] + "/.key", "w").write(j["key"])
    # 2) 장면 합성
    with ThreadPoolExecutor(4) as ex: parts = list(ex.map(compose, [(i, s, D, L) for i, (s, D, L) in enumerate(zip(SCENES, Ds, all_layers))]))
    # 3) 전환
    vins, fc, starts, t, prev = [], [], [], 0.0, "0:v"
    for k, (mp4, D) in enumerate(zip(parts, Ds)):
        vins += ["-i", mp4]; starts.append(t)
        if k:
            fc.append(f"[{prev}][{k}:v]xfade=transition={SCENES[k].get('tin', 'fade')}:duration={XF}:offset={t:.3f}[x{k}]"); prev = f"x{k}"
        t += D - XF
    total = t + XF; vid = f"{OUT}/video.mp4"
    run(["ffmpeg", "-v", "error", "-y", *vins, "-filter_complex", ";".join(fc), "-map", f"[{prev}]", *ENC, vid])
    # 4) 오디오
    mix_audio(vid, wavs, starts, Ds, total)
    print(f"DONE {os.path.abspath(FINAL)} {dur(FINAL):.1f}s")

def scene_start(k, starts):  # 전환이 끝나 장면이 온전히 보이는 시점
    return starts[k] + (XF if k else 0)

def mix_audio(vid, wavs, starts, Ds, total):
    ins, af, idx = ["-i", vid], [], 1
    # 내레이션
    nar = []
    for k, w in enumerate(wavs):
        ins += ["-i", w]; ms = int((scene_start(k, starts) + LEAD) * 1000)
        af.append(f"[{idx}:a]adelay={ms}|{ms}[n{k}]"); nar.append(f"[n{k}]"); idx += 1
    af.append("".join(nar) + f"amix=inputs={len(nar)}:normalize=0:duration=longest,apad,atrim=0:{total:.3f},asplit=2[nar][sc]")
    # 음악: 긴장(공포 구간) ↔ 희망(나머지)
    first_main = next(k for k, s in enumerate(SCENES) if s.get("act") == "main")
    Tm = starts[first_main] + XF * 0.5
    fear_windows = []
    for k, s in enumerate(SCENES):
        if k > first_main and s.get("act") == "fear":
            a, b = starts[k], starts[k] + Ds[k]
            if fear_windows and abs(fear_windows[-1][1] - XF - a) < 0.6: fear_windows[-1] = (fear_windows[-1][0], b)
            else: fear_windows.append((a, b))
    ins += ["-i", f"{A}/music_tense.mp3"]; ti = idx; idx += 1
    ins += ["-i", f"{A}/music_hope.mp3"]; hi = idx; idx += 1
    nseg = 1 + len(fear_windows)
    af.append(f"[{ti}:a]asplit={nseg}" + "".join(f"[t{j}]" for j in range(nseg)))
    af.append(f"[t0]atrim=0:{Tm + 0.6:.3f},asetpts=N/SR/TB,afade=t=in:d=0.6,afade=t=out:st={Tm - 0.5:.3f}:d=1.0,volume=0.42[m0]")
    segs = ["[m0]"]
    for j, (a, b) in enumerate(fear_windows, 1):
        L = b - a; off = 20 + 12 * j
        af.append(f"[t{j}]atrim={off}:{off + L:.3f},asetpts=N/SR/TB,afade=t=in:d=0.5,afade=t=out:st={L - 0.6:.3f}:d=0.6,volume=0.42,"
                  f"adelay={int(a * 1000)}|{int(a * 1000)}[m{j}]"); segs.append(f"[m{j}]")
    hope_len = total - Tm
    dips = "*".join(f"(1-0.75*clip((t-{a - Tm:.2f})/0.6,0,1)*clip(({b - Tm:.2f}-t)/0.6,0,1))" for a, b in fear_windows) or "1"
    if hope_len > 138:
        af.append(f"[{hi}:a]asplit=2[h1][h2];[h1]atrim=0:139,asetpts=N/SR/TB,afade=t=out:st=136:d=3[h1b];"
                  f"[h2]atrim=24:{24 + hope_len - 134:.3f},asetpts=N/SR/TB,afade=t=in:d=3,adelay=134000|134000[h2b];[h1b][h2b]amix=inputs=2:normalize=0[hraw]")
    else:
        af.append(f"[{hi}:a]atrim=0:{hope_len:.3f},asetpts=N/SR/TB[hraw]")
    af.append(f"[hraw]volume='0.34*{dips}':eval=frame,afade=t=in:d=0.4,afade=t=out:st={hope_len - 3:.3f}:d=3,adelay={int(Tm * 1000)}|{int(Tm * 1000)}[mh]"); segs.append("[mh]")
    af.append("".join(segs) + f"amix=inputs={len(segs)}:normalize=0:duration=longest,atrim=0:{total:.3f}[mus]")
    af.append("[mus][sc]sidechaincompress=threshold=0.03:ratio=7:attack=15:release=380[musd]")
    # 효과음 이벤트
    ev = []
    for k, (s, D) in enumerate(zip(SCENES, Ds)):
        t0 = starts[k]; tin = s.get("tin", "fade")   # 장면 클립의 0초 = 전환 시작 시점
        if k:
            if tin in ("pixelize", "hblur"): ev.append(("glitch", starts[k], 0.9))
            elif tin in ("slideleft", "smoothleft", "slideup", "squeezeh", "zoomin", "circleopen", "radial"): ev.append(("whoosh", starts[k] - 0.12, 0.55))
            elif tin == "fadewhite": ev += [("riser", starts[k] - 1.9, 0.75), ("sparkle", starts[k] + 0.2, 0.6)]
            elif tin == "fadeblack": ev.append(("thud", starts[k] + 0.1, 0.8))
        if s.get("glitch"): ev.append(("glitch", t0, 0.9))
        if s.get("stamp"): ev.append(("impact", t0 + s["stamp"][1] * D, 1.0))
        if s.get("badges"): ev += [("pop", t0 + 0.35 + i * 0.28, 0.7) for i in range(len(s["badges"]))]
        if s["kind"] == "photos": ev += [("shutter", t0 + t - 0.05, 0.8) for t in cards4.photo_flash_times(s, D)]
        if s["kind"] == "screen": ev.append(("pop", t0 + 0.55, 0.45))
        if s["kind"] == "builder":
            ev.append(("type", t0 + 0.03 * D + 0.2, 0.55))
            if s["step"] == "build": ev += [("whoosh", t0 + 0.55 * D, 0.6), ("sparkle", t0 + 0.8 * D, 0.8)]
            else: ev += [("pop", t0 + 0.47 * D, 0.8), ("ding", t0 + 0.70 * D, 0.8), ("sparkle", t0 + 0.72 * D, 0.6)]
        if s["kind"] == "kinetic" and s.get("style") == "qs": ev += [("thud", t0 + 0.08 * D + i * 0.26 * D, 0.8) for i in range(len(s["qs"]))]
        if s["kind"] == "kinetic" and s.get("style") in ("mission", "chapter"): ev.append(("impact", t0 + 0.35, 0.6))
        if s["kind"] == "cta": ev += [("impact", t0 + 0.3, 0.8), ("sparkle", t0 + 0.4, 0.8)]
        if s["kind"] == "wall": ev.append(("whoosh", t0 + 0.05, 0.5))
    names = sorted({e[0] for e in ev}); sfx_lbl = []
    for n in names:
        es = [e for e in ev if e[0] == n and e[1] >= 0]
        ins += ["-i", f"{SFX}/{n}.wav"]; si = idx; idx += 1
        af.append(f"[{si}:a]asplit={len(es)}" + "".join(f"[{n}{j}]" for j in range(len(es))))
        for j, (_, t, v) in enumerate(es):
            ms = int(t * 1000); af.append(f"[{n}{j}]volume={v},adelay={ms}|{ms}[e_{n}{j}]"); sfx_lbl.append(f"[e_{n}{j}]")
    af.append("".join(sfx_lbl) + f"amix=inputs={len(sfx_lbl)}:normalize=0:duration=longest,volume=0.55,atrim=0:{total:.3f}[fx]")
    af.append("[nar][musd][fx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[a]")
    fcf = f"{OUT}/audio_graph.txt"; open(fcf, "w").write(";\n".join(af))
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", fcf, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total:.3f}", FINAL])

if __name__ == "__main__": main()
