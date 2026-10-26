import json
import os
from pathlib import Path
import subprocess

repo = Path.cwd()
out = repo / ".github/issue-1220-evidence/linux-results"
config = out / "config"
config.mkdir(parents=True, exist_ok=True)
settings = {"editor": {"wordWrap": True, "wordWrapColumn": 80, "syntaxHighlight": False,
                       "languageOverrides": {"typescript": {"wordWrapColumn": 80}, "markdown": {"wordWrapColumn": 65}}},
            "lsp": {"enabled": False}}
(config / "settings.json").write_text(json.dumps(settings))
md, ts = out / "README.md", out / "main.ts"
md.write_text("x" * 200)
ts.write_text("y" * 200)
script = (f'screenshot {out}/markdown.txt; debug {out}/markdown.json; '
          f'click 120 4; debug {out}/pointer.json; exec "View: Previous Tab"; '
          f'screenshot {out}/typescript.txt; debug {out}/typescript.json; '
          f'exec "Reload Settings"; debug {out}/reload.json; quit')
subprocess.run([str(repo / "bin/ttt"), str(ts), str(md), "--size", "160x35", "--exec", script],
               env={**os.environ, "TTT_CONFIG_DIR": str(config)}, check=True, timeout=30)
states = {name: json.loads((out / f"{name}.json").read_text()) for name in ("markdown", "typescript", "pointer", "reload")}
assert states["markdown"]["viewport"]["width"] == 65
assert states["typescript"]["viewport"]["width"] == states["reload"]["viewport"]["width"] == 80
assert states["pointer"]["cursor"] == {"line": 0, "col": 64}
assert all(not state["buffer"]["modified"] for state in states.values())
assert md.read_text() == "x" * 200 and ts.read_text() == "y" * 200
print("Real-binary language caps, tab switch, reload and blank-space hit testing passed without LSP or syntax coloring.")
