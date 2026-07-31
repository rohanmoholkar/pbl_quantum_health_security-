// ===== Quantum Particle Canvas =====
const canvas = document.getElementById('quantumCanvas');
const ctx = canvas.getContext('2d');
let particles = [];
let mouseX = 0, mouseY = 0;

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

class Particle {
    constructor() {
        this.reset();
    }
    reset() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 0.5;
        this.speedX = (Math.random() - 0.5) * 0.5;
        this.speedY = (Math.random() - 0.5) * 0.5;
        this.opacity = Math.random() * 0.5 + 0.1;
        this.hue = Math.random() > 0.5 ? 260 : 190; // purple or cyan
    }
    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
        if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
    }
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${this.hue}, 80%, 70%, ${this.opacity})`;
        ctx.fill();
    }
}

function initParticles() {
    const count = Math.min(80, Math.floor(window.innerWidth * 0.05));
    particles = [];
    for (let i = 0; i < count; i++) {
        particles.push(new Particle());
    }
}
initParticles();

function drawConnections() {
    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 150) {
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.strokeStyle = `rgba(108, 92, 231, ${0.1 * (1 - dist / 150)})`;
                ctx.lineWidth = 0.5;
                ctx.stroke();
            }
        }
    }
}

function animateCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    drawConnections();
    requestAnimationFrame(animateCanvas);
}
animateCanvas();

// ===== Navbar Scroll Effect =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// ===== Mobile Nav Toggle =====
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});
// Close on link click
navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('active'));
});

// ===== Intersection Observer for Animations =====
const observerOptions = { threshold: 0.15, rootMargin: '0px 0px -50px 0px' };

const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            // Animate threat meters
            if (entry.target.classList.contains('threat-card')) {
                const meter = entry.target.querySelector('.threat-meter');
                const fill = entry.target.querySelector('.meter-fill');
                if (meter && fill) {
                    const level = fill.getAttribute('data-level');
                    setTimeout(() => {
                        fill.style.width = level + '%';
                        meter.setAttribute('data-animated', 'true');
                    }, 300);
                }
            }
        }
    });
}, observerOptions);

// Observe elements
document.querySelectorAll('.threat-card, .pillar-card, .app-card, .timeline-item, .learn-card, .comparison-visual, .diff-summary-card, .architecture-diagram, .stride-card, .lit-insight-card, .stride-summary-card, .lit-table-wrapper').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    fadeObserver.observe(el);
});

// Add visible class styles
const style = document.createElement('style');
style.textContent = `.visible { opacity: 1 !important; transform: translateY(0) !important; }`;
document.head.appendChild(style);

// ===== Flow Steps Interactive =====
const flowSteps = document.querySelectorAll('.flow-step');
const flowProgressBar = document.getElementById('flowProgressBar');
let currentStep = 1;
let flowAutoTimer;

function setFlowStep(step) {
    currentStep = step;
    flowSteps.forEach(s => {
        const sNum = parseInt(s.getAttribute('data-step'));
        s.classList.toggle('active', sNum === step);
    });
    if (flowProgressBar) {
        flowProgressBar.style.width = (step * 25) + '%';
    }
}

flowSteps.forEach(step => {
    step.addEventListener('click', () => {
        setFlowStep(parseInt(step.getAttribute('data-step')));
        clearInterval(flowAutoTimer);
        startFlowAuto();
    });
});

function startFlowAuto() {
    flowAutoTimer = setInterval(() => {
        currentStep = currentStep >= 4 ? 1 : currentStep + 1;
        setFlowStep(currentStep);
    }, 3000);
}
startFlowAuto();

// ===== Smooth Scroll for Nav Links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// ===== Staggered animations for grids =====
function staggerChildren(parentSelector, childSelector, delay = 100) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const children = entry.target.querySelectorAll(childSelector);
                children.forEach((child, i) => {
                    child.style.transitionDelay = `${i * delay}ms`;
                    child.classList.add('visible');
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll(parentSelector).forEach(el => observer.observe(el));
}

staggerChildren('.threat-grid', '.threat-card', 150);
staggerChildren('.pillars-grid', '.pillar-card', 120);
staggerChildren('.apps-showcase', '.app-card', 150);
staggerChildren('.learn-grid', '.learn-card', 100);
staggerChildren('.roadmap-timeline', '.timeline-item', 200);
staggerChildren('.stride-grid', '.stride-card', 150);

// ===== Parallax on hero =====
window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const hero = document.querySelector('.hero-content');
    if (hero && scrolled < window.innerHeight) {
        hero.style.transform = `translateY(${scrolled * 0.15}px)`;
        hero.style.opacity = 1 - scrolled / (window.innerHeight * 0.8);
    }
});

// ===== Active Nav Link Highlight =====
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
    const scrollPos = window.scrollY + 120;
    sections.forEach(section => {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        const id = section.getAttribute('id');
        const link = document.querySelector(`.nav-link[href="#${id}"]`);
        if (link) {
            link.classList.toggle('active-link', scrollPos >= top && scrollPos < top + height);
        }
    });
});

// Active link style
const navStyle = document.createElement('style');
navStyle.textContent = `.nav-link.active-link { color: var(--text-primary); } .nav-link.active-link::after { width: 100%; }`;
document.head.appendChild(navStyle);

console.log('🔐 Quantum-Secured Digital Health Identity System — Loaded Successfully');

// ===== Research Models Section - Interactive Simulations =====

// QKD Model Simulation
const qkdCanvas = document.getElementById('qkdCanvas');
const qkdSlider = document.getElementById('qkd-slider');
const qkdDistanceDisplay = document.getElementById('qkd-distance');
const qkdSurvivalDisplay = document.getElementById('qkd-survival');
const qkdRateDisplay = document.getElementById('qkd-rate');
const qkdQberDisplay = document.getElementById('qkd-qber');
const qkdStatusDisplay = document.getElementById('qkd-status');
const qkdFeasibilityBadge = document.getElementById('qkd-feasibility');

if (qkdCanvas) {
    const qkdCtx = qkdCanvas.getContext('2d');

    // QKD Parameters
    const ATTENUATION_DB_PER_KM = 0.2;
    const DETECTOR_EFFICIENCY = 0.1;
    const DARK_COUNT_RATE = 1e-6;
    const SOURCE_RATE_HZ = 1e9;

    function calculatePhotonSurvival(distance) {
        const loss_db = ATTENUATION_DB_PER_KM * distance;
        return Math.pow(10, -loss_db / 10);
    }

    function estimateSecureKeyRate(distance) {
        const transmittance = calculatePhotonSurvival(distance);
        const raw_rate = SOURCE_RATE_HZ * transmittance * DETECTOR_EFFICIENCY;
        const skr = raw_rate * (1 - (DARK_COUNT_RATE / (transmittance * DETECTOR_EFFICIENCY)));
        return Math.max(skr, 0);
    }

    function calculateQBER(distance) {
        // Quantum Bit Error Rate - increases with distance
        const transmittance = calculatePhotonSurvival(distance);
        const qber = DARK_COUNT_RATE / (2 * transmittance * DETECTOR_EFFICIENCY) * 100;
        return Math.min(qber, 15); // Cap at 15% (beyond this QKD fails)
    }

    function getFeasibilityInfo(distance) {
        if (distance <= 50) {
            return { class: 'excellent', text: 'Excellent', color: 'rgba(0,230,118,0.1)' };
        } else if (distance <= 100) {
            return { class: 'good', text: 'Feasible', color: 'rgba(255,215,64,0.1)' };
        } else {
            return { class: 'poor', text: 'Challenging', color: 'rgba(255,82,82,0.1)' };
        }
    }

    function drawQKDGraph(highlightDistance = 75) {
        const width = qkdCanvas.width = qkdCanvas.offsetWidth;
        const height = qkdCanvas.height = qkdCanvas.offsetHeight;

        qkdCtx.clearRect(0, 0, width, height);

        // Draw feasibility zones
        const feasibility = getFeasibilityInfo(highlightDistance);
        qkdCtx.fillStyle = feasibility.color;
        qkdCtx.fillRect(0, 0, width, height);

        // Draw grid
        qkdCtx.strokeStyle = 'rgba(255,255,255,0.05)';
        qkdCtx.lineWidth = 1;
        for (let i = 0; i <= 5; i++) {
            const y = (height - 60) * i / 5 + 30;
            qkdCtx.beginPath();
            qkdCtx.moveTo(50, y);
            qkdCtx.lineTo(width - 20, y);
            qkdCtx.stroke();
        }

        // Draw axes
        qkdCtx.strokeStyle = 'rgba(255,255,255,0.3)';
        qkdCtx.lineWidth = 2;
        qkdCtx.beginPath();
        qkdCtx.moveTo(50, 30);
        qkdCtx.lineTo(50, height - 30);
        qkdCtx.lineTo(width - 20, height - 30);
        qkdCtx.stroke();

        // Draw labels
        qkdCtx.fillStyle = '#8b8f9a';
        qkdCtx.font = '11px Inter';
        qkdCtx.textAlign = 'center';
        qkdCtx.fillText('Distance (km)', width / 2, height - 5);
        qkdCtx.save();
        qkdCtx.translate(15, height / 2);
        qkdCtx.rotate(-Math.PI / 2);
        qkdCtx.fillText('Key Rate (log scale)', 0, 0);
        qkdCtx.restore();

        // Draw zone boundaries
        const zone50 = 50 + (50 / 150) * (width - 70);
        const zone100 = 50 + (100 / 150) * (width - 70);

        // Excellent zone (0-50km)
        qkdCtx.strokeStyle = 'rgba(0,230,118,0.3)';
        qkdCtx.lineWidth = 1;
        qkdCtx.setLineDash([3, 3]);
        qkdCtx.beginPath();
        qkdCtx.moveTo(zone50, 30);
        qkdCtx.lineTo(zone50, height - 30);
        qkdCtx.stroke();

        // Good zone (50-100km)
        qkdCtx.strokeStyle = 'rgba(255,215,64,0.3)';
        qkdCtx.beginPath();
        qkdCtx.moveTo(zone100, 30);
        qkdCtx.lineTo(zone100, height - 30);
        qkdCtx.stroke();
        qkdCtx.setLineDash([]);

        // Zone labels
        qkdCtx.fillStyle = '#00e676';
        qkdCtx.font = '9px Inter';
        qkdCtx.fillText('Excellent', zone50 / 2 + 25, 45);
        qkdCtx.fillStyle = '#ffd740';
        qkdCtx.fillText('Feasible', (zone50 + zone100) / 2, 45);
        qkdCtx.fillStyle = '#ff5252';
        qkdCtx.fillText('Challenging', (zone100 + width - 20) / 2, 45);

        // Draw SKR curve
        qkdCtx.strokeStyle = '#00d2ff';
        qkdCtx.lineWidth = 3;
        qkdCtx.shadowColor = '#00d2ff';
        qkdCtx.shadowBlur = 8;
        qkdCtx.beginPath();

        const maxRate = estimateSecureKeyRate(0);
        const minRate = 1e-3;

        for (let dist = 0; dist <= 150; dist += 0.5) {
            const x = 50 + (dist / 150) * (width - 70);
            const rate = estimateSecureKeyRate(dist);
            const logRate = Math.log10(Math.max(rate, minRate));
            const logMax = Math.log10(maxRate);
            const logMin = Math.log10(minRate);
            const y = height - 30 - ((logRate - logMin) / (logMax - logMin)) * (height - 60);

            if (dist === 0) {
                qkdCtx.moveTo(x, y);
            } else {
                qkdCtx.lineTo(x, y);
            }
        }
        qkdCtx.stroke();
        qkdCtx.shadowBlur = 0;

        // Draw highlight point
        const highlightX = 50 + (highlightDistance / 150) * (width - 70);
        const highlightRate = estimateSecureKeyRate(highlightDistance);
        const logHighlight = Math.log10(Math.max(highlightRate, minRate));
        const logMax2 = Math.log10(maxRate);
        const logMin2 = Math.log10(minRate);
        const highlightY = height - 30 - ((logHighlight - logMin2) / (logMax2 - logMin2)) * (height - 60);

        // Highlight circle with pulse effect
        qkdCtx.fillStyle = '#6c5ce7';
        qkdCtx.shadowColor = '#6c5ce7';
        qkdCtx.shadowBlur = 15;
        qkdCtx.beginPath();
        qkdCtx.arc(highlightX, highlightY, 8, 0, Math.PI * 2);
        qkdCtx.fill();
        qkdCtx.shadowBlur = 0;

        // Vertical line to axis
        qkdCtx.strokeStyle = '#6c5ce7';
        qkdCtx.lineWidth = 2;
        qkdCtx.setLineDash([3, 3]);
        qkdCtx.beginPath();
        qkdCtx.moveTo(highlightX, highlightY);
        qkdCtx.lineTo(highlightX, height - 30);
        qkdCtx.stroke();
        qkdCtx.setLineDash([]);

        // Update stats
        const survival = calculatePhotonSurvival(highlightDistance);
        const qber = calculateQBER(highlightDistance);

        qkdSurvivalDisplay.textContent = (survival * 100).toFixed(4) + '%';
        qkdRateDisplay.textContent = highlightRate.toExponential(2);
        qkdQberDisplay.textContent = qber.toFixed(3) + '%';

        // Update status
        if (highlightDistance <= 50) {
            qkdStatusDisplay.textContent = '✓ Optimal';
            qkdStatusDisplay.style.color = 'var(--success)';
        } else if (highlightDistance <= 100) {
            qkdStatusDisplay.textContent = '⚠ Acceptable';
            qkdStatusDisplay.style.color = 'var(--warning)';
        } else {
            qkdStatusDisplay.textContent = '✗ Impractical';
            qkdStatusDisplay.style.color = 'var(--danger)';
        }

        // Update feasibility badge
        qkdFeasibilityBadge.textContent = feasibility.text;
        qkdFeasibilityBadge.className = 'feasibility-badge ' + feasibility.class;
    }

    qkdSlider.addEventListener('input', (e) => {
        const distance = parseInt(e.target.value);
        qkdDistanceDisplay.textContent = distance;
        drawQKDGraph(distance);
    });

    // Preset distance function
    window.setQKDDistance = function (distance) {
        qkdSlider.value = distance;
        qkdDistanceDisplay.textContent = distance;
        drawQKDGraph(distance);
    };

    // Initial draw
    drawQKDGraph(75);
    window.addEventListener('resize', () => drawQKDGraph(parseInt(qkdSlider.value)));
}

// AI Defense Simulation
const aiCanvas = document.getElementById('aiCanvas');
const aiNormalDisplay = document.getElementById('ai-normal');
const aiAttacksDisplay = document.getElementById('ai-attacks');
const aiDdosDisplay = document.getElementById('ai-ddos');
const aiRansomwareDisplay = document.getElementById('ai-ransomware');
const aiConfidenceFill = document.getElementById('ai-confidence');
const aiConfidenceText = document.getElementById('ai-confidence-text');

let aiData = { normal: [], attacks: [] };

if (aiCanvas) {
    const aiCtx = aiCanvas.getContext('2d');

    // Simple Isolation Forest simulation
    function generateNormalData(count) {
        const data = [];
        for (let i = 0; i < count / 2; i++) {
            data.push({
                x: 2 + (Math.random() - 0.5) * 0.6,
                y: 2 + (Math.random() - 0.5) * 0.6,
                type: 'normal'
            });
            data.push({
                x: -2 + (Math.random() - 0.5) * 0.6,
                y: -2 + (Math.random() - 0.5) * 0.6,
                type: 'normal'
            });
        }
        return data;
    }

    function generateAttackData(count) {
        const data = [];
        const attackTypes = ['ddos', 'ransomware', 'breach'];
        for (let i = 0; i < count; i++) {
            data.push({
                x: (Math.random() - 0.5) * 8,
                y: (Math.random() - 0.5) * 8,
                type: 'attack',
                attackType: attackTypes[Math.floor(Math.random() * attackTypes.length)]
            });
        }
        return data;
    }

    function detectAnomalies(data) {
        // Simple anomaly detection: points far from clusters
        return data.map(point => {
            const distToCluster1 = Math.sqrt(Math.pow(point.x - 2, 2) + Math.pow(point.y - 2, 2));
            const distToCluster2 = Math.sqrt(Math.pow(point.x + 2, 2) + Math.pow(point.y + 2, 2));
            const minDist = Math.min(distToCluster1, distToCluster2);
            const isAnomaly = minDist > 1.5;
            const confidence = isAnomaly ? Math.min((minDist - 1.5) / 2, 1) : 0;
            return { ...point, isAnomaly, confidence };
        });
    }

    function drawAIGraph() {
        const width = aiCanvas.width = aiCanvas.offsetWidth;
        const height = aiCanvas.height = aiCanvas.offsetHeight;

        aiCtx.clearRect(0, 0, width, height);

        // Draw grid
        aiCtx.strokeStyle = 'rgba(255,255,255,0.05)';
        aiCtx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
            const x = width * i / 4;
            const y = height * i / 4;
            aiCtx.beginPath();
            aiCtx.moveTo(x, 0);
            aiCtx.lineTo(x, height);
            aiCtx.stroke();
            aiCtx.beginPath();
            aiCtx.moveTo(0, y);
            aiCtx.lineTo(width, y);
            aiCtx.stroke();
        }

        // Draw axes
        aiCtx.strokeStyle = 'rgba(255,255,255,0.3)';
        aiCtx.lineWidth = 2;
        aiCtx.beginPath();
        aiCtx.moveTo(width / 2, 0);
        aiCtx.lineTo(width / 2, height);
        aiCtx.moveTo(0, height / 2);
        aiCtx.lineTo(width, height / 2);
        aiCtx.stroke();

        // Draw labels
        aiCtx.fillStyle = '#8b8f9a';
        aiCtx.font = '11px Inter';
        aiCtx.textAlign = 'center';
        aiCtx.fillText('Access Frequency →', width - 80, height - 10);
        aiCtx.save();
        aiCtx.translate(15, 80);
        aiCtx.rotate(-Math.PI / 2);
        aiCtx.fillText('Data Volume →', 0, 0);
        aiCtx.restore();

        // Transform coordinates
        const toCanvasX = (x) => width / 2 + (x / 4) * (width / 2);
        const toCanvasY = (y) => height / 2 - (y / 4) * (height / 2);

        // Draw points
        const allData = detectAnomalies([...aiData.normal, ...aiData.attacks]);

        let normalCount = 0;
        let attackCount = 0;
        let ddosCount = 0;
        let ransomwareCount = 0;
        let totalConfidence = 0;
        let anomalyCount = 0;

        allData.forEach(point => {
            const cx = toCanvasX(point.x);
            const cy = toCanvasY(point.y);

            if (point.isAnomaly) {
                attackCount++;
                totalConfidence += point.confidence;
                anomalyCount++;

                // Color by attack type
                if (point.attackType === 'ddos') {
                    ddosCount++;
                    aiCtx.fillStyle = '#ff5252';
                    aiCtx.strokeStyle = '#ff5252';
                } else if (point.attackType === 'ransomware') {
                    ransomwareCount++;
                    aiCtx.fillStyle = '#ff9800';
                    aiCtx.strokeStyle = '#ff9800';
                } else {
                    aiCtx.fillStyle = '#e040fb';
                    aiCtx.strokeStyle = '#e040fb';
                }

                // Larger size for attacks
                aiCtx.beginPath();
                aiCtx.arc(cx, cy, 5, 0, Math.PI * 2);
                aiCtx.fill();
                aiCtx.lineWidth = 2;
                aiCtx.stroke();

                // Add warning icon for high confidence
                if (point.confidence > 0.7) {
                    aiCtx.strokeStyle = 'rgba(255,255,255,0.8)';
                    aiCtx.lineWidth = 1.5;
                    aiCtx.beginPath();
                    aiCtx.arc(cx, cy, 8, 0, Math.PI * 2);
                    aiCtx.stroke();
                }
            } else {
                normalCount++;
                aiCtx.fillStyle = '#00e676';
                aiCtx.strokeStyle = '#00e676';

                aiCtx.beginPath();
                aiCtx.arc(cx, cy, 4, 0, Math.PI * 2);
                aiCtx.fill();
                aiCtx.lineWidth = 1;
                aiCtx.stroke();
            }
        });

        // Update stats
        aiNormalDisplay.textContent = normalCount;
        aiAttacksDisplay.textContent = attackCount;
        aiDdosDisplay.textContent = ddosCount;
        aiRansomwareDisplay.textContent = ransomwareCount;

        // Update confidence meter
        const avgConfidence = anomalyCount > 0 ? (totalConfidence / anomalyCount) * 100 : 0;
        aiConfidenceFill.style.width = avgConfidence + '%';
        aiConfidenceText.textContent = avgConfidence.toFixed(0) + '%';

        // Draw legend in top-right corner
        const legend = [
            { color: '#00e676', label: 'Normal' },
            { color: '#ff5252', label: 'DDoS' },
            { color: '#ff9800', label: 'Ransomware' },
            { color: '#e040fb', label: 'Data Breach' },
        ];
        const legendX = width - 110;
        let legendY = 18;
        aiCtx.font = '10px Inter';
        aiCtx.textAlign = 'left';
        legend.forEach(item => {
            aiCtx.fillStyle = item.color;
            aiCtx.beginPath();
            aiCtx.arc(legendX, legendY, 5, 0, Math.PI * 2);
            aiCtx.fill();
            aiCtx.fillStyle = 'rgba(255,255,255,0.7)';
            aiCtx.fillText(item.label, legendX + 10, legendY + 4);
            legendY += 18;
        });
    }

    window.regenerateAIData = function () {
        aiData.normal = generateNormalData(100);
        aiData.attacks = generateAttackData(20);
        drawAIGraph();
    };

    // Initial draw
    regenerateAIData();
    window.addEventListener('resize', drawAIGraph);
}

// PQC Comparison Simulation
const pqcCanvas = document.getElementById('pqcCanvas');

if (pqcCanvas) {
    const pqcCtx = pqcCanvas.getContext('2d');

    const algorithms = ['RSA-2048', 'ECC-256', 'Kyber-512', 'Dilithium-II'];
    const keyGenTime = [160000, 200, 10, 20]; // microseconds
    const securityBits = [112, 128, 128, 128];

    let currentView = 'both'; // 'both', 'speed', 'security'
    let animationProgress = 1; // For smooth transitions

    function drawPQCGraph() {
        const width = pqcCanvas.width = pqcCanvas.offsetWidth;
        const height = pqcCanvas.height = pqcCanvas.offsetHeight;

        pqcCtx.clearRect(0, 0, width, height);

        const barWidth = currentView === 'both'
            ? (width - 100) / algorithms.length / 2.5
            : (width - 100) / algorithms.length / 1.8;
        const spacing = (width - 100) / algorithms.length;

        // Draw axes
        pqcCtx.strokeStyle = 'rgba(255,255,255,0.3)';
        pqcCtx.lineWidth = 2;
        pqcCtx.beginPath();
        pqcCtx.moveTo(50, 30);
        pqcCtx.lineTo(50, height - 50);
        pqcCtx.lineTo(width - 50, height - 50);
        pqcCtx.stroke();

        // Draw bars
        const maxTime = Math.max(...keyGenTime);
        const maxSecurity = 140;

        algorithms.forEach((algo, i) => {
            const x = 50 + spacing * i + spacing / 2;

            // Speed bar (log scale)
            if (currentView === 'both' || currentView === 'speed') {
                const logTime = Math.log10(keyGenTime[i]);
                const logMax = Math.log10(maxTime);
                const timeHeight = (logTime / logMax) * (height - 80) * animationProgress;

                const gradient = pqcCtx.createLinearGradient(0, height - 50 - timeHeight, 0, height - 50);
                gradient.addColorStop(0, '#ff9800');
                gradient.addColorStop(1, '#ff6f00');
                pqcCtx.fillStyle = gradient;

                const barX = currentView === 'both' ? x - barWidth : x - barWidth / 2;
                pqcCtx.fillRect(barX, height - 50 - timeHeight, barWidth - 5, timeHeight);

                // Add glow effect
                pqcCtx.shadowColor = '#ff9800';
                pqcCtx.shadowBlur = 10;
                pqcCtx.fillRect(barX, height - 50 - timeHeight, barWidth - 5, timeHeight);
                pqcCtx.shadowBlur = 0;

                // Values
                pqcCtx.fillStyle = '#ff9800';
                pqcCtx.font = 'bold 10px Inter';
                pqcCtx.textAlign = 'center';
                const labelX = currentView === 'both' ? barX + barWidth / 2 : x;
                pqcCtx.fillText(keyGenTime[i] + 'μs', labelX, height - 50 - timeHeight - 8);
            }

            // Security bar
            if (currentView === 'both' || currentView === 'security') {
                const secHeight = (securityBits[i] / maxSecurity) * (height - 80) * animationProgress;

                const gradient = pqcCtx.createLinearGradient(0, height - 50 - secHeight, 0, height - 50);
                gradient.addColorStop(0, '#00d2ff');
                gradient.addColorStop(1, '#0099cc');
                pqcCtx.fillStyle = gradient;

                const barX = currentView === 'both' ? x + 5 : x - barWidth / 2;
                pqcCtx.fillRect(barX, height - 50 - secHeight, barWidth - 5, secHeight);

                // Add glow effect
                pqcCtx.shadowColor = '#00d2ff';
                pqcCtx.shadowBlur = 10;
                pqcCtx.fillRect(barX, height - 50 - secHeight, barWidth - 5, secHeight);
                pqcCtx.shadowBlur = 0;

                // Values
                pqcCtx.fillStyle = '#00d2ff';
                pqcCtx.font = 'bold 10px Inter';
                pqcCtx.textAlign = 'center';
                const labelX = currentView === 'both' ? barX + barWidth / 2 : x;
                pqcCtx.fillText(securityBits[i] + ' bits', labelX, height - 50 - secHeight - 8);
            }

            // Algorithm labels
            pqcCtx.fillStyle = '#e8eaed';
            pqcCtx.font = '11px Inter';
            pqcCtx.textAlign = 'center';
            pqcCtx.save();
            pqcCtx.translate(x, height - 30);
            pqcCtx.rotate(-Math.PI / 6);
            pqcCtx.fillText(algo, 0, 0);
            pqcCtx.restore();
        });

        // Y-axis labels
        pqcCtx.fillStyle = '#8b8f9a';
        pqcCtx.font = '11px Inter';
        pqcCtx.textAlign = 'right';

        if (currentView === 'both' || currentView === 'speed') {
            pqcCtx.fillStyle = '#ff9800';
            pqcCtx.fillText('Time (μs)', 45, 20);
        }
        if (currentView === 'both' || currentView === 'security') {
            pqcCtx.fillStyle = '#00d2ff';
            pqcCtx.fillText('Security', 45, currentView === 'both' ? 35 : 20);
        }

        // Add comparison annotations
        if (currentView === 'speed') {
            pqcCtx.fillStyle = 'rgba(255,152,0,0.1)';
            pqcCtx.fillRect(50, 30, width - 100, 40);
            pqcCtx.fillStyle = '#ff9800';
            pqcCtx.font = 'bold 12px Inter';
            pqcCtx.textAlign = 'center';
            pqcCtx.fillText('⚡ PQC algorithms are 1000-16000× faster!', width / 2, 55);
        } else if (currentView === 'security') {
            pqcCtx.fillStyle = 'rgba(0,210,255,0.1)';
            pqcCtx.fillRect(50, 30, width - 100, 40);
            pqcCtx.fillStyle = '#00d2ff';
            pqcCtx.font = 'bold 12px Inter';
            pqcCtx.textAlign = 'center';
            pqcCtx.fillText('🔒 All provide strong 112-128 bit security', width / 2, 55);
        }
    }

    // Animate view transitions
    function animateViewChange() {
        animationProgress = 0;
        const animate = () => {
            animationProgress += 0.1;
            if (animationProgress <= 1) {
                drawPQCGraph();
                requestAnimationFrame(animate);
            } else {
                animationProgress = 1;
                drawPQCGraph();
            }
        };
        animate();
    }

    // Set view mode
    window.setPQCView = function (view) {
        currentView = view;

        // Update button states
        document.querySelectorAll('.pqc-view-btn').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-view') === view);
        });

        animateViewChange();
    };

    // Initial draw
    drawPQCGraph();
    window.addEventListener('resize', drawPQCGraph);
}

// Stagger research cards
document.querySelectorAll('.research-card, .research-usage').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    fadeObserver.observe(el);
});
