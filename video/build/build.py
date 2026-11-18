import os, sys, subprocess, wave, json, html
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from scenes import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))
HF, SHOTS = f"{HERE}/assets/hf", f"{HERE}/assets/shots"
VOICE = os.path.join(HERE, "..", "voice")  # your recordings: <scene id>_<line no>.m4a/.wav/.mp3
OUT = f"{HERE}/out"; OV = f"{OUT}/ov"; AU = f"{OUT}/au"; SC = f"{OUT}/sc"
for d in (OUT, OV, AU, SC): os.makedirs(d, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H, FPS = 1280, 720, 30
LEAD, GAP, TAIL = 0.5, 0.35, 0.8
FINAL = sys.argv[1]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)); print(r.stderr[-3000:]); sys.exit(1)
    return r.stdout

def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).strip())

# ---------- overlays (HTML -> transparent PNG via headless Chrome) ----------
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1280px;height:720px;background:transparent;overflow:hidden;
 font-family:"Apple SD Gothic Neo","AppleSDGothicNeo",sans-serif;color:#fff}
.brand{position:absolute;top:26px;right:30px;font-size:15px;font-weight:600;letter-spacing:.5px;
 color:rgba(255,255,255,.85);background:rgba(10,12,30,.45);padding:7px 14px;border-radius:999px}
