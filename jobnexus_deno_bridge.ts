// jobnexus_deno_bridge.ts
import express from "npm:express@4.18.2";
import cors from "npm:cors@2.8.5";
import puppeteer from "npm:puppeteer-extra@3.3.6";
import StealthPlugin from "npm:puppeteer-extra-plugin-stealth@2.11.2";
import RecaptchaPlugin from "npm:puppeteer-extra-plugin-recaptcha@3.6.8";

puppeteer.use(StealthPlugin());
puppeteer.use(
  RecaptchaPlugin({
    provider: {
        id: '2captcha', // Change to 'anticaptcha' if you swapped providers
        token: Deno.env.get("CAPTCHA_KEY") || 'YOUR_OMNIFEED_KEY_HERE'
    },
    visualFeedback: true // Color-codes CAPTCHA solving in the visual browser for debugging
  })
);

const app = express();
app.use(cors());

// --- INDEED SCRAPER ---
app.get('/api/indeed', async (req: any, res: any) => {
  const q = req.query.q || '';
  const l = req.query.l || '';
  console.log(`[Indeed] Deno Scrape Initiated: "${q}" in "${l}"`);

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: "new",
      executablePath: "/usr/bin/google-chrome",
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    const url = `https://www.indeed.com/jobs?q=${encodeURIComponent(q)}&l=${encodeURIComponent(l)}&sort=date`;
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

    // Auto-solve Datadome/Cloudflare CAPTCHAs
    await page.solveRecaptchas();
    await page.waitForSelector('.job_seen_beacon', { timeout: 15000 }).catch(() => {});

    const jobs = await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('.job_seen_beacon'));
      return cards.map((card, index) => {
        const titleEl = card.querySelector('h2.jobTitle span[title]') as HTMLElement;
        const companyEl = card.querySelector('[data-testid="company-name"]') as HTMLElement;
        const locEl = card.querySelector('[data-testid="text-location"]') as HTMLElement;
        const salEl = card.querySelector('.salary-snippet-container') as HTMLElement;
        const descEl = card.querySelector('.job-snippet') as HTMLElement;
        const linkEl = card.querySelector('h2.jobTitle a') as HTMLAnchorElement;

        return {
          id: `ind-${Date.now()}-${index}`,
          title: titleEl ? titleEl.innerText.trim() : 'Unknown',
          company: companyEl ? companyEl.innerText.trim() : 'Unknown',
          location: locEl ? locEl.innerText.trim() : 'Remote',
          salaryRaw: salEl ? salEl.innerText.trim() : '',
          description: descEl ? descEl.innerText.trim() : '',
          link: linkEl ? linkEl.href : '',
          source: 'Indeed', srcAbbr: 'IN', srcColor: '#34d399',
          postedDays: 0, verified: true
        };
      });
    });

    console.log(`[Indeed] Scraped ${jobs.length} listings successfully.`);
    res.json(jobs);
  } catch (error: any) {
    console.error('[Indeed] Deno Scrape Error:', error.message);
    res.status(500).json({ error: error.message });
  } finally {
    if (browser) await browser.close();
  }
});

// --- ZIPRECRUITER SCRAPER ---
app.get('/api/ziprecruiter', async (req: any, res: any) => {
  const q = req.query.q || '';
  const l = req.query.l || '';
  console.log(`[ZipRecruiter] Deno Scrape Initiated: "${q}" in "${l}"`);

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: "new",
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    const url = `https://www.ziprecruiter.com/jobs-search?search=${encodeURIComponent(q)}&location=${encodeURIComponent(l)}&days=5`;

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.solveRecaptchas();
    await page.waitForSelector('.job_result', { timeout: 15000 }).catch(() => {});

    const jobs = await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('.job_result'));
      return cards.map((card, index) => {
        const titleEl = card.querySelector('h2.title a') as HTMLAnchorElement;
        const companyEl = card.querySelector('a.company_name') as HTMLElement;
        const locEl = card.querySelector('a.company_location') as HTMLElement;
        const descEl = card.querySelector('p.job_snippet') as HTMLElement;

        return {
          id: `zip-${Date.now()}-${index}`,
          title: titleEl ? titleEl.innerText.trim() : 'Unknown Title',
          company: companyEl ? companyEl.innerText.trim() : 'Unknown Company',
          location: locEl ? locEl.innerText.trim() : 'Remote',
          salaryRaw: '',
          description: descEl ? descEl.innerText.trim() : '',
          link: titleEl ? titleEl.href : '',
          source: 'ZipRecruiter', srcAbbr: 'ZR', srcColor: '#fbbf24',
          postedDays: 0, verified: true
        };
      });
    });

    console.log(`[ZipRecruiter] Scraped ${jobs.length} listings successfully.`);
    res.json(jobs);
  } catch (error: any) {
    console.error('[ZipRecruiter] Deno Scrape Error:', error.message);
    res.status(500).json({ error: error.message });
  } finally {
    if (browser) await browser.close();
  }
});

const PORT = 3456;
app.listen(PORT, () => console.log(`🚀 JobNexus Deno API Bridge running on http://localhost:${PORT}`));
app.get('/api/system', async (req: any, res: any) => {
  const cmd = req.query.cmd;
  const command = new Deno.Command("python3", {
    args: ["/home/tsann/Scripts/JohsNexus_GUI/system_integrator.py", cmd],
  });
  const { stdout } = await command.output();
  res.send(new TextDecoder().decode(stdout));
});
// ... existing app.listen line ...

// --- SYSTEM INTEGRATION ENDPOINT ---
app.get('/api/system', async (req: any, res: any) => {
  const cmd = req.query.cmd;
  console.log(`[System] Executing integrator command: ${cmd}`);
  try {
    const command = new Deno.Command("python3", {
      args: ["/home/tsann/Scripts/JohsNexus_GUI/system_integrator.py", cmd],
    });
    const { stdout } = await command.output();
    res.send(new TextDecoder().decode(stdout));
  } catch (err) {
    console.error(`[System] Command failed: ${err.message}`);
    res.status(500).send("ERROR");
  }
});
