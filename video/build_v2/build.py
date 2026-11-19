"""바이브 코딩 프로젝트 수업 — 숏폼 v3 편집 스크립트 (1080x1920, 30fps)

입력
  assets/img/*.png      도입부 AI 이미지 (Higgsfield · Nano Banana 2.1)
  assets/screens/*.png  실제 서비스 화면 (rec/capture.mjs 로 캡처)
  assets/music.mp3      배경음 (Higgsfield · ElevenLabs Music)
  내레이션              edge-tts 한국어 신경망 음성 (기본 ko-KR-InJoonNeural) — 텍스트가 Microsoft 음성 서비스로 전송됨
                        직접 녹음한 파일이 assets/voice_mine/<장면id>.(m4a|wav|mp3) 에 있으면 그걸 우선 사용
편집: 켄번스 / 폰 목업 스크롤 + 자막·라벨(headless Chrome) + xfade 전환 + 오디오 믹스(ffmpeg)

사용법: python3 video/build_v2/build.py [출력.mp4]
환경변수: NARR_VOICE=ko-KR-HyunsuMultilingualNeural  NARR_RATE=+8%
"""
import os, sys, re, html, hashlib, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from scenes import SCENES
from PIL import Image, ImageDraw

A = f"{HERE}/assets"; OUT = f"{HERE}/out"; TTS = f"{OUT}/tts"
for d in (OUT, TTS): os.makedirs(d, exist_ok=True)
FONT_B = f"{A}/fonts/Pretendard-Bold.ttf"; FONT_S = f"{A}/fonts/Pretendard-SemiBold.ttf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
EDGE = f"{HERE}/.venv/bin/edge-tts"
VOICE = os.environ.get("NARR_VOICE", "ko-KR-InJoonNeural"); RATE = os.environ.get("NARR_RATE", "+8%")
W, H, FPS = 1080, 1920, 30
XF, LEAD, TAIL = 0.35, 0.25, 0.35
FINAL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "바이브코딩_프로젝트수업_숏폼_v3.mp4")

# 폰 목업 (실제 화면 장면)
SW, SH = 640, round(640 * 844 / 390)      # 화면 영역 640x1385
BZ = 20                                    # 베젤
PX, PY = (W - SW) // 2, 292                # 화면 좌상단
SR = 58                                    # 화면 모서리 반경

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(map(str, cmd))[:900]); print(r.stderr[-2500:]); sys.exit(1)
    return r.stdout
def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).strip())

GRN, YEL, INK = "#58CC02", "#FFD900", "#1f1f1f"
CSS = f"""@font-face{{font-family:P;src:url("file://{FONT_B}");font-weight:700}}
@font-face{{font-family:P;src:url("file://{FONT_S}");font-weight:600}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:transparent;font-family:P,"Apple SD Gothic Neo",sans-serif;font-weight:700;color:{INK};letter-spacing:-1.5px}}
.abs{{position:absolute}}
.top{{position:absolute;left:0;right:0;top:0;height:420px;background:linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,0))}}
.bot{{position:absolute;left:0;right:0;bottom:0;height:760px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.6))}}
.brand{{position:absolute;top:62px;left:0;right:0;text-align:center;font-weight:600;font-size:32px;color:#fff;opacity:.95;letter-spacing:-.5px}}
.brand i{{font-style:normal;color:{GRN}}}
.pill{{position:absolute;top:112px;left:50%;transform:translateX(-50%);white-space:nowrap;background:{GRN};color:#fff;font-size:46px;
  padding:14px 40px;border-radius:999px;border-bottom:8px solid #3f9a00;box-shadow:0 10px 24px rgba(0,0,0,.25)}}
.url{{position:absolute;left:50%;transform:translateX(-50%);white-space:nowrap;background:rgba(255,255,255,.96);color:#333;font-weight:600;
  font-size:30px;letter-spacing:-.3px;padding:9px 24px;border-radius:999px;box-shadow:0 8px 20px rgba(0,0,0,.25)}}
.url s{{text-decoration:none;color:#2e9d00}}
.cap{{position:absolute;left:64px;right:64px;bottom:130px;text-align:center;background:#fff;border-radius:44px;border-bottom:12px solid #dcdcdc;
  padding:34px 30px;font-size:64px;line-height:1.3;word-break:keep-all;box-shadow:0 20px 50px rgba(0,0,0,.35)}}
.cap b{{font-weight:inherit;background:linear-gradient(transparent 58%,{YEL} 58%);padding:0 6px}}
.mini{{position:absolute;border-radius:34px;background:#111;padding:9px;box-shadow:0 18px 40px rgba(0,0,0,.45)}}
.mini div{{width:100%;height:100%;border-radius:26px;overflow:hidden;background:#fff}}
.mini img{{width:100%;display:block}}
"""
def page(body, bg="transparent"):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:{bg}}}</style></head><body>{body}</body></html>'
BRAND = '<div class="brand"><i>●</i> AI Maker Lab · 바이브 코딩 프로젝트 수업</div>'

