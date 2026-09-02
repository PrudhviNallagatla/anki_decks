import csv

batch3_cards = [
    # --- SHELL TRICKS, SCRIPTING & SHORTCUTS ---
    {
        "Question": "What does `sudo !!` do in the Linux bash terminal?",
        "Answer": "<b>ANSWER:</b> Re-runs the immediately previous command with `sudo`.<br><br><b>Example:</b> You type `systemctl restart nginx` and get `Permission denied`. Typing `sudo !!` executes `sudo systemctl restart nginx` instantly without re-typing.",
        "Topic": "Shell Productivity",
        "Tags": "linux bash shortcuts sudo productivity"
    },
    {
        "Question": "What does `!$` do in bash?",
        "Answer": "<b>ANSWER:</b> Expands to the LAST argument of the previous command.<br><br><b>Example:</b><br><code>mkdir /opt/very/long/nested/directory/path</code><br><code>cd !$</code><br>Immediately changes directory into that path without copying and pasting.",
        "Topic": "Shell Productivity",
        "Tags": "linux bash shortcuts arguments productivity"
    },
    {
        "Question": "What is the `tee` command and why is it used with `sudo`?",
        "Answer": "<b>ANSWER:</b> Reads from standard input and writes simultaneously to standard output AND files.<br><br><b>The Problem:</b> <code>sudo echo \"1\" > /proc/sys/vm/swappiness</code> fails with `Permission denied` because redirection `>` is handled by your unprivileged shell.<br><b>The Fix:</b> <code>echo \"1\" | sudo tee /proc/sys/vm/swappiness</code>.",
        "Topic": "Shell Streams",
        "Tags": "linux tee sudo redirection permissions"
    },
    {
        "Question": "What is the difference between `command1 && command2` and `command1 || command2`?",
        "Answer": "<b>ANSWER:</b> Conditional execution based on exit code ($?).<br><br>• <b>`&&` (AND):</b> Runs `command2` ONLY if `command1` succeeds (returns exit code 0).<br>• <b>`||` (OR):</b> Runs `command2` ONLY if `command1` fails (returns non-zero error code).",
        "Topic": "Shell Productivity",
        "Tags": "linux bash conditional logic operators"
    },
    {
        "Question": "How do you check the Exit Status Code of the last executed command?",
        "Answer": "<b>ANSWER:</b> Inspect the `$?` variable.<br><br><b>The Command:</b><br><code>echo $?</code><br>• `0`: Success / clean exit.<br>• Non-zero (1–255): Error, failure, or signal termination.",
        "Topic": "Shell Productivity",
        "Tags": "linux bash exit_code scripting"
    },
    {
        "Question": "How do you instantly truncate a 50GB log file to 0 bytes without deleting it or dropping open file handles?",
        "Answer": "<b>ANSWER:</b> Use `truncate -s 0 filename` or `: > filename`.<br><br><b>The Command:</b><br><code>truncate -s 0 /var/log/huge_app.log</code><br>Instantly reclaims 50GB of disk space while allowing running applications to continue logging without restart.",
        "Topic": "Storage & Disks",
        "Tags": "linux truncate disk_space logs maintenance"
    },
    {
        "Question": "What is the `watch` command in Linux?",
        "Answer": "<b>ANSWER:</b> Executes a program periodically and displays the output fullscreen.<br><br><b>Example:</b><br><code>watch -n 2 -d 'free -m'</code><br>Runs `free -m` every 2 seconds, highlighting differences (`-d`) live as memory changes.",
        "Topic": "Performance Triage",
        "Tags": "linux watch monitoring real_time"
    },
    {
        "Question": "What does `strace` do and when is it a sysadmin's ultimate debugging weapon?",
        "Answer": "<b>ANSWER:</b> Traces every system call (`syscall`) and signal received by a process.<br><br><b>Usage:</b><br><code>sudo strace -p <PID></code><br>When a process is frozen or hung at 100% CPU, `strace` reveals the exact file it is trying to open, socket it is waiting on, or memory lock it is stuck acquiring.",
        "Topic": "Performance Triage",
        "Tags": "linux strace debugging syscalls troubleshooting"
    },

    # --- SECURITY, ACCESS & IDENTITY ---
    {
        "Question": "How do you temporarily lock a user account to prevent login without deleting it?",
        "Answer": "<b>ANSWER:</b> Use `passwd -l username`.<br><br>Places an exclamation mark (`!`) in front of the encrypted password hash in `/etc/shadow`, disabling all password-based logins. Unlock with: `passwd -u username`.",
        "Topic": "User Administration",
        "Tags": "linux security passwd lock user"
    },
    {
        "Question": "What are the 3 modes of SELinux and how do you check the current mode?",
        "Answer": "<b>ANSWER:</b> Enforcing, Permissive, and Disabled.<br><br>• <b>Enforcing:</b> Policies strictly enforced; unauthorized actions blocked and logged.<br>• <b>Permissive:</b> Warnings logged, but actions are NOT blocked (ideal for debugging).<br>• <b>Check mode:</b> `getenforce`<br>• <b>Temporarily switch:</b> `sudo setenforce 0` (Permissive) or `1` (Enforcing).",
        "Topic": "Permissions & Security",
        "Tags": "linux selinux security enforcing permissive"
    },
    {
        "Question": "What is `AppArmor` and how does it compare to `SELinux`?",
        "Answer": "<b>ANSWER:</b> Path-based mandatory access control (MAC) default on Ubuntu/Debian.<br><br>While RHEL uses SELinux (label-based), Ubuntu uses AppArmor (file path-based profiles) to restrict what files and network sockets individual binaries can access. Check with: `sudo aa-status`.",
        "Topic": "Permissions & Security",
        "Tags": "linux apparmor security ubuntu debian"
    },

    # --- NETWORKING & HARDWARE ---
    {
        "Question": "How do you check the physical link speed (e.g. 1Gbps vs 10Gbps) of a network card?",
        "Answer": "<b>ANSWER:</b> Use `ethtool`.<br><br><b>The Command:</b><br><code>sudo ethtool eth0</code><br>Displays physical transceiver speed (`Speed: 10000Mb/s`), Duplex mode (`Full`), and whether the physical cable link is detected (`Link detected: yes`).",
        "Topic": "Networking & Ports",
        "Tags": "linux networking ethtool hardware speed"
    },
    {
        "Question": "What command displays the kernel ARP cache (IP to MAC address mapping)?",
        "Answer": "<b>ANSWER:</b> `ip neigh`<br><br><b>Usage:</b><br><code>ip neigh show</code><br>(Modern replacement for legacy `arp -a`). Shows neighboring devices on the local subnet and their hardware MAC addresses.",
        "Topic": "Networking & Ports",
        "Tags": "linux networking ip arp mac"
    },
    {
        "Question": "What does `nameserver 127.0.0.53` in `/etc/resolv.conf` mean on modern Ubuntu?",
        "Answer": "<b>ANSWER:</b> The system is using `systemd-resolved` as a local caching DNS stub resolver.<br><br>Actual upstream DNS servers are configured through netplan or systemd-resolved, not directly inside `/etc/resolv.conf`. Inspect true upstream DNS with: <code>resolvectl status</code>.",
        "Topic": "Networking & Ports",
        "Tags": "linux dns systemd_resolved resolv_conf"
    },

    # --- ADVANCED STORAGE & KERNEL TUNING ---
    {
        "Question": "Why must you NEVER run `fsck` on a currently mounted filesystem?",
        "Answer": "<b>ANSWER:</b> It can cause catastrophic filesystem corruption.<br><br>`fsck` assumes it has exclusive direct access to block structures. If the running kernel is simultaneously writing data to the mounted filesystem, `fsck` will misinterpret active writes as corruption and destroy valid data. Always unmount first or boot into single-user rescue mode.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage fsck disk corruption caution"
    },
    {
        "Question": "What is Transparent Huge Pages (THP) and why do databases require disabling it?",
        "Answer": "<b>ANSWER:</b> Automatic OS aggregation of 4KB memory pages into 2MB huge pages.<br><br>While great for compute algorithms, THP causes high memory allocation latency and CPU lockups for databases (Postgres, Oracle, Redis).<br><b>Disable command:</b><br><code>echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled</code>",
        "Topic": "Kernel Tuning",
        "Tags": "linux kernel thp memory database tuning"
    },
    {
        "Question": "What is `/dev/shm` in Linux?",
        "Answer": "<b>ANSWER:</b> A shared memory RAM-backed virtual filesystem (`tmpfs`).<br><br>Any file created in `/dev/shm` resides in physical RAM rather than on disk. Used for ultra-fast inter-process communication (IPC) and high-speed temporary file caching.",
        "Topic": "Storage & Disks",
        "Tags": "linux memory dev_shm tmpfs ipc"
    },
    {
        "Question": "How does `logrotate` prevent logs from filling the server hard drive?",
        "Answer": "<b>ANSWER:</b> Automatically rotates, compresses, and purges old log files based on schedule or size.<br><br>Configured in `/etc/logrotate.conf` and `/etc/logrotate.d/`. Can compress archives with gzip (`compress`), keep a fixed number of days (`rotate 14`), and signal daemons to start writing to a fresh file.",
        "Topic": "Logs & Diagnostics",
        "Tags": "linux logrotate logs maintenance storage"
    },
    {
        "Question": "What does `update-alternatives` do on Debian/Ubuntu/RHEL?",
        "Answer": "<b>ANSWER:</b> Manages default system versions when multiple versions of software are installed.<br><br><b>Example:</b> If both Java 11 and Java 21 are installed, run:<br><code>sudo update-alternatives --config java</code><br>Displays an interactive menu to switch the system-wide default `/usr/bin/java` symlink.",
        "Topic": "Package Management",
        "Tags": "linux package_management update_alternatives symlinks"
    }
]

# Append Batch 3 to decks/linux_mastery_deck.csv
with open('decks/linux_mastery_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batch3_cards:
        writer.writerow(card)

print(f"Batch 3 complete: appended {len(batch3_cards)} cards.")
