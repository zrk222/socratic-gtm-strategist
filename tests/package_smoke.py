"""Install a built wheel into a fresh environment and exercise it off-checkout."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import venv


def main():
    wheel = Path(sys.argv[1]).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        env = root / "environment"
        venv.create(env, with_pip=True)
        scripts = env / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        cli = scripts / ("socratic-gtm.exe" if os.name == "nt" else "socratic-gtm")
        cwd = root / "outside-checkout"
        cwd.mkdir()
        def run(args, **kwargs):
            result = subprocess.run([str(arg) for arg in args], cwd=cwd, capture_output=True,
                                    text=True, encoding="utf-8", timeout=90, **kwargs)
            if result.returncode:
                raise AssertionError(result.stdout + result.stderr)
            return result
        run([python, "-m", "pip", "install", "--no-index", "--no-deps", wheel])
        assert "Available subcommands" in run([cli, "--help"]).stdout
        run([cli, "simulate", "--project", "Installed wheel", "--scores", "0,10,20,30,40,50,60,70"])
        assert (cwd / "gtm_simulator.html").is_file()
        run([python, "-I", "-c",
             "import server, mcp_server, socratic_gtm; from pathlib import Path; "
             "assert 'Socratic GTM' in socratic_gtm.get_system_prompt(); "
             "ui=Path(server.__file__).parent/'ui'; "
             "assert (ui/'index.html').is_file(); assert (ui/'session.js').is_file(); assert (ui/'prep.js').is_file(); assert (ui/'prep-ui.js').is_file(); assert (ui/'prep.css').is_file(); "
             "assert (ui/'openapi.json').is_file(); print('resources OK')"])
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
                "name": "gtm_socratic_evaluate", "arguments": {"phase": 1, "founder_answer": "word " * 40}}},
            {"jsonrpc": "2.0", "id": 3, "method": "ping"},
        ]
        result = run([cli, "mcp"], input="\n".join(json.dumps(item) for item in requests) + "\n")
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        assert responses[0]["result"]["serverInfo"]["name"] == "socratic-gtm-strategist"
        assessment = json.loads(responses[1]["result"]["content"][0]["text"])
        assert assessment["status"] == "REVIEW_REQUIRED" and assessment["confidence_score"] is None
        assert responses[2]["result"] == {}
        print(json.dumps({"status": "PASS", "wheel": wheel.name, "python": sys.version.split()[0],
                          "checks": ["isolated-install", "console-entrypoint", "html-generation",
                                     "sdk-prompt", "packaged-ui-schema-js", "mcp-initialize",
                                     "mcp-evaluation", "mcp-ping"]}))


if __name__ == "__main__":
    main()
