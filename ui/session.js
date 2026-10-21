/* Portable session data and explicit local exports. No network or provider calls. */
(function (root, factory) {
    const api = factory();
    if (typeof module === 'object' && module.exports) module.exports = api;
    else root.GTMSession = api;
})(typeof globalThis === 'undefined' ? this : globalThis, function () {
    'use strict';
    const titles = ['Interaction frequency', 'Incumbent alternatives', 'User and buyer',
        'Initial market and expansion', 'Value delivery', 'Model and context control',
        'Pricing and costs', 'Integration and exit'];
    const schema = 'socratic-gtm.session.v1';
    const maxBytes = 262144;
    const isObject = value => value !== null && typeof value === 'object' && !Array.isArray(value);
    function text(value, name, max = 10000) {
        if (typeof value !== 'string' || value.length > max) throw new Error(name + ' must be text within ' + max + ' characters.');
        return value;
    }
    function normalize(value) {
        if (!isObject(value) || value.schema !== schema) throw new Error('Unsupported session format.');
        if (new TextEncoder().encode(JSON.stringify(value)).length > maxBytes) throw new Error('Session exceeds 256 KiB.');
        if (!Number.isInteger(value.phase) || value.phase < 0 || value.phase > 9) throw new Error('Session phase must be 0 through 9.');
        if (!isObject(value.context) || !isObject(value.context.phases) || !isObject(value.reviews)) {
            throw new Error('Session context and reviews must be objects.');
        }
        const clean = {schema, name: text(value.name, 'Project name', 200), phase: value.phase,
            draft: text(value.draft || '', 'Draft'), context: {concept: text(value.context.concept || '', 'Concept'), phases: {}},
            reviews: {}};
        for (const [key, answer] of Object.entries(value.context.phases)) {
            if (!/^[1-8]$/.test(key)) throw new Error('Unknown answer phase.');
            clean.context.phases[key] = text(answer, 'Answer');
        }
        for (const [key, review] of Object.entries(value.reviews)) {
            if (!/^[1-8]$/.test(key) || !isObject(review)) throw new Error('Invalid evidence record.');
            const date = text(review.date || '', 'Decision date', 10);
            if (date && (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !Number.isFinite(Date.parse(date))
                || new Date(date).toISOString().slice(0, 10) !== date)) throw new Error('Invalid decision date.');
            clean.reviews[key] = {evidence: text(review.evidence || '', 'Evidence'),
                experiment: text(review.experiment || '', 'Experiment'),
                owner: text(review.owner || '', 'Owner', 200), date};
        }
        if (value.prep !== undefined) {
            const prep = typeof module === 'object' && module.exports ? require('./prep.js') : globalThis.GTMPrep;
            if (!prep) throw new Error('Practice module is unavailable; current session retained.');
            clean.prep = prep.normalize(value.prep);
        }
        return clean;
    }
    function parse(raw) {
        if (typeof raw !== 'string' || new TextEncoder().encode(raw).length > maxBytes) throw new Error('Session exceeds 256 KiB.');
        return normalize(JSON.parse(raw));
    }
    function serialize(value) {
        const raw = JSON.stringify(normalize(value), null, 2);
        if (new TextEncoder().encode(raw).length > maxBytes) throw new Error('Session exceeds 256 KiB. Export and remove old practice attempts.');
        return raw;
    }
    const indent = value => String(value || 'EVIDENCE REQUIRED').split(/\r?\n/).map(line => '    ' + line).join('\n');
    function playbook(value) {
        const s = normalize(value);
        const lines = ['# GTM review draft', '', 'Project:', indent(s.name),
            '', 'Founder-reported inputs and reviewer notes. No strategic validation or confidence probability is inferred.',
            '', '## Startup concept', '', indent(s.context.concept)];
        titles.forEach((title, i) => {
            const key = String(i + 1), review = s.reviews[key] || {};
            lines.push('', '## ' + key + '. ' + title, '', 'Founder answer:', indent(s.context.phases[key]),
                '', 'Evidence / source / counterexample:', indent(review.evidence),
                '', 'Next falsifiable experiment:', indent(review.experiment),
                '', 'Owner:', indent(review.owner), '', 'Decision date:', indent(review.date));
        });
        if (s.draft) lines.push('', '## Unsent draft', '', indent(s.draft));
        return lines.join('\n') + '\n';
    }
    function csvCell(value) {
        let s = String(value || '');
        if (/^[\s]*[=+\-@\t\r]/.test(s)) s = "'" + s;
        return '"' + s.replace(/"/g, '""') + '"';
    }
    function experimentsCSV(value) {
        const s = normalize(value);
        const rows = [['Phase', 'Topic', 'Founder answer', 'Evidence', 'Next experiment', 'Owner', 'Decision date', 'Status']];
        titles.forEach((title, i) => {
            const key = String(i + 1), r = s.reviews[key] || {};
            rows.push([key, title, s.context.phases[key], r.evidence, r.experiment, r.owner, r.date, 'REVIEW_REQUIRED']);
        });
        return rows.map(row => row.map(csvCell).join(',')).join('\r\n') + '\r\n';
    }
    return {titles, normalize, parse, serialize, playbook, experimentsCSV, maxBytes, schema};
});
