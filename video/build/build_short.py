"""Vertical 1080x1920 short in the LingoPang v11 style.
Layers per scene: background (generated photo / existing clip / drawn card) + foreground overlay
(pill, badges, partial phone capture, caption bubble) rendered as transparent PNG by headless Chrome.
Usage: python3 video/build/build_short.py [output.mp4]
"""
import os, sys, re, subprocess, html, json
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from scenes_short import SCENES
from drawn import DRAWN

A = f"{HERE}/assets"; GEN = f"{A}/gen"; MOB = f"{A}/mobile"; SHOTS = f"{A}/shots"
VOICE = os.path.join(HERE, "..", "voice")          # optional own recordings: short_<id>.m4a
OUT = f"{HERE}/out_short"; os.makedirs(OUT, exist_ok=True); os.makedirs(GEN, exist_ok=True)
FONT = "/Users/jongphilkim/Documents/GitHub/lingoPang-frontend/frontend-expo/lingopang-app/assets/fonts/Pretendard-Bold.ttf"
MUSIC = f"{A}/hf/music.mp3"
EDGE = f"{HERE}/.venv/bin/edge-tts"      # optional: python3 -m venv video/build/.venv && video/build/.venv/bin/pip install edge-tts
NARR_VOICE = os.environ.get("NARR_VOICE", "ko-KR-SunHiNeural")   # or ko-KR-InJoonNeural / ko-KR-HyunsuMultilingualNeural
NARR_RATE = os.environ.get("NARR_RATE", "+18%")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H, FPS = 1080, 1920, 30
FINAL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "바이브코딩_프로젝트수업_숏폼.mp4")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(map(str, cmd))[:600]); print(r.stderr[-2500:]); sys.exit(1)
    return r.stdout
def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).strip())

GRN, YEL, INK = "#58CC02", "#FFD900", "#2B2B2B"
CSS = f"""@font-face{{font-family:Pret;src:url("file://{FONT}")}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:transparent;font-family:Pret,"Apple SD Gothic Neo",sans-serif;color:{INK};letter-spacing:-1px}}
.abs{{position:absolute}}
.brand{{position:absolute;top:54px;left:0;right:0;text-align:center;font-size:30px;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.45)}}
.pill{{position:absolute;top:120px;left:50%;transform:translateX(-50%);white-space:nowrap;background:{GRN};color:#fff;font-size:46px;
  padding:16px 38px;border-radius:999px;border-bottom:8px solid #3f9a00;box-shadow:0 10px 24px rgba(0,0,0,.18)}}
.cap{{position:absolute;left:70px;right:70px;bottom:150px;text-align:center;background:#fff;border:5px solid #E5E5E5;border-bottom-width:13px;
  border-radius:44px;padding:34px 30px;font-size:66px;line-height:1.3;word-break:keep-all;box-shadow:0 18px 40px rgba(0,0,0,.18)}}
.cap b{{font-weight:inherit;background:linear-gradient(transparent 55%,{YEL} 55%);padding:0 4px}}
.badge{{position:absolute;white-space:nowrap;font-size:40px;color:#fff;padding:14px 28px;border-radius:999px;border-bottom:8px solid rgba(0,0,0,.18);box-shadow:0 8px 20px rgba(0,0,0,.18)}}
.phone{{position:absolute;width:440px;height:900px;border-radius:64px;background:#111;padding:18px;box-shadow:0 30px 60px rgba(0,0,0,.35)}}
.phone .scr{{width:100%;height:100%;border-radius:48px;overflow:hidden;background:#fff}}
.phone img{{width:100%;display:block}}
.phone .notch{{position:absolute;top:30px;left:50%;transform:translateX(-50%);width:120px;height:32px;border-radius:20px;background:#111}}
.browser{{position:absolute;border-radius:28px;overflow:hidden;background:#fff;box-shadow:0 30px 60px rgba(0,0,0,.3)}}
.browser .bar{{height:54px;background:#f1f1f4;display:flex;align-items:center;gap:12px;padding:0 22px}}
.browser .bar i{{width:18px;height:18px;border-radius:50%;display:block}}
.browser .url{{margin-left:14px;font-size:22px;color:#777;background:#fff;border-radius:999px;padding:6px 20px}}
.browser img{{display:block;width:100%}}
.full{{position:absolute;inset:0}}
"""
def page(body, bg="transparent"):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:{bg}}}</style></head><body>{body}</body></html>'

