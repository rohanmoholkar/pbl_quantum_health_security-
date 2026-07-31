// --- Utility Functions ---

function copyCode(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Find the button that was clicked and temporarily change its text
        const btns = document.querySelectorAll('.copy-btn');
        btns.forEach(btn => {
            if (btn.getAttribute('onclick').includes(text)) {
                const originalText = btn.innerText;
                btn.innerText = 'Copied!';
                btn.style.background = 'rgba(16, 185, 129, 0.5)'; // Green flash
                
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.style.background = '';
                }, 2000);
            }
        });
    });
}


// --- Scroll Reveal Animations (Intersection Observer) ---

function reveal() {
    var reveals = document.querySelectorAll(".reveal");
    for (var i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = reveals[i].getBoundingClientRect().top;
        var elementVisible = 100;
        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add("active");
        }
    }
}

window.addEventListener("scroll", reveal);
// Trigger once on load
reveal();


// --- Quantum Particle Background (Canvas) ---

const canvas = document.getElementById('particle-canvas');
const ctx = canvas.getContext('2d');

let particlesArray;
let w, h;

function initCanvas() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
}

window.addEventListener('resize', initCanvas);
initCanvas();

class Particle {
    constructor(x, y, directionX, directionY, size, color) {
        this.x = x;
        this.y = y;
        this.directionX = directionX;
        this.directionY = directionY;
        this.size = size;
        this.color = color;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
    }

    update() {
        if (this.x > w || this.x < 0) {
            this.directionX = -this.directionX;
        }
        if (this.y > h || this.y < 0) {
            this.directionY = -this.directionY;
        }
        
        // Very slow movement to represent quantum states
        this.x += this.directionX * 0.5;
        this.y += this.directionY * 0.5;
        
        this.draw();
    }
}

function initParticles() {
    particlesArray = [];
    const numberOfParticles = (w * h) / 15000;
    // Cyberpunk/Quantum color palette
    const colors = ['#06b6d4', '#a855f7', '#334155']; 

    for (let i = 0; i < numberOfParticles; i++) {
        const size = (Math.random() * 2) + 1;
        const x = Math.random() * (innerWidth - size * 2) + size * 2;
        const y = Math.random() * (innerHeight - size * 2) + size * 2;
        const directionX = (Math.random() * 2) - 1;
        const directionY = (Math.random() * 2) - 1;
        const color = colors[Math.floor(Math.random() * colors.length)];

        particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
    }
}

function connectParticles() {
    let opacityValue = 1;
    for (let a = 0; a < particlesArray.length; a++) {
        for (let b = a; b < particlesArray.length; b++) {
            const dx = particlesArray[a].x - particlesArray[b].x;
            const dy = particlesArray[a].y - particlesArray[b].y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            // Connect particles that are close
            if (distance < 120) {
                opacityValue = 1 - (distance / 120);
                // Draw line
                ctx.strokeStyle = `rgba(148, 163, 184, ${opacityValue * 0.2})`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                ctx.stroke();
            }
        }
    }
}

function animateParticles() {
    requestAnimationFrame(animateParticles);
    ctx.clearRect(0, 0, w, h);

    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
    }
    connectParticles();
}

// Start Background Animation
initParticles();
animateParticles();


// --- Live Full-Stack AI Demo ---
const aiBtn = document.getElementById('run-ai-btn');
if (aiBtn) {
    aiBtn.addEventListener('click', async () => {
        const logsDiv = document.getElementById('ai-logs');
        
        // Show loading state
        const loadingMsg = document.createElement('p');
        loadingMsg.style.color = '#e2e8f0';
        loadingMsg.innerHTML = '<span class="prompt">user@macbook:~$</span> <i>Capturing live network packet...</i>';
        logsDiv.appendChild(loadingMsg);
        logsDiv.scrollTop = logsDiv.scrollHeight;
        
        // Disable button to prevent spam
        aiBtn.disabled = true;
        aiBtn.innerText = 'Analyzing...';
        
        try {
            // Wait a tiny bit just for cinematic effect, then fetch
            await new Promise(r => setTimeout(r, 600));
            const response = await fetch('/api/analyze_traffic');
            
            if (!response.ok) {
                throw new Error("Backend server not responding");
            }
            
            const data = await response.json();
            
            // Remove loading message
            logsDiv.removeChild(loadingMsg);
            
            // Log Telemetry
            const teleMsg = document.createElement('p');
            teleMsg.style.color = '#94a3b8';
            teleMsg.innerHTML = `> Extracted Features: Duration=${data.telemetry.Duration}ms, SrcBytes=${data.telemetry.Src_Bytes}, DstBytes=${data.telemetry.Dst_Bytes}`;
            logsDiv.appendChild(teleMsg);
            
            // Wait slightly for AI to "think"
            await new Promise(r => setTimeout(r, 400));
            
            // Display Result
            const resultMsg = document.createElement('p');
            if (data.is_attack_prediction) {
                resultMsg.style.color = '#ef4444'; // Red
                resultMsg.style.fontWeight = 'bold';
                resultMsg.innerHTML = `[CRITICAL ALERT] Malicious Intrusion Detected! (Confidence: ${data.confidence.toFixed(1)}%) <br> <span style="color:#f59e0b">>> Action: Connection dropped.</span>`;
            } else {
                resultMsg.style.color = '#10b981'; // Green
                resultMsg.style.fontWeight = 'bold';
                resultMsg.innerHTML = `[SAFE] Normal Health API Request. (Confidence: ${data.confidence.toFixed(1)}%) <br> >> Action: Traffic allowed.`;
            }
            logsDiv.appendChild(resultMsg);
            
            // Separator
            const sep = document.createElement('p');
            sep.style.color = '#334155';
            sep.innerText = '----------------------------------------';
            logsDiv.appendChild(sep);
            
        } catch (error) {
            logsDiv.removeChild(loadingMsg);
            const errMsg = document.createElement('p');
            errMsg.style.color = '#ef4444';
            errMsg.innerText = '[ERROR] Failed to connect to Python Backend. Is Flask running on port 5001?';
            logsDiv.appendChild(errMsg);
        } finally {
            logsDiv.scrollTop = logsDiv.scrollHeight;
            aiBtn.disabled = false;
            aiBtn.innerText = 'Run Live AI Analysis';
        }
    });
}
