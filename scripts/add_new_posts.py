"""
1. Copy 3 new germany posts from source folder to worktree
2. Add standard nav + footer (Fredoka One / Nunito design)
3. Add GA4 Consent Mode v2 + Silktide cookie consent
4. Regenerate posts.json
"""
import re, os, shutil

SRC  = r'C:\Users\Leona\Desktop\lenaportal-main (1)\lenaportal-main\germany'
DEST = r'C:\Users\Leona\Desktop\lenaportal-main (1)\lenaportal-main\.claude\worktrees\lucid-shtern-f81fee\germany'
ROOT = os.path.dirname(DEST)

NEW_FILES = [
    'mainau-tulpen.html',
    'muttertag-deutschland.html',
    'hamburg-schlepperballett.html',
]

# ── Fonts ──────────────────────────────────────────────────────────────────
FONT_IMPORT = '  <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">\n'

# ── Nav + Footer CSS ───────────────────────────────────────────────────────
NAV_FOOTER_CSS = """
  <!-- ═══ Standard Nav & Footer CSS ═══ -->
  <style>
    body { padding-top: 64px; padding-bottom: 64px; }
    nav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 200;
      padding: 16px 32px;
      display: flex; justify-content: space-between; align-items: center;
      background: rgba(254,254,254,0.92);
      backdrop-filter: blur(16px);
      border-bottom: 2.5px dashed #e0e0e0;
    }
    .nav-logo {
      font-family: 'Fredoka One', cursive;
      font-size: 22px; color: #2d2d44;
      text-decoration: none;
      display: flex; align-items: center; gap: 8px;
    }
    .logo-dot {
      width: 10px; height: 10px; border-radius: 50%;
      background: #FF6B9D;
      animation: dotpop 1.4s ease-in-out infinite alternate;
    }
    @keyframes dotpop { from { transform: scale(1); } to { transform: scale(1.6); } }
    .nav-links { display: flex; gap: 8px; list-style: none; }
    .nav-links a {
      font-size: 13px; font-weight: 700;
      text-decoration: none; color: #2d2d44;
      padding: 6px 14px; border-radius: 20px;
      border: 2px solid transparent; transition: all 0.2s;
      font-family: 'Nunito', sans-serif;
    }
    .nav-links a:hover { border-color: #2d2d44; background: #FFD93D; }
    @media (max-width: 480px) { .nav-links { display: none; } }
    footer {
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 200;
      padding: 14px 40px;
      display: flex; justify-content: space-between; align-items: center;
      background: rgba(254,254,254,0.92);
      backdrop-filter: blur(16px);
      border-top: 2.5px dashed #e0e0e0;
      flex-wrap: wrap; gap: 8px;
    }
    .footer-logo {
      font-family: 'Fredoka One', cursive; font-size: 20px;
      color: #2d2d44; text-decoration: none;
    }
    .footer-dots { display: flex; gap: 8px; }
    .footer-dot {
      width: 12px; height: 12px; border-radius: 50%;
      border: 2px solid #2d2d44; transition: background 0.2s; cursor: pointer;
    }
    .footer-dot:nth-child(1) { background: #FFD93D; }
    .footer-dot:nth-child(2) { background: #FF6B9D; }
    .footer-dot:nth-child(3) { background: #4ECDC4; }
    .footer-dot:nth-child(4) { background: #4D96FF; }
    .footer-dot:hover { background: #2d2d44 !important; }
    .footer-text { font-size: 13px; font-weight: 600; color: #aaa; font-family: 'Nunito', sans-serif; }
    .footer-links { display: flex; gap: 16px; }
    .footer-links a {
      font-size: 12px; font-weight: 700; color: #999;
      text-decoration: none; font-family: 'Nunito', sans-serif;
    }
    .footer-links a:hover { color: #FF6B9D; }
    @media (max-width: 768px) { nav { padding: 14px 20px; } footer { padding: 12px 20px; } }
  </style>
"""

# ── Nav HTML ───────────────────────────────────────────────────────────────
NAV_HTML = """
  <nav role="navigation" aria-label="Main navigation">
    <a href="../index.html" class="nav-logo" aria-label="lena-var4 home">
      <span class="logo-dot" aria-hidden="true"></span>
      lena-var4
    </a>
    <ul class="nav-links">
      <li><a href="./index.html">🇩🇪 Germany Blog</a></li>
    </ul>
  </nav>
"""

# ── Footer HTML ────────────────────────────────────────────────────────────
FOOTER_HTML = """
  <footer role="contentinfo">
    <a href="../index.html" class="footer-logo">lena-var4.com</a>
    <div class="footer-dots" aria-hidden="true">
      <div class="footer-dot"></div>
      <div class="footer-dot"></div>
      <div class="footer-dot"></div>
      <div class="footer-dot"></div>
    </div>
    <p class="footer-text">Made with ☕ somewhere in Germany</p>
    <div class="footer-links">
      <a href="../about/index.html">About</a>
      <a href="../privacy-policy.html">Privacy Policy</a>
    </div>
  </footer>
"""

