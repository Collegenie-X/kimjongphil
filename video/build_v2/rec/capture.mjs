// 실제 서비스 화면 캡처 (모바일 뷰포트, 전체 페이지). 스크롤로 lazy/등장 애니메이션을 모두 띄운 뒤 찍는다.
// 사용법: node video/build_v2/rec/capture.mjs [id ...]
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "..", "assets", "screens");
fs.mkdirSync(OUT, { recursive: true });

export const TARGETS = [
  { id: "aimakerlab", url: "https://aimakerlab.com/curriculum/vive-coding" },
  { id: "lingopang", url: "https://www.lingopang.com/" },
  { id: "playstore", url: "https://play.google.com/store/apps/details?id=com.yk.lingopang&hl=ko" },
  { id: "careerpath", url: "https://ai-career-path-eight.vercel.app/" },
  { id: "readingclue", url: "https://www.readingclue.com/" },
  { id: "teenspark", url: "https://teenspark.vercel.app/" },
  { id: "zzingong", url: "https://zzingongai.vercel.app/" },
  { id: "deepq", url: "https://deepq-omega.vercel.app/" },
  { id: "maum", url: "https://teen-dramaro.vercel.app/about/" },
  { id: "stock", url: "https://stock-simulation-delta.vercel.app/" },
];

const MAX_H = 7000; // css px
const want = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: true });
for (const t of TARGETS.filter((t) => !want.length || want.includes(t.id))) {
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, locale: "ko-KR",
    userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
  });
  const page = await ctx.newPage();
  try {
    await page.goto(t.url, { waitUntil: "networkidle", timeout: 45000 }).catch(() => page.waitForTimeout(3000));
    await page.waitForTimeout(1500);
    // 천천히 끝까지 스크롤해서 whileInView/lazy 이미지 로드
    let y = 0;
    for (let i = 0; i < 40; i++) {
      const h = await page.evaluate(() => document.documentElement.scrollHeight);
      if (y >= Math.min(h, MAX_H)) break;
      y += 500; await page.mouse.wheel(0, 500); await page.waitForTimeout(250);
    }
    await page.waitForTimeout(800);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(1200);
    const h = Math.min(await page.evaluate(() => document.documentElement.scrollHeight), MAX_H);
    await page.screenshot({ path: path.join(OUT, `${t.id}.png`), clip: { x: 0, y: 0, width: 390, height: h }, fullPage: true, animations: "disabled" });
    console.log(`ok ${t.id} ${h}px`);
  } catch (e) {
    console.log(`FAIL ${t.id} ${e.message.split("\n")[0]}`);
  }
  await ctx.close();
}
await browser.close();
