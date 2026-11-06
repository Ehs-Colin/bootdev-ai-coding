---
description: Start the SlopLang playground server, reusing a running instance
---

Start the SlopLang playground server on port $ARGUMENTS, using 8080 when $ARGUMENTS is empty.

Current TCP listeners:

!`lsof -nP -iTCP -sTCP:LISTEN`

Follow these steps:

1. Resolve the port. If $ARGUMENTS is empty, use 8080. Otherwise require it to be a
   single integer between 1 and 65535; if it is not, stop and ask for a valid port.
2. Check for an existing Sloperator server. A Sloperator server is a process whose
   command line contains `playground/server.py`; confirm candidates with
   `pgrep -af 'playground/server.py'` and `ps -p <pid> -o args=`. Do not confuse
   unrelated listeners with the playground.
   - If a Sloperator server is already listening on the chosen port, report that it
     is running at `http://localhost:<port>` and stop without starting another.
   - If one is running on a different port, report that port and ask whether to
     reuse it or start a second instance on the chosen port. Do not start a second
     server without an answer.
   - An empty listener list is normal when nothing is running.
3. If no Sloperator server is running, start one in the background from the project
   root with `uv run playground/server.py <port>`, substituting the validated port
   as a literal number. Run it as a background command so it returns immediately,
   and note the process ID.
4. Verify the server is listening, for example with
   `curl -sS -o /dev/null -w '%{http_code}' http://localhost:<port>/` or
   `lsof -nP -iTCP:<port> -sTCP:LISTEN`, then report the URL.

Only use the validated numeric port in shell commands. Do not stop or restart an
existing server unless the user asks.
