import csv
import os

batch1_cards = [
    # --- MODULE 1: CLI NAVIGATION, SEARCH & FILE WRANGLING ---
    {
        "Question": "What is the fastest way to switch back to the previous working directory in Linux?",
        "Answer": "<b>ANSWER:</b> `cd -`<br><br><b>Usage:</b><br>Toggles between your current directory and the immediately previous directory, printing the full path on execution. Equivalent to using the `$OLDPWD` environment variable.",
        "Topic": "CLI Navigation",
        "Tags": "linux cli navigation cd basics"
    },
    {
        "Question": "What is the difference between `pushd` and `popd` in Linux?",
        "Answer": "<b>ANSWER:</b> Directory history stack navigation.<br><br>• <code>pushd /var/log</code>: Saves your current directory onto a stack and changes into `/var/log`.<br>• <code>popd</code>: Removes the top directory from the stack and immediately returns you to it. Ideal for shell scripts needing to return to original paths.",
        "Topic": "CLI Navigation",
        "Tags": "linux cli navigation pushd popd"
    },
    {
        "Question": "Why is `ls -ltr` one of the most useful commands for Linux administrators?",
        "Answer": "<b>ANSWER:</b> Sorts files by modification time in reverse order, putting the newest files at the very bottom.<br><br><b>The Flags:</b><br>• `-l`: Long listing format.<br>• `-t`: Sort by modification time.<br>• `-r`: Reverse order.<br>In a busy `/var/log` directory with 500 files, the most recently updated log appears right above your command prompt.",
        "Topic": "File Management",
        "Tags": "linux cli ls file_management"
    },
    {
        "Question": "How do you find all files larger than 100MB anywhere on the system using `find`?",
        "Answer": "<b>ANSWER:</b> Use `find / -size +100M`.<br><br><b>The Command:</b><br><code>find / -type f -size +100M -exec ls -lh {} + 2>/dev/null</code><br>Scans the filesystem for regular files (`-type f`) exceeding 100 Megabytes, suppressing permission denied errors (`2>/dev/null`).",
        "Topic": "File Search",
        "Tags": "linux find search size disk"
    },
    {
        "Question": "What is the difference between `-mtime` and `-mmin` in the `find` command?",
        "Answer": "<b>ANSWER:</b> Days vs. Minutes.<br><br>• <code>find . -mtime -7</code>: Files modified in the last 7 days (24-hour periods).<br>• <code>find . -mmin -60</code>: Files modified in the last 60 minutes.<br>• Negative (`-`): Less than. Positive (`+`): Greater than.",
        "Topic": "File Search",
        "Tags": "linux find mtime mmin timestamps"
    },
    {
        "Question": "What is the difference between `find ... -exec ... {} +` and `find ... -exec ... {} \\;`?",
        "Answer": "<b>ANSWER:</b> Batch execution vs. One execution per file.<br><br>• <b>`{} \\;`:</b> Spawns a brand new process for EVERY single matching file (e.g. running `rm` 10,000 times; very slow).<br>• <b>`{} +`:</b> Batches thousands of files as arguments into a single process execution (e.g. running `rm file1 file2 ...`; 100x faster).",
        "Topic": "File Search",
        "Tags": "linux find exec xargs performance"
    },
    {
        "Question": "How do you safely pass filenames with spaces or newlines into `xargs` without errors?",
        "Answer": "<b>ANSWER:</b> Use NUL (`\\0`) delimiters with `-print0` and `-0`.<br><br><b>The Command:</b><br><code>find . -type f -name \"*.log\" -print0 | xargs -0 rm -f</code><br>Standard `xargs` splits on whitespace. Using `-print0` and `-0` separates arguments by null bytes, preventing accidental deletion of wrong files.",
        "Topic": "File Search",
        "Tags": "linux xargs find print0 spaces"
    },
    {
        "Question": "What are the essential flags for creating and extracting a `tar.gz` archive?",
        "Answer": "<b>ANSWER:</b> `c` (create) vs. `x` (extract) with `zvf`.<br><br>• <b>Create:</b> <code>tar -czvf backup.tar.gz /path/to/data</code><br>• <b>Extract:</b> <code>tar -xzvf backup.tar.gz -C /target/dir</code><br>• <b>Flags:</b> `c`=create, `x`=extract, `z`=gzip, `v`=verbose, `f`=filename.",
        "Topic": "Archiving & Compression",
        "Tags": "linux tar compression gzip"
    },
    {
        "Question": "How do you inspect the contents of a `tar.gz` archive WITHOUT extracting it?",
        "Answer": "<b>ANSWER:</b> Use the `-t` (list) flag.<br><br><b>The Command:</b><br><code>tar -tzvf backup.tar.gz</code><br>Lists all files, permissions, sizes, and timestamps inside the archive without writing anything to disk.",
        "Topic": "Archiving & Compression",
        "Tags": "linux tar list inspection"
    },
    {
        "Question": "Why is `rsync -avzP` the gold standard for copying files locally and over networks?",
        "Answer": "<b>ANSWER:</b> Delta transfers, attribute preservation, and resumable partial transfers.<br><br><b>The Flags:</b><br>• `-a` (Archive): Preserves timestamps, permissions, symlinks, and ownership.<br>• `-v`: Verbose output.<br>• `-z`: Compresses data in transit.<br>• `-P`: Shows progress bar and keeps partial files to resume interrupted transfers.",
        "Topic": "File Transfer",
        "Tags": "linux rsync backup transfer"
    },
    {
        "Question": "What does the `--delete` flag do in `rsync`, and why must you use it carefully?",
        "Answer": "<b>ANSWER:</b> Deletes files from the destination directory if they no longer exist in the source directory.<br><br>Creates an exact mirror. If you point to the wrong source directory, it will permanently erase all files in the destination directory!",
        "Topic": "File Transfer",
        "Tags": "linux rsync delete mirror caution"
    },
    {
        "Question": "What is the difference between `df -h` and `du -sh *`?",
        "Answer": "<b>ANSWER:</b> Filesystem total allocation vs. Specific directory sizes.<br><br>• <code>df -h</code>: Shows overall disk capacity, used space, and free space per mounted filesystem partition.<br>• <code>du -sh * | sort -h</code>: Summarizes human-readable sizes of all subdirectories in current folder, sorted from smallest to largest.",
        "Topic": "Storage & Disks",
        "Tags": "linux storage df du disk_space"
    },
    {
        "Question": "How do you search for text recursively across all files showing line numbers using `grep`?",
        "Answer": "<b>ANSWER:</b> Use `grep -rn \"search_term\" .`<br><br><b>The Flags:</b><br>• `-r` (or `-R`): Recursive search through subdirectories.<br>• `-n`: Displays the exact line number of each match.<br>• `-i`: Case-insensitive match.<br>• `-I`: Ignore binary files.",
        "Topic": "Text Processing",
        "Tags": "linux grep text search"
    },
    {
        "Question": "How do you filter out comments and blank lines from a configuration file in Linux?",
        "Answer": "<b>ANSWER:</b> Use `grep -v` with extended regex.<br><br><b>The Command:</b><br><code>grep -Ev '^(#|$)' /etc/postgresql/postgresql.conf</code><br>• `-v`: Invert match (exclude).<br>• `^#`: Starts with comment `#`.<br>• `^$`: Empty blank line.",
        "Topic": "Text Processing",
        "Tags": "linux grep regex comments filter"
    },
    {
        "Question": "How do you search for an error pattern inside compressed `.gz` log files without extracting them?",
        "Answer": "<b>ANSWER:</b> Use `zgrep`.<br><br><b>The Command:</b><br><code>zgrep -i \"FATAL\" /var/log/nginx/access.log.*.gz</code><br>Decompresses in-memory on the fly and searches directly across archived logs.",
        "Topic": "Text Processing",
        "Tags": "linux zgrep gzip logs"
    },
    {
        "Question": "How do you perform an in-place find and replace across a file using `sed`?",
        "Answer": "<b>ANSWER:</b> Use `sed -i 's/old/new/g' filename`.<br><br>• `-i`: In-place editing (modifies the file directly).<br>• `s`: Substitute.<br>• `g`: Global (replaces all occurrences on each line, not just the first).<br><b>Safe practice:</b> <code>sed -i.bak 's/old/new/g' file</code> creates an automatic backup `file.bak`.",
        "Topic": "Text Processing",
        "Tags": "linux sed regex text replace"
    },
    {
        "Question": "How do you print column 1 and column 3 of `/etc/passwd` using `awk`?",
        "Answer": "<b>ANSWER:</b> Use `awk -F: '{print $1, $3}' /etc/passwd`.<br><br>• `-F:`: Sets field separator to colon (`:`).<br>• `$1`: First field (username).<br>• `$3`: Third field (UID).",
        "Topic": "Text Processing",
        "Tags": "linux awk text columns delimiter"
    },
    {
        "Question": "Why must you always `sort` data before piping it into `uniq`?",
        "Answer": "<b>ANSWER:</b> `uniq` ONLY detects duplicate lines that are adjacent (consecutive).<br><br>If identical lines are on line 1 and line 10, `uniq` will not remove them. Always pipe through `sort` first: <code>sort file.txt | uniq -c</code>.",
        "Topic": "Text Processing",
        "Tags": "linux sort uniq text duplicates"
    },
    {
        "Question": "Explain the 3 Standard I/O Streams in Linux.",
        "Answer": "<b>ANSWER:</b> File descriptors 0, 1, and 2.<br><br>• <b>`stdin` (0):</b> Standard input (keyboard / piped input).<br>• <b>`stdout` (1):</b> Standard output (normal program results).<br>• <b>`stderr` (2):</b> Standard error (error messages and diagnostic alerts).",
        "Topic": "Shell Streams",
        "Tags": "linux streams stdin stdout stderr file_descriptors"
    },
    {
        "Question": "What does `command > output.log 2>&1` mean in Linux?",
        "Answer": "<b>ANSWER:</b> Redirects both `stdout` and `stderr` to the same file.<br><br>• `> output.log`: Redirects standard output (1) to `output.log`.<br>• `2>&1`: Redirects standard error (2) to wherever standard output (1) is currently pointing. In modern bash, `&> output.log` is a shortcut.",
        "Topic": "Shell Streams",
        "Tags": "linux streams redirection stdout stderr"
    },
    {
        "Question": "What is `/dev/null` in Linux?",
        "Answer": "<b>ANSWER:</b> The virtual 'black hole' device that discards all data written to it.<br><br><b>Usage:</b><br><code>command > /dev/null 2>&1</code><br>Runs a command completely silently, discarding all normal output and error messages.",
        "Topic": "Shell Streams",
        "Tags": "linux dev_null redirection silence"
    },
    {
        "Question": "Why is `less +F filename` superior to `tail -f` for monitoring live logs?",
        "Answer": "<b>ANSWER:</b> It allows pausing the live stream and scrolling backwards instantly.<br><br>`tail -f` streams continuously; if an error flies by, you cannot easily scroll up. With `less +F`, you press `Ctrl+C` to pause and search/scroll, and press `Shift+F` to resume live scrolling.",
        "Topic": "File Management",
        "Tags": "linux less tail logs live"
    },

    # --- MODULE 2: PERMISSIONS, USERS, GROUPS & SECURITY ---
    {
        "Question": "Explain the numeric values for Linux file permissions (`rwx`).",
        "Answer": "<b>ANSWER:</b> Read = 4, Write = 2, Execute = 1.<br><br>• <b>7 (`4+2+1`):</b> Read, write, and execute.<br>• <b>6 (`4+2`):</b> Read and write.<br>• <b>5 (`4+1`):</b> Read and execute.<br>• <b>4:</b> Read only.<br>• <b>`755`:</b> Owner=7 (`rwx`), Group=5 (`r-x`), Others=5 (`r-x`).",
        "Topic": "Permissions & Security",
        "Tags": "linux permissions chmod rwx"
    },
    {
        "Question": "What does the Execute (`x`) permission mean on a Directory vs. a File?",
        "Answer": "<b>ANSWER:</b> Traversing (`cd`) into the directory.<br><br>• <b>File:</b> Allows executing the file as a program/script.<br>• <b>Directory:</b> Allows entering (`cd`) into the directory and accessing files inside it. Without `x`, you cannot read or open files inside even if you have read (`r`) permission on the directory!",
        "Topic": "Permissions & Security",
        "Tags": "linux permissions execute directory nuance"
    },
    {
        "Question": "Why can a user delete a read-only file (`chmod 444`) if they have write permission on the directory?",
        "Answer": "<b>ANSWER:</b> Deleting a file modifies the parent directory, not the file itself.<br><br>In Linux, a directory is simply a list mapping filenames to Inodes. Deleting a file removes an entry from the directory list; if the user has write (`w`) permission on the directory, they can delete any file inside it.",
        "Topic": "Permissions & Security",
        "Tags": "linux permissions delete directory inode"
    },
    {
        "Question": "What is the SUID (Set Owner User ID) bit on Linux binaries?",
        "Answer": "<b>ANSWER:</b> Runs the executable with the permissions of the file's OWNER rather than the running user.<br><br><b>Example:</b> `/usr/bin/passwd` is owned by `root` with SUID (`-rwsr-xr-x`). When regular users run it to change their password, it temporarily executes as root to write to `/etc/shadow`. Set with: <code>chmod 4755 binary</code> (or `u+s`).",
        "Topic": "Permissions & Security",
        "Tags": "linux permissions suid security"
    },
    {
        "Question": "What is the SGID (Set Group ID) bit on a Directory?",
        "Answer": "<b>ANSWER:</b> New files created inside the directory inherit the directory's GROUP owner.<br><br><b>Use Case:</b> Shared team directory. When multiple users create files inside, SGID guarantees all files belong to the shared group rather than individual user primary groups. Set with: <code>chmod 2755 /shared/dir</code> (or `g+s`).",
        "Topic": "Permissions & Security",
        "Tags": "linux permissions sgid collaboration"
    },
    {
        "Question": "What is the Sticky Bit and why is it set on `/tmp`?",
        "Answer": "<b>ANSWER:</b> Prevents users from deleting or renaming files owned by OTHER users.<br><br>Even if a directory has full `777` permissions, the Sticky Bit ensures only the file's owner or `root` can delete it. Appears as `t` in `ls -ld /tmp` (`drwxrwxrwt`). Set with: <code>chmod 1777 /tmp</code> (or `+t`).",
        "Topic": "Permissions & Security",
        "Tags": "linux permissions sticky_bit tmp security"
    },
    {
        "Question": "How does `umask` determine default file and directory creation permissions?",
        "Answer": "<b>ANSWER:</b> Subtraction from base permission limits (`777` for dirs, `666` for files).<br><br>If `umask = 022`:<br>• <b>Directory:</b> `777 - 022` = <b>`755`</b> (`rwxr-xr-x`)<br>• <b>File:</b> `666 - 022` = <b>`644`</b> (`rw-r--r--`)<br>Files never receive execute (`x`) by default for security.",
        "Topic": "Permissions & Security",
        "Tags": "linux umask permissions defaults"
    },
    {
        "Question": "What is the difference between `sudo -i` and `su -`?",
        "Answer": "<b>ANSWER:</b> Sudo authorization vs. Direct root password switch.<br><br>• <b>`sudo -i`:</b> Authenticates with the <b>user's own password</b> (if in sudoers), logging in as root with root's full environment.<br>• <b>`su -`:</b> Requires knowing the <b>root user's actual password</b> to switch to the root account.",
        "Topic": "Permissions & Security",
        "Tags": "linux sudo su root administration"
    },
    {
        "Question": "Why must you ALWAYS edit `/etc/sudoers` using `visudo`?",
        "Answer": "<b>ANSWER:</b> `visudo` locks the file and performs strict syntax validation before saving.<br><br>A single typo in `/etc/sudoers` locks ALL users (including admins) out of root `sudo` access, potentially requiring single-user rescue mode to recover.",
        "Topic": "Permissions & Security",
        "Tags": "linux sudo visudo sudoers administration"
    },
    {
        "Question": "How do you add an existing user to the `docker` and `sudo` groups on Linux?",
        "Answer": "<b>ANSWER:</b> Use `usermod -aG sudo,docker username`.<br><br><b>Crucial Flag:</b> Always include <b>`-a` (append)</b>! If you omit `-a` and run `usermod -G`, the user will be removed from all their other supplementary groups!",
        "Topic": "User Administration",
        "Tags": "linux user usermod groups sudo"
    },
    {
        "Question": "What is the recommended modern algorithm for generating SSH key pairs?",
        "Answer": "<b>ANSWER:</b> Ed25519 (faster, shorter, and more secure than RSA).<br><br><b>The Command:</b><br><code>ssh-keygen -t ed25519 -C \"admin@company.com\"</code><br>Generates private key `~/.ssh/id_ed25519` and public key `~/.ssh/id_ed25519.pub`.",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh ssh_keygen ed25519 security"
    },
    {
        "Question": "What exact file permissions are required for `~/.ssh` and SSH key files?",
        "Answer": "<b>ANSWER:</b> Strict permissions or SSH will refuse connections:<br><br>• <code>chmod 700 ~/.ssh</code> (Directory: owner only)<br>• <code>chmod 600 ~/.ssh/id_ed25519</code> (Private key: read/write owner only)<br>• <code>chmod 644 ~/.ssh/id_ed25519.pub</code> (Public key)<br>• <code>chmod 600 ~/.ssh/authorized_keys</code>",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh permissions security"
    },
    {
        "Question": "How do you copy your public SSH key to a remote server for passwordless login?",
        "Answer": "<b>ANSWER:</b> Use `ssh-copy-id`.<br><br><b>The Command:</b><br><code>ssh-copy-id -i ~/.ssh/id_ed25519.pub user@192.168.1.50</code><br>Automatically connects, sets permissions, and appends the key to `~/.ssh/authorized_keys` on the remote server.",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh ssh_copy_id remote_access"
    },
    {
        "Question": "How do you configure convenient SSH host aliases in `~/.ssh/config`?",
        "Answer": "<b>ANSWER:</b> Create Host blocks in `~/.ssh/config`.<br><br><b>Example:</b><br><code>Host prod-db <br>    HostName 10.0.1.50 <br>    User ubuntu <br>    Port 2222 <br>    IdentityFile ~/.ssh/prod_key</code><br>Now you connect simply by typing: `ssh prod-db`!",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh ssh_config shortcuts"
    },
    {
        "Question": "What two lines in `/etc/ssh/sshd_config` harden an SSH server against brute-force attacks?",
        "Answer": "<b>ANSWER:</b> Disable root login and disable password authentication.<br><br>1. <code>PermitRootLogin no</code><br>2. <code>PasswordAuthentication no</code><br>Forces all users to connect via public SSH keys and prevents direct root attacks. Restart ssh with: `systemctl restart sshd`.",
        "Topic": "SSH & Remote Access",
        "Tags": "linux ssh sshd_config hardening security"
    },

    # --- MODULE 3: PROCESS MANAGEMENT, MEMORY & PERFORMANCE TRIAGE ---
    {
        "Question": "What is the difference between `VSZ` and `RSS` in `ps aux` output?",
        "Answer": "<b>ANSWER:</b> Virtual Memory Size vs. Resident Set Size.<br><br>• <b>`VSZ` (Virtual Size):</b> Total memory the process has *requested* or mapped, including shared libraries and unused virtual allocations.<br>• <b>`RSS` (Resident Set Size):</b> The actual, physical RAM (in KB) currently held in hardware memory chips. Always use RSS to judge true memory consumption!",
        "Topic": "Performance Triage",
        "Tags": "linux processes ps vsz rss memory"
    },
    {
        "Question": "How do you interpret the 3 numbers in 'Load Average' (e.g. `load average: 4.00, 2.00, 1.00`)?",
        "Answer": "<b>ANSWER:</b> Average number of processes in runnable or uninterruptible state over 1, 5, and 15 minutes.<br><br>• Must be compared to CPU core count (`nproc`).<br>• On a <b>4-core machine</b>, a load of `4.00` = 100% CPU capacity.<br>• On a <b>2-core machine</b>, a load of `4.00` = 200% overloaded (processes are queueing up waiting for CPU or disk I/O).",
        "Topic": "Performance Triage",
        "Tags": "linux performance load_average cpu triage"
    },
    {
        "Question": "What are the 4 primary interactive sorting keys in `top` / `htop`?",
        "Answer": "<b>ANSWER:</b> Interactive triage hotkeys in `top`:<br><br>• <b>`Shift + P`:</b> Sort by % CPU usage.<br>• <b>`Shift + M`:</b> Sort by % Memory usage.<br>• <b>`k`:</b> Kill a process (prompts for PID and signal number).<br>• <b>`u`:</b> Filter processes by a specific username.",
        "Topic": "Performance Triage",
        "Tags": "linux top htop triage monitoring"
    },
    {
        "Question": "Explain the difference between `kill -15` (SIGTERM), `kill -9` (SIGKILL), and `kill -1` (SIGHUP).",
        "Answer": "<b>ANSWER:</b> The 3 most important Linux signals:<br><br>• <b>`kill -15 <pid>` (SIGTERM):</b> Polite request to terminate. Process catches signal, cleans up temp files, closes sockets, and exits cleanly.<br>• <b>`kill -9 <pid>` (SIGKILL):</b> Kernel immediately halts the process. Cannot be caught or ignored. Use ONLY as a last resort.<br>• <b>`kill -1 <pid>` (SIGHUP):</b> Tells daemons (Nginx, Postgres) to reload config files without restarting.",
        "Topic": "Process Management",
        "Tags": "linux kill signals sigterm sigkill sighup"
    },
    {
        "Question": "Why is a low 'Free' memory number normal and expected on a healthy Linux server in `free -m`?",
        "Answer": "<b>ANSWER:</b> Linux uses idle RAM as Page Cache to accelerate disk reads.<br><br>Unused RAM is wasted RAM. Linux automatically borrows free RAM to cache disk blocks. Look at the <b>`available`</b> column—this shows memory that can be instantly reclaimed for applications if needed.",
        "Topic": "Performance Triage",
        "Tags": "linux memory free page_cache available"
    },
    {
        "Question": "How do you create and activate a 4GB Swap file on Linux?",
        "Answer": "<b>ANSWER:</b> Using `fallocate`, `mkswap`, and `swapon`.<br><br><b>The Commands:</b><br>1. <code>fallocate -l 4G /swapfile</code><br>2. <code>chmod 600 /swapfile</code><br>3. <code>mkswap /swapfile</code><br>4. <code>swapon /swapfile</code><br>Make permanent by adding `/swapfile swap swap defaults 0 0` to `/etc/fstab`.",
        "Topic": "Storage & Disks",
        "Tags": "linux swap memory fallocate swapon"
    },
    {
        "Question": "What are the most critical columns to inspect in `vmstat 1`?",
        "Answer": "<b>ANSWER:</b> Real-time OS triage metrics:<br><br>• <b>`r` (run queue):</b> Processes waiting for CPU. If higher than core count, CPU is overloaded.<br>• <b>`b` (blocked):</b> Processes waiting on disk I/O.<br>• <b>`si` / `so` (swap in/out):</b> If non-zero, server is actively swapping RAM to disk.<br>• <b>`wa` (I/O wait):</b> Percentage of CPU time spent idle waiting for slow disk.",
        "Topic": "Performance Triage",
        "Tags": "linux vmstat performance triage cpu disk"
    },
    {
        "Question": "What does `%util = 100%` indicate in `iostat -xz 1`?",
        "Answer": "<b>ANSWER:</b> Disk storage device saturation.<br><br>Indicates the hard drive or SSD is spending 100% of its time processing I/O requests. Any new disk read/write will queue up, causing high `await` times and freezing database performance.",
        "Topic": "Performance Triage",
        "Tags": "linux iostat disk saturation performance"
    },
    {
        "Question": "Why does `df -h` show 100% full even after you delete a 50GB log file?",
        "Answer": "<b>ANSWER:</b> A running process still holds an open file descriptor to the deleted file.<br><br>Linux will not reclaim physical disk blocks until all processes close the file.<br><b>Find it:</b> <code>lsof | grep deleted</code><br><b>Fix:</b> Restart the process holding the file descriptor, or truncate it: <code>> /proc/<PID>/fd/<FD_NUM></code>.",
        "Topic": "Storage & Disks",
        "Tags": "linux lsof deleted disk_space fd"
    },
    {
        "Question": "What is the difference between `nice` and `renice`?",
        "Answer": "<b>ANSWER:</b> Launch priority vs. Running priority.<br><br>• <b>`nice -n 10 ./script.sh`:</b> Sets priority *before* starting (-20 highest to +19 lowest).<br>• <b>`renice -n -5 -p 1234`:</b> Adjusts scheduling priority of an *already running* process.",
        "Topic": "Process Management",
        "Tags": "linux nice renice priority scheduling"
    },
    {
        "Question": "How do you keep a long-running script alive after disconnecting from an SSH session?",
        "Answer": "<b>ANSWER:</b> Use `nohup` or `tmux`.<br><br>• <b>Approach 1:</b> <code>nohup python3 script.py > script.log 2>&1 &</code><br>• <b>Approach 2:</b> Run inside a `tmux` session (`tmux new -s job`). If your SSH connection drops, the process keeps running in the background.",
        "Topic": "Process Management",
        "Tags": "linux nohup tmux background ssh"
    },
    {
        "Question": "How do you verify if the Linux Out-Of-Memory (OOM) Killer recently killed a process?",
        "Answer": "<b>ANSWER:</b> Inspect kernel ring buffer logs using `dmesg`.<br><br><b>The Command:</b><br><code>dmesg -T | grep -i oom</code><br>Or: <code>journalctl -k | grep -i \"killed process\"</code><br>Reveals which process consumed excessive RAM and was forcefully terminated by the kernel.",
        "Topic": "Performance Triage",
        "Tags": "linux oom dmesg kernel memory"
    }
]

# Write Batch 1 to decks/linux_mastery_deck.csv
os.makedirs('decks', exist_ok=True)
with open('decks/linux_mastery_deck.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    writer.writeheader()
    for card in batch1_cards:
        writer.writerow(card)

print(f"Batch 1 complete: wrote {len(batch1_cards)} cards to decks/linux_mastery_deck.csv.")
