/* Run with an already-installed Playwright module; does not install browsers. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {spawn} = require('node:child_process');
const {chromium} = require(process.env.GTM_PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '..');
const out = path.join(root, '.factory/evidence/browser');
fs.mkdirSync(out, {recursive: true});
const server = spawn(process.env.GTM_PYTHON || 'python',
    ['-c', 'import server; server.start_server(port=0, open_browser=False)'],
    {cwd: root, stdio: ['ignore', 'pipe', 'pipe']});
const observations = [];
let browser;
let testPage;
const pass = (id, detail) => observations.push({id, status: 'PASS', detail});

(async () => {
    const url = await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => reject(new Error('Local server did not start')), 10000);
        server.stderr.on('data', data => {
            const match = data.toString().match(/http:\/\/127\.0\.0\.1:\d+\/ui\/index\.html/);
            if (match) { clearTimeout(timeout); resolve(match[0]); }
        });
        server.on('error', reject);
    });
    browser = await chromium.launch({headless: true, channel: 'chrome'});
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}, acceptDownloads: true});
    testPage = page;
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('dialog', dialog => dialog.accept());
    await page.goto(url, {waitUntil: 'networkidle'});
    await page.waitForFunction(() => typeof GTMSession !== 'undefined');
    await page.getByTitle('Voice & API Key Settings').click();
    await page.locator('#sttProviderSelect').selectOption('openai');
    await page.locator('#sttApiKeyInput').fill('fixture-transcription-key');
    await page.locator('#ttsProviderSelect').selectOption('elevenlabs');
    await page.locator('#ttsApiKeyInput').fill('fixture-speech-key');
    await page.locator('#elevenVoiceId').fill('fixtureVoice123');
    await page.getByRole('button', {name: 'Save Settings', exact: true}).click();
    assert.equal(await page.evaluate(() => voiceConfig.sttApiKey), 'fixture-transcription-key');
    assert.equal(await page.evaluate(() => JSON.stringify(localStorage).includes('fixture-transcription-key')), false);
    assert.equal(await page.evaluate(() => GTMSession.serialize(snapshotSession()).includes('fixture-speech-key')), false);
    await page.reload({waitUntil: 'networkidle'});
    assert.equal(await page.evaluate(() => voiceConfig.sttApiKey), '');
    assert.equal(await page.evaluate(() => voiceConfig.ttsApiKey), '');
    pass('voice_integration', 'Voice provider controls preserved; fixture keys stayed in memory and were excluded from device/session data. No provider call made.');
    await page.locator('#projectName').fill('Founder pilot');
    await page.locator('#userInput').fill('We help independent founders review their weekly customer interviews.');
    await page.locator('#sendBtn').click();
    await page.waitForFunction(() => currentPhase === 1);
    await page.locator('#userInput').fill('Weekly, based on interviews with 5 founders. Referral demand is still unknown.');
    await page.locator('#sendBtn').click();
    await page.waitForFunction(() => currentPhase === 2);
    assert.equal(await page.evaluate(() => accumulatedContext.phases['1'].includes('5 founders')), true);
    pass('intake_context', 'Two API turns retained concept and answer; no numerical confidence gate.');

    await page.locator('#reviewAnswersBtn').click();
    await page.locator('#reviewAnswer').fill('Weekly demand; observed in 5 founder interviews.');
    await page.locator('#reviewEvidence').fill('Interview notes dated 2026-10-20; small self-selected sample.');
    await page.locator('#reviewExperiment').fill('=Test 3 paid pilot offers; stop after 7 days without interest.');
    await page.locator('#reviewOwner').fill('Founder');
    await page.locator('#reviewDate').fill('2026-11-01');
    await page.getByRole('button', {name: 'Save changes', exact: true}).click();
    assert.match(await page.locator('#reviewStatus').innerText(), /saved/);
    await page.getByRole('button', {name: 'Close answer review'}).click();
    await page.locator('#rememberSession').check();
    await page.reload({waitUntil: 'networkidle'});
    assert.equal(await page.locator('#rememberSession').isChecked(), true);
    assert.equal(await page.evaluate(() => currentPhase), 2);
    assert.match(await page.evaluate(() => sessionReviews['1'].evidence), /self-selected/);
    pass('session_roundtrip', 'Opt-in device save survived reload with revised answer, evidence, experiment, owner and date.');

    async function captureDownload(action, filename) {
        const waiting = page.waitForEvent('download');
        await action();
        const download = await waiting;
        const target = path.join(out, filename);
        await download.saveAs(target);
        return fs.readFileSync(target, 'utf8');
    }
    const md = await captureDownload(() => page.getByRole('button', {name: 'Draft playbook', exact: true}).click(), 'playbook.md');
    assert.match(md, /5 founder interviews/);
    assert.match(md, /self-selected sample/);
    assert.match(md, /EVIDENCE REQUIRED/);
    const raw = await captureDownload(() => page.getByRole('button', {name: 'Save session file'}).click(), 'session.json');
    const saved = JSON.parse(raw);
    assert.equal(saved.name, 'Founder pilot');
    const csv = await captureDownload(() => page.locator('#moreTools').selectOption('experiments'), 'experiments.csv');
    assert.match(csv, /"'=Test 3 paid pilot/);
    pass('review_exports', 'Downloaded actual playbook, JSON and formula-neutralized CSV, preserving edited inputs.');

    await page.locator('#sessionFile').setInputFiles({name: 'bad.json', mimeType: 'application/json', buffer: Buffer.from('{"schema":"invalid"}')});
    await page.waitForFunction(() => document.getElementById('workspaceStatus').textContent.includes('Import failed'));
    assert.equal(await page.evaluate(() => currentPhase), 2);
    const hostile = {...saved, name: '<img src=x onerror="window.injected=1">'};
    hostile.context.phases['1'] = '</script><img src=x onerror="window.injected=1">';
    await page.locator('#sessionFile').setInputFiles({name: 'session.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(hostile))});
    await page.waitForFunction(() => document.getElementById('projectName').value.includes('<img'));
    assert.match(await page.locator('#workspaceStatus').innerText(), /Session loaded/);
    assert.equal(await page.evaluate(() => window.injected), undefined);
    pass('import_rejection_xss', 'Malformed session retained active state; hostile imported text did not execute.');

    const before = await page.evaluate(() => currentPhase);
    await page.route('**/api/chat', route => route.fulfill({status: 500, contentType: 'application/json', body: '{"error":"Injected API failure"}'}));
    await page.locator('#userInput').fill('Keep this answer after a failed request.');
    await page.locator('#sendBtn').click();
    await page.getByText('Injected API failure', {exact: false}).waitFor();
    assert.equal(await page.evaluate(() => currentPhase), before);
    assert.equal(await page.locator('#userInput').inputValue(), 'Keep this answer after a failed request.');
    await page.unroute('**/api/chat');
    pass('api_failure_recovery', 'Injected 500 retained phase and recoverable answer; no synthetic success.');
    await page.locator('#rememberSession').uncheck();
    assert.equal(await page.evaluate(() => localStorage.getItem(SESSION_KEY)), null);
    pass('device_copy_removal', 'Disabling device saving removed the saved copy.');

    const artifact = await page.evaluate(async () => {
        const response = await fetch('/api/simulate', {method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({project_name: '</script><img src=x onerror="window.injected=1">', scores: [0,0,0,0,0,0,0,0]})});
        return response.json();
    });
    const radar = await browser.newPage();
    await radar.route('**/cdn.jsdelivr.net/**', route => route.abort());
    await radar.goto(new URL(artifact.path, url).href);
    const row = await radar.locator('#vectorTableBody tr').first().innerText();
    assert.match(row, /0\/100/);
    assert.equal(await radar.evaluate(() => window.injected), undefined);
    assert.notEqual(await radar.locator('#marginVal').innerText(), '');
    const oldCost = await radar.locator('#costVal').innerText();
    await radar.locator('#tasksInput').fill('100');
    await radar.locator('#tasksInput').dispatchEvent('input');
    assert.notEqual(await radar.locator('#costVal').innerText(), oldCost);
    await radar.close();
    pass('simulator_runtime', 'Generated artifact preserves zero and escapes hostile project text; table and calculator work with chart CDN blocked.');

    await page.setViewportSize({width: 390, height: 844});
    await page.locator('#reviewAnswersBtn').click();
    await page.locator('#reviewPhase').selectOption('2');
    await page.locator('#reviewEvidence').fill('Needs competitor research.');
    await page.getByRole('button', {name: 'Continue interview here'}).click();
    assert.equal(await page.evaluate(() => currentPhase), 2);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    assert.equal(await page.locator('#reviewAnswersBtn').isVisible(), true);
    await page.evaluate(saved => applySession(saved), saved);
    await page.screenshot({path: path.join(out, 'mobile.png'), fullPage: true});
    pass('mobile_session_controls', '390px viewport: review, evidence edit and resume accessible; zero horizontal overflow.');
    await page.setViewportSize({width: 1440, height: 1000});
    await page.screenshot({path: path.join(out, 'desktop.png'), fullPage: true});
    await page.locator('#reviewAnswersBtn').click();
    await page.screenshot({path: path.join(out, 'review.png'), fullPage: true});
    assert.deepEqual(errors, []);
    pass('browser_runtime', 'No uncaught browser JavaScript errors across tested actions.');
})().catch(async error => {
    if (testPage) {
        console.error(await testPage.locator('#workspaceStatus').innerText());
        await testPage.screenshot({path: path.join(out, 'failure.png'), fullPage: true});
    }
    observations.push({id: 'browser_runtime', status: 'FAIL', detail: error.stack});
    console.error(error);
    process.exitCode = 1;
}).finally(async () => {
    fs.writeFileSync(path.join(out, 'observations.json'), JSON.stringify({
        observed_at: new Date().toISOString(), profile: 'Chrome headless, desktop 1440x1000 and mobile 390x844',
        observations}, null, 2));
    if (browser) await browser.close();
    server.kill();
    console.log(JSON.stringify(observations));
});