def cap_html(c):
    t = html.escape(c).replace("|", "<br>")
    return '<div class="cap">' + re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t) + "</div>"

def shoot(htmlstr, png):
    hp = png[:-4] + ".html"; open(hp, "w").write(htmlstr)
    if os.path.exists(png): os.remove(png)
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", f"--window-size={W},{H}",
           "--default-background-color=00000000", "--allow-file-access-from-files", f"--screenshot={png}", "file://" + hp]
    for _ in range(3):
        try:
            subprocess.run(cmd, capture_output=True, timeout=45)
            if os.path.exists(png) and os.path.getsize(png) > 0: return png
        except subprocess.TimeoutExpired: pass
    sys.exit(f"screenshot failed: {png}")

def scr(name): return f"{A}/screens/{name}.png"

# ---------- 레이어 HTML ----------
def fg_img(s):
    body = '<div class="top"></div><div class="bot"></div>' + BRAND
    if s.get("tag"): body += f'<div class="pill">{html.escape(s["tag"])}</div>'
    return page(body + cap_html(s["cap"]))

def under_screen(s):
    """흐린 배경 + 폰 몸체 (화면 자리는 나중에 PIL로 투명하게 뚫음)"""
    return page(f'<img class="abs" src="file://{scr(s["screen"])}" style="left:-80px;top:-80px;width:1240px;height:2080px;object-fit:cover;object-position:top;filter:blur(36px) saturate(1.2) brightness(.55)">'
                f'<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0),rgba(0,0,0,.45))"></div>'
                f'<div class="abs" style="left:{PX-BZ}px;top:{PY-BZ}px;width:{SW+2*BZ}px;height:{SH+2*BZ}px;border-radius:{SR+BZ}px;background:#0d0d0f;'
                f'box-shadow:0 40px 90px rgba(0,0,0,.55),inset 0 0 0 3px #2a2a2e"></div>', "#111")

def fg_screen(s):
    body = BRAND
    if s.get("tag"): body += f'<div class="pill">{html.escape(s["tag"])}</div>'
    if s.get("url"): body += f'<div class="url" style="top:{PY-BZ-58}px"><s>🔒</s> {html.escape(s["url"])}</div>'
    return page(body + cap_html(s["cap"]))

def wall_html(names, dim=False):
    w, h = 236, 470; xs = [30, 290, 554, 814]; out = ""
    for i, n in enumerate(names):
        c, r = i % 4, i // 4
        rot = (-4, 3, -2, 4)[c] * (1 if r else -1)
        out += (f'<div class="mini" style="left:{xs[c]}px;top:{360 + r * 560 + (40 if c % 2 else 0)}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)">'
                f'<div><img src="file://{scr(n)}"></div></div>')
    bg = "linear-gradient(160deg,#16222f,#0e1a12)"
    return page(f'<div class="abs" style="inset:0;background:{bg}"></div>' + out)

def fg_plain(s):
    return page(BRAND + cap_html(s["cap"]))

def cta_html(wall_png):
    box = lambda c, e, t, sub: (f'<div style="background:#fff;border-radius:40px;border-bottom:12px solid #dcdcdc;padding:32px 44px;display:flex;align-items:center;gap:30px">'
                                f'<div style="font-size:88px">{e}</div><div><div style="font-size:62px;color:{c}">{t}</div>'
                                f'<div style="font-size:40px;font-weight:600;color:#444;margin-top:6px">{sub}</div></div></div>')
    chips = "".join(f'<span style="font-size:36px;font-weight:600;background:rgba(255,255,255,.95);border-radius:999px;padding:12px 26px">{t}</span>'
                    for t in ["☀️ 주말반", "🌙 야간반", "💻 줌 온라인", "🏫 오프라인"])
    body = (f'<img class="abs" src="file://{wall_png}" style="inset:0;width:{W}px;height:{H}px;filter:blur(10px)">'
            '<div class="abs" style="inset:0;background:linear-gradient(rgba(30,90,0,.78),rgba(40,120,0,.92) 45%,rgba(30,95,0,.97))"></div>' + BRAND +
            '<div class="abs" style="left:0;right:0;top:250px;text-align:center;color:#fff">'
            '<div style="font-size:50px;font-weight:600;opacity:.95">코딩 몰라도 괜찮아요</div>'
            '<div style="font-size:120px;line-height:1.18;margin-top:24px;text-shadow:0 6px 24px rgba(0,0,0,.25)">수업에서<br>만나요!</div></div>'
            '<div class="abs" style="left:70px;right:70px;top:820px;display:flex;flex-direction:column;gap:30px">'
            + box(GRN, "🌱", "기초반", "아이디어로 첫 작품 완성")
            + box("#1CB0F6", "🚀", "심화반", "내 프로젝트를 실제 출시까지")
            + f'<div style="display:flex;flex-wrap:wrap;gap:16px;justify-content:center;margin-top:6px">{chips}</div></div>'
            '<div class="abs" style="left:0;right:0;bottom:130px;text-align:center;color:#fff;font-size:42px;line-height:1.5">'
            '프로젝트 AI 코디네이터 김종필<br><span style="font-size:54px">aimakerlab.com</span></div>')
    return page(body)

