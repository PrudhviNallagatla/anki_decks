import csv

batchC = [
    {
        "Question": "How do you inspect PCI hardware devices (NICs, RAID cards) and verify which kernel driver is controlling them?",
        "Answer": "<b>ANSWER:</b> Use `lspci -nnk`.<br><br>• `-nn`: Shows both vendor name and numeric device IDs.<br>• `-k`: Displays the kernel driver (`Kernel driver in use: e1000e`) and kernel modules handling the device.",
        "Topic": "Hardware Inspection",
        "Tags": "linux lspci hardware drivers pci"
    },
    {
        "Question": "How do you check if hardware CPU Throttling is occurring due to overheating?",
        "Answer": "<b>ANSWER:</b> Search kernel messages for throttle events.<br><br><b>The Command:</b><br><code>dmesg -T | grep -i throttle</code><br>Reports messages like: `CPU0: Package temperature above threshold, cpu clock throttled`.",
        "Topic": "Hardware Inspection",
        "Tags": "linux cpu thermal throttling hardware dmesg"
    },
    {
        "Question": "How do you inspect static HugePages allocations in Linux?",
        "Answer": "<b>ANSWER:</b> Inspect `/proc/meminfo`.<br><br><b>The Command:</b><br><code>grep -i huge /proc/meminfo</code><br>Shows `HugePages_Total`, `HugePages_Free`, and `Hugepagesize` (typically 2048 kB / 2MB). Used to pre-allocate dedicated static RAM buffers for PostgreSQL or Oracle.",
        "Topic": "Kernel Tuning",
        "Tags": "linux kernel hugepages memory tuning"
    },
    {
        "Question": "How do you profile system call time for a running process using `strace -c`?",
        "Answer": "<b>ANSWER:</b> Use `strace -c -p <PID>`.<br><br>Accumulates system calls and outputs a clean statistical table showing: % time spent in each syscall (`epoll_wait`, `read`, `futex`), total calls, errors, and average microseconds per call.",
        "Topic": "Performance Triage",
        "Tags": "linux strace profiling syscalls performance"
    },
    {
        "Question": "How do you measure the Peak Physical RAM (Max RSS) consumed by a program during execution?",
        "Answer": "<b>ANSWER:</b> Use GNU time with verbose output: `/usr/bin/time -v command`.<br><br>Displays detailed execution diagnostics including: <code>Maximum resident set size (kbytes): 452890</code> (exact peak RAM used) and major page faults.",
        "Topic": "Performance Triage",
        "Tags": "linux time rss memory profiling"
    },
    {
        "Question": "How do you verify the SHA-256 cryptographic checksum of a downloaded file?",
        "Answer": "<b>ANSWER:</b> Use `sha256sum`.<br><br>• <b>Calculate:</b> <code>sha256sum postgresql-16.tar.gz</code><br>• <b>Automated verification:</b> <code>sha256sum -c checksums.txt</code><br>Guarantees the downloaded installer has not been corrupted or tampered with by malware.",
        "Topic": "Permissions & Security",
        "Tags": "linux security sha256sum checksum integrity"
    },
    {
        "Question": "How do you extract ONLY the HTTP status code (e.g. `200`) using `curl` for automated health checks?",
        "Answer": "<b>ANSWER:</b> Use `curl -s -o /dev/null -w \"%{http_code}\" URL`.<br><br><b>The Script:</b><br><code>STATUS=$(curl -s -o /dev/null -w \"%{http_code}\" https://myapi.com/health) <br>if [[ \"$STATUS\" -eq 200 ]]; then echo \"Healthy\"; fi</code>",
        "Topic": "Networking & Ports",
        "Tags": "linux curl healthcheck http_code bash"
    },
    {
        "Question": "How do you parse a JSON attribute directly in the terminal using `jq`?",
        "Answer": "<b>ANSWER:</b> Use `jq -r`.<br><br><b>The Command:</b><br><code>curl -s https://api.github.com/repos/postgres/postgres | jq -r '.stargazers_count'</code><br>• `-r`: Raw string output (omits surrounding JSON quotes).",
        "Topic": "Text Processing",
        "Tags": "linux jq json text_processing cli"
    },
    {
        "Question": "What is the difference between `basename` and `dirname` in Linux shell scripts?",
        "Answer": "<b>ANSWER:</b> Filename extractor vs. Directory path extractor.<br><br>• <code>basename /var/log/nginx/access.log</code> -> returns: <b>`access.log`</b><br>• <code>dirname /var/log/nginx/access.log</code> -> returns: <b>`/var/log/nginx`</b>",
        "Topic": "CLI Navigation",
        "Tags": "linux bash basename dirname path"
    },
    {
        "Question": "What is `chroot` in Linux?",
        "Answer": "<b>ANSWER:</b> Changes the apparent root directory (`/`) for the current running process and its children.<br><br>The program cannot see or access any files outside the designated directory tree jail. The foundational technology behind FreeBSD jails, containers, and secure rescue shells.",
        "Topic": "Permissions & Security",
        "Tags": "linux chroot security isolation"
    },
    {
        "Question": "How do you inspect the distribution of hardware interrupts across CPU cores?",
        "Answer": "<b>ANSWER:</b> `cat /proc/interrupts`<br><br>Displays IRQ counts per CPU core for network cards and disk controllers. If one core has 10,000,000 interrupts while others have 0, configure `irqbalance` to distribute network packet processing evenly across all CPU cores.",
        "Topic": "Performance Triage",
        "Tags": "linux hardware interrupts irqbalance performance"
    },
    {
        "Question": "What does `git log --oneline --graph --all --decorate` do?",
        "Answer": "<b>ANSWER:</b> Renders an ASCII branch and merge tree of your entire Git history.<br><br>Displays commit hashes, branch pointers (`main`, `feature`), release tags (`v1.0`), and visual lines connecting merges across all branches in a single terminal screen.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git log graph branch history"
    },
    {
        "Question": "How do you resolve a Git merge conflict from the terminal?",
        "Answer": "<b>ANSWER:</b> Inspect status, edit markers, and stage.<br><br>1. Run <code>git status</code> to find `both modified` files.<br>2. Open file and edit conflict markers: <code><<<<<<< HEAD ... ======= ... >>>>>>></code>.<br>3. Stage resolved file: <code>git add file.txt</code>.<br>4. Complete merge: <code>git commit</code>.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git merge conflict resolution"
    },
    {
        "Question": "How do you remove untracked files and directories from your Git working directory?",
        "Answer": "<b>ANSWER:</b> Use `git clean -fd`.<br><br>• `-f` (force): Deletes untracked files.<br>• `-d`: Recursively removes untracked directories.<br>• Add `-n` (dry-run) first to preview what would be deleted: <code>git clean -nd</code>.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git clean untracked working_tree"
    },
    {
        "Question": "How do you create an annotated Git tag and push it to the remote repository?",
        "Answer": "<b>ANSWER:</b> `git tag -a` and `git push --tags`.<br><br><b>The Commands:</b><br><code>git tag -a v2.1.0 -m \"Production Release 2.1.0\"</code><br><code>git push origin v2.1.0</code><br>Stores full author, date, and message metadata attached to the commit.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git tag release semver"
    }
]

with open('decks/linux_mastery_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batchC:
        writer.writerow(card)

print(f"Linux Batch C complete: appended {len(batchC)} cards.")
