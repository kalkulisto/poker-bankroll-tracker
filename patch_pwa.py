path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

pwa = (
    '<link rel="manifest" href="/static/manifest.json">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
    '<meta name="apple-mobile-web-app-title" content="C&amp;Z Poker">\n'
    '<link rel="apple-touch-icon" href="/static/icon-192.png">\n'
    '<meta name="theme-color" content="#0a0f0a">\n'
)
sw = '<script>if("serviceWorker"in navigator){navigator.serviceWorker.register("/static/sw.js");}</script>\n'

if 'manifest.json' not in c:
    c = c.replace('</head>', pwa + '</head>', 1)
    c = c.replace('</body>', sw + '</body>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('patched')
else:
    print('already patched')
