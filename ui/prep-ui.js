/* DOM adapter: text-only rendering, explicit actions, no provider calls. */
(function (root) {
    'use strict';
    const api = root.GTMPrep;
    let hooks, dialog, selectedClaim = '', selectedRun = '', returnFocus;
    const clock = {key: '', elapsed: 0, started: null, expired: false};
    const byId = id => document.getElementById(id);
    function element(tag, text, className = '') {
        const node = document.createElement(tag);
        if (text !== undefined) node.textContent = text;
        node.className = className;
        return node;
    }
    function button(text, id, action) {
        const node = element('button', text);
        node.type = 'button'; node.id = id; node.addEventListener('click', () => safely(action));
        return node;
    }
    function safely(action) {
        try { action(); }
        catch (error) { status(error.message); }
    }
    function status(message) { byId('prepStatus').textContent = message; }
    function labelled(parent, title, node, id) {
        node.id = id;
        const label = element('label', title); label.htmlFor = id;
        const wrap = element('div', undefined, 'prep-field'); wrap.append(label, node); parent.append(wrap);
        return node;
    }
    function select(parent, title, id, values) {
        const node = labelled(parent, title, element('select'), id);
        values.forEach(([value, label]) => { const option = element('option', label); option.value = value; node.append(option); });
        return node;
    }
    function field(parent, title, id, max = 2000, rows = 3) {
        const node = element('textarea'); node.maxLength = max; node.rows = rows;
        return labelled(parent, title, node, id);
    }
    function commit(next) { hooks.write(next); render(); }
    function buildHeader() {
        const header = element('header', undefined, 'prep-header');
        const intro = element('div');
        const title = element('h2', 'Prepare for the hard questions'); title.id = 'prepTitle';
        intro.append(element('p', 'ADVERSARIAL PRACTICE', 'prep-eyebrow'), title,
            element('p', 'Make a claim. Test your defense. Leave with the next thing to verify.'));
        header.append(intro, button('Close practice', 'prepClose', () => dialog.close()));
        const note = element('p', 'Guided local practice. Follow-ups use your claim and missing supporting fields. Possible conflicts need your review; this engine does not verify facts or run a language model.', 'prep-note');
        note.id = 'prepDescription';
        const live = element('p', 'Add a claim or pull statements from your interview to begin.', 'prep-status');
        live.id = 'prepStatus'; live.setAttribute('role', 'status');
        dialog.append(header, note, live);
    }
    function section(title, className = '') {
        const node = element('section', undefined, 'prep-section ' + className);
        node.append(element('h3', title)); return node;
    }
    function buildClaimEditor(parent) {
        const form = element('form'); form.id = 'prepClaimForm';
        select(form, 'Claim to review', 'prepClaimSelect', [['', 'Add a new claim']]);
        field(form, 'Claim or assumption', 'prepClaimText');
        select(form, 'Evidence label (your assessment)', 'prepClaimKind', api.kinds.map(k => [k, k]));
        const details = element('details'); details.append(element('summary', 'Evidence and next action'));
        field(details, 'Evidence / source / date — not independently verified', 'prepClaimEvidence', 4000);
        field(details, 'Strongest counterexample or alternative explanation', 'prepClaimCounterexample', 4000);
        field(details, 'Next test and disconfirming observation', 'prepClaimAction');
        const row = element('div', undefined, 'prep-grid');
        const owner = labelled(row, 'Action owner', element('input'), 'prepClaimOwner'); owner.maxLength = 200;
        const due = labelled(row, 'Decision date', element('input'), 'prepClaimDue'); due.type = 'date';
        details.append(row);
        select(details, 'Founder review status', 'prepClaimResolution', api.resolutions.map(k => [k, k]));
        const save = element('button', 'Save claim'); save.id = 'prepSaveClaim'; save.type = 'submit';
        form.append(details, save);
        form.addEventListener('submit', event => { event.preventDefault(); safely(saveClaim); });
        byIdLater(form, 'prepClaimSelect').addEventListener('change', event => { selectedClaim = event.target.value; renderClaim(); });
        parent.append(form);
    }
    function byIdLater(parent, id) { return parent.querySelector('#' + id); }
    function saveClaim() {
        const keys = {text: 'Text', kind: 'Kind', evidence: 'Evidence', counterexample: 'Counterexample', action: 'Action', owner: 'Owner', due: 'Due', resolution: 'Resolution'};
        const fields = {};
        Object.entries(keys).forEach(([key, suffix]) => { fields[key] = byId('prepClaim' + suffix).value; });
        const next = api.upsertClaim(hooks.read(), fields, selectedClaim);
        selectedClaim = selectedClaim || next.claims[next.claims.length - 1].id;
        commit(next); status('Claim saved. Labels and supporting notes remain founder supplied.');
    }
    function buildLedger() {
        const ledger = section('1 / Choose what to defend'); ledger.id = 'prepLedger';
        ledger.append(button('Pull statements from interview', 'prepExtract', showCandidates));
        const candidates = element('div'); candidates.id = 'prepCandidates'; ledger.append(candidates);
        buildClaimEditor(ledger);
        const conflicts = element('details'); conflicts.id = 'prepConflicts';
        conflicts.append(element('summary', 'Review possible conflicts'));
        const pairs = element('div'); pairs.id = 'prepConflictList'; conflicts.append(pairs); ledger.append(conflicts);
        return ledger;
    }
    function showCandidates() {
        const target = byId('prepCandidates'); target.replaceChildren();
        const candidates = api.candidates(hooks.context());
        if (!candidates.length) { status('No interview statements yet. Enter a claim below.'); return; }
        candidates.forEach((candidate, i) => {
            const card = element('div', undefined, 'prep-candidate');
            card.append(element('p', candidate.text), button('Add statement ' + (i + 1), 'prepCandidate' + i, () => {
                const state = hooks.read();
                if (state.claims.some(c => c.text === candidate.text)) throw new Error('That exact statement is already in the ledger.');
                const next = api.upsertClaim(state, {...candidate, kind: 'assertion'});
                selectedClaim = next.claims[next.claims.length - 1].id; commit(next);
                status('Verbatim statement added as an assertion. Review its wording and evidence.');
            })); target.append(card);
        });
    }
    function buildSetup(parent) {
        const setup = element('div', undefined, 'prep-grid');
        select(setup, 'Opposing perspective', 'prepPersona', Object.entries(api.personas).map(([k, v]) => [k, v.name]));
        select(setup, 'Hypothetical scenario', 'prepScenario', Object.entries(api.scenarios).map(([k, v]) => [k, v.name]));
        select(setup, 'Answer rehearsal', 'prepLimit', [['0', 'Untimed'], ['30', '30 seconds'], ['120', '2 minutes']]);
        parent.append(setup, button('Start cross-examination', 'prepStart', () => {
            if (Object.values(hooks.read().draft).some(value => value.trim()) &&
                !confirm('Start a new attempt and clear the unsent practice draft? Save a session file first to retain it.')) return;
            const state = api.start(hooks.read(), {claimId: selectedClaim, persona: byId('prepPersona').value,
                scenario: byId('prepScenario').value, limit: Number(byId('prepLimit').value)});
            selectedRun = state.activeId; commit(state); status('Practice started. Your interview remains at the same phase.');
            byId('prepAnswer').focus();
        }));
    }
    function buildResponse(parent) {
        const form = element('form'); form.id = 'prepAnswerForm';
        const question = element('p', '', 'prep-question'); question.id = 'prepQuestion'; question.tabIndex = -1;
        const criterion = element('p', '', 'prep-note'); criterion.id = 'prepCriterion';
        const timer = element('div', undefined, 'prep-actions');
        const output = element('output', 'Timer paused'); output.id = 'prepTimer';
        timer.append(output, button('Start timer', 'prepTimerToggle', toggleTimer),
            button('Interrupt me', 'prepInterrupt', () => { saveDraft(); commit(api.interrupt(hooks.read())); status('Interruption posed. Your draft is retained.'); }));
        field(form, 'Your defense — an explicit unknown is a valid answer', 'prepAnswer', 4000, 5);
        const details = element('details'); details.append(element('summary', 'Add supporting fields for targeted follow-ups'));
        field(details, 'Evidence cited / source / date', 'prepEvidence', 4000);
        field(details, 'Counterexample or alternative explanation', 'prepCounterexample', 4000);
        field(details, 'Next test and what would disprove the claim', 'prepTest');
        const contested = element('input'); contested.type = 'checkbox'; contested.id = 'prepContested';
        const label = element('label', undefined, 'prep-check'); label.append(contested, document.createTextNode(' I contest the premise; my answer explains the correction.'));
        const send = element('button', 'Answer and challenge further'); send.id = 'prepRespond'; send.type = 'submit';
        const actions = element('div', undefined, 'prep-actions');
        actions.append(send, button('Finish and debrief', 'prepFinish', () => {
            saveDraft(); commit(api.finish(hooks.read()));
            status('Practice retained. Review gaps and record the next test below.');
            byId('prepDebrief').focus();
        }));
        form.prepend(question, criterion, timer); form.append(details, label, actions);
        form.addEventListener('submit', event => { event.preventDefault(); safely(submitAnswer); });
        form.querySelectorAll('textarea').forEach(input => input.addEventListener('input', () => safely(saveDraft)));
        parent.append(form);
    }
    function buildPractice() {
        const practice = section('2 / Pressure-test your answer');
        buildSetup(practice); buildResponse(practice);
        const transcript = element('details'); transcript.append(element('summary', 'Review this attempt’s transcript'));
        const body = element('div'); body.id = 'prepTranscript'; transcript.append(body); practice.append(transcript);
        return practice;
    }
    function buildDebrief() {
        const sectionNode = section('3 / Leave with a better next move');
        select(sectionNode, 'Practice history', 'prepRunSelect', [['', 'No attempts yet']]);
        const result = element('div'); result.id = 'prepDebrief'; result.tabIndex = -1;
        const actions = element('div', undefined, 'prep-actions');
        actions.append(button('Retest this objection', 'prepRetest', () => {
            if (Object.values(hooks.read().draft).some(value => value.trim()) &&
                !confirm('Retest and clear the unsent practice draft? Save a session file first to retain it.')) return;
            const state = api.retest(hooks.read(), selectedRun); selectedRun = state.activeId;
            selectedClaim = api.active(state).claimId; commit(state); byId('prepAnswer').focus();
        }), button('Download debrief', 'prepDownload', () => hooks.download('GTM_PREP_DEBRIEF.md', api.markdown(hooks.read(), selectedRun), 'text/markdown')),
        button('Export action CSV', 'prepCSV', () => hooks.download('gtm_prep_actions.csv', api.actionsCSV(hooks.read()), 'text/csv')),
        button('Download agent-coach packet', 'prepCoach', () => hooks.download('GTM_COACH_PACKET.md', api.coachPacket(hooks.read(), selectedRun), 'text/markdown')),
        button('Remove this attempt', 'prepRemove', () => {
            if (!confirm('Remove this practice attempt from the session? Download its debrief first if you need to keep it.')) return;
            commit(api.removeRun(hooks.read(), selectedRun)); status('Attempt removed from this session. Existing downloaded files are unchanged.');
        }));
        sectionNode.append(result, actions);
        return sectionNode;
    }
    function init(config) {
        hooks = config;
        dialog = element('dialog', undefined, 'prep-dialog'); dialog.id = 'prepDialog';
        dialog.setAttribute('aria-labelledby', 'prepTitle'); dialog.setAttribute('aria-describedby', 'prepDescription');
        buildHeader();
        const layout = element('div', undefined, 'prep-layout');
        layout.append(buildLedger(), buildPractice()); dialog.append(layout, buildDebrief());
        document.body.append(dialog);
        byId('prepRunSelect').addEventListener('change', event => { selectedRun = event.target.value; renderRun(); });
        dialog.addEventListener('close', () => { pauseTimer(); returnFocus?.focus(); });
        setInterval(tick, 250);
    }
    function open(persona) {
        returnFocus = document.activeElement;
        render();
        if (api.personas[persona]) byId('prepPersona').value = persona;
        if (!dialog.open) dialog.showModal();
        status('Your practice is saved with the session when device saving is enabled. Timers start paused and reset after reload.');
        byId('prepClaimSelect').focus();
    }
    function renderClaim() {
        const claim = hooks.read().claims.find(c => c.id === selectedClaim) || {kind: 'assertion', resolution: 'open'};
        const fields = {Text: 'text', Kind: 'kind', Evidence: 'evidence', Counterexample: 'counterexample', Action: 'action', Owner: 'owner', Due: 'due', Resolution: 'resolution'};
        Object.entries(fields).forEach(([suffix, key]) => { byId('prepClaim' + suffix).value = claim[key] || ''; });
        byId('prepClaimSelect').value = selectedClaim;
    }
    function replaceOptions(id, records, selected, fallback) {
        const node = byId(id); node.replaceChildren();
        if (fallback) { const option = element('option', fallback); option.value = ''; node.append(option); }
        records.forEach(([value, label]) => { const option = element('option', label); option.value = value; node.append(option); });
        node.value = selected;
    }
    function renderConflicts() {
        const target = byId('prepConflictList'); target.replaceChildren();
        target.append(element('p', 'Limited pattern check: shared English terms with changed numbers or negation. It can miss conflicts and flag consistent statements. Check dates, units and scope.'));
        const pairs = api.conflicts(hooks.read());
        if (!pairs.length) target.append(element('p', 'No pattern candidates found. This does not establish consistency.'));
        pairs.forEach(pair => {
            const item = element('article', undefined, 'prep-candidate');
            item.append(element('p', 'Possible conflict — review required'), element('blockquote', pair.left), element('blockquote', pair.right), element('p', pair.reason));
            target.append(item);
        });
    }
    function renderActive() {
        const state = hooks.read(), run = api.active(state);
        byId('prepStart').disabled = !!run;
        byId('prepAnswerForm').hidden = !run;
        if (!run) { pauseTimer(); return; }
        byId('prepPersona').value = run.persona;
        byId('prepScenario').value = run.scenario;
        byId('prepLimit').value = String(run.limit);
        byId('prepQuestion').textContent = api.personas[run.persona].name + '\n' + run.pending.question;
        byId('prepCriterion').textContent = run.pending.criterion + '\nScenario: ' + api.scenarios[run.scenario].name + ' (practice condition).';
        Object.entries({prepAnswer: 'answer', prepEvidence: 'evidence', prepCounterexample: 'counterexample', prepTest: 'test'}).forEach(([id, key]) => { byId(id).value = state.draft[key]; });
        byId('prepContested').checked = false;
        syncClock(run); tick();
    }
    function renderTranscript(run) {
        const target = byId('prepTranscript'); target.replaceChildren();
        if (!run) return;
        run.turns.forEach(turn => {
            const item = element('article', undefined, 'prep-candidate');
            item.append(element('h4', 'Turn ' + turn.id + (turn.challenged ? ' / premise contested' : '')),
                element('p', turn.question), element('blockquote', turn.answer));
            target.append(item);
        });
    }
    function renderRun() {
        const state = hooks.read(), run = state.runs.find(r => r.id === selectedRun);
        const target = byId('prepDebrief'); target.replaceChildren();
        ['prepRetest', 'prepDownload', 'prepCoach', 'prepRemove'].forEach(id => { byId(id).disabled = !run; });
        byId('prepRetest').disabled = !run || run.status !== 'complete' || !!api.active(state);
        renderTranscript(run);
        if (!run) { target.append(element('p', 'Your objections, answers and next actions will appear here after practice.')); return; }
        const d = api.debrief(state, selectedRun);
        target.append(element('p', api.personas[run.persona].name + ' / ' + api.scenarios[run.scenario].name + ' / ' + run.status),
            element('p', run.turns.length + ' answers recorded. ' + d.contested + ' premises contested.'),
            element('p', d.missing.length ? 'Supporting fields still missing: ' + d.missing.join(', ') : 'Supporting fields contain notes. Review what they actually establish.'),
            element('p', d.note), element('p', 'Next test: ' + (d.claim.action || 'Not recorded — add it in the claim ledger.')),
            element('p', 'Owner: ' + (d.claim.owner || 'Not recorded') + ' / Decision date: ' + (d.claim.due || 'Not recorded')));
        if (d.previous) renderComparison(target, d);
    }
    function renderComparison(target, d) {
        target.append(element('h4', 'Retest comparison — review required'));
        [[d.previous, 'Previous'], [d.run, 'Current']].forEach(([run, label]) => {
            const turn = run.turns[0];
            target.append(element('h4', label + ' first answer'), element('blockquote', turn?.answer || 'Not answered yet'),
                element('p', 'Evidence: ' + (turn?.evidence || 'Not recorded')),
                element('p', 'Counterexample: ' + (turn?.counterexample || 'Not recorded')),
                element('p', 'Next test: ' + (turn?.test || 'Not recorded')));
        });
    }
    function render() {
        const state = hooks.read();
        if (!state.claims.some(c => c.id === selectedClaim)) selectedClaim = state.claims[0]?.id || '';
        if (!state.runs.some(r => r.id === selectedRun)) selectedRun = state.activeId || state.runs[state.runs.length - 1]?.id || '';
        replaceOptions('prepClaimSelect', state.claims.map(c => [c.id, c.text.slice(0, 80)]), selectedClaim, 'Add a new claim');
        replaceOptions('prepRunSelect', state.runs.map(r => [r.id, r.id + ' / ' + api.personas[r.persona].name + ' / ' + r.status]), selectedRun, 'Choose an attempt');
        renderClaim(); renderConflicts(); renderActive(); renderRun();
    }
    function saveDraft() {
        const state = api.normalize(hooks.read());
        state.draft = {answer: byId('prepAnswer').value, evidence: byId('prepEvidence').value,
            counterexample: byId('prepCounterexample').value, test: byId('prepTest').value};
        hooks.write(api.normalize(state));
    }
    function submitAnswer() {
        const state = hooks.read();
        const next = api.answer(state, {answer: byId('prepAnswer').value, evidence: byId('prepEvidence').value,
            counterexample: byId('prepCounterexample').value, test: byId('prepTest').value,
            elapsed: Math.round(elapsed()), challenged: byId('prepContested').checked});
        selectedRun = state.activeId; commit(next);
        status('Answer recorded. The next challenge targets a missing field or a new scenario; it does not validate the answer.');
        byId('prepQuestion').focus();
    }
    function elapsed() { return Math.min(86400, clock.elapsed + (clock.started === null ? 0 : (performance.now() - clock.started) / 1000)); }
    function pauseTimer() { clock.elapsed = elapsed(); clock.started = null; }
    function syncClock(run) {
        const key = run.id + ':' + run.turns.length;
        if (clock.key === key) return;
        clock.key = key; clock.elapsed = 0; clock.started = null; clock.expired = false;
    }
    function toggleTimer() {
        if (clock.started === null) clock.started = performance.now();
        else pauseTimer();
        tick();
    }
    function tick() {
        if (!hooks) return;
        const run = api.active(hooks.read());
        if (!run) return;
        const seconds = elapsed(), remaining = Math.max(0, run.limit - seconds);
        byId('prepTimer').textContent = run.limit ? Math.ceil(remaining) + ' seconds remaining' : Math.floor(seconds) + ' seconds elapsed';
        byId('prepTimerToggle').textContent = clock.started === null ? 'Start / resume timer' : 'Pause timer';
        if (run.limit && seconds >= run.limit && !clock.expired) {
            pauseTimer(); clock.expired = true;
            status('Rehearsal time reached. Your draft is retained; submit when ready or keep refining it.');
        }
    }
    root.GTMPrepUI = {init, open, render};
})(globalThis);
