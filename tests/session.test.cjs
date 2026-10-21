const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const context = vm.createContext({TextEncoder});
vm.runInContext(fs.readFileSync(require('node:path').join(__dirname, '../ui/prep.js'), 'utf8'), context);
vm.runInContext(fs.readFileSync(require('node:path').join(__dirname, '../ui/session.js'), 'utf8'), context);
const api = context.GTMSession;
const base = () => ({schema: api.schema, name: 'Pilot', phase: 2, draft: 'Unsent',
    context: {concept: 'Tools for a founder', phases: {'1': 'Weekly review'}},
    reviews: {'1': {evidence: 'Interview 1, 2026-10-20', experiment: 'Offer paid pilot', owner: 'Rick', date: '2026-11-01'}}});

test('session roundtrip preserves answers, draft and evidence', () => {
    const session = base();
    assert.deepEqual(JSON.parse(JSON.stringify(api.parse(api.serialize(session)))), session);
});
test('invalid imports are rejected', () => {
    for (const mutate of [
        s => s.schema = 'other', s => s.phase = 99, s => s.context.phases['9'] = 'bad',
        s => s.context.phases['1'] = [], s => s.reviews['1'].date = '2026-02-30',
        s => s.reviews['1'].owner = 'x'.repeat(201), s => s.reviews = [],
        s => s.context.concept = 'x'.repeat(10001),
    ]) {
        const s = base(); mutate(s);
        assert.throws(() => api.normalize(s));
    }
    assert.throws(() => api.parse('x'.repeat(api.maxBytes + 1)));
    assert.throws(() => api.parse('{'));
    assert.throws(() => api.parse('null'));
});
test('unknown object properties cannot pollute prototypes', () => {
    const raw = JSON.stringify(base()).replace('"phases":{', '"phases":{"__proto__":{"polluted":true},');
    assert.throws(() => api.parse(raw));
    assert.equal({}.polluted, undefined);
});
test('playbook retains inputs as text and marks unknown evidence', () => {
    const s = base();
    s.context.phases['1'] = '</script><img src=x onerror=alert(1)>';
    const md = api.playbook(s);
    assert.ok(md.includes('    </script><img'));
    assert.ok(md.includes('Interview 1'));
    assert.ok(md.includes('EVIDENCE REQUIRED'));
    assert.equal((md.match(/^## [1-8]\./gm) || []).length, 8);
});
test('CSV preserves quotes, commas and multiline values; neutralizes formulas', () => {
    const s = base();
    s.reviews['1'].experiment = '=HYPERLINK("evil", "click")\nsecond line';
    s.reviews['1'].owner = '  +SUM(1,2)';
    const csv = api.experimentsCSV(s);
    assert.ok(csv.includes('"\'=HYPERLINK(""evil"", ""click"")\nsecond line"'));
    assert.ok(csv.includes('"\'  +SUM(1,2)"'));
    assert.ok(csv.includes('"REVIEW_REQUIRED"'));
});

test('practice_restore: legacy files work and practice data is validated before replacement', () => {
    assert.equal(api.normalize(base()).prep, undefined);
    const session = base();
    session.prep = context.GTMPrep.upsertClaim(context.GTMPrep.empty(), {text: 'Observed weekly need.'});
    assert.equal(api.parse(api.serialize(session)).prep.claims[0].text, 'Observed weekly need.');
    const original = api.serialize(session);
    session.prep.activeId = 'r99';
    assert.throws(() => api.normalize(session));
    assert.equal(api.parse(original).prep.activeId, '');
});