def punch_hole(png):
    im = Image.open(png).convert("RGBA")
    m = Image.new("L", im.size, 255); ImageDraw.Draw(m).rounded_rectangle([PX, PY, PX + SW - 1, PY + SH - 1], radius=SR, fill=0)
    im.putalpha(m); im.save(png)

# ---------- 내레이션 ----------
def narration(s):
    out = f"{OUT}/{s['id']}_v.wav"
    af = ("silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
          "loudnorm=I=-15:TP=-1.5:LRA=7")
    for ext in (".m4a", ".wav", ".mp3"):           # 직접 녹음이 있으면 우선
        mine = f"{A}/voice_mine/{s['id']}{ext}"
        if os.path.exists(mine):
            run(["ffmpeg", "-v", "error", "-y", "-i", mine, "-af", af, "-ar", "48000", "-ac", "2", out]); return out
    key = hashlib.md5(f"{VOICE}|{RATE}|{s['narr']}".encode()).hexdigest()[:10]
    mp3 = f"{TTS}/{s['id']}_{key}.mp3"
    if not os.path.exists(mp3):
        for _ in range(3):
            r = subprocess.run([EDGE, "--voice", VOICE, f"--rate={RATE}", "--text", s["narr"], "--write-media", mp3], capture_output=True, text=True, timeout=60)
            if r.returncode == 0 and os.path.exists(mp3) and os.path.getsize(mp3) > 1000: break
        else: sys.exit(f"edge-tts failed for {s['id']}: {r.stderr[-400:]}")
    run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af", af, "-ar", "48000", "-ac", "2", out]); return out

# ---------- 장면 렌더 ----------
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS)]
MOVES = [("1.0+0.10*on/{n}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"),
         ("1.10-0.10*on/{n}", "iw/2-iw/zoom/2", "ih*0.35-ih/zoom*0.35"),
         ("1.04+0.08*on/{n}", "(iw-iw/zoom)*(0.35+0.3*on/{n})", "ih/2-ih/zoom/2")]
FG_IN = f"[2]format=rgba,fade=t=in:st={XF*0.6:.2f}:d=0.3:alpha=1[f]"
FG_OV = f"overlay=x=0:y='if(lt(t,{XF*0.6+0.3:.2f}),max(0,50*(1-(t-{XF*0.6:.2f})/0.3)),0)'"