def cap_html(c):
    if not c: return ""
    t = html.escape(c).replace("|", "<br>")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return f'<div class="cap">{t}</div>'

def phone(src, x, y, rot, w=440, crop_top=0):
    h = round(w * 900 / 440)
    return (f'<div class="phone" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)">'
            f'<div class="scr"><img src="file://{src}" style="margin-top:-{crop_top}px"></div><div class="notch"></div></div>')

def browser(src, x, y, w, rot=0, url="", h=None):
    hh = f"height:{h}px;" if h else ""
    return (f'<div class="browser" style="left:{x}px;top:{y}px;width:{w}px;{hh}transform:rotate({rot}deg)"><div class="bar">'
            f'<i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i><span class="url">{url}</span></div>'
            f'<img src="file://{src}"></div>')

BADGE_COLORS = [("#1CB0F6", -4), ("#FF9600", 3), ("#CE82FF", -2)]
def badges_html(items, top=300):
    out = ""
    for i, t in enumerate(items):
        col, rot = BADGE_COLORS[i % 3]
        x = [70, 470, 160][i % 3]; y = top + [0, 30, 130][i % 3]
        out += f'<div class="badge" style="left:{x}px;top:{y}px;background:{col};transform:rotate({rot}deg)">{t}</div>'
    return out

def mob(name):
    alt = {"stock": f"{SHOTS}/stock_m.png"}
    return alt.get(name, f"{MOB}/{name}.png")

def fg_html(s):
    body = '<div class="brand">AI Maker Lab · 바이브 코딩 프로젝트 수업</div>'
    if s.get("pill"): body += f'<div class="pill">{s["pill"]}</div>'
    if s.get("badges"): body += badges_html(s["badges"])
    if s.get("shot"):
        kind, f, side = s["shot"]
        x = {"right": 650, "left": 50, "center": 350}[side]; rot = {"right": 6, "left": -6, "center": 0}[side]
        body += phone(mob(f), x, 800, rot, w=380)
    body += cap_html(s["cap"])
    return page(body)

