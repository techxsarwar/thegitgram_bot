<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GitGram — README</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #080c10;
    --bg2: #0d1117;
    --bg3: #111820;
    --border: rgba(255,255,255,0.07);
    --border2: rgba(255,255,255,0.12);
    --tg: #29B6F6;
    --tg2: #0288D1;
    --gh: #7ee787;
    --amber: #f0a500;
    --red: #f85149;
    --muted: #8b949e;
    --text: #e6edf3;
    --text2: #cdd9e5;
    --mono: 'JetBrains Mono', monospace;
    --display: 'Syne', sans-serif;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--mono);
    font-size: 14px;
    line-height: 1.7;
    overflow-x: hidden;
  }

  /* GRID BACKGROUND */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(41,182,246,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(41,182,246,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  /* SCAN LINE */
  body::after {
    content: '';
    position: fixed;
    top: -100%;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(transparent 50%, rgba(41,182,246,0.015) 50%);
    background-size: 100% 4px;
    animation: scan 8s linear infinite;
    pointer-events: none;
    z-index: 0;
  }

  @keyframes scan {
    to { top: 100%; }
  }

  .wrapper { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; padding: 0 24px 80px; }

  /* HERO */
  .hero {
    padding: 80px 0 60px;
    text-align: center;
    position: relative;
  }

  .hero-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -60%);
    width: 600px;
    height: 400px;
    background: radial-gradient(ellipse, rgba(41,182,246,0.12) 0%, transparent 70%);
    pointer-events: none;
  }

  .badge-row {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 28px;
  }

  .badge {
    font-family: var(--mono);
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 4px;
    border: 1px solid;
    letter-spacing: 0.05em;
    opacity: 0;
    animation: fadein 0.5s forwards;
  }

  .badge-tg { background: rgba(41,182,246,0.1); border-color: rgba(41,182,246,0.4); color: var(--tg); animation-delay: 0.2s; }
  .badge-gh { background: rgba(126,231,135,0.1); border-color: rgba(126,231,135,0.4); color: var(--gh); animation-delay: 0.35s; }
  .badge-py { background: rgba(240,165,0,0.1); border-color: rgba(240,165,0,0.4); color: var(--amber); animation-delay: 0.5s; }
  .badge-mit { background: rgba(255,255,255,0.05); border-color: var(--border2); color: var(--muted); animation-delay: 0.65s; }

  @keyframes fadein {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .hero-logo {
    font-family: var(--display);
    font-size: clamp(52px, 8vw, 90px);
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1;
    margin-bottom: 8px;
    opacity: 0;
    animation: fadein 0.6s 0.1s forwards;
  }

  .hero-logo .tg { color: var(--tg); }
  .hero-logo .gh { color: var(--gh); }

  .hero-sub {
    font-family: var(--mono);
    font-size: 13px;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 24px;
    opacity: 0;
    animation: fadein 0.6s 0.3s forwards;
  }

  .hero-desc {
    font-size: 15px;
    color: var(--text2);
    max-width: 520px;
    margin: 0 auto 36px;
    opacity: 0;
    animation: fadein 0.6s 0.5s forwards;
    line-height: 1.8;
  }

  .hero-btns {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
    opacity: 0;
    animation: fadein 0.6s 0.7s forwards;
  }

  .btn {
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: 0.06em;
    padding: 10px 22px;
    border-radius: 6px;
    text-decoration: none;
    transition: all 0.2s;
    cursor: pointer;
    border: 1px solid;
  }

  .btn-primary {
    background: var(--tg);
    color: #080c10;
    border-color: var(--tg);
    font-weight: 700;
  }

  .btn-primary:hover { background: #1de9b6; border-color: #1de9b6; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(41,182,246,0.3); }

  .btn-secondary {
    background: transparent;
    color: var(--text);
    border-color: var(--border2);
  }

  .btn-secondary:hover { background: rgba(255,255,255,0.06); transform: translateY(-2px); }

  /* TERMINAL CARD */
  .terminal {
    background: var(--bg2);
    border: 1px solid var(--border2);
    border-radius: 10px;
    overflow: hidden;
    margin: 48px 0;
    opacity: 0;
    animation: fadein 0.7s 0.9s forwards;
  }

  .terminal-bar {
    background: #1a2030;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid var(--border);
  }

  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot-red { background: #f85149; }
  .dot-amber { background: #f0a500; }
  .dot-green { background: #7ee787; }

  .terminal-title { font-size: 11px; color: var(--muted); margin-left: auto; letter-spacing: 0.08em; }

  .terminal-body { padding: 20px 24px; font-size: 13px; line-height: 2; }

  .line { display: flex; align-items: flex-start; gap: 8px; }
  .prompt { color: var(--tg); user-select: none; flex-shrink: 0; }
  .cmd { color: var(--text); }
  .out { color: var(--muted); padding-left: 16px; }
  .out.green { color: var(--gh); }
  .out.blue { color: var(--tg); }
  .out.amber { color: var(--amber); }

  .cursor {
    display: inline-block;
    width: 8px;
    height: 14px;
    background: var(--tg);
    animation: blink 1s step-end infinite;
    vertical-align: text-bottom;
    margin-left: 2px;
  }

  @keyframes blink { 50% { opacity: 0; } }

  /* DIVIDER */
  .divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 56px 0 40px;
  }

  .divider-line { flex: 1; height: 1px; background: var(--border); }
  .divider-label { font-size: 11px; color: var(--muted); letter-spacing: 0.12em; text-transform: uppercase; }

  /* FEATURE GRID */
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; margin-bottom: 48px; }

  .card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
    transition: all 0.3s;
    opacity: 0;
    animation: fadein 0.5s forwards;
    position: relative;
    overflow: hidden;
  }

  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    opacity: 0;
    transition: opacity 0.3s;
  }

  .card:hover { border-color: var(--border2); transform: translateY(-3px); background: var(--bg3); }
  .card:hover::before { opacity: 1; }

  .card-tg::before { background: linear-gradient(90deg, var(--tg), transparent); }
  .card-gh::before { background: linear-gradient(90deg, var(--gh), transparent); }
  .card-amber::before { background: linear-gradient(90deg, var(--amber), transparent); }
  .card-red::before { background: linear-gradient(90deg, var(--red), transparent); }

  .card-icon { font-size: 22px; margin-bottom: 12px; }
  .card-title { font-family: var(--display); font-size: 16px; font-weight: 700; margin-bottom: 6px; color: var(--text); }
  .card-desc { font-size: 12px; color: var(--muted); line-height: 1.7; }
  .card-items { margin-top: 12px; list-style: none; }
  .card-items li { font-size: 12px; color: var(--muted); padding: 2px 0; }
  .card-items li::before { content: '→ '; color: var(--tg); }

  /* ARCH */
  .arch-block {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 32px;
    margin-bottom: 48px;
    font-size: 13px;
  }

  .arch-flow {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
  }

  .arch-node {
    background: var(--bg3);
    border: 1px solid var(--border2);
    border-radius: 8px;
    padding: 12px 32px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-align: center;
    min-width: 240px;
    transition: all 0.25s;
    position: relative;
  }

  .arch-node:hover { border-color: var(--tg); color: var(--tg); box-shadow: 0 0 16px rgba(41,182,246,0.15); }

  .arch-node.tg-node { border-color: rgba(41,182,246,0.4); color: var(--tg); }
  .arch-node.gh-node { border-color: rgba(126,231,135,0.4); color: var(--gh); }

  .arch-arrow {
    width: 1px;
    height: 28px;
    background: linear-gradient(to bottom, var(--tg), rgba(41,182,246,0.2));
    position: relative;
    flex-shrink: 0;
  }

  .arch-arrow::after {
    content: '▼';
    position: absolute;
    bottom: -6px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 8px;
    color: var(--tg);
  }

  .arch-label {
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    position: absolute;
    right: -80px;
    top: 50%;
    transform: translateY(-50%);
    white-space: nowrap;
  }

  /* TECH TABLE */
  .tech-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-bottom: 48px;
  }

  .tech-table th {
    text-align: left;
    padding: 10px 16px;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
  }

  .tech-table td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--border);
  }

  .tech-table tr:last-child td { border-bottom: none; }
  .tech-table tr:hover td { background: rgba(255,255,255,0.02); }

  .tech-table .layer { color: var(--muted); font-size: 12px; }
  .tech-table .tech { color: var(--text); font-weight: 600; }
  .tech-table .pill {
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 20px;
    border: 1px solid;
    letter-spacing: 0.05em;
  }
  .pill-tg { background: rgba(41,182,246,0.1); border-color: rgba(41,182,246,0.3); color: var(--tg); }
  .pill-gh { background: rgba(126,231,135,0.1); border-color: rgba(126,231,135,0.3); color: var(--gh); }
  .pill-amber { background: rgba(240,165,0,0.1); border-color: rgba(240,165,0,0.3); color: var(--amber); }
  .pill-gray { background: rgba(255,255,255,0.05); border-color: var(--border2); color: var(--muted); }

  /* CMD TABLE */
  .cmd-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-bottom: 48px;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }

  .cmd-table th {
    padding: 12px 20px;
    text-align: left;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    background: #1a2030;
    border-bottom: 1px solid var(--border);
  }

  .cmd-table td { padding: 13px 20px; border-bottom: 1px solid var(--border); }
  .cmd-table tr:last-child td { border-bottom: none; }
  .cmd-table tr:hover td { background: rgba(255,255,255,0.02); }

  .cmd-tag {
    font-family: var(--mono);
    font-size: 12px;
    background: rgba(41,182,246,0.08);
    color: var(--tg);
    padding: 3px 10px;
    border-radius: 4px;
    border: 1px solid rgba(41,182,246,0.2);
    white-space: nowrap;
  }

  /* WORKFLOW */
  .workflow { display: flex; flex-direction: column; gap: 0; margin-bottom: 48px; }

  .wf-step {
    display: flex;
    gap: 20px;
    align-items: flex-start;
  }

  .wf-left {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
  }

  .wf-num {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(41,182,246,0.12);
    border: 1px solid rgba(41,182,246,0.4);
    color: var(--tg);
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    z-index: 1;
  }

  .wf-line { width: 1px; flex: 1; min-height: 32px; background: var(--border); margin: 4px 0; }

  .wf-content {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 20px;
    flex: 1;
    transition: border-color 0.2s;
  }

  .wf-content:hover { border-color: var(--border2); }
  .wf-title { font-weight: 700; color: var(--text); font-size: 13px; margin-bottom: 4px; }
  .wf-body { font-size: 12px; color: var(--muted); }
  .wf-code {
    margin-top: 8px;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 12px;
    color: var(--tg);
  }

  /* NOTIFICATION PREVIEW */
  .notif {
    background: var(--bg2);
    border: 1px solid var(--border2);
    border-radius: 10px;
    padding: 16px 20px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-top: 8px;
  }

  .notif-icon { font-size: 18px; flex-shrink: 0; margin-top: 2px; }

  .notif-title { font-weight: 700; font-size: 13px; color: var(--text); margin-bottom: 2px; }
  .notif-body { font-size: 12px; color: var(--muted); }
  .notif-repo { color: var(--tg); }
  .notif-meta { font-size: 11px; color: var(--muted); margin-top: 4px; }

  /* ROADMAP */
  .roadmap { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 48px; }
  .rm-item {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    color: var(--text2);
    transition: all 0.2s;
  }
  .rm-item:hover { border-color: var(--border2); transform: translateX(3px); }
  .rm-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--tg); flex-shrink: 0; }
  .rm-dot.done { background: var(--gh); }

  /* SECURITY */
  .security-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin-bottom: 48px; }
  .sec-item {
    background: var(--bg2);
    border: 1px solid rgba(248,81,73,0.15);
    border-radius: 8px;
    padding: 14px 16px;
    font-size: 12px;
  }
  .sec-icon { color: var(--red); font-size: 16px; margin-bottom: 8px; }
  .sec-text { color: var(--muted); }

  /* INSTALL */
  .install-steps { display: flex; flex-direction: column; gap: 12px; margin-bottom: 48px; }
  .install-step {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    transition: border-color 0.2s;
  }
  .install-step:hover { border-color: var(--border2); }
  .install-header {
    padding: 10px 16px;
    background: #1a2030;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .step-n {
    width: 18px; height: 18px;
    border-radius: 50%;
    background: rgba(41,182,246,0.15);
    border: 1px solid rgba(41,182,246,0.3);
    color: var(--tg);
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .install-code { padding: 14px 20px; font-size: 12px; color: var(--gh); }
  .install-code span { color: var(--muted); }

  /* FOOTER */
  .footer {
    margin-top: 80px;
    border-top: 1px solid var(--border);
    padding-top: 40px;
    text-align: center;
  }

  .footer-name {
    font-family: var(--display);
    font-size: 22px;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 4px;
  }

  .footer-tagline { font-size: 12px; color: var(--muted); letter-spacing: 0.08em; }

  .footer-vision {
    margin: 24px auto;
    max-width: 480px;
    font-size: 13px;
    color: var(--muted);
    border-left: 2px solid var(--tg);
    padding-left: 16px;
    text-align: left;
  }

  .footer-vision strong { color: var(--text); }

  .footer-links { display: flex; gap: 16px; justify-content: center; margin-top: 24px; }
  .footer-links a {
    font-size: 12px;
    color: var(--muted);
    text-decoration: none;
    transition: color 0.2s;
    letter-spacing: 0.06em;
  }
  .footer-links a:hover { color: var(--tg); }

  .footer-copy { font-size: 11px; color: rgba(255,255,255,0.2); margin-top: 32px; letter-spacing: 0.08em; }

  /* SECTION TITLE */
  .sec-title {
    font-family: var(--display);
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 20px;
    letter-spacing: -0.5px;
  }

  .sec-title span { color: var(--tg); }

  /* PULSE ANIMATION for cards */
  @keyframes pulse-border {
    0%, 100% { box-shadow: 0 0 0 0 rgba(41,182,246,0); }
    50% { box-shadow: 0 0 0 4px rgba(41,182,246,0.06); }
  }

  /* STAGGER HELPERS */
  .card:nth-child(1) { animation-delay: 0.1s; }
  .card:nth-child(2) { animation-delay: 0.2s; }
  .card:nth-child(3) { animation-delay: 0.3s; }
  .card:nth-child(4) { animation-delay: 0.4s; }

  /* SCROLLED IN */
  .scroll-reveal {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }
  .scroll-reveal.visible { opacity: 1; transform: none; }

  @media (max-width: 600px) {
    .roadmap { grid-template-columns: 1fr; }
    .hero-logo { font-size: 48px; }
    .arch-label { display: none; }
  }
</style>
</head>
<body>

<div class="wrapper">

  <!-- HERO -->
  <div class="hero">
    <div class="hero-glow"></div>
    <div class="badge-row">
      <span class="badge badge-tg">TELEGRAM</span>
      <span class="badge badge-gh">GITHUB</span>
      <span class="badge badge-py">FASTAPI + PYTHON</span>
      <span class="badge badge-mit">MIT LICENSE</span>
    </div>
    <div class="hero-logo">
      <span class="tg">Git</span><span class="gh">Gram</span> 🚀
    </div>
    <div class="hero-sub">Manage GitHub. From Telegram.</div>
    <p class="hero-desc">
      Close issues. Monitor PRs. Get real-time repository alerts — all without touching GitHub.
      Your codebase in your pocket.
    </p>
    <div class="hero-btns">
      <a class="btn btn-primary" href="#install">Get Started</a>
      <a class="btn btn-secondary" href="#features">See Features →</a>
    </div>
  </div>

  <!-- TERMINAL -->
  <div class="terminal">
    <div class="terminal-bar">
      <span class="dot dot-red"></span>
      <span class="dot dot-amber"></span>
      <span class="dot dot-green"></span>
      <span class="terminal-title">gitgram — session</span>
    </div>
    <div class="terminal-body">
      <div class="line"><span class="prompt">$</span><span class="cmd">python main.py</span></div>
      <div class="out green">✓ FastAPI server started on port 8000</div>
      <div class="out blue">✓ Telegram bot polling initialized</div>
      <div class="out amber">◎ Waiting for GitHub webhook events...</div>
      <br>
      <div class="out">📦 [incoming] issues event from frontend-app</div>
      <div class="out green">🚨 Issue #42 opened — "Login page crashing"</div>
      <div class="out blue">📨 Telegram notification dispatched → @sarwar_dev</div>
      <br>
      <div class="line"><span class="prompt">$</span><span class="cmd">/close 42<span class="cursor"></span></span></div>
    </div>
  </div>

  <!-- FEATURES -->
  <div id="features">
    <div class="divider">
      <div class="divider-line"></div>
      <div class="divider-label">Features</div>
      <div class="divider-line"></div>
    </div>

    <div class="grid">
      <div class="card card-tg">
        <div class="card-icon">📡</div>
        <div class="card-title">Repository Monitoring</div>
        <div class="card-desc">Real-time event streaming from GitHub directly into Telegram.</div>
        <ul class="card-items">
          <li>Issue notifications</li>
          <li>Pull Request alerts</li>
          <li>Commit event tracking</li>
          <li>Status monitoring</li>
        </ul>
      </div>
      <div class="card card-gh">
        <div class="card-icon">⚡</div>
        <div class="card-title">Telegram Actions</div>
        <div class="card-desc">Trigger GitHub operations without leaving your chat.</div>
        <ul class="card-items">
          <li>Close issues</li>
          <li>Comment on issues</li>
          <li>Reopen closed issues</li>
          <li>Merge PRs (planned)</li>
        </ul>
      </div>
      <div class="card card-amber">
        <div class="card-icon">🔐</div>
        <div class="card-title">Auth System</div>
        <div class="card-desc">Secure, multi-user GitHub integration via Personal Access Tokens.</div>
        <ul class="card-items">
          <li>PAT-based login</li>
          <li>Multi-user support</li>
          <li>Repo-level access control</li>
        </ul>
      </div>
      <div class="card card-red">
        <div class="card-icon">🧠</div>
        <div class="card-title">Smart Workflow</div>
        <div class="card-desc">Mobile-first, zero context-switching dev experience.</div>
        <ul class="card-items">
          <li>Instant push notifications</li>
          <li>No browser switching</li>
          <li>AI summaries (planned)</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- ARCHITECTURE -->
  <div class="divider scroll-reveal">
    <div class="divider-line"></div>
    <div class="divider-label">Architecture</div>
    <div class="divider-line"></div>
  </div>

  <div class="arch-block scroll-reveal">
    <div class="arch-flow">
      <div class="arch-node tg-node">Telegram Bot</div>
      <div class="arch-arrow"></div>
      <div class="arch-node">FastAPI App</div>
      <div class="arch-arrow"></div>
      <div class="arch-node gh-node">GitHub Webhooks</div>
      <div class="arch-arrow"></div>
      <div class="arch-node" style="color:var(--amber); border-color:rgba(240,165,0,0.4);">SQLite / DB</div>
    </div>
  </div>

  <!-- TECH STACK -->
  <div class="divider scroll-reveal">
    <div class="divider-line"></div>
    <div class="divider-label">Tech Stack</div>
    <div class="divider-line"></div>
  </div>

  <table class="tech-table scroll-reveal">
    <thead>
      <tr>
        <th>Layer</th>
        <th>Technology</th>
        <th>Type</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="layer">Backend</td>
        <td class="tech">Python</td>
        <td><span class="pill pill-amber">Language</span></td>
      </tr>
      <tr>
        <td class="layer">API Framework</td>
        <td class="tech">FastAPI</td>
        <td><span class="pill pill-amber">Framework</span></td>
      </tr>
      <tr>
        <td class="layer">Telegram Integration</td>
        <td class="tech">python-telegram-bot</td>
        <td><span class="pill pill-tg">Bot</span></td>
      </tr>
      <tr>
        <td class="layer">Database</td>
        <td class="tech">SQLite</td>
        <td><span class="pill pill-gray">Storage</span></td>
      </tr>
      <tr>
        <td class="layer">GitHub Integration</td>
        <td class="tech">GitHub REST API</td>
        <td><span class="pill pill-gh">API</span></td>
      </tr>
      <tr>
        <td class="layer">Webhooks</td>
        <td class="tech">GitHub Webhooks</td>
        <td><span class="pill pill-gh">Events</span></td>
      </tr>
      <tr>
        <td class="layer">Deployment</td>
        <td class="tech">Render / Ngrok</td>
        <td><span class="pill pill-gray">Infra</span></td>
      </tr>
    </tbody>
  </table>

  <!-- COMMANDS -->
  <div class="divider scroll-reveal">
    <div class="divider-line"></div>
    <div class="divider-label">Commands</div>
    <div class="divider-line"></div>
  </div>

  <table class="cmd-table scroll-reveal">
    <thead>
      <tr>
        <th>Command</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="cmd-tag">/start</span></td>
        <td style="color:var(--muted);font-size:13px;">Initialize the bot</td>
      </tr>
      <tr>
        <td><span class="cmd-tag">/connect</span></td>
        <td style="color:var(--muted);font-size:13px;">Link GitHub account via PAT</td>
      </tr>
      <tr>
        <td><span class="cmd-tag">/status</span></td>
        <td style="color:var(--muted);font-size:13px;">Check repository connection status</td>
      </tr>
      <tr>
        <td><span class="cmd-tag">/close &lt;id&gt;</span></td>
        <td style="color:var(--muted);font-size:13px;">Close a GitHub issue by ID</td>
      </tr>
      <tr>
        <td><span class="cmd-tag">/comment &lt;id&gt;</span></td>
        <td style="color:var(--muted);font-size:13px;">Post a comment on an issue</td>
      </tr>
      <tr>
        <td><span class="cmd-tag">/repos</span></td>
        <td style="color:var(--muted);font-size:13px;">List all connected repositories</td>
      </tr>
    </tbody>
  </table>

  <!-- WORKFLOW -->
  <div class="divider scroll-reveal">
    <div class="divider-line"></div>
    <div class="divider-label">Example Workflow</div>
    <div class="divider-line"></div>
  </div>

  <div class="workflow scroll-reveal">
    <div class="wf-step">
      <div class="wf-left">
        <div class="wf-num">1</div>
        <div class="wf-line"></div>
      </div>
      <div class="wf-content">
        <div class="wf-title">Connect Your GitHub Account</div>
        <div class="wf-body">Send /connect to the bot. It prompts for your GitHub Personal Access Token, links your account, and sets up repository access.</div>
        <div class="wf-code">/connect</div>
      </div>
    </div>

    <div class="wf-step">
      <div class="wf-left">
        <div class="wf-num">2</div>
        <div class="wf-line"></div>
      </div>
      <div class="wf-content">
        <div class="wf-title">GitHub Fires a Webhook</div>
        <div class="wf-body">A developer opens an issue. GitHub sends an event to your FastAPI endpoint. You get an instant Telegram notification.</div>
        <div class="notif">
          <div class="notif-icon">🚨</div>
          <div>
            <div class="notif-title">New Issue Opened</div>
            <div class="notif-body">Repository: <span class="notif-repo">frontend-app</span></div>
            <div class="notif-body">Issue #42: Login page crashing</div>
            <div class="notif-meta">just now · via GitGram</div>
          </div>
        </div>
      </div>
    </div>

    <div class="wf-step">
      <div class="wf-left">
        <div class="wf-num">3</div>
      </div>
      <div class="wf-content">
        <div class="wf-title">Take Action From Telegram</div>
        <div class="wf-body">Close the issue without switching apps. The bot hits the GitHub API and confirms instantly.</div>
        <div class="wf-code">/close 42</div>
      </div>
    </div>
  </div>

  <!-- INSTALL -->
  <div id="install" class="divider scroll-reveal">
    <div class="divider-line"></div>
    <div class="divider-label">Installation</div>
    <div class="divider-line"></div>
  </div>

  <div class="install-steps scroll-reveal">
    <div class="install-step">
      <div class="install-header"><span class="step-n">1</span> Clone Repository</div>
      <div class="install-code">git clone https://github.com/your-username/thegitgram_bot.git<br><span>cd thegitgram_bot</span></div>
    </div>
    <div class="install-step">
      <div class="install-header"><span class="step-n">2</span> Create Virtual Environment</div>
      <div class="install-code"><span># Linux / macOS</span><br>python3 -m venv venv && source venv/bin/activate</div>
    </div>
    <div class="install-step">
      <div class="install-header"><span class="step-n">3</span> Install Dependencies</div>
      <div class="install-code">pip install -r requirements.txt</div>
    </div>
    <div class="install-step">
      <div class="install-header"><span class="step-n">4</span> Configure Environment</div>
      <div class="install-code">
        <span># .env</span><br>
        TELEGRAM_BOT_TOKEN=your_telegram_bot_token<br>
        GITHUB_WEBHOOK_SECRET=your_webhook_secret<br>
        DATABASE_URL=sqlite:///gitgram.db<br>
        NGROK_AUTH_TOKEN=your_ngrok_token
      </div>
    </div>
    <div class="install-step">
      <div class="install-header"><span class="step-n">5</span> Launch</div>
      <div class="install-code">python main.py</div>
    </div>
  </div>

  <!-- SECURITY -->
  <div class="divider scroll-reveal">
    <div class="divider-line"></div>
    <div class="divider-label">Security Notes</div>
    <div class="divider-line"></div>
  </div>

  <div class="security-grid scroll-reveal">
    <div class="sec-item">
      <div class="sec-icon">🔒</div>
      <div class="sec-text">Encrypt tokens before saving to database</div>
    </div>
    <div class="sec-item">
      <div class="sec-icon">🌐</div>
      <div class="sec-text">Use environment variables — never hardcode secrets</div>
    </div>
    <div class="sec-item">
      <div class="sec-icon">✅</div>
      <div class="sec-text">Implement webhook signature verification</div>
    </div>
    <div class="sec-item">
      <div class="sec-icon">🛡️</div>
      <div class="sec-text">Add rate limiting on all endpoints</div>
    </div>
    <div class="sec-item">
      <div class="sec-icon">⚙️</div>
      <div class="sec-text">Use GitHub Apps in production environments</div>
    </div>
    <div class="sec-item">
      <div class="sec-icon">🚫</div>
      <div class="sec-text">Never store PATs in plain text — ever</div>
    </div>
  </div>

  <!-- ROADMAP -->
  <div class="divider scroll-reveal">
    <div class="divider-line"></div>
    <div class="divider-label">Roadmap</div>
    <div class="divider-line"></div>
  </div>

  <div class="roadmap scroll-reveal">
    <div class="rm-item"><span class="rm-dot done"></span>Real-time issue notifications</div>
    <div class="rm-item"><span class="rm-dot done"></span>Close / reopen issues from Telegram</div>
    <div class="rm-item"><span class="rm-dot done"></span>Comment on issues</div>
    <div class="rm-item"><span class="rm-dot done"></span>Multi-user architecture</div>
    <div class="rm-item"><span class="rm-dot"></span>GitHub OAuth login</div>
    <div class="rm-item"><span class="rm-dot"></span>Merge PRs from Telegram</div>
    <div class="rm-item"><span class="rm-dot"></span>Inline issue management buttons</div>
    <div class="rm-item"><span class="rm-dot"></span>AI-generated issue summaries</div>
    <div class="rm-item"><span class="rm-dot"></span>CI/CD pipeline alerts</div>
    <div class="rm-item"><span class="rm-dot"></span>Deployment notifications</div>
    <div class="rm-item"><span class="rm-dot"></span>Multi-repository dashboards</div>
    <div class="rm-item"><span class="rm-dot"></span>GitHub App integration</div>
  </div>

  <!-- FOOTER -->
  <div class="footer scroll-reveal">
    <div class="footer-name">Sarwar Altaf Dar</div>
    <div class="footer-tagline">Built with caffeine and chaos · MIT License</div>
    <div class="footer-vision">
      <strong>Vision:</strong> GitGram aims to become the Telegram-powered operating system for developers — from issue management to deployments, a complete DevOps communication layer.
    </div>
    <div class="footer-links">
      <a href="#">⭐ Star on GitHub</a>
      <a href="#">🍴 Fork</a>
      <a href="#">🐛 Report Bug</a>
      <a href="#">🤝 Contribute</a>
    </div>
    <div class="footer-copy">© 2025 GitGram · Fast. Minimal. Developer-first.</div>
  </div>

</div>

<script>
  const reveals = document.querySelectorAll('.scroll-reveal');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  reveals.forEach(el => obs.observe(el));
</script>

</body>
</html>
