import csv

batch4_cards = [
    {
        "Question": "What is the difference between `which`, `whereis`, and `type -a` in Linux?",
        "Answer": "<b>ANSWER:</b> PATH binary locator vs. Source/manual finder vs. Shell builtin detector.<br><br>• <b>`which cmd`:</b> Returns the first executable binary found in `$PATH`.<br>• <b>`whereis cmd`:</b> Finds binary, source code, and man pages.<br>• <b>`type -a cmd`:</b> Tells you if `cmd` is an alias, a shell builtin (like `cd` or `echo`), or an external disk binary.",
        "Topic": "CLI Navigation",
        "Tags": "linux cli which whereis type builtins"
    },
    {
        "Question": "How do you search through your bash command history interactively?",
        "Answer": "<b>ANSWER:</b> Press `Ctrl + R`.<br><br>Opens the reverse incremental history search prompt: `(reverse-i-search)`. Type a fragment of any previous command (e.g. `docker run`), and press `Ctrl + R` repeatedly to cycle backwards through previous matching commands.",
        "Topic": "Shell Productivity",
        "Tags": "linux bash history ctrl_r productivity"
    },
    {
        "Question": "How do you count the number of lines, words, and bytes in a file?",
        "Answer": "<b>ANSWER:</b> Use `wc` (Word Count).<br><br>• <code>wc -l file.txt</code>: Total lines (essential for checking dataset row counts).<br>• <code>wc -w file.txt</code>: Total words.<br>• <code>wc -c file.txt</code>: Total byte size.",
        "Topic": "Text Processing",
        "Tags": "linux text wc word_count lines"
    },
    {
        "Question": "How do you find the real physical target path of a symbolic link?",
        "Answer": "<b>ANSWER:</b> Use `readlink -f`.<br><br><b>The Command:</b><br><code>readlink -f /usr/bin/java</code><br>Recursively resolves nested symlinks to print the absolute, canonical destination path on disk.",
        "Topic": "File Management",
        "Tags": "linux symlinks readlink files"
    },
    {
        "Question": "How do you securely erase a sensitive file so it cannot be recovered by forensic tools?",
        "Answer": "<b>ANSWER:</b> Use `shred -u`.<br><br><b>The Command:</b><br><code>shred -u -z -n 3 secret_key.pem</code><br>• `-n 3`: Overwrites the file with random patterns 3 times.<br>• `-z`: Final zero-overwrite to hide shredding.<br>• `-u`: Deletes and removes the file after overwriting.",
        "Topic": "Permissions & Security",
        "Tags": "linux security shred secure_delete"
    },
    {
        "Question": "How do you inspect user password expiration and account aging policy?",
        "Answer": "<b>ANSWER:</b> Use `chage -l username`.<br><br><b>Usage:</b><br><code>sudo chage -l appuser</code><br>Displays last password change date, password expiration date, and account expiry date.",
        "Topic": "User Administration",
        "Tags": "linux security chage password user"
    },
    {
        "Question": "How do you check all groups a specific user belongs to?",
        "Answer": "<b>ANSWER:</b> `groups username` or `id -Gn username`<br><br><b>Example:</b><br><code>groups ubuntu</code><br>Outputs: `ubuntu : ubuntu adm dialout cdrom sudo dip plugdev lxd docker`.",
        "Topic": "User Administration",
        "Tags": "linux user groups id administration"
    },
    {
        "Question": "Explain Real, User, and Sys time in the `time` command output.",
        "Answer": "<b>ANSWER:</b> Elapsed wall clock vs. CPU calculation time.<br><br>• <b>Real (Wall Clock):</b> Total elapsed time from start to finish (including waiting on disk I/O and network).<br>• <b>User:</b> CPU time spent executing user-space program code.<br>• <b>Sys:</b> CPU time spent inside kernel system calls.",
        "Topic": "Performance Triage",
        "Tags": "linux time performance cpu profiling"
    },
    {
        "Question": "How do you inspect the exact Linux kernel version and OS architecture?",
        "Answer": "<b>ANSWER:</b> `uname -r` and `uname -m`<br><br>• <code>uname -r</code>: Kernel release version (e.g. `6.5.0-28-generic`).<br>• <code>uname -m</code>: Architecture (e.g. `x86_64` vs `aarch64` / ARM).<br>• <code>uname -a</code>: Full system summary.",
        "Topic": "Kernel Tuning",
        "Tags": "linux kernel uname architecture"
    },
    {
        "Question": "How do you set a server's hostname permanently without rebooting?",
        "Answer": "<b>ANSWER:</b> Use `hostnamectl set-hostname`.<br><br><b>The Command:</b><br><code>sudo hostnamectl set-hostname prod-db-01</code><br>Immediately updates the kernel hostname and persists it to `/etc/hostname`.",
        "Topic": "Systemd & Services",
        "Tags": "linux hostnamectl hostname administration"
    },
    {
        "Question": "How do you check system time, timezone, and NTP synchronization status?",
        "Answer": "<b>ANSWER:</b> `timedatectl`<br><br>Displays local time, UTC time, current timezone, and verifies if `NTP service: active` and `System clock synchronized: yes`.",
        "Topic": "Systemd & Services",
        "Tags": "linux timedatectl ntp time timezone"
    },
    {
        "Question": "How do you check NTP time synchronization sources using Chrony?",
        "Answer": "<b>ANSWER:</b> `chronyc sources -v`<br><br>Displays upstream NTP time servers, stratum levels, and time offset drift in milliseconds.",
        "Topic": "Systemd & Services",
        "Tags": "linux ntp chrony time synchronization"
    },
    {
        "Question": "What is `ncdu` and why is it beloved by Linux sysadmins?",
        "Answer": "<b>ANSWER:</b> NCurses Disk Usage - an interactive visual terminal disk usage explorer.<br><br><b>Usage:</b> <code>ncdu /</code><br>Scans the filesystem and provides an interactive visual browser with arrow-key navigation to identify, browse, and delete giant folders instantly.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage ncdu disk_space interactive"
    },
    {
        "Question": "What is Network Bonding (or Teaming) in Linux?",
        "Answer": "<b>ANSWER:</b> Combining two or more physical network interfaces (e.g. `eth0` and `eth1`) into a single logical interface (`bond0`).<br><br>Provides active-passive high availability (if one network cable is severed, traffic shifts instantly with zero packet loss) or Link Aggregation (802.3ad / LACP) for doubled throughput.",
        "Topic": "Networking & Ports",
        "Tags": "linux networking bonding teaming ha"
    },
    {
        "Question": "What does `/etc/nsswitch.conf` control in Linux?",
        "Answer": "<b>ANSWER:</b> Name Service Switch - controls the lookup order for system databases (hosts, passwords, groups).<br><br><b>Example:</b> `hosts: files dns`<br>Tells Linux to look for hostnames in `/etc/hosts` (`files`) FIRST, and query external DNS servers (`dns`) SECOND.",
        "Topic": "Networking & Ports",
        "Tags": "linux nsswitch dns configuration"
    },
    {
        "Question": "How do you save and restore `iptables` firewall rules permanently?",
        "Answer": "<b>ANSWER:</b> `iptables-save` and `iptables-restore`.<br><br>• <b>Save:</b> <code>sudo iptables-save > /etc/iptables/rules.v4</code><br>• <b>Restore:</b> <code>sudo iptables-restore < /etc/iptables/rules.v4</code><br>(Or install `iptables-persistent` on Debian/Ubuntu).",
        "Topic": "Firewalls & Security",
        "Tags": "linux firewall iptables rules persistence"
    },
    {
        "Question": "How do you inspect why SELinux denied an action on RHEL/Rocky Linux?",
        "Answer": "<b>ANSWER:</b> Use `ausearch` to inspect the audit log.<br><br><b>The Command:</b><br><code>sudo ausearch -m avc -ts recent</code><br>Or pipe into `audit2why`: <code>sudo ausearch -m avc -ts recent | audit2why</code> to get plain-English explanations of which security context blocked the operation.",
        "Topic": "Permissions & Security",
        "Tags": "linux selinux ausearch audit security"
    },
    {
        "Question": "How do you inspect ext4 filesystem parameters like block size and mount count?",
        "Answer": "<b>ANSWER:</b> Use `tune2fs -l /dev/sda1`.<br><br>Displays superblock metadata: block size (4096 bytes), total inode count, free block count, filesystem state (`clean`), and last mount timestamp.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage tune2fs ext4 superblock"
    },
    {
        "Question": "What parameter in `limits.conf` controls the maximum number of processes a user can spawn?",
        "Answer": "<b>ANSWER:</b> `nproc`<br><br><b>Syntax in `/etc/security/limits.conf`:</b><br><code>appuser soft nproc 4096</code><br><code>appuser hard nproc 8192</code><br>Prevents a runaway process or fork bomb from consuming all system PIDs and locking up the operating system.",
        "Topic": "Kernel Tuning",
        "Tags": "linux limits nproc limits_conf security"
    },
    {
        "Question": "How do you bypass SSL certificate verification with `curl` for testing internal endpoints?",
        "Answer": "<b>ANSWER:</b> Use the `-k` (or `--insecure`) flag.<br><br><b>The Command:</b><br><code>curl -k https://internal-service.local</code><br>Allows testing development environments with self-signed SSL certificates without throwing an SSL validation error.",
        "Topic": "Networking & Ports",
        "Tags": "linux curl ssl certificates testing"
    },
    {
        "Question": "How do you set the system-wide UTF-8 character encoding on Linux?",
        "Answer": "<b>ANSWER:</b> `localectl set-locale LANG=en_US.UTF-8`<br><br>Updates `/etc/locale.conf` to guarantee international UTF-8 character support and prevent character corruption across terminal sessions and log outputs.",
        "Topic": "Systemd & Services",
        "Tags": "linux locale localectl encoding utf8"
    }
]

# Append Batch 4 to decks/linux_mastery_deck.csv
with open('decks/linux_mastery_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batch4_cards:
        writer.writerow(card)

print(f"Batch 4 complete: appended {len(batch4_cards)} cards.")