# ---------- drawn cards (opaque backgrounds) ----------
STRIPE = "repeating-linear-gradient(135deg,#f6fbef 0 40px,#eef7e4 40px 80px)"
def card_html(kind):
    if kind in DRAWN:
        body, bg = DRAWN[kind](); return page(body, bg)
    if kind == "versus":
        b = ('<div class="abs" style="left:90px;right:90px;top:330px;display:flex;flex-direction:column;gap:46px">'
             '<div style="background:#fff;border:5px solid #E5E5E5;border-bottom-width:12px;border-radius:40px;padding:44px;text-align:center;opacity:.75">'
             '<div style="font-size:120px">📚</div><div style="font-size:64px;color:#AFAFAF;text-decoration:line-through">외우는 수업</div>'
             '<div style="font-size:40px;color:#AFAFAF;margin-top:10px">시험 끝나면 잊어버려요</div></div>'
             f'<div style="background:#fff;border:6px solid {GRN};border-bottom-width:14px;border-radius:40px;padding:44px;text-align:center">'
             f'<div style="font-size:120px">🛠️</div><div style="font-size:76px;color:{GRN}">만드는 수업</div>'
             '<div style="font-size:42px;color:#555;margin-top:10px">내 손으로 만든 건 남아요</div></div></div>')
        return page(b, STRIPE)
    if kind == "lp_launch":
        b = (browser(f"{SHOTS}/lingopang.png", 70, 300, 940, -2, "lingopang.com")
             + phone(f"{MOB}/playstore.png", 70, 820, -5, w=400)
             + phone(f"{MOB}/youtube.png", 600, 860, 5, w=400)
             + '<div class="abs" style="left:350px;top:1090px;font-size:110px">➜</div>')
        return page(b, STRIPE)
    if kind == "wall":
        items = ["lingopang", "careerpath", "readingclue", "teenspark", "zzingong", "deepq", "dramaro", "stock"]
        b = ""
        for i, n in enumerate(items):
            col, row = i % 4, i // 4
            b += phone(mob(n), 30 + col * 262, 330 + row * 560, (-4, 3, -2, 4)[i % 4] * (1 if row else -1), w=240)
        return page(b, STRIPE)
    if kind == "classes":
        box = lambda c, e, t, lines: (f'<div style="background:#fff;border:6px solid {c};border-bottom-width:14px;border-radius:40px;padding:40px 46px">'
                                      f'<div style="font-size:70px;color:{c}">{e} {t}</div>'
                                      + "".join(f'<div style="font-size:44px;margin-top:16px;color:#444">· {l}</div>' for l in lines) + "</div>")
        b = ('<div class="abs" style="left:80px;right:80px;top:300px;display:flex;flex-direction:column;gap:40px">'
             + box(GRN, "🌱", "기초반", ["코딩 경험 없어도 OK", "아이디어로 첫 작품 완성", "데모데이 시연"])
             + box("#1CB0F6", "🚀", "심화반 (프로젝트)", ["내 프로젝트에 AI·카메라 연결", "실제 출시·상용화까지", "포트폴리오 완성"])
             + '<div style="display:flex;flex-wrap:wrap;gap:18px;justify-content:center">'
             + "".join(f'<span style="font-size:40px;background:#fff;border:4px solid #E5E5E5;border-bottom-width:9px;border-radius:999px;padding:12px 28px">{t}</span>'
                       for t in ["☀️ 주말반", "🌙 야간반", "💻 줌 온라인", "🏫 오프라인 공간"]) + "</div></div>")
        return page(b, STRIPE)
    if kind == "cta":
        b = (f'<div class="abs" style="left:0;right:0;top:330px;text-align:center;color:#fff">'
             '<div style="font-size:52px;opacity:.95">아이디어에 불꽃, 설계는 내가</div>'
             '<div style="font-size:120px;line-height:1.2;margin-top:40px">기초반 · 심화반<br>수업에서<br>만나요!</div></div>'
             '<div class="abs" style="left:90px;right:90px;top:1180px;background:#fff;border-radius:40px;border-bottom:12px solid #d9d9d9;padding:40px;text-align:center">'
             f'<div style="font-size:54px">주말반 · 야간반</div><div style="font-size:46px;color:{GRN};margin-top:14px">줌 온라인 · 오프라인 공간</div></div>'
             '<div class="abs" style="left:0;right:0;top:1560px;text-align:center;color:#fff;font-size:44px">프로젝트 AI 코디네이터 김종필<br>aimakerlab.com</div>')
        return page(b, GRN)

def placeholder_html(name):
    return page(f'<div class="full" style="background:linear-gradient(160deg,#cfd9e8,#8ea3c2);display:flex;align-items:center;justify-content:center">'
                f'<div style="font-size:54px;color:#fff;text-align:center">이미지 생성 대기<br>{name}</div></div>', "#999")

def shoot(htmlstr, png):
    hp = png[:-4] + ".html"; open(hp, "w").write(htmlstr)
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", f"--window-size={W},{H}",
           "--default-background-color=00000000", f"--screenshot={png}", "file://" + hp]
    for attempt in range(3):  # headless Chrome occasionally hangs; retry with a timeout
        try:
            subprocess.run(cmd, capture_output=True, timeout=45)
            if os.path.exists(png) and os.path.getsize(png) > 0: return
        except subprocess.TimeoutExpired:
            pass
    sys.exit(f"screenshot failed: {png}")

