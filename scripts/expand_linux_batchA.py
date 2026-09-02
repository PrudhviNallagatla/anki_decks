import csv

batchA = [
    # --- BASH SCRIPTING MASTERY FOR SYSADMINS & DBAS ---
    {
        "Question": "What does `set -euxo pipefail` do at the top of a production Bash script?",
        "Answer": "<b>ANSWER:</b> The 'Bash Unofficial Strict Mode' safety flags.<br><br>• <b>`-e` (errexit):</b> Exit immediately if any command exits with a non-zero error.<br>• <b>`-u` (nounset):</b> Treat unset variables as an error and exit immediately (prevents accidental `rm -rf $DIR/` disasters).<br>• <b>`-x` (xtrace):</b> Prints every command to stdout before executing (great for debugging).<br>• <b>`-o pipefail`:</b> Pipeline fails if ANY command inside the pipe fails, not just the last one.",
        "Topic": "Bash Scripting",
        "Tags": "linux bash scripting safety strict_mode"
    },
    {
        "Question": "What is the difference between `[[ ... ]]` and `[ ... ]` in Bash scripts?",
        "Answer": "<b>ANSWER:</b> Modern Bash enhanced test vs. Legacy POSIX test.<br><br>• <b>`[[ ... ]]`:</b> Modern keyword. Supports regex matching (`=~`), logical `&&` and `||` without escaping, and does NOT perform word splitting or pathname expansion on variables.<br>• <b>`[ ... ]`:</b> Legacy external binary (`/usr/bin/[`). Fails or throws syntax errors if variables contain spaces unless quoted.",
        "Topic": "Bash Scripting",
        "Tags": "linux bash conditionals test syntax"
    },
    {
        "Question": "How do you check if a file exists, a directory exists, or a string is empty in Bash?",
        "Answer": "<b>ANSWER:</b> File and string test operators.<br><br>• <code>[[ -f /path/to/file ]]</code>: True if path exists and is a regular file.<br>• <code>[[ -d /path/to/dir ]]</code>: True if path exists and is a directory.<br>• <code>[[ -z \"$var\" ]]</code>: True if string is empty (zero length).<br>• <code>[[ -n \"$var\" ]]</code>: True if string is not empty.",
        "Topic": "Bash Scripting",
        "Tags": "linux bash conditionals operators test"
    },
    {
        "Question": "How do you loop through files safely in Bash without word-splitting issues on spaces?",
        "Answer": "<b>ANSWER:</b> Use globbing, NEVER `for file in $(ls)`.<br><br><b>The Script:</b><br><code>for file in /var/log/*.log; do <br>    [[ -f \"$file\" ]] || continue <br>    echo \"Processing: $file\" <br>done</code><br>Direct globbing handles spaces, tabs, and newlines safely.",
        "Topic": "Bash Scripting",
        "Tags": "linux bash loops globbing safety"
    },
    {
        "Question": "How do you read a text file line-by-line safely in Bash?",
        "Answer": "<b>ANSWER:</b> Use `while IFS= read -r line; do ... done < file.txt`.<br><br>• `IFS=`: Prevents stripping leading/trailing whitespace.<br>• `-r`: Prevents backslash escapes from being interpreted.<br>• `< file.txt`: Redirects input into the loop.",
        "Topic": "Bash Scripting",
        "Tags": "linux bash read while_loop text"
    },
    {
        "Question": "How do you define and use an array in Bash?",
        "Answer": "<b>ANSWER:</b> Array syntax in modern Bash.<br><br>• <b>Define:</b> <code>servers=(\"db1\" \"db2\" \"db3\")</code><br>• <b>Access first:</b> <code>${servers[0]}</code><br>• <b>Total count:</b> <code>${#servers[@]}</code><br>• <b>Loop over all:</b> <code>for s in \"${servers[@]}\"; do echo \"$s\"; done</code>",
        "Topic": "Bash Scripting",
        "Tags": "linux bash arrays syntax"
    },
    {
        "Question": "What is a `trap` in Bash and how do you ensure temporary files are deleted on script exit?",
        "Answer": "<b>ANSWER:</b> Catches signals and script termination events to execute cleanup routines.<br><br><b>The Script:</b><br><code>TMP_FILE=$(mktemp) <br>trap 'rm -f \"$TMP_FILE\"; echo \"Cleaned up temp files\";' EXIT INT TERM</code><br>Guarantees `TMP_FILE` is deleted even if the script crashes or user presses `Ctrl+C`.",
        "Topic": "Bash Scripting",
        "Tags": "linux bash trap cleanup signal safety"
    },
    {
        "Question": "Explain the special arguments `$#`, `$0`, `$1`, and `$@` in Bash scripts.",
        "Answer": "<b>ANSWER:</b> Positional script parameters:<br><br>• <b>`$0`:</b> Name/path of the executing script itself.<br>• <b>`$1`, `$2`:</b> First and second arguments passed to the script.<br>• <b>`$#`:</b> Total number of arguments passed.<br>• <b>`$@`:</b> All arguments as an array (preserves quotes when used as `\"$@\"`).",
        "Topic": "Bash Scripting",
        "Tags": "linux bash arguments positional parameters"
    },
    {
        "Question": "How do you check if a command (e.g. `psql`) exists on the system inside a Bash script?",
        "Answer": "<b>ANSWER:</b> Use `command -v`.<br><br><b>The Script:</b><br><code>if ! command -v psql &>/dev/null; then <br>    echo \"Error: postgresql-client is not installed!\" >&2 <br>    exit 1 <br>fi</code><br>Portable across all shells (superior to `which`).",
        "Topic": "Bash Scripting",
        "Tags": "linux bash command_v portable verification"
    },
    {
        "Question": "What is a Heredoc (`<<EOF`) in Bash and how do you write multi-line configs to a file?",
        "Answer": "<b>ANSWER:</b> Multi-line string redirection.<br><br><b>The Script:</b><br><code>cat <<EOF > /etc/myapp.conf <br>DB_HOST=127.0.0.1 <br>DB_PORT=5432 <br>DB_NAME=production <br>EOF</code>",
        "Topic": "Bash Scripting",
        "Tags": "linux bash heredoc multiline configuration"
    },
    {
        "Question": "How do you reliably obtain the directory of the currently running Bash script?",
        "Answer": "<b>ANSWER:</b> Use `BASH_SOURCE[0]`.<br><br><b>The Script:</b><br><code>SCRIPT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" >/dev/null 2>&1 && pwd)\"</code><br>Guarantees you get the true directory of the script regardless of what working directory you executed it from.",
        "Topic": "Bash Scripting",
        "Tags": "linux bash script_dir portable path"
    },
    {
        "Question": "How do you execute commands in the background inside a loop and wait for all of them to finish?",
        "Answer": "<b>ANSWER:</b> Append `&` to background jobs, and call `wait` at the end.<br><br><b>The Script:</b><br><code>for host in s1 s2 s3; do <br>    ssh \"$host\" \"backup.sh\" & <br>done <br>wait <br>echo \"All 3 remote backups finished!\"</code>",
        "Topic": "Bash Scripting",
        "Tags": "linux bash parallel wait background concurrency"
    },
    {
        "Question": "How do you prevent a script from exiting under `set -e` when a command is expected to fail?",
        "Answer": "<b>ANSWER:</b> Append `|| true` to the command.<br><br><b>The Script:</b><br><code>grep \"FATAL\" app.log || true</code><br>If `grep` finds no matches, it returns exit code 1; `|| true` forces the combined statement to return 0, preventing `set -e` from aborting the script.",
        "Topic": "Bash Scripting",
        "Tags": "linux bash set_e errexit safety"
    },
    {
        "Question": "What is a Subshell in Bash and how do parentheses `( ... )` isolate directory changes?",
        "Answer": "<b>ANSWER:</b> Spawns a child shell environment.<br><br><b>The Script:</b><br><code>(cd /tmp && make build)</code><br>Changes into `/tmp` and executes `make build` inside the child process. When it finishes, your parent shell remains in your original directory with zero path pollution.",
        "Topic": "Bash Scripting",
        "Tags": "linux bash subshell parentheses isolation"
    },

    # --- ADVANCED NETWORKING, SSH TUNNELS & REMOTE DIAGNOSTICS ---
    {
        "Question": "How do you set up an SSH Local Port Forward (`ssh -L`) to connect to a remote private database?",
        "Answer": "<b>ANSWER:</b> `ssh -L local_port:dest_host:dest_port user@jumpbox`<br><br><b>The Command:</b><br><code>ssh -L 5433:10.0.1.50:5432 ubuntu@bastion.company.com -N</code><br>Forwards your laptop's `localhost:5433` directly into the private database at `10.0.1.50:5432` through an encrypted SSH tunnel!",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh tunneling local_port_forwarding security"
    },
    {
        "Question": "How do you set up an SSH Remote Reverse Tunnel (`ssh -R`) to expose a local web app to the internet?",
        "Answer": "<b>ANSWER:</b> `ssh -R remote_port:local_host:local_port user@remote_server`<br><br><b>The Command:</b><br><code>ssh -R 8080:localhost:3000 user@cloud-server.com -N</code><br>Traffic arriving on port 8080 of `cloud-server.com` is tunneled reverse into your local laptop's `localhost:3000`.",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh tunneling reverse_tunnel remote"
    },
    {
        "Question": "How do you create an instant SOCKS5 proxy using SSH Dynamic Port Forwarding (`ssh -D`)?",
        "Answer": "<b>ANSWER:</b> `ssh -D 1080 user@remote_server -N`<br><br>Opens a local SOCKS5 proxy on `localhost:1080`. Configure your browser to use `socks5://127.0.0.1:1080` to route all internet browsing securely through the remote server's IP address.",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh socks proxy dynamic_tunneling"
    },
    {
        "Question": "How do you SSH through a Bastion / Jump Host in a single command?",
        "Answer": "<b>ANSWER:</b> Use the `-J` (ProxyJump) flag.<br><br><b>The Command:</b><br><code>ssh -J jumpuser@bastion.company.com dbuser@10.0.1.50</code><br>Or in `~/.ssh/config`:<br><code>Host prod-db <br>    HostName 10.0.1.50 <br>    ProxyJump jumpuser@bastion.company.com</code>",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh jump_host bastion proxyjump"
    },
    {
        "Question": "How do you escape an unresponsive, completely frozen SSH terminal session?",
        "Answer": "<b>ANSWER:</b> Press `Enter`, then type `~.` (tilde followed by period).<br><br>The SSH client escape character sequence. Immediately drops the local SSH client connection and returns you to your local prompt without waiting for TCP keepalive timeouts.",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh escape frozen session"
    },
    {
        "Question": "How do you send a JSON POST request with an Authorization Bearer token using `curl`?",
        "Answer": "<b>ANSWER:</b> Combine `-X POST`, `-H`, and `-d`.<br><br><b>The Command:</b><br><code>curl -X POST https://api.example.com/v1/deploy <br>     -H \"Authorization: Bearer my_secret_token\" <br>     -H \"Content-Type: application/json\" <br>     -d '{\"env\": \"production\", \"version\": \"2.4.0\"}'</code>",
        "Topic": "Networking & Ports",
        "Tags": "linux curl json post api auth"
    },
    {
        "Question": "How do you benchmark network throughput between two Linux servers using `iperf3`?",
        "Answer": "<b>ANSWER:</b> Run `iperf3` in server mode on one machine and client mode on the other.<br><br>• <b>Server:</b> <code>iperf3 -s</code><br>• <b>Client:</b> <code>iperf3 -c 192.168.1.50 -t 10</code><br>Measures exact TCP/UDP throughput (e.g. 9.42 Gbits/sec), latency jitter, and packet loss.",
        "Topic": "Networking & Ports",
        "Tags": "linux networking iperf3 throughput bandwidth benchmarking"
    },
    {
        "Question": "How do you add a persistent static network route in modern Linux?",
        "Answer": "<b>ANSWER:</b> `sudo ip route add <network> via <gateway> dev <interface>`<br><br><b>Example:</b><br><code>sudo ip route add 10.50.0.0/16 via 192.168.1.254 dev eth0</code><br>Routes all traffic for the `10.50.0.0/16` subnet out through the internal router gateway.",
        "Topic": "Networking & Ports",
        "Tags": "linux networking ip_route static_route gateway"
    },
    {
        "Question": "How do you test Path MTU size to diagnose dropped network packets?",
        "Answer": "<b>ANSWER:</b> Use `ping` with the Don't Fragment (`-M do`) flag.<br><br><b>The Command:</b><br><code>ping -M do -s 1472 8.8.8.8</code><br>Sends a 1500-byte packet (1472 data + 28 header). If the network path has a smaller MTU (e.g. VPN or PPPoE), it returns: `Frag needed and DF set`.",
        "Topic": "Networking & Ports",
        "Tags": "linux networking ping mtu fragmentation"
    },
    {
        "Question": "How do you inspect HTTP plain-text traffic live over the wire using `tcpdump`?",
        "Answer": "<b>ANSWER:</b> Use `tcpdump -A -s 0 'tcp port 80'`.<br><br>• `-A`: Prints each packet payload in ASCII text.<br>• `-s 0`: Sniff full packet length (do not truncate).<br>Instantly reveals HTTP headers, query parameters, and raw API responses.",
        "Topic": "Networking & Ports",
        "Tags": "linux networking tcpdump ascii packets sniffing"
    }
]

with open('decks/linux_mastery_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batchA:
        writer.writerow(card)

print(f"Linux Batch A complete: appended {len(batchA)} cards.")
