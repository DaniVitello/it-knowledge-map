
import os, re, json
project = r"C:\Users\DGVit\Proyectos\IT Career"
matches = []
for root, dirs, files in os.walk(project):
    # skip .git
    dirs[:] = [d for d in dirs if d != '.git']
    for f in files:
        if f.endswith(('.gitignore',)):
            continue
        p = os.path.join(root, f)
        try:
            with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                txt = fh.read()
            # Look for typical groq key patterns: gsk_ followed by long alphanumeric
            hits = re.findall(r'gsk_[A-Za-z0-9]{20,}', txt)
            if hits:
                matches.append((p, len(hits), hits[0][:12]+'...'))
        except: pass
print("FILES_WITH_GROQ_KEYS")
for m in matches:
    print(m[0], 'hits=', m[1], 'sample=', m[2])
