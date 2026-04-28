"""
Installs Silktide Cookie Consent Manager on all HTML pages.
- Adds Google Consent Mode v2 defaults BEFORE the GA4 tag
- Adds Silktide CSS + JS + German config AFTER the GA4 tag
- Skips files that already have silktideConsentManager
"""
import glob, re, os

WORKTREE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONSENT_MODE_DEFAULTS = """  <!-- Google Consent Mode v2 – defaults (must be before GA4) -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {
      analytics_storage:   (localStorage.getItem('silktideCookieChoice_analytics')    === 'true') ? 'granted' : 'denied',
      ad_storage:          (localStorage.getItem('silktideCookieChoice_advertising')  === 'true') ? 'granted' : 'denied',
      ad_user_data:        (localStorage.getItem('silktideCookieChoice_advertising')  === 'true') ? 'granted' : 'denied',
      ad_personalization:  (localStorage.getItem('silktideCookieChoice_advertising')  === 'true') ? 'granted' : 'denied',
      functionality_storage:(localStorage.getItem('silktideCookieChoice_externe_medien') === 'true') ? 'granted' : 'denied',
      wait_for_update: 500
    });
  </script>
"""

SILKTIDE_BLOCK = """
  <!-- Cookie Consent Manager (Silktide) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/silktide/consent-manager@main/silktide-consent-manager.css">
  <script src="https://cdn.jsdelivr.net/gh/silktide/consent-manager@main/silktide-consent-manager.js"></script>
  <script>
  window.silktideConsentManager.init({
    consentTypes: [
      {
        id: "necessary",
        name: "Notwendig",
        description: "Diese Cookies sind für das ordnungsgemäße Funktionieren der Website erforderlich und können nicht deaktiviert werden.",
        required: true,
        onAccept: function() {}
      },
      {
        id: "analytics",
        name: "Analytik",
        description: "Diese Cookies helfen uns zu verstehen, wie Besucher mit unserer Website interagieren (z. B. Google Analytics). Alle Daten werden anonymisiert erhoben.",
        required: false,
        onAccept: function() {
          gtag('consent', 'update', { analytics_storage: 'granted' });
        },
        onReject: function() {
          gtag('consent', 'update', { analytics_storage: 'denied' });
        }
      },
      {
        id: "advertising",
        name: "Werbung",
        description: "Diese Cookies werden verwendet, um Ihnen relevante Werbeanzeigen zu zeigen (z. B. Google AdSense). Ohne Ihre Einwilligung sehen Sie nur nicht-personalisierte Werbung.",
        required: false,
        onAccept: function() {
          gtag('consent', 'update', {
            ad_storage: 'granted',
            ad_user_data: 'granted',
            ad_personalization: 'granted'
          });
        },
        onReject: function() {
          gtag('consent', 'update', {
            ad_storage: 'denied',
            ad_user_data: 'denied',
            ad_personalization: 'denied'
          });
        }
      },
      {
        id: "externe_medien",
        name: "Externe Medien",
        description: "Diese Cookies ermöglichen das Laden externer Inhalte wie Videos oder Karten. Ohne Ihre Einwilligung werden diese Inhalte blockiert.",
        required: false,
        onAccept: function() {
          gtag('consent', 'update', { functionality_storage: 'granted' });
        },
        onReject: function() {
          gtag('consent', 'update', { functionality_storage: 'denied' });
        }
      }
    ],
    text: {
      title: "Wir verwenden Cookies",
      description: "Wir setzen Cookies ein, um die Nutzung der Website zu analysieren und Ihnen relevante Inhalte und Werbung anzuzeigen. Sie können Ihre Einstellungen jederzeit ändern.",
      acceptAll: "Alle akzeptieren",
      rejectAll: "Alle ablehnen",
      customize: "Einstellungen",
      save: "Speichern",
      privacyPolicy: "Datenschutzerklärung",
      poweredBy: "Cookie-Einstellungen"
    },
    links: {
      privacyPolicy: "https://lena-var4.com/privacy-policy.html"
    },
    prompt: {
      banner: "bottomLeft"
    },
    icon: {
      position: "bottomLeft"
    }
  });
  </script>"""

# Pattern to match the complete GA4 tag block
GA4_PATTERN = re.compile(
    r'([ \t]*<!--[ \t]*Google tag.*?</script>)',
    re.DOTALL
)

files = glob.glob(os.path.join(WORKTREE, '**/*.html'), recursive=True)
fixed = 0
skipped = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # Skip files already processed
    if 'silktideConsentManager' in content:
        skipped += 1
        continue

    # Find the GA4 block
    m = GA4_PATTERN.search(content)
    if not m:
        # No GA4 tag found — just add consent defaults + silktide before </head>
        new_content = content.replace(
            '</head>',
            CONSENT_MODE_DEFAULTS + SILKTIDE_BLOCK + '\n</head>',
            1
        )
    else:
        ga4_block = m.group(0)
        # Insert consent defaults before GA4 block
        replacement = CONSENT_MODE_DEFAULTS + ga4_block + SILKTIDE_BLOCK
        new_content = content[:m.start()] + replacement + content[m.end():]

    if new_content != content:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        fixed += 1

with open(os.path.join(WORKTREE, 'scripts', 'cookie_consent_result.txt'), 'w', encoding='utf-8') as fh:
    fh.write(f'Installed cookie consent on {fixed} files\n')
    fh.write(f'Skipped (already present): {skipped} files\n')
    fh.write(f'Total HTML files scanned: {len(files)}\n')
