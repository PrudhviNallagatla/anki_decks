import csv

batchB = [
    # --- GIT CLI MASTERY FOR DBAS & DEVOPS ---
    {
        "Question": "How do you temporarily shelf uncommitted changes without committing them in Git?",
        "Answer": "<b>ANSWER:</b> Use `git stash`.<br><br>• <b>Save to stash:</b> <code>git stash -u</code> (includes untracked files).<br>• <b>Inspect stashes:</b> <code>git stash list</code>.<br>• <b>Reapply latest stash:</b> <code>git stash pop</code> (restores changes and removes from stash list).",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git stash workflow devops"
    },
    {
        "Question": "What is the modern Git command to create and switch to a new branch?",
        "Answer": "<b>ANSWER:</b> `git switch -c new-feature-branch`<br><br>(Replaces legacy `git checkout -b`). Modern Git separated branch switching (`git switch`) from file restoration (`git restore`) for clarity.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git switch branch modern"
    },
    {
        "Question": "How do you discard uncommitted local modifications to a specific file?",
        "Answer": "<b>ANSWER:</b> `git restore path/to/file`<br><br>(Or legacy `git checkout -- path/to/file`). Restores the file in your working directory back to the state of the last commit (`HEAD`).",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git restore undo working_tree"
    },
    {
        "Question": "What is the difference between `git reset --soft HEAD~1` and `git reset --hard HEAD~1`?",
        "Answer": "<b>ANSWER:</b> Preserving changes vs. Destroying changes.<br><br>• <b>`--soft`:</b> Undoes the last commit, but keeps all modified code safely staged in your index (ready to re-commit).<br>• <b>`--hard`:</b> Completely wipes out the commit, the staged index, and all file changes in your working directory (irreversible data loss).",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git reset soft hard undo safety"
    },
    {
        "Question": "What is `git bisect` and how does it find which commit introduced a production bug?",
        "Answer": "<b>ANSWER:</b> Automated binary search across git commit history.<br><br><b>Workflow:</b><br>1. <code>git bisect start</code><br>2. <code>git bisect bad</code> (current commit is broken)<br>3. <code>git bisect good v1.0.0</code> (last known working release)<br>Git automatically checks out midpoint commits; you test and mark `good` or `bad` until Git identifies the exact commit that broke the build.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git bisect debugging forensics"
    },
    {
        "Question": "How do you apply a single specific commit from another branch into your current branch?",
        "Answer": "<b>ANSWER:</b> Use `git cherry-pick <commit-hash>`.<br><br>Copies the changeset introduced by that specific commit and applies it cleanly as a brand new commit on top of your current branch.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git cherry_pick branches workflow"
    },
    {
        "Question": "How do you add forgotten file modifications to your previous commit without creating a new commit?",
        "Answer": "<b>ANSWER:</b> Stage the forgotten file and run `git commit --amend --no-edit`.<br><br>Combines the newly staged changes directly into the most recent commit, keeping the exact same commit message.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git amend commit productivity"
    },
    {
        "Question": "How do you see who wrote a specific line in a file and in which commit using Git?",
        "Answer": "<b>ANSWER:</b> Use `git blame`.<br><br><b>The Command:</b><br><code>git blame -L 120,135 postgresql.conf</code><br>Displays the commit hash, author name, timestamp, and line content for lines 120 through 135.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git blame forensics auditing"
    },
    {
        "Question": "What is `git reflog` and why is it a developer's ultimate safety net?",
        "Answer": "<b>ANSWER:</b> A local log of EVERY position of `HEAD` across all branches.<br><br>Even if you run `git reset --hard` or delete a local branch, the commits still exist in your local Git object store. `git reflog` lists their hashes so you can run `git checkout <hash>` and resurrect lost work!",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git reflog recovery safety"
    },
    {
        "Question": "How do you remove a file from Git tracking without deleting it from your local disk?",
        "Answer": "<b>ANSWER:</b> Use `git rm --cached filename`.<br><br>Removes the file from Git's staging index so you can add it to `.gitignore`, while preserving the physical file on your local filesystem.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git gitignore rm_cached files"
    },
    {
        "Question": "How do you force your local branch to match the remote `origin/main` branch exactly?",
        "Answer": "<b>ANSWER:</b> Fetch and hard reset.<br><br><b>The Commands:</b><br><code>git fetch origin</code><br><code>git reset --hard origin/main</code><br>Discards all local divergent commits and synchronizes your working directory to the exact state of the remote repository.",
        "Topic": "Git CLI Mastery",
        "Tags": "linux git reset sync origin remote"
    },

    # --- ADVANCED PERFORMANCE TRIAGE, HARDWARE & KERNEL ---
    {
        "Question": "What is CPU Affinity (`taskset`) and why is it used on high-performance database servers?",
        "Answer": "<b>ANSWER:</b> Pins specific processes to dedicated physical CPU cores.<br><br><b>Example:</b><br><code>taskset -c 0,1,2,3 /usr/bin/postgres -D /data</code><br>Prevents the OS scheduler from bouncing processes between different CPU sockets, maximizing L1/L2/L3 hardware CPU cache hits and eliminating NUMA memory interconnect latency.",
        "Topic": "Performance Triage",
        "Tags": "linux taskset cpu affinity numa performance"
    },
    {
        "Question": "How do you inspect the health and wear percentage of an enterprise NVMe SSD in Linux?",
        "Answer": "<b>ANSWER:</b> Use `nvme smart-log`.<br><br><b>The Command:</b><br><code>sudo nvme smart-log /dev/nvme0</code><br>Displays `percentage_used` (wear level), temperature in Celsius, and critical warnings before drive failure.",
        "Topic": "Storage & Disks",
        "Tags": "linux nvme storage smart health ssd"
    },
    {
        "Question": "How do you check hard drive SMART health using `smartctl`?",
        "Answer": "<b>ANSWER:</b> `sudo smartctl -H /dev/sda`<br><br>Returns `SMART overall-health self-assessment test result: PASSED`. Run <code>smartctl -a /dev/sda</code> to inspect reallocated sector counts and pending sector warnings.",
        "Topic": "Storage & Disks",
        "Tags": "linux smartctl smart disks storage health"
    },
    {
        "Question": "How do you inspect physical RAM chip speed, slot count, and manufacturer without opening the server case?",
        "Answer": "<b>ANSWER:</b> Use `dmidecode -t memory`.<br><br><b>The Command:</b><br><code>sudo dmidecode -t memory | grep -E 'Size|Speed|Manufacturer|Part Number'</code><br>Extracts motherboard DMI tables showing installed DIMMs (e.g. DDR4 3200 MT/s) and empty expansion slots.",
        "Topic": "Hardware Inspection",
        "Tags": "linux dmidecode hardware ram memory motherboard"
    },
    {
        "Question": "What is the optimal Disk I/O Scheduler for NVMe SSDs in Linux?",
        "Answer": "<b>ANSWER:</b> `none` (No-Op).<br><br>• <b>NVMe drives:</b> Hardware has 64,000 parallel submission queues. OS elevator algorithms (`bfq`, `mq-deadline`) only add CPU latency overhead. Set to `none`: <code>echo none | sudo tee /sys/block/nvme0n1/queue/scheduler</code>.<br>• <b>Spinning disks:</b> Use `mq-deadline` or `bfq` to reorder requests physically.",
        "Topic": "Kernel Tuning",
        "Tags": "linux kernel scheduler nvme disk io tuning"
    },
    {
        "Question": "What is `net.core.somaxconn` in `/etc/sysctl.conf` and why should high-traffic servers increase it?",
        "Answer": "<b>ANSWER:</b> The maximum listen queue backlog for incoming TCP connections.<br><br>• Default is `128` (or `4096`).<br>• Under sudden traffic spikes, if the listen queue fills up, incoming client connections are rejected or dropped with connection timeouts.<br>• Raise to <b>`65535`</b> on production web and database servers.",
        "Topic": "Kernel Tuning",
        "Tags": "linux sysctl somaxconn networking tcp backlog"
    },
    {
        "Question": "What is Ephemeral Port Exhaustion and how do you prevent it via `sysctl`?",
        "Answer": "<b>ANSWER:</b> Outgoing connections exhausting all available client TCP port numbers (ports in `TIME_WAIT`).<br><br><b>The Fix in `/etc/sysctl.conf`:</b><br><code>net.ipv4.ip_local_port_range = 10240 65535</code><br><code>net.ipv4.tcp_tw_reuse = 1</code><br>Expands the pool of available outgoing client ports and safely reuses `TIME_WAIT` sockets for outgoing traffic.",
        "Topic": "Kernel Tuning",
        "Tags": "linux sysctl tcp ports ephemeral time_wait"
    },
    {
        "Question": "How do you inspect hardware temperature and fan speeds on Linux?",
        "Answer": "<b>ANSWER:</b> Use the `sensors` command (from `lm-sensors`).<br><br><b>The Command:</b><br><code>sensors</code><br>Displays real-time temperature readings for CPU cores, NVMe controllers, and motherboard sensors, alerting you if CPU is thermal throttling.",
        "Topic": "Hardware Inspection",
        "Tags": "linux sensors temperature hardware fan cpu"
    },
    {
        "Question": "How do you list all active kernel modules and view details on a specific driver?",
        "Answer": "<b>ANSWER:</b> `lsmod` and `modinfo`.<br><br>• <b>List active:</b> <code>lsmod</code><br>• <b>Inspect module:</b> <code>modinfo e1000e</code> (shows driver version, author, and parameters).<br>• <b>Load/Unload:</b> <code>sudo modprobe <module></code> and <code>sudo modprobe -r <module></code>.",
        "Topic": "Kernel Tuning",
        "Tags": "linux kernel modules lsmod modprobe modinfo"
    },
    {
        "Question": "How do you check when the server last rebooted and whether it was an orderly shutdown or power crash?",
        "Answer": "<b>ANSWER:</b> Use `last reboot`.<br><br><b>Usage:</b><br><code>last -x reboot shutdown</code><br>Reads `/var/log/wtmp` to show boot timestamps and system uptime intervals, distinguishing clean reboots from sudden crashes.",
        "Topic": "Performance Triage",
        "Tags": "linux last reboot shutdown uptime crash"
    }
]

with open('decks/linux_mastery_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batchB:
        writer.writerow(card)

print(f"Linux Batch B complete: appended {len(batchB)} cards.")