def tts(s):
    out = f"{OUT}/{s['id']}.wav"
    for ext in (".m4a", ".wav", ".mp3"):
        src = os.path.join(VOICE, f"short_{s['id']}{ext}")
        if os.path.exists(src):
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5",
                 "-ar", "48000", "-ac", "1", out]); return out
    trim = ("silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
            "silenceremove=start_periods=1:start_threshold=-50dB,areverse,loudnorm=I=-16:TP=-1.5")
    if os.path.exists(EDGE):  # Microsoft neural voice (free; text is sent to Microsoft's speech service)
        mp3 = out[:-4] + ".mp3"
        for attempt in range(3):
            r = subprocess.run([EDGE, "--voice", NARR_VOICE, f"--rate={NARR_RATE}", "--text", s["narr"], "--write-media", mp3],
                               capture_output=True, text=True, timeout=60)
            if r.returncode == 0 and os.path.exists(mp3) and os.path.getsize(mp3) > 1000: break
        else:
            sys.exit(f"edge-tts failed for {s['id']}: {r.stderr[-500:]}")
        run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af", trim, "-ar", "48000", "-ac", "1", out]); return out
    a = out[:-4] + ".aiff"
    run(["say", "-v", "Yuna", "-r", "190", "-o", a, s["narr"]])
    run(["ffmpeg", "-v", "error", "-y", "-i", a, "-ar", "48000", "-ac", "1", out]); return out

def render(s):
    sid = s["id"]; wav = tts(s); D = round(dur(wav) + 0.75, 3)
    enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS)]
    frames = int(D * FPS) + 2
    kind, val = s["bg"]
    bgv = f"{OUT}/{sid}_bg.mp4"
    if kind == "img":
        src = f"{GEN}/{val}.png"
        if not os.path.exists(src):
            src = f"{OUT}/ph_{val}.png"; shoot(placeholder_html(val), src)
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-t", f"{D}", "-vf",
             f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1.18+0.07*on/{frames}':x='iw/2-iw/zoom/2':y='(ih-ih/zoom)*0.12':d=1:s={W}x{H}:fps={FPS}"] + enc + ["-an", bgv])
    elif kind == "clip":
        run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", val, "-t", f"{D}", "-vf",
             f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"] + enc + ["-an", bgv])
    else:
        png = f"{OUT}/{sid}_card.png"; shoot(card_html(val), png)
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", png, "-t", f"{D}", "-vf",
             f"scale=2160:3840,zoompan=z='1+0.03*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={FPS}"] + enc + ["-an", bgv])
    fg = f"{OUT}/{sid}_fg.png"; shoot(fg_html(s), fg)
    out = f"{OUT}/{sid}.mp4"
    fc = (f"[1]format=rgba,fade=t=in:st=0:d=0.3:alpha=1[f];"
          f"[0][f]overlay=x=0:y='if(lt(t,0.3),70*(1-t/0.3),0)':shortest=1,"
          f"fade=t=in:st=0:d=0.15,fade=t=out:st={D-0.15}:d=0.15,format=yuv420p[v]")
    run(["ffmpeg", "-v", "error", "-y", "-i", bgv, "-loop", "1", "-i", fg, "-i", wav, "-filter_complex", fc,
         "-map", "[v]", "-map", "2:a", "-t", f"{D}"] + enc + ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-af", "apad", out])
    print(f"{sid} {D:.1f}s", flush=True); return out

def main():
    with ThreadPoolExecutor(4) as ex: files = list(ex.map(render, SCENES))
    lst = f"{OUT}/all.txt"; open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{OUT}/all.mp4"])
    T = dur(f"{OUT}/all.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/all.mp4", "-stream_loop", "-1", "-i", MUSIC, "-filter_complex",
         f"[1:a]atrim=0:{T:.3f},asetpts=N/SR/TB,volume=0.14,afade=t=in:st=0:d=1,afade=t=out:st={T-2.5:.3f}:d=2.5[m];"
         f"[0:a]volume=1.5[v];[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", FINAL])
    missing = [v for s in SCENES if s["bg"][0] == "img" for v in [s["bg"][1]] if not os.path.exists(f"{GEN}/{v}.png")]
    print(f"DONE {FINAL} {T:.1f}s  missing images: {sorted(set(missing)) or 'none'}")

if __name__ == "__main__": main()
