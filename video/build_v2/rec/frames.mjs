// HTML 애니메이션 → 프레임 시퀀스 (결정적 렌더링)
// 모든 CSS 애니메이션을 멈추고 currentTime 을 직접 지정 + window.seek(t) 호출로 카운터·타이핑 등을 갱신한다.
// 사용법: node frames.mjs jobs.json   (jobs: [{html, out, dur, fps, alpha, hold}])
//   hold: 이 시간(초) 이후는 화면이 변하지 않으므로 캡처를 멈춘다(나머지는 ffmpeg 에서 마지막 프레임 유지)
import { chromium } from "playwright-core";
import fs from "node:fs";

const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const browser = await chromium.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: true,
  args: ["--allow-file-access-from-files", "--font-render-hinting=none"] });
const W = 1080, H = 1920, PAR = 5;

async function runJob(ctx, j) {
  const page = await ctx.newPage();
  await page.goto("file://" + j.html, { waitUntil: "load" });
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map((im) => im.complete ? 0 : new Promise((r) => { im.onload = im.onerror = r; })));
  });
  fs.mkdirSync(j.out, { recursive: true });
  const fps = j.fps || 30, end = Math.min(j.dur, j.hold ?? j.dur);
  const n = Math.max(1, Math.ceil(end * fps));
  for (let i = 0; i < n; i++) {
    const t = i / fps;
    await page.evaluate((t) => {
      for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
      if (window.seek) window.seek(t);
    }, t);
    const p = `${j.out}/f${String(i).padStart(5, "0")}.${j.alpha ? "png" : "jpg"}`;
    await page.screenshot(j.alpha ? { path: p, omitBackground: true } : { path: p, type: "jpeg", quality: 93 });
  }
  await page.close();
  return n;
}

const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
let idx = 0;
async function worker() {
  while (idx < jobs.length) {
    const j = jobs[idx++];
    const n = await runJob(ctx, j);
    console.log(`frames ${j.out.split("/").pop()} ${n}`);
  }
}
await Promise.all(Array.from({ length: PAR }, worker));
await browser.close();
