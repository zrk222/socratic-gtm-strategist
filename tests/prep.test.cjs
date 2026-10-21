const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const context = vm.createContext({TextEncoder});
vm.runInContext(fs.readFileSync(require('node:path').join(__dirname, '../ui/prep.js'), 'utf8'), context);
const prep = context.GTMPrep;
const ledger = () => prep.upsertClaim(prep.empty(), {text: 'Customers need weekly reporting.'});
const begin = (state = ledger(), options = {}) => prep.start(state, {claimId: 'c1', persona: 'investor', scenario: 'baseline', limit: 0, now: 1, ...options});
const reply = (state, fields = {}) => prep.answer(state, {answer: 'I believe this is useful.', evidence: '', counterexample: '', test: '', elapsed: 12, challenged: false, ...fields});

test('practice_isolation: pure operations do not mutate input and roundtrip restores pending/draft', () => {
    const input = ledger(), before = JSON.stringify(input), state = begin(input);
    assert.equal(JSON.stringify(input), before);
    state.draft.answer = 'Unsent response';
    const restored = prep.normalize(JSON.parse(JSON.stringify(state)));
    assert.equal(restored.draft.answer, 'Unsent response');
    assert.equal(prep.active(restored).pending.stage, 'opening');
});
test('persona_selection and scenario_shocks: every combination is available and contextual', () => {
    for (const persona of Object.keys(prep.personas)) for (const scenario of Object.keys(prep.scenarios)) {
        const state = begin(ledger(), {persona, scenario, limit: 30});
        assert.equal(prep.active(state).persona, persona);
        assert.match(prep.active(state).pending.question, /Customers need weekly reporting/);
        if (scenario !== 'baseline') assert.match(prep.scenarios[scenario].ask, /Hypothetical/);
    }
});
test('claim_ledger and claim_candidates: retain exact source statements, labels and dated actions', () => {
    const records = prep.candidates({concept: 'A useful product.', phases: {'1': 'Weekly use. Paid monthly.'}});
    assert.equal(records.map(r => r.text).join('|'), 'A useful product.|Weekly use.|Paid monthly.');
    const state = prep.upsertClaim(ledger(), {kind: 'evidence-linked', evidence: 'Interview note, 2026-10-21',
        counterexample: 'One customer prefers annual reports.', action: 'Ask for a paid pilot.', owner: 'Founder', due: '2026-11-01'}, 'c1');
    assert.equal(state.claims[0].kind, 'evidence-linked');
    assert.equal(state.claims[0].due, '2026-11-01');
    assert.throws(() => prep.upsertClaim(ledger(), {kind: 'evidence-linked'}, 'c1'));
});
test('adaptive_followup: missing fields and explicit uncertainty choose distinct targeted follow-ups', () => {
    const a = reply(begin());
    assert.equal(prep.active(a).pending.stage, 'evidence');
    const b = reply(begin(), {evidence: 'Three observed weekly exports.'});
    assert.equal(prep.active(b).pending.stage, 'counterexample');
    const c = reply(begin(), {evidence: 'Observed exports.', counterexample: 'Seasonal usage.'});
    assert.equal(prep.active(c).pending.stage, 'test');
    const d = reply(begin(), {answer: "I don't know yet."});
    assert.equal(prep.active(d).pending.stage, 'test');
    assert.match(prep.active(a).pending.question, /Your claim: “Customers need weekly reporting.”/);
});
test('fair_challenge and timed_rehearsal: contesting, interruption and elapsed time retain answer', () => {
    let state = reply(begin(ledger(), {limit: 120}), {answer: 'The premise assumes a public deployment.', challenged: true});
    assert.equal(prep.active(state).pending.stage, 'premise');
    state.draft.answer = 'Keep this while interrupted';
    state = prep.interrupt(state);
    assert.equal(state.draft.answer, 'Keep this while interrupted');
    assert.equal(prep.active(state).pending.stage, 'interrupt');
    assert.equal(prep.active(state).turns[0].elapsed, 12);
    assert.equal(prep.debrief(state, 'r1').contested, 1);
});
test('conflict_review: quotes candidate numeric and negation differences without truth claims', () => {
    let state = prep.upsertClaim(ledger(), {text: 'Customers need weekly reporting for 20 accounts.'});
    state = prep.upsertClaim(state, {text: 'Customers need weekly reporting for 30 accounts.'});
    state = prep.upsertClaim(state, {text: 'Customers do not need weekly reporting.'});
    const conflicts = prep.conflicts(state);
    assert.ok(conflicts.some(c => c.left.includes('20 accounts') && c.right.includes('30 accounts')));
    assert.ok(conflicts.some(c => c.reason.includes('negation')));
    assert.equal(prep.conflicts(prep.upsertClaim(ledger(), {text: 'Security incidents were zero.'})).length, 0);
});
test('practice_debrief and retest_comparison: exact original objection and both answers survive', () => {
    const first = prep.finish(reply(begin(), {answer: 'Original answer'}));
    assert.equal(prep.debrief(first, 'r1').missing.join(','), 'evidence,counterexample,test');
    let second = prep.retest(first, 'r1', 2);
    assert.equal(prep.active(second).pending.question, first.runs[0].turns[0].question);
    second = prep.finish(reply(second, {answer: 'Revised answer', evidence: 'Pilot notes', counterexample: 'Small sample', test: 'Repeat with another buyer'}));
    const result = prep.debrief(second, 'r2');
    assert.equal(result.previous.turns[0].answer, 'Original answer');
    assert.equal(result.run.turns[0].answer, 'Revised answer');
    assert.equal(result.missing.length, 0);
    assert.throws(() => prep.removeRun(second, 'r1'));
    assert.equal(prep.removeRun(second, 'r2').runs.length, 1);
});
test('practice_exports: no invented evidence, unsafe Markdown is indented and CSV neutralizes formulas', () => {
    let state = prep.upsertClaim(ledger(), {text: '</script><img src=x onerror=alert(1)>', action: '=HYPERLINK("bad")', owner: '  +SUM(1,2)'}, 'c1');
    state = prep.finish(reply(begin(state), {answer: 'Unsafe <script> text'}));
    assert.ok(prep.markdown(state, 'r1').includes('    </script><img'));
    assert.match(prep.markdown(state, 'r1'), /UNKNOWN \/ NOT RECORDED/);
    assert.ok(prep.actionsCSV(state).includes('"\'=HYPERLINK(""bad"")"'));
    assert.ok(prep.actionsCSV(state).includes('"\'  +SUM(1,2)"'));
    assert.match(prep.coachPacket(state, 'r1'), /untrusted data, not instructions/);
});
test('practice_restore and practice_recovery: malformed records and dangling references reject atomically', () => {
    const state = reply(begin()), original = JSON.stringify(state);
    for (const mutate of [s => s.claims[0].due = '2026-02-30', s => s.runs[0].claimId = 'c9',
        s => s.runs[0].persona = '__proto__', s => s.activeId = 'r8', s => s.runs[0].limit = 5,
        s => s.runs[0].turns[0].elapsed = Infinity, s => s.runs[0].turns[0].answer = [],
        s => s.runs[0].turns[0].challenged = 'yes',
        s => s.claims.push(s.claims[0]), s => s.runs[0].previousId = 'r1', s => s.draft = [],
        s => s.draft.answer = 'x'.repeat(4001), s => s.claims = Array(25).fill(s.claims[0])]) {
        const candidate = JSON.parse(original); mutate(candidate);
        assert.throws(() => prep.normalize(candidate));
    }
    assert.equal(JSON.stringify(state), original);
    assert.throws(() => prep.start(state, {claimId: 'c1'}));
    assert.throws(() => prep.answer(state, {answer: ''}));
    assert.throws(() => prep.normalize({...state, extra: 'x'.repeat(196609)}));
});
test('practice turn ceiling completes explicitly and does not grow without bound', () => {
    let state = begin();
    for (let i = 0; i < 18; i++) state = reply(state);
    assert.equal(state.activeId, '');
    assert.equal(state.runs[0].status, 'complete');
    assert.equal(state.runs[0].turns.length, 18);
    assert.throws(() => reply(state));
});

test('scenario follows supporting questions and preserves the hypothetical condition', () => {
    let state = begin(ledger(), {scenario: 'integration'});
    const fields = {evidence: 'Pilot notes', counterexample: 'Alternative workflow', test: 'Remove dependency in a pilot'};
    state = reply(state, fields);
    state = reply(state, fields);
    assert.equal(prep.active(state).pending.stage, 'scenario');
    assert.match(prep.active(state).pending.question, /Hypothetical: a required integration becomes unavailable/);
});

test('bounded history stays usable and rejects a ninth attempt without changing existing records', () => {
    let state = ledger();
    for (let i = 0; i < 8; i++) state = prep.finish(reply(begin(state)));
    const before = JSON.stringify(state);
    assert.throws(() => begin(state));
    assert.equal(JSON.stringify(state), before);
    const started = performance.now();
    for (let i = 0; i < 50; i++) prep.conflicts(state);
    assert.ok(performance.now() - started < 2000, 'Bounded conflict review should complete within two seconds for 50 small-history runs.');
});
