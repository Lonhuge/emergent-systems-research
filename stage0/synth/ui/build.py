"""Compose the publishable page from template.html and engine.js."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "template.html")).read()
eng = open(os.path.join(HERE, "engine.js")).read()
assert "</script" not in eng
assert tpl.count("/*__ENGINE__*/") == 2
out = tpl.replace("/*__ENGINE__*/", eng)
open(os.path.join(HERE, "teiltongarten.html"), "w").write(out)
print("wrote teiltongarten.html", len(out), "bytes")
