// ============================================================
// QuantumHealth — Full-Stack Frontend Logic
// ============================================================

(function () {
    'use strict';

    // ---- Scroll-triggered fade-in (IntersectionObserver) ----
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((e) => {
                if (e.isIntersecting) {
                    e.target.classList.add('visible');
                    observer.unobserve(e.target); // animate only once
                }
            });
        },
        { threshold: 0.12 }
    );

    document.querySelectorAll('.fade-in').forEach((el) => observer.observe(el));

    // ---- Copy-to-clipboard buttons ----
    document.querySelectorAll('.copy-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
            const cmd = btn.dataset.cmd;
            navigator.clipboard.writeText(cmd).then(() => {
                btn.classList.add('copied');
                setTimeout(() => btn.classList.remove('copied'), 1500);
            });
        });
    });

    // ---- Canvas particle background ----
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let W, H, particles;

    function resize() {
        W = canvas.width = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    class Dot {
        constructor() {
            this.x = Math.random() * W;
            this.y = Math.random() * H;
            this.vx = (Math.random() - 0.5) * 0.4;
            this.vy = (Math.random() - 0.5) * 0.4;
            this.r = Math.random() * 1.8 + 0.6;
            this.color = ['#22d3ee', '#a78bfa', '#475569'][Math.floor(Math.random() * 3)];
        }
        update() {
            this.x += this.vx;
            this.y += this.vy;
            if (this.x < 0 || this.x > W) this.vx *= -1;
            if (this.y < 0 || this.y > H) this.vy *= -1;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
    }

    function initDots() {
        const count = Math.min(Math.floor((W * H) / 18000), 120);
        particles = Array.from({ length: count }, () => new Dot());
    }

    function drawLines() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 130) {
                    ctx.strokeStyle = `rgba(148,163,184,${(1 - dist / 130) * 0.15})`;
                    ctx.lineWidth = 0.8;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
    }

    function tick() {
        requestAnimationFrame(tick);
        ctx.clearRect(0, 0, W, H);
        particles.forEach((p) => { p.update(); p.draw(); });
        drawLines();
    }

    initDots();
    tick();

    // ---- AI Demo Engine ----
    const termBody = document.getElementById('term-body');
    const analyzeBtn = document.getElementById('analyze-btn');
    const autoBtn = document.getElementById('auto-btn');
    const statTotal = document.getElementById('stat-total');
    const statAttacks = document.getElementById('stat-attacks');
    const statSafe = document.getElementById('stat-safe');
    const statConfidence = document.getElementById('stat-confidence');
    const accuracyFill = document.getElementById('accuracy-fill');
    const accuracyPct = document.getElementById('accuracy-pct');

    let sessionTotal = 0;
    let sessionAttacks = 0;
    let sessionSafe = 0;
    let sessionCorrect = 0;
    let confidenceSum = 0;

    function addLine(text, cls) {
        const div = document.createElement('div');
        div.className = 'term-line ' + (cls || '');
        div.textContent = text;
        termBody.appendChild(div);
        termBody.scrollTop = termBody.scrollHeight;
    }

    function updateStats(data) {
        sessionTotal++;
        if (data.is_attack_prediction) sessionAttacks++;
        else sessionSafe++;
        if (data.is_attack_prediction === data.is_actual_attack) sessionCorrect++;
        confidenceSum += data.confidence;

        statTotal.textContent = sessionTotal;
        statAttacks.textContent = sessionAttacks;
        statSafe.textContent = sessionSafe;
        statConfidence.textContent = (confidenceSum / sessionTotal).toFixed(1) + '%';

        const accPct = Math.round((sessionCorrect / sessionTotal) * 100);
        accuracyFill.style.width = accPct + '%';
        accuracyPct.textContent = accPct;
    }

    async function analyzeOne() {
        addLine('> Capturing TCP packet on Health API port 443…', 'muted');

        try {
            const res = await fetch('/api/analyze_traffic');
            if (!res.ok) throw new Error('Backend offline');
            const data = await res.json();

            // Show telemetry
            addLine(
                `  Telemetry → Duration: ${data.telemetry['Flow Duration']}s  FwdPkts: ${data.telemetry['Total Fwd Packets']}  BwdPkts: ${data.telemetry['Total Bwd Packets']}  Bytes/s: ${data.telemetry['Flow Bytes/s']}`,
                'data'
            );

            // Show ground truth vs prediction
            const truthTag = data.is_actual_attack ? 'ATTACK' : 'NORMAL';

            if (data.is_attack_prediction) {
                addLine(`✗ [BLOCKED] Intrusion Detected — Confidence ${data.confidence.toFixed(1)}% (Ground Truth: ${truthTag})`, 'error');
                addLine(`→ Connection dropped. Source IP blacklisted.`, 'warning');
            } else {
                addLine(`✓ [PASSED] Normal Traffic — Confidence ${data.confidence.toFixed(1)}% (Ground Truth: ${truthTag})`, 'success');
            }

            addLine('─'.repeat(60), 'sep');
            updateStats(data);
        } catch (err) {
            addLine('[ERROR] Could not reach Flask backend. Is app.py running on port 5001?', 'danger');
        }
    }

    // Single analysis
    analyzeBtn.addEventListener('click', async () => {
        analyzeBtn.disabled = true;
        await analyzeOne();
        analyzeBtn.disabled = false;
    });

    // Auto-stream
    autoBtn.addEventListener('click', async () => {
        analyzeBtn.disabled = true;
        autoBtn.disabled = true;
        addLine('[AUTO] Streaming 5 consecutive packets…', 'sys');
        for (let i = 0; i < 5; i++) {
            await new Promise((r) => setTimeout(r, 700));
            await analyzeOne();
        }
        addLine('[AUTO] Stream complete.', 'sys');
        analyzeBtn.disabled = false;
        autoBtn.disabled = false;
    });

})();
