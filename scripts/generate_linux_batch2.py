import csv

batch2_cards = [
    # --- MODULE 4: SYSTEMD, SERVICES, LOGS & CRONTAB ---
    {
        "Question": "What does `systemctl daemon-reload` do and when is it required?",
        "Answer": "<b>ANSWER:</b> Reloads systemd manager configuration and scans for new or modified unit files.<br><br><b>When required:</b> Any time you create or edit a `.service`, `.socket`, or `.timer` file in `/etc/systemd/system/`. Without running this, systemd will continue using the old in-memory configuration.",
        "Topic": "Systemd & Services",
        "Tags": "linux systemd systemctl daemon_reload"
    },
    {
        "Question": "What does `systemctl enable --now service_name` do?",
        "Answer": "<b>ANSWER:</b> Enables the service to start automatically on boot AND starts it immediately right now.<br><br>Combines `systemctl enable` (creates symlink in target directory) and `systemctl start` into a single atomic command.",
        "Topic": "Systemd & Services",
        "Tags": "linux systemd systemctl enable services"
    },
    {
        "Question": "What is the difference between `systemctl restart` and `systemctl reload`?",
        "Answer": "<b>ANSWER:</b> Full process restart vs. In-flight configuration reload.<br><br>• <b>`restart`:</b> Kills the running process and spawns a new one (causes brief service downtime).<br>• <b>`reload`:</b> Sends SIGHUP to the running process to re-read its configuration files with <b>zero downtime</b> and zero dropped client connections.",
        "Topic": "Systemd & Services",
        "Tags": "linux systemd systemctl restart reload zero_downtime"
    },
    {
        "Question": "What are the 3 primary sections in a standard Systemd Unit file (`.service`)?",
        "Answer": "<b>ANSWER:</b> `[Unit]`, `[Service]`, and `[Install]`.<br><br>• <b>`[Unit]`:</b> Metadata and dependencies (e.g. `Description=My App`, `After=network.target`).<br>• <b>`[Service]`:</b> Execution instructions (`ExecStart=/usr/bin/app`, `User=appuser`, `Restart=always`).<br>• <b>`[Install]`:</b> Boot target triggers (`WantedBy=multi-user.target`).",
        "Topic": "Systemd & Services",
        "Tags": "linux systemd unit_file service configuration"
    },
    {
        "Question": "How do you configure a Systemd service to automatically restart if it crashes?",
        "Answer": "<b>ANSWER:</b> Set `Restart=always` (or `Restart=on-failure`) and `RestartSec=5` in the `[Service]` section.<br><br><b>Example:</b><br><code>[Service] <br>ExecStart=/usr/bin/python3 /opt/app.py <br>Restart=always <br>RestartSec=5</code><br>Systemd will automatically revive the process 5 seconds after any unexpected exit.",
        "Topic": "Systemd & Services",
        "Tags": "linux systemd restart auto_restart"
    },
    {
        "Question": "How do you stream live logs for a specific service using `journalctl`?",
        "Answer": "<b>ANSWER:</b> `journalctl -u service_name -f`<br><br>• `-u`: Filter by systemd unit name.<br>• `-f`: Follow active log output in real-time (equivalent to `tail -f`).<br>• Add `-n 100` to display the last 100 lines before following.",
        "Topic": "Logs & Diagnostics",
        "Tags": "linux journalctl logs systemd follow"
    },
    {
        "Question": "How do you query system logs from the last 1 hour filtered by error level in `journalctl`?",
        "Answer": "<b>ANSWER:</b> Use `--since` and `-p err`.<br><br><b>The Command:</b><br><code>journalctl -u myapp --since \"1 hour ago\" -p err -e</code><br>• `--since \"1 hour ago\"`: Time window.<br>• `-p err`: Shows only errors, critical, and alert messages.<br>• `-e`: Jump to end of pager.",
        "Topic": "Logs & Diagnostics",
        "Tags": "linux journalctl logs errors time"
    },
    {
        "Question": "How do you reclaim disk space from bloated `journald` system logs?",
        "Answer": "<b>ANSWER:</b> Use `journalctl --vacuum-time` or `--vacuum-size`.<br><br>• <code>journalctl --vacuum-time=7d</code>: Deletes archived journal files older than 7 days.<br>• <code>journalctl --vacuum-size=1G</code>: Shrinks journal logs until total size is under 1 Gigabyte.",
        "Topic": "Logs & Diagnostics",
        "Tags": "linux journalctl vacuum logs disk_space"
    },
    {
        "Question": "Explain the 5 fields of a standard `crontab` schedule.",
        "Answer": "<b>ANSWER:</b> `* * * * *`<br><br>1. <b>Minute:</b> 0–59<br>2. <b>Hour:</b> 0–23<br>3. <b>Day of Month:</b> 1–31<br>4. <b>Month:</b> 1–12<br>5. <b>Day of Week:</b> 0–7 (0 or 7 = Sunday)",
        "Topic": "Cron & Automation",
        "Tags": "linux cron crontab schedule automation"
    },
    {
        "Question": "Write a Crontab entry to run a script every 5 minutes.",
        "Answer": "<b>ANSWER:</b> `*/5 * * * *`<br><br><b>Example:</b><br><code>*/5 * * * * /usr/bin/python3 /opt/check_health.py >> /var/log/health.log 2>&1</code>",
        "Topic": "Cron & Automation",
        "Tags": "linux cron crontab schedule syntax"
    },
    {
        "Question": "Write a Crontab entry to run a backup every Monday at 3:30 AM.",
        "Answer": "<b>ANSWER:</b> `30 3 * * 1`<br><br><b>Example:</b><br><code>30 3 * * 1 /usr/local/bin/backup.sh > /dev/null 2>&1</code>",
        "Topic": "Cron & Automation",
        "Tags": "linux cron crontab schedule backup"
    },
    {
        "Question": "Why do scripts that work in your interactive terminal often silently fail when run via Cron?",
        "Answer": "<b>ANSWER:</b> Cron runs in an extremely stripped-down, non-interactive environment with a minimal `$PATH`.<br><br>Commands like `python3`, `psql`, or `node` may not be in cron's `$PATH`.<br><b>Rule:</b> ALWAYS use full absolute paths in cron scripts (e.g. `/usr/bin/python3` instead of `python3`), and explicitly set environment variables.",
        "Topic": "Cron & Automation",
        "Tags": "linux cron path environment gotcha"
    },
    {
        "Question": "What is the `@reboot` directive in Crontab?",
        "Answer": "<b>ANSWER:</b> Runs the specified command once immediately upon system boot.<br><br><b>Example:</b><br><code>@reboot /opt/scripts/init_tunnels.sh</code><br>Convenient lightweight alternative to creating a full systemd service for simple reboot tasks.",
        "Topic": "Cron & Automation",
        "Tags": "linux cron reboot automation"
    },

    # --- MODULE 5: NETWORKING, PORTS, DNS & FIREWALLS ---
    {
        "Question": "Why is `ss -tulnp` the modern replacement for `netstat` to inspect listening ports?",
        "Answer": "<b>ANSWER:</b> Directly queries kernel socket tables, making it 10x faster and standard on modern Linux.<br><br><b>The Flags:</b><br>• `-t`: TCP sockets<br>• `-u`: UDP sockets<br>• `-l`: Listening sockets only<br>• `-n`: Numeric IP/port (skips slow DNS resolution)<br>• `-p`: Shows Process Name and PID holding the port (requires sudo)",
        "Topic": "Networking & Ports",
        "Tags": "linux networking ss ports sockets netstat"
    },
    {
        "Question": "How do you test if a remote database port (e.g. 5432) is open and reachable without installing a database client?",
        "Answer": "<b>ANSWER:</b> Use `nc` (Netcat).<br><br><b>The Command:</b><br><code>nc -zv 192.168.1.50 5432</code><br>• `-z`: Zero-I/O scan mode (scans without sending data).<br>• `-v`: Verbose.<br>Outputs `succeeded!` if the port is open and firewall accepts connection.",
        "Topic": "Networking & Ports",
        "Tags": "linux networking netcat nc ports testing"
    },
    {
        "Question": "How do you fetch only the HTTP response headers of a web endpoint using `curl`?",
        "Answer": "<b>ANSWER:</b> `curl -I https://api.example.com`<br><br>Sends an HTTP `HEAD` request instead of downloading the body. Instantly displays HTTP status code (`200 OK`, `404`, `502`), Content-Type, and server headers.",
        "Topic": "Networking & Ports",
        "Tags": "linux curl http networking headers"
    },
    {
        "Question": "What is `mtr` (My Traceroute) and why is it superior to standard `traceroute`?",
        "Answer": "<b>ANSWER:</b> Combines `ping` and `traceroute` into a real-time, interactive diagnostic tool.<br><br>Continuously pings every network hop between you and the destination server, updating packet loss percentage and latency jitter per hop live. Pinpoints the exact faulty router causing network drops.",
        "Topic": "Networking & Ports",
        "Tags": "linux networking mtr traceroute latency"
    },
    {
        "Question": "What modern commands replace `ifconfig` and `route -n` in Linux?",
        "Answer": "<b>ANSWER:</b> The `ip` command suite.<br><br>• Replace `ifconfig`: <code>ip a</code> (or `ip addr show`)<br>• Replace `route -n`: <code>ip route</code><br>• Show link stats: <code>ip -s link</code>",
        "Topic": "Networking & Ports",
        "Tags": "linux networking ip ifconfig route modern"
    },
    {
        "Question": "What is the difference between `/etc/hosts` and `/etc/resolv.conf`?",
        "Answer": "<b>ANSWER:</b> Static local IP overrides vs. Upstream DNS nameserver configuration.<br><br>• <b>`/etc/hosts`:</b> Local hardcoded hostname-to-IP mappings (always evaluated first by default).<br>• <b>`/etc/resolv.conf`:</b> Defines external DNS nameservers (e.g. `nameserver 8.8.8.8`) used to resolve public domain names.",
        "Topic": "Networking & Ports",
        "Tags": "linux dns hosts resolv_conf networking"
    },
    {
        "Question": "How do you query a domain's IP address directly from a specific DNS server using `dig`?",
        "Answer": "<b>ANSWER:</b> Use `dig @dns_server domain`.<br><br><b>Example:</b><br><code>dig @8.8.8.8 +short mydomain.com</code><br>Queries Google DNS directly, bypassing local caches to verify if global DNS propagation has completed.",
        "Topic": "Networking & Ports",
        "Tags": "linux dns dig networking query"
    },
    {
        "Question": "How do you capture live network packets on port 5432 using `tcpdump`?",
        "Answer": "<b>ANSWER:</b> Use `tcpdump -i any -n port 5432 -c 10`.<br><br>• `-i any`: Listen on all network interfaces.<br>• `-n`: Numeric IP/port display (no DNS lookups).<br>• `port 5432`: Filter traffic.<br>• `-c 10`: Capture 10 packets and stop.",
        "Topic": "Networking & Ports",
        "Tags": "linux networking tcpdump packets sniffing"
    },
    {
        "Question": "How do you open port 5432 on Ubuntu/Debian using UFW?",
        "Answer": "<b>ANSWER:</b> Using `ufw allow`.<br><br><b>Commands:</b><br><code>sudo ufw allow 5432/tcp</code><br><code>sudo ufw status verbose</code>",
        "Topic": "Firewalls & Security",
        "Tags": "linux firewall ufw ubuntu debian"
    },
    {
        "Question": "How do you permanently open port 5432 on RHEL / CentOS / Rocky Linux using `firewalld`?",
        "Answer": "<b>ANSWER:</b> Using `firewall-cmd` with `--permanent`.<br><br><b>Commands:</b><br><code>sudo firewall-cmd --add-port=5432/tcp --permanent</code><br><code>sudo firewall-cmd --reload</code><br>The `--reload` flag applies permanent changes to the active runtime firewall.",
        "Topic": "Firewalls & Security",
        "Tags": "linux firewall firewalld rhel centos rocky"
    },

    # --- MODULE 6: STORAGE, FILESYSTEMS, LVM & KERNEL TUNING ---
    {
        "Question": "What command displays all block storage devices and their filesystem types in a tree format?",
        "Answer": "<b>ANSWER:</b> `lsblk -f`<br><br>Displays disk drives (`sda`, `nvme0n1`), partitions, filesystem formats (`ext4`, `xfs`), UUIDs, and active mount points in an intuitive hierarchy.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage lsblk disks partitions"
    },
    {
        "Question": "What command reveals the unique UUID of all disk partitions on Linux?",
        "Answer": "<b>ANSWER:</b> `blkid`<br><br><b>Usage:</b><br><code>sudo blkid /dev/sdb1</code><br>Extracts the Universally Unique Identifier (`UUID=\"...\"`) required for safe, persistent disk mounting in `/etc/fstab`.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage blkid uuid fstab"
    },
    {
        "Question": "What is the difference between `fdisk` and `gdisk` / `parted`?",
        "Answer": "<b>ANSWER:</b> MBR partition tables vs. Modern GPT partition tables.<br><br>• <b>`fdisk`:</b> Legacy MBR partition tables. Limited to disks smaller than 2 Terabytes and maximum 4 primary partitions.<br>• <b>`gdisk` / `parted`:</b> Modern GPT (GUID Partition Table) standard. Supports disks larger than 2TB (exabytes) and virtually unlimited partitions.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage partitioning fdisk gdisk parted"
    },
    {
        "Question": "Explain the 6 fields of an entry in `/etc/fstab`.",
        "Answer": "<b>ANSWER:</b> `UUID=/dev/disk /mountpoint fstype options dump pass`<br><br>1. <b>Device:</b> `UUID=\"...\"`<br>2. <b>Mount Point:</b> `/data`<br>3. <b>Filesystem:</b> `ext4` or `xfs`<br>4. <b>Options:</b> `defaults,noatime`<br>5. <b>Dump:</b> `0` (backup flag)<br>6. <b>Pass:</b> `2` (fsck check order at boot; `1` for root, `0` to disable)",
        "Topic": "Storage & Disks",
        "Tags": "linux storage fstab mounting configuration"
    },
    {
        "Question": "Why should high-throughput database storage mounts use the `noatime` option in `/etc/fstab`?",
        "Answer": "<b>ANSWER:</b> Disables updating the access timestamp on every single read operation.<br><br>By default, Linux writes to disk every time a file is read to update `atime`. For databases reading millions of data blocks, `noatime` eliminates up to 30% of unnecessary disk write I/O.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage fstab noatime performance"
    },
    {
        "Question": "How do you safely test an edited `/etc/fstab` file without rebooting the server?",
        "Answer": "<b>ANSWER:</b> Run `mount -a`.<br><br>Attempts to mount all filesystems specified in `/etc/fstab`. If there is a syntax error or non-existent UUID, it prints an error immediately, preventing the server from hanging unbootable on the next reboot.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage fstab mount_a safety"
    },
    {
        "Question": "Explain the 3-Tier Architecture of LVM (Logical Volume Manager).",
        "Answer": "<b>ANSWER:</b> Physical Volume (PV) -> Volume Group (VG) -> Logical Volume (LV).<br><br>1. <b>PV (`pvcreate /dev/sdb`):</b> Raw physical hard drives or partitions.<br>2. <b>VG (`vgcreate datavg /dev/sdb`):</b> Pools multiple PVs into a single storage pool.<br>3. <b>LV (`lvcreate -L 100G datavg`):</b> Slices the VG into virtual partitions formatted and mounted like regular disks.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage lvm pv vg lv architecture"
    },
    {
        "Question": "How do you dynamically expand an LVM volume and resize its filesystem on the fly with zero downtime?",
        "Answer": "<b>ANSWER:</b> Use `lvextend` with the `-r` flag.<br><br><b>The Command:</b><br><code>sudo lvextend -L +50G /dev/datavg/datalv -r</code><br>• `-L +50G`: Expands the logical volume by 50 Gigabytes.<br>• `-r` (resizefs): Automatically resizes the underlying `ext4` or `xfs` filesystem in the same step while the system is live and mounted.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage lvm lvextend resize zero_downtime"
    },
    {
        "Question": "What does `vm.swappiness` control and what should it be set to on database servers?",
        "Answer": "<b>ANSWER:</b> The kernel's tendency to swap memory pages to disk (scale 0 to 100).<br><br>• Default is `60` (frequent swapping).<br>• On database servers (Postgres, Oracle, MySQL), set to <b>`10` (or `1`)</b> in `/etc/sysctl.conf`. Forces Linux to retain database cache in physical RAM and avoid catastrophic disk-swapping lag.",
        "Topic": "Kernel Tuning",
        "Tags": "linux kernel sysctl swappiness memory tuning"
    },
    {
        "Question": "What is `vm.overcommit_memory = 2` and why does it protect production databases?",
        "Answer": "<b>ANSWER:</b> Prevents the kernel from allocating more memory than physically exists.<br><br>• `0` (Default): Heuristic overcommit. Linux promises more RAM than exists; when processes use it, the OOM Killer panics and kills processes.<br>• `2`: Strict refusal. Never allocates beyond `Swap + (overcommit_ratio% * RAM)`. Guarantees database processes are never randomly assassinated by the OOM Killer.",
        "Topic": "Kernel Tuning",
        "Tags": "linux kernel sysctl overcommit_memory oom"
    },
    {
        "Question": "How do you permanently raise the Open Files Limit (`ulimit -n`) for a user on Linux?",
        "Answer": "<b>ANSWER:</b> Edit `/etc/security/limits.conf`.<br><br><b>Add lines:</b><br><code>postgres soft nofile 65536</code><br><code>postgres hard nofile 65536</code><br>Prevents high-concurrency servers from hitting the fatal error: <code>Too many open files</code>.",
        "Topic": "Kernel Tuning",
        "Tags": "linux limits ulimit nofile configuration"
    },
    {
        "Question": "Compare package installation across Debian/Ubuntu, RHEL/Rocky, and Arch Linux.",
        "Answer": "<b>ANSWER:</b> Major package managers:<br><br>• <b>Debian/Ubuntu:</b> `sudo apt update && sudo apt install -y package`<br>• <b>RHEL / Rocky / Fedora:</b> `sudo dnf install -y package` (replaces legacy `yum`)<br>• <b>Arch Linux:</b> `sudo pacman -Syu package`",
        "Topic": "Package Management",
        "Tags": "linux package_management apt dnf yum pacman"
    },
    {
        "Question": "How do you find which installed package owns a specific file on Debian vs. RHEL?",
        "Answer": "<b>ANSWER:</b> Reverse package lookup.<br><br>• <b>Debian/Ubuntu:</b> <code>dpkg -S /usr/bin/curl</code><br>• <b>RHEL / Rocky:</b> <code>rpm -qf /usr/bin/curl</code><br>Reveals the exact package name responsible for installing that binary.",
        "Topic": "Package Management",
        "Tags": "linux package_management dpkg rpm query"
    }
]

# Append Batch 2 to decks/linux_mastery_deck.csv
with open('decks/linux_mastery_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batch2_cards:
        writer.writerow(card)

print(f"Batch 2 complete: appended {len(batch2_cards)} cards.")