.label{position:absolute;top:24px;left:28px;font-size:20px;font-weight:700;
 background:linear-gradient(90deg,#7c5cff,#ff7a59);padding:9px 18px;border-radius:999px;
 box-shadow:0 6px 20px rgba(0,0,0,.35)}
.shade{position:absolute;left:0;right:0;bottom:0;height:230px;background:linear-gradient(to bottom,rgba(0,0,0,0),rgba(0,0,0,.78))}
.cap{position:absolute;left:50%;bottom:44px;transform:translateX(-50%);max-width:1120px;
 text-align:center;font-size:33px;line-height:1.38;font-weight:700;word-break:keep-all;
 background:rgba(8,10,24,.96);padding:14px 30px;border-radius:16px;
 text-shadow:0 2px 6px rgba(0,0,0,.5)}
.full{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;
 background:radial-gradient(ellipse at center,rgba(10,10,30,.55) 0%,rgba(6,6,20,.86) 75%)}
.kicker{font-size:24px;font-weight:700;color:#ffb38a;letter-spacing:2px;margin-bottom:18px}
.title{font-size:62px;font-weight:800;line-height:1.25;word-break:keep-all}
.title em{font-style:normal;background:linear-gradient(90deg,#a78bfa,#ff8a65);-webkit-background-clip:text;color:transparent}
.sub{margin-top:24px;font-size:24px;font-weight:600;color:rgba(255,255,255,.82)}
.num{font-size:120px;font-weight:800;line-height:1;margin-bottom:6px;
 background:linear-gradient(180deg,#fff,rgba(255,255,255,.15));-webkit-background-clip:text;color:transparent}
.cls{display:flex;gap:28px;margin-top:8px}
.box{width:470px;border-radius:22px;padding:28px 30px;text-align:left;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18)}
.box h3{font-size:34px;font-weight:800;margin-bottom:12px}
.box p{font-size:23px;line-height:1.5;color:rgba(255,255,255,.88);word-break:keep-all}
.b1{border-color:#7ee08a;box-shadow:0 0 30px rgba(126,224,138,.25)} .b1 h3{color:#9ef0a7}
.b2{border-color:#8fa8ff;box-shadow:0 0 30px rgba(143,168,255,.25)} .b2 h3{color:#aebfff}
.chips{display:flex;gap:14px;margin-top:30px}
.chip{font-size:22px;font-weight:700;padding:10px 20px;border-radius:999px;background:rgba(255,255,255,.12)}
"""
BRAND = '<div class="brand">AI Maker Lab · 바이브 코딩 프로젝트 수업</div>'

def card_html(c):
    k = c["kind"]
    if k == "title":
        return f'<div class="full"><div class="kicker">{c["kicker"]}</div><div class="title">{c["title"]}</div><div class="sub">{c["sub"]}</div></div>'
    if k == "chapter":
        return f'<div class="full"><div class="num">{c["num"]}</div><div class="kicker">{c["kicker"]}</div><div class="title">{c["title"]}</div><div class="sub">{c["sub"]}</div></div>'
    if k == "classes":
        return ('<div class="full" style="justify-content:flex-start;padding-top:96px"><div class="kicker">함께 만들어요</div>'
                '<div class="cls"><div class="box b1"><h3>🌱 기초반</h3><p>코딩 경험이 없어도 OK<br>아이디어로 <b>첫 작품</b> 완성<br>데모데이에서 직접 시연</p></div>'
                '<div class="box b2"><h3>🚀 심화반 (프로젝트)</h3><p>내 프로젝트에 AI·카메라 연결<br>실제 <b>출시·상용화</b>까지<br>포트폴리오로 완성</p></div></div>'
                '<div class="chips"><div class="chip">☀️ 주말반</div><div class="chip">🌙 야간반</div><div class="chip">💻 줌 온라인</div><div class="chip">🏫 오프라인 공간</div></div></div>')
    if k == "end":
        return ('<div class="full"><div class="kicker">아이디어에 불꽃, 설계는 내가</div>'
                '<div class="title">기초반 · 심화반<br><em>수업에서 만나요!</em></div>'
                '<div class="sub">주말반 · 야간반 | 줌 온라인 · 오프라인 공간<br>프로젝트 AI 코디네이터 김종필 · aimakerlab.com</div></div>')

def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'

jobs = []  # (html_path, png_path)
def add_overlay(name, body):
    hp, pp = f"{OV}/{name}.html", f"{OV}/{name}.png"
    open(hp, "w").write(page(body)); jobs.append((hp, pp)); return pp

def shoot(j):
    hp, pp = j
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                    "--default-background-color=00000000", f"--screenshot={pp}", "file://" + hp],
                   capture_output=True)

# ---------- audio ----------
USED = []
def tts(text, path, rec):
    # Prefer your own recording; trim leading/trailing silence and normalise loudness.
    for ext in (".m4a", ".wav", ".mp3", ".aiff"):
        src = os.path.join(VOICE, rec + ext)
        if os.path.exists(src):
            USED.append(rec)
            af = ("silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                  "silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5")
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ar", "48000", "-ac", "1", "-sample_fmt", "s16", path])
            return
    aiff = path[:-4] + ".aiff"
    run(["say", "-v", "Yuna", "-r", "188", "-o", aiff, text])
    run(["ffmpeg", "-v", "error", "-y", "-i", aiff, "-ar", "48000", "-ac", "1", "-sample_fmt", "s16", path])

def build_audio(sid, lines):
    paths = [f"{AU}/{sid}_{i}.wav" for i in range(len(lines))]
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(lambda a: tts(*a), [(l[0], p, f"{sid}_{i+1}") for i, (l, p) in enumerate(zip(lines, paths))]))
    frames, starts, t = [], [], LEAD
    sil = lambda s: b"\x00\x00" * int(48000 * s)
    frames.append(sil(LEAD))
    for i, p in enumerate(paths):
        with wave.open(p) as w: data = w.readframes(w.getnframes()); d = w.getnframes() / 48000
        starts.append(t); frames.append(data); t += d
        if i < len(paths) - 1: frames.append(sil(GAP)); t += GAP
    frames.append(sil(TAIL)); t += TAIL
    out = f"{AU}/{sid}.wav"
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes(b"".join(frames))
    return out, starts, t

# ---------- visuals ----------
def base_video(sid, v, D, dim):
    out = f"{SC}/{sid}_base.mp4"
    enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]
    p = f"min(t/{D:.3f},1)"; ease = f"(3*pow({p},2)-2*pow({p},3))"
    dimf = ",eq=brightness=-0.06:saturation=0.9" if dim else ""
    if v["type"] == "clips":
        lst = f"{SC}/{sid}_list.txt"; files = [f"{HF}/{f}.mp4" for f in v["files"]]
        total = sum(dur(f) for f in files); reps = int(D // total) + 1
        open(lst, "w").write("".join(f"file '{f}'\n" for _ in range(reps) for f in files))
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-t", f"{D:.3f}",
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1{dimf}"] + enc + [out])
    elif v["type"] == "scroll":
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", f"{SHOTS}/{v['file']}.png", "-t", f"{D:.3f}",
             "-vf", f"scale={W}:-2,crop={W}:{H}:0:'(ih-{H})*{ease}',setsar=1"] + enc + [out])
    elif v["type"] == "still":
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", f"{SHOTS}/{v['file']}.png", "-t", f"{D:.3f}",
             "-vf", f"scale={W}:-2,crop={W}:{H}:0:'(ih-{H})*{ease}',setsar=1"] + enc + [out])
    elif v["type"] == "phone":
        img = f"{SHOTS}/{v['file']}.png"
        fg = (f"[0]crop=430:932:0:'(ih-932)*{ease}'" if v.get("scroll") else "[0]crop=430:932:0:0") + ",scale=-2:650,format=rgba[fg]"
        fc = (f"[0]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.25[bg];"
              f"{fg};[bg][fg]overlay=(W-w)/2:(H-h)/2+10,setsar=1")
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", img, "-t", f"{D:.3f}",
             "-filter_complex", fc] + enc + [out])
    return out

def main():
    plan = []
    for s in SCENES:
        sid = s["id"]
        wav, starts, D = build_audio(sid, s["lines"])
        ovs = []
        if s.get("card"):
            ovs.append((add_overlay(f"{sid}_card", card_html(s["card"])), 0, D))
        label = f'<div class="label">{s["label"]}</div>' if s.get("label") else ""
        for i, (tt, cap) in enumerate(s["lines"]):
            cap = cap or tt
            body = (BRAND if not s.get("card") else "") + label + '<div class="shade"></div>' + f'<div class="cap">{html.escape(cap)}</div>'
            end = starts[i + 1] if i + 1 < len(starts) else D
            ovs.append((add_overlay(f"{sid}_l{i}", body), starts[i] - 0.15 if i else 0, end))
        plan.append((s, wav, D, ovs))
        print(f"{sid}: {D:.1f}s", flush=True)

    with ThreadPoolExecutor(6) as ex: list(ex.map(shoot, jobs))

    scene_files = []
    def render(item):
        s, wav, D, ovs = item; sid = s["id"]
        base = base_video(sid, s["visual"], D, s.get("dim"))
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", base]
        for p, _, _ in ovs: cmd += ["-loop", "1", "-framerate", str(FPS), "-i", p]
        cmd += ["-i", wav]
        chain, last = [], "[0:v]"
        for k, (p, a, b) in enumerate(ovs):
            nxt = f"[v{k}]"
            chain.append(f"{last}[{k+1}:v]overlay=0:0:enable='between(t,{max(a,0):.3f},{b:.3f})'{nxt}")
            last = nxt
        chain.append(f"{last}fade=t=in:st=0:d=0.25,fade=t=out:st={D-0.3:.3f}:d=0.3,format=yuv420p[vout]")
        cmd += ["-filter_complex", ";".join(chain), "-map", "[vout]", "-map", f"{len(ovs)+1}:a",
                "-t", f"{D:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-r", str(FPS),
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", f"{SC}/{sid}.mp4"]
        run(cmd); return f"{SC}/{sid}.mp4"
    with ThreadPoolExecutor(3) as ex: scene_files = list(ex.map(render, plan))

    lst = f"{OUT}/all.txt"; open(lst, "w").write("".join(f"file '{f}'\n" for f in scene_files))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{OUT}/all.mp4"])
    T = dur(f"{OUT}/all.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/all.mp4", "-stream_loop", "-1", "-i", f"{HF}/music.mp3",
         "-filter_complex",
         f"[1:a]atrim=0:{T:.3f},asetpts=N/SR/TB,volume=0.13,afade=t=in:st=0:d=1.5,afade=t=out:st={T-3:.3f}:d=3[m];"
         f"[0:a]volume=1.5[v];[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", FINAL])
    print(f"DONE {FINAL} {T:.1f}s  (your recordings used: {len(USED)} lines; the rest are Yuna)")
    json.dump([(s['id'], D) for s, _, D, _ in plan], open(f"{OUT}/timing.json", "w"))

main()