def render(args):
    i, s = args; sid, kind = s["id"], s["kind"]
    wav = narration(s); D = round(LEAD + dur(wav) + TAIL + XF, 3)
    if kind == "cta": D += 1.8
    n = int(D * FPS) + 1; out = f"{OUT}/{sid}.mp4"
    if kind == "img":
        z, x, y = (m.format(n=n) for m in MOVES[i % len(MOVES)])
        fg = shoot(fg_img(s), f"{OUT}/{sid}_fg.png")
        fc = (f"[0]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS},setsar=1[bg];"
              f"[1]format=rgba,fade=t=in:st={XF*0.6:.2f}:d=0.3:alpha=1[f];[bg][f]{FG_OV},format=yuv420p[v]")
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{A}/img/{s['img']}.png", "-loop", "1", "-i", fg,
             "-filter_complex", fc, "-map", "[v]", "-t", f"{D}", *ENC, out])
    elif kind == "screen":
        under = shoot(under_screen(s), f"{OUT}/{sid}_under.png"); punch_hole(under)
        fg = shoot(fg_screen(s), f"{OUT}/{sid}_fg.png")
        iw, ih = Image.open(scr(s["screen"])).size; sh = round(ih * SW / iw)
        L = max(0, min(sh - SH, int(150 * D)))     # 스크롤 거리 (첫 화면을 충분히 보여 준 뒤 천천히)
        a, b = 1.4, max(0.5, D - 2.0)
        p = f"clip((t-{a})/{b},0,1)"
        fc = (f"[0]scale={SW}:-2,crop={SW}:{SH}:0:'{L}*(3*pow({p},2)-2*pow({p},3))'[s];"
              f"color=c=black:s={W}x{H}:r={FPS}[base];[base][s]overlay={PX}:{PY}:shortest=1[b1];[b1][1]overlay=0:0[b2];"
              f"{FG_IN};[b2][f]{FG_OV},format=yuv420p[v]")
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", scr(s["screen"]), "-loop", "1", "-i", under, "-loop", "1", "-i", fg,
             "-filter_complex", fc, "-map", "[v]", "-t", f"{D}", *ENC, out])
    else:  # wall / cta
        wall = shoot(wall_html(s.get("screens") or WALL_DEFAULT), f"{OUT}/{sid}_wall.png")
        if kind == "cta":
            bgp = shoot(cta_html(wall), f"{OUT}/{sid}_cta.png"); fg = shoot(page(""), f"{OUT}/{sid}_fg.png"); z = "1.0+0.03*on/{n}"
        else:
            bgp = wall; fg = shoot(fg_plain(s), f"{OUT}/{sid}_fg.png"); z = "1.0+0.07*on/{n}"
        fc = (f"[0]scale=2160:3840,zoompan=z='{z.format(n=n)}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={FPS},setsar=1[bg];"
              f"[1]format=rgba,fade=t=in:st={XF*0.6:.2f}:d=0.3:alpha=1[f];[bg][f]{FG_OV},format=yuv420p[v]")
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", bgp, "-loop", "1", "-i", fg,
             "-filter_complex", fc, "-map", "[v]", "-t", f"{D}", *ENC, out])
    print(f"{sid} {kind:6s} {D:.2f}s", flush=True)
    return out, wav, D

WALL_DEFAULT = ["lingopang", "playstore", "readingclue", "teenspark", "zzingong", "deepq", "maum", "stock"]

def main():
    with ThreadPoolExecutor(4) as ex: parts = list(ex.map(render, enumerate(SCENES)))
    # 영상: xfade 체인
    vins, fc, starts, t, prev = [], [], [], 0.0, "0:v"
    for k, (mp4, _, D) in enumerate(parts):
        vins += ["-i", mp4]; starts.append(t)
        if k:
            kind = SCENES[k]["kind"]
            tr = "fadewhite" if kind == "cta" else "slideleft" if kind == "screen" and SCENES[k - 1]["kind"] == "screen" else "fade"
            fc.append(f"[{prev}][{k}:v]xfade=transition={tr}:duration={XF}:offset={t:.3f}[x{k}]"); prev = f"x{k}"
        t += D - XF
    total = t + XF; vid = f"{OUT}/video.mp4"
    run(["ffmpeg", "-v", "error", "-y", *vins, "-filter_complex", ";".join(fc), "-map", f"[{prev}]", *ENC, vid])
    # 오디오: 내레이션 배치 + 배경음 덕킹
    ains, af, nk = [], [], len(parts)
    for k, (_, wav, _) in enumerate(parts):
        ains += ["-i", wav]; ms = int((starts[k] + (XF if k else 0) + LEAD) * 1000)
        af.append(f"[{k+1}:a]adelay={ms}|{ms}[n{k}]")
    af.append("".join(f"[n{k}]" for k in range(nk)) + f"amix=inputs={nk}:normalize=0:duration=longest,apad,atrim=0:{total:.3f}[nar]")
    af.append("[nar]asplit=2[nar1][sc]")
    af.append(f"[{nk+1}:a]atrim=0:{total:.3f},asetpts=N/SR/TB,volume=0.30,afade=t=in:st=0:d=0.8,afade=t=out:st={total-2.5:.3f}:d=2.5[m]")
    af.append("[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md]")
    af.append("[nar1][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]")
    run(["ffmpeg", "-v", "error", "-y", "-i", vid, *ains, "-i", f"{A}/music.mp3", "-filter_complex", ";".join(af),
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-movflags", "+faststart", "-t", f"{total:.3f}", FINAL])
    print(f"DONE {os.path.abspath(FINAL)} {dur(FINAL):.1f}s  voice={VOICE}")

if __name__ == "__main__": main()