# ── GA4 + Consent Mode v2 + Silktide ──────────────────────────────────────
CONSENT_MODE = """  <!-- Google Consent Mode v2 – defaults (must be before GA4) -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {
      analytics_storage:    (localStorage.getItem('silktideCookieChoice_analytics')       === 'true') ? 'granted' : 'denied',
      ad_storage:           (localStorage.getItem('silktideCookieChoice_advertising')     === 'true') ? 'granted' : 'denied',
      ad_user_data:         (localStorage.getItem('silktideCookieChoice_advertising')     === 'true') ? 'granted' : 'denied',
      ad_personalization:   (localStorage.getItem('silktideCookieChoice_advertising')     === 'true') ? 'granted' : 'denied',
      functionality_storage:(localStorage.getItem('silktideCookieChoice_externe_medien')  === 'true') ? 'granted' : 'denied',
      wait_for_update: 500
    });
  </script>
"""

GA4_TAG = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-H0Y00EL355"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-H0Y00EL355');
  </script>
"""

SILKTIDE = """
  <!-- Cookie Consent Manager (Silktide) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/silktide/consent-manager@main/silktide-consent-manager.css">
  <script src="https://cdn.jsdelivr.net/gh/silktide/consent-manager@main/silktide-consent-manager.js"></script>
  <script>
  window.silktideConsentManager.init({
    consentTypes: [
      { id: "necessary", name: "Notwendig", description: "Diese Cookies sind für das ordnungsgemäße Funktionieren der Website erforderlich und können nicht deaktiviert werden.", required: true, onAccept: function() {} },
      { id: "analytics", name: "Analytik", description: "Diese Cookies helfen uns zu verstehen, wie Besucher mit unserer Website interagieren (z. B. Google Analytics). Alle Daten werden anonymisiert erhoben.", required: false,
        onAccept: function() { gtag('consent', 'update', { analytics_storage: 'granted' }); },
        onReject: function() { gtag('consent', 'update', { analytics_storage: 'denied' }); }
      },
      { id: "advertising", name: "Werbung", description: "Diese Cookies werden verwendet, um Ihnen relevante Werbeanzeigen zu zeigen (z. B. Google AdSense). Ohne Ihre Einwilligung sehen Sie nur nicht-personalisierte Werbung.", required: false,
        onAccept: function() { gtag('consent', 'update', { ad_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted' }); },
        onReject: function() { gtag('consent', 'update', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' }); }
      },
      { id: "externe_medien", name: "Externe Medien", description: "Diese Cookies ermöglichen das Laden externer Inhalte wie Videos oder Karten. Ohne Ihre Einwilligung werden diese Inhalte blockiert.", required: false,
        onAccept: function() { gtag('consent', 'update', { functionality_storage: 'granted' }); },
        onReject: function() { gtag('consent', 'update', { functionality_storage: 'denied' }); }
      }
    ],
    text: {
      title: "Wir verwenden Cookies",
      description: "Wir setzen Cookies ein, um die Nutzung der Website zu analysieren und Ihnen relevante Inhalte und Werbung anzuzeigen. Sie können Ihre Einstellungen jederzeit ändern.",
      acceptAll: "Alle akzeptieren", rejectAll: "Alle ablehnen",
      customize: "Einstellungen", save: "Speichern",
      privacyPolicy: "Datenschutzerklärung", poweredBy: "Cookie-Einstellungen"
    },
    links: { privacyPolicy: "https://lena-var4.com/privacy-policy.html" },
    prompt: { banner: "bottomLeft" },
    icon: { position: "bottomLeft" }
  });
  </script>"""

results = []

for fname in NEW_FILES:
    src_path  = os.path.join(SRC,  fname)
    dest_path = os.path.join(DEST, fname)

    # 1. Copy file
    shutil.copy2(src_path, dest_path)

    with open(dest_path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 2. Add font import before </head> if Fredoka not present
    if 'Fredoka' not in c:
        c = c.replace('</head>', FONT_IMPORT + '</head>', 1)

    # 3. Add Nav+Footer CSS before </head>
    c = c.replace('</head>', NAV_FOOTER_CSS + '</head>', 1)

    # 4. Add Consent Mode + GA4 + Silktide before </head>
    c = c.replace('</head>', CONSENT_MODE + GA4_TAG + SILKTIDE + '\n</head>', 1)

    # 5. Add nav HTML right after <body> (and any immediate whitespace)
    c = re.sub(r'(<body[^>]*>)', r'\1\n' + NAV_HTML, c, count=1)

    # 6. Add footer HTML before </body>
    c = c.replace('</body>', FOOTER_HTML + '\n</body>', 1)

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(c)

    results.append(f'Done: {fname}')

# 7. Regenerate posts.json
import subprocess
result = subprocess.run(
    ['python', os.path.join(ROOT, 'scripts', 'scan_posts.py')],
    cwd=ROOT, capture_output=True, text=True
)
results.append(f'scan_posts.py: {result.returncode}')
if result.stderr:
    results.append(f'stderr: {result.stderr[:300]}')

with open(os.path.join(ROOT, 'scripts', 'add_new_posts_result.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(results) + '\n')
