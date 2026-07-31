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
