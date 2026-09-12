"""
In-Depth Topic Knowledge Base for AI Personal Tutor.
===================================================
Provides crystal-clear, pedagogical, student-friendly lesson explanations,
real-world analogies, concrete examples, and accurate quizzes for all standard
computer science subjects and topics.
"""

from typing import Dict, Any, List


# ---------------------------------------------------------------------------
# Comprehensive Explanations for Common Curriculum Topics
# ---------------------------------------------------------------------------

EXPANDED_TOPIC_EXPLANATIONS: Dict[str, Dict[str, Any]] = {
    # =======================================================================
    # OPERATING SYSTEMS
    # =======================================================================
    "Introduction to OS": {
        "summary": "Core role of the Operating System as a resource manager and hardware abstraction layer.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Think of an Operating System (OS) like the manager of a busy restaurant. The computer hardware (CPU, RAM, hard drive) is the kitchen and staff. The software apps (browser, games, word processor) are the customers placing orders. Without a manager, customers would barge into the kitchen, fight over ovens, and create chaos. The OS acts as the mediator: it takes orders, allocates kitchen resources fairly, and makes sure no single app crashes the entire system.",
                "concepts": [
                    "Hardware Abstraction: Hiding raw device circuitry behind simple interfaces like read() and write().",
                    "Resource Management: Fairly dividing CPU time, memory space, and storage among running programs.",
                    "Dual-Mode Operation: User Mode (restricted instructions for apps) vs. Kernel Mode (full hardware access for the OS).",
                    "System Calls: The official doorway (API) programs use to request OS services like opening files or printing."
                ],
                "example": "When you click 'Save' in a text editor, the app cannot directly write electrical signals to your SSD. Instead, it issues a 'sys_write' system call. The OS checks permissions, writes the bytes safely to disk, and reports success back to the app.",
                "practice": "Why does an operating system run regular user applications in User Mode instead of Kernel Mode?"
            },
            "Normal": {
                "explanation": "An Operating System is system software that manages computer hardware, software resources, and provides common services. It operates in Dual Mode (User Mode vs. Kernel Mode) using a hardware trap mechanism to switch modes during system calls, interrupts, and exceptions.",
                "concepts": [
                    "Kernel Architecture: Monolithic (Linux) vs. Microkernel (Mach/QNX) trade-offs between execution speed and fault isolation.",
                    "Interrupt Handling: Hardware interrupt controller (APIC) signals the CPU to invoke an Interrupt Service Routine (ISR).",
                    "System Call Interface: Trap instructions save register state, elevate privilege to ring 0, and invoke the syscall dispatcher table.",
                    "Virtualization: Giving each process the illusion of having its own dedicated CPU and private address space."
                ],
                "example": "Dual-mode transition: A C program executes `read(fd, buf, 1024)`. The CPU triggers software interrupt `0x80` or `syscall` instruction, changes privilege bit from 3 (User) to 0 (Kernel), executes kernel disk driver logic, and returns via `sysret`.",
                "practice": "Compare how a monolithic kernel handles device driver crashes versus a microkernel architecture."
            },
            "Advanced": {
                "explanation": "Modern OS kernels implement layered security rings, capability-based access control, preemption timers, and hardware-enforced isolation (e.g. Intel VT-x/AMD-V) to support high-throughput, multi-tenant server workloads.",
                "concepts": [
                    "Privilege Rings & Page Protection: Ring 0 (Kernel), Ring 3 (User), and hypervisor Ring -1 execution contexts.",
                    "Asynchronous System Calls: io_uring in Linux avoiding context switch overhead via shared memory submission/completion rings.",
                    "Interrupt Affinity & SoftIRQs: Binding network card interrupts to specific CPU cores to optimize cache locality."
                ],
                "example": "High-performance network packet processing using Linux `io_uring` and eBPF kernel bytecode filters to inspect packets without round-tripping through user space.",
                "practice": "Explain why modern Linux kernels moved from traditional syscalls to io_uring for high-IOPS NVMe drives."
            }
        },
        "quiz": [
            {
                "id": 1,
                "question": "What is the primary reason the CPU switches from User Mode to Kernel Mode during a system call?",
                "options": [
                    "To allow user programs to access privileged hardware instructions safely under OS control",
                    "To increase the clock speed of the CPU",
                    "To compress files on the storage drive",
                    "To prevent other applications from using the internet"
                ],
                "correct_option": 0,
                "explanation": "Kernel mode grants unrestricted access to physical hardware; switching via system calls ensures safety and isolation."
            },
            {
                "id": 2,
                "question": "Which software architecture places minimal services (IPC, basic scheduling) in kernel space while running file systems and device drivers in user space?",
                "options": ["Monolithic Kernel", "Microkernel", "Single-tasking Kernel", "Exokernel only"],
                "correct_option": 1,
                "explanation": "A Microkernel strips down the kernel to absolute essentials, enhancing stability because driver crashes do not take down the OS."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Review: What happens if an application in User Mode tries to execute a privileged CPU instruction directly?",
                "options": [
                    "The CPU generates a hardware trap/exception and the OS terminates or flags the process",
                    "The CPU executes it normally",
                    "The computer shuts down immediately",
                    "The instruction is ignored with no error"
                ],
                "correct_option": 0,
                "explanation": "Hardware prevents user-mode execution of privileged instructions by throwing an exception (e.g., General Protection Fault)."
            },
            {
                "id": 2,
                "question": "What mechanism allows an external hardware device (like a keyboard or network card) to alert the CPU immediately?",
                "options": ["Hardware Interrupt", "Polling Loop", "System Call", "Virtual Memory"],
                "correct_option": 0,
                "explanation": "Hardware interrupts signal the CPU via electrical pins, triggering immediate execution of an Interrupt Service Routine."
            }
        ]
    },

    "CPU Scheduling": {
        "summary": "Algorithms used by the OS to allocate CPU time among runnable processes.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Imagine you are the single doctor in a busy emergency room with 10 patients waiting. How do you decide who to treat first? If you treat whoever arrived first (First-Come, First-Served), someone with a small splinter might hold up a person needing urgent care. If you treat the shortest injury first (Shortest Job First), the doctor stays efficient. CPU scheduling is the OS scheduler's strategy for deciding which process gets to use the CPU next and for how long.",
                "concepts": [
                    "CPU Burst vs I/O Burst: A program alternates between doing math on the CPU and waiting for disk/network I/O.",
                    "Preemptive Scheduling: The OS forcibly pauses a running process when its time is up or a higher priority task arrives.",
                    "Time Quantum (Slice): In Round Robin scheduling, the fixed slice of time (e.g. 10ms) given to each process.",
                    "Starvation: When a low-priority process waits forever because higher-priority jobs keep arriving."
                ],
                "example": "Round Robin (RR) with a 20ms time slice: Process A needs 50ms, Process B needs 15ms. The CPU runs A for 20ms, pauses A, runs B for 15ms (B finishes!), and returns to A. The user sees both tasks progressing smoothly.",
                "practice": "Calculate the average waiting time for 3 processes with burst times 6ms, 4ms, 2ms arriving simultaneously under Shortest Job First."
            },
            "Normal": {
                "explanation": "CPU Scheduling determines process order to optimize metrics: CPU Utilization, Throughput, Turnaround Time, Waiting Time, and Response Time. Schedulers range from non-preemptive (FCFS, Non-preemptive SJF) to preemptive (Preemptive SJF / SRTF, Round Robin, Multilevel Feedback Queue).",
                "concepts": [
                    "Turnaround Time: Total time from process arrival to completion (Completion Time - Arrival Time).",
                    "Waiting Time: Total time spent in ready queue waiting for CPU (Turnaround Time - Burst Time).",
                    "Convoy Effect: In FCFS, when many short I/O-bound processes are stuck behind one massive CPU-bound process.",
                    "Multilevel Feedback Queue (MLFQ): Dynamically demotes CPU-heavy processes and prioritizes interactive I/O jobs."
                ],
                "example": "Gantt Chart analysis: P1 (Burst 24ms), P2 (Burst 3ms), P3 (Burst 3ms). Under FCFS, average wait is (0 + 24 + 27)/3 = 17ms. Under SJF (P2 -> P3 -> P1), average wait drops to (0 + 3 + 6)/3 = 3ms!",
                "practice": "Why does setting the Round Robin time quantum too small degrade system throughput?"
            },
            "Advanced": {
                "explanation": "Production schedulers (like Linux CFS - Completely Fair Scheduler) replace simple priority queues with red-black trees indexed by virtual runtime (`vruntime`), balancing fairness, multicore cache locality, and NUMA node latency.",
                "concepts": [
                    "Linux CFS & Virtual Runtime: Tasks are tracked via `vruntime`; the leftmost node in the red-black tree is picked in O(log N).",
                    "Real-Time Scheduling: Rate-Monotonic Scheduling (RMS) and Earliest Deadline First (EDF) with deterministic deadline guarantees.",
                    "Processor Affinity & Load Balancing: Keeping threads on the same CPU core to preserve L1/L2 cache warmth."
                ],
                "example": "In Linux CFS, when a task with high priority (lower nice value) runs, its `vruntime` increases much more slowly than a low-priority task, naturally yielding more CPU time.",
                "practice": "Prove the condition under which Earliest Deadline First (EDF) guarantees 100% schedulability."
            }
        },
        "quiz": [
            {
                "id": 1,
                "question": "Which CPU scheduling algorithm minimizes the theoretical average waiting time for a given set of stationary processes?",
                "options": [
                    "First-Come, First-Served (FCFS)",
                    "Shortest Job First (SJF) / Shortest Remaining Time First",
                    "Round Robin with large time quantum",
                    "Priority Scheduling with no preemption"
                ],
                "correct_option": 1,
                "explanation": "Shortest Job First (SJF) is mathematically optimal for minimizing average waiting time by clearing short jobs first."
            },
            {
                "id": 2,
                "question": "What negative phenomenon occurs if the Round Robin time quantum is set to an extremely tiny interval (e.g. 1 microsecond)?",
                "options": [
                    "CPU spends excessive time performing context switches rather than executing useful work",
                    "Processes experience deadlock",
                    "Average turnaround time becomes zero",
                    "Hard drive crashes"
                ],
                "correct_option": 0,
                "explanation": "Too small a quantum causes context switch overhead to dominate CPU time, destroying throughput."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Refresher: What is the 'Convoy Effect' in operating systems?",
                "options": [
                    "Short processes waiting a long time behind a large CPU-heavy process in FCFS scheduling",
                    "Multiple CPUs running at the same speed",
                    "A network packet queue overflowing",
                    "Threads locking each other in deadlock"
                ],
                "correct_option": 0,
                "explanation": "The convoy effect occurs in FCFS when fast I/O tasks stall waiting for one long compute job to finish."
            },
            {
                "id": 2,
                "question": "In a Multilevel Feedback Queue (MLFQ), how does the scheduler treat a process that repeatedly exhausts its full time slice?",
                "options": [
                    "It demotes the process to a lower-priority queue with a larger time slice",
                    "It kills the process immediately",
                    "It promotes the process to the top priority queue",
                    "It ignores the process"
                ],
                "correct_option": 0,
                "explanation": "MLFQ penalizes CPU-intensive jobs by moving them to lower priority queues, preserving top queues for interactive jobs."
            }
        ]
    },

    "Process Synchronization & Semaphores": {
        "summary": "Mechanisms to prevent race conditions and synchronize concurrent threads.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Imagine two people sharing a single bank account with $100. Both go to different ATMs at the exact same second to withdraw $80. ATM 1 reads $100 and approves. ATM 2 reads $100 at the same split-second and approves! Suddenly $160 is withdrawn from a $100 account! This bug is called a Race Condition. Process Synchronization is like putting a lock on the bank account: while ATM 1 is doing its transaction, ATM 2 MUST wait outside until ATM 1 is finished.",
                "concepts": [
                    "Critical Section: The specific piece of code where shared memory/data is read and modified.",
                    "Race Condition: An unexpected bug where the output depends on the random timing of concurrent threads.",
                    "Mutex (Mutual Exclusion Lock): A simple lock with two states: Locked and Unlocked. Only the holder can unlock it.",
                    "Semaphore: A signaling counter. Counting Semaphore allows up to N threads; Binary Semaphore acts like a lock."
                ],
                "example": "Using a Mutex in Python: `with lock: balance -= amount`. If Thread B arrives while Thread A is inside the `with` block, Thread B sleeps until Thread A releases the lock.",
                "practice": "What three conditions must any valid solution to the Critical Section problem satisfy?"
            },
            "Normal": {
                "explanation": "Concurrent processes accessing shared resources require synchronization to maintain data consistency. A solution to the Critical Section problem must satisfy three criteria: Mutual Exclusion, Progress, and Bounded Waiting.",
                "concepts": [
                    "Peterson's Algorithm: Classic software solution for 2 processes using `turn` and `flag[2]` variables.",
                    "Hardware Primitives: Atomic instructions `TestAndSet()` and `CompareAndSwap()` (CAS) enabling spinlocks.",
                    "Semaphores (Dijkstra): An integer variable accessed only via atomic operations `wait()` (P) and `signal()` (V).",
                    "Classical Problems: Producer-Consumer (Bounded Buffer), Readers-Writers, and Dining Philosophers."
                ],
                "example": "Producer-Consumer with Semaphores: `mutex` (protects buffer index), `empty` (initialized to buffer size N), `full` (initialized to 0). Producer calls `wait(empty)`, `wait(mutex)`, inserts item, `signal(mutex)`, `signal(full)`.",
                "practice": "Why can an improper order of nested semaphore wait calls cause immediate deadlock?"
            },
            "Advanced": {
                "explanation": "Advanced synchronization avoids the overhead of OS context switching and priority inversion using Lock-Free data structures (CAS loops), Read-Copy-Update (RCU), and Priority Inheritance Protocols.",
                "concepts": [
                    "Memory Barriers & Ordering: Preventing CPU and compiler instruction reordering (acquire-release semantics).",
                    "Priority Inversion & Inheritance: A low-priority task holding a lock blocks a high-priority task; solved by temporarily raising the lock holder's priority.",
                    "Lock-Free Concurrency: Michael-Scott queue and Atomic ABA problem mitigation using generation counters."
                ],
                "example": "Linux Kernel RCU (Read-Copy-Update): Readers access linked list elements lock-free without delays. Writers make a modified copy, swap pointers atomically, and defer freeing old memory until all readers finish the grace period.",
                "practice": "Explain how the Mars Pathfinder spacecraft was rescued from priority inversion in 1997."
            }
        },
        "quiz": [
            {
                "id": 1,
                "question": "What three requirements MUST be satisfied by any correct solution to the Critical Section problem?",
                "options": [
                    "Mutual Exclusion, Progress, and Bounded Waiting",
                    "Speed, Memory Compression, and Encryption",
                    "Multithreading, Paging, and Swapping",
                    "Deadlock, Starvation, and Livelock"
                ],
                "correct_option": 0,
                "explanation": "The 3 formal criteria are Mutual Exclusion (only 1 inside), Progress (selection cannot be stalled), and Bounded Waiting (no starvation)."
            },
            {
                "id": 2,
                "question": "If a counting semaphore is initialized to value S = 5, and 8 consecutive wait() operations are executed, what is the final semaphore value?",
                "options": ["-3 (indicating 3 processes are queued/waiting)", "0", "3", "5"],
                "correct_option": 0,
                "explanation": "Each wait() decrements S. 5 - 8 = -3. The negative magnitude (| -3 | = 3) indicates 3 processes are blocked waiting."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Quick check: What is the defining characteristic of a 'Race Condition'?",
                "options": [
                    "The final outcome depends on the uncontrollable execution order of concurrent threads",
                    "The computer CPU runs at maximum turbo frequency",
                    "Two processes finish at the exact same microsecond",
                    "A network cable transmits packets faster than the NIC"
                ],
                "correct_option": 0,
                "explanation": "A race condition occurs when concurrent read/write operations produce nondeterministic results depending on thread timing."
            },
            {
                "id": 2,
                "question": "How does a Binary Semaphore differ from a traditional Mutex?",
                "options": [
                    "A Mutex enforces ownership (only the locking thread can unlock), whereas any thread can signal a semaphore",
                    "A Mutex can hold numbers up to 100",
                    "A Binary Semaphore only runs on 64-bit hardware",
                    "There is no difference at all"
                ],
                "correct_option": 0,
                "explanation": "Strictly speaking, a Mutex includes ownership semantics; semaphores are signaling variables that can be signaled by any thread."
            }
        ]
    },

    "Memory Management & Paging": {
        "summary": "Virtual memory, address translation, paging, and page table hierarchies.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Imagine going to a giant library with 1,000,000 books, but your backpack can only fit 10 books at a time. Do you give up studying? No! You grab the 2 chapters you need today, read them at your desk, and if you need a new book tomorrow, you swap it with one in your backpack. Virtual memory does this for your computer. Programs think they have unlimited continuous memory (Virtual Address Space), while the OS breaks memory into uniform chunks called Pages and maps them to physical RAM Frames.",
                "concepts": [
                    "Logical vs. Physical Address: Program sees clean addresses starting at 0; physical RAM has actual hardware chips.",
                    "Pages & Frames: Memory is divided into fixed-size blocks (typically 4 KB). Pages = virtual; Frames = physical.",
                    "Page Table: The master lookup map that translates Virtual Page Numbers into Physical Frame Numbers.",
                    "Page Fault: What happens when a program accesses a page that is on the SSD rather than loaded into RAM."
                ],
                "example": "If Page size is 4 KB (4096 bytes) and a program requests virtual address 5000: Virtual Page = 5000 // 4096 = Page 1. Offset = 5000 % 4096 = 904. The Page Table looks up Page 1 -> finds Frame 7. Physical address = (7 * 4096) + 904 = 29576.",
                "practice": "Why does fixed-size paging eliminate external fragmentation while still leaving minor internal fragmentation?"
            },
            "Normal": {
                "explanation": "Memory Management Unit (MMU) translates virtual addresses to physical addresses using multi-level page tables and hardware Translation Lookaside Buffers (TLB). Paging eliminates external fragmentation but incurs page table space overhead and translation latency.",
                "concepts": [
                    "TLB (Translation Lookaside Buffer): High-speed hardware associative cache holding recent virtual-to-physical translations.",
                    "Effective Memory Access Time (EMAT): EMAT = (TLB Hit Rate * (TLB Time + Memory Time)) + (TLB Miss Rate * (TLB Time + 2 * Memory Time)).",
                    "Multi-Level Paging: Hierarchical page tables (e.g. 4-level on x86-64) avoid storing massive contiguous page tables in RAM.",
                    "Page Replacement Algorithms: FIFO, Optimal (MIN), LRU (Least Recently Used), and Clock (Second Chance) algorithm."
                ],
                "example": "Given TLB access time = 20ns, RAM access time = 100ns, and TLB hit ratio = 90%: EMAT = 0.90 * (20 + 100) + 0.10 * (20 + 100 + 100) = (0.9 * 120) + (0.1 * 220) = 108 + 22 = 130ns.",
                "practice": "Calculate EMAT if the TLB hit ratio increases to 98% with the same parameters."
            },
            "Advanced": {
                "explanation": "Production 64-bit systems utilize 4-level or 5-level paging (PML4 / PML5), Inverted Page Tables, HugePages (2MB / 1GB) to reduce TLB misses, and kernel Copy-on-Write (CoW) during `fork()` operations.",
                "concepts": [
                    "Copy-on-Write (CoW): Parent and child processes share the same read-only physical pages after `fork()`. Pages duplicate only when written.",
                    "HugePages & TLB Reach: 2MB and 1GB page sizes cover vast memory regions with single TLB entries, critical for databases like Oracle/Postgres.",
                    "Thrashing & Working Set Model: When a system spends more time swapping pages than executing instructions; resolved by checking page fault frequency."
                ],
                "example": "Linux `fork()`: Creates a new process in microseconds because 2GB of parent memory is not copied. Page table entries are simply marked read-only. When child writes byte 1, MMU triggers page fault, and OS duplicates only that 4KB page.",
                "practice": "Explain Belady's Anomaly and prove why the Least Recently Used (LRU) algorithm is immune to it."
            }
        },
        "quiz": [
            {
                "id": 1,
                "question": "What is the primary function of the Translation Lookaside Buffer (TLB)?",
                "options": [
                    "Hardware cache that stores recent virtual-to-physical page translations to accelerate memory access",
                    "Compressing disk sectors for virtual memory swap space",
                    "Allocating CPU registers to thread stacks",
                    "Checking firewall rules for memory packets"
                ],
                "correct_option": 0,
                "explanation": "The TLB caches page table lookups so the CPU does not need to traverse page tables in main memory on every instruction."
            },
            {
                "id": 2,
                "question": "Which fragmentation type is completely eliminated by dividing memory into fixed-size physical frames and pages?",
                "options": ["External Fragmentation", "Internal Fragmentation", "Cache Fragmentation", "Register Fragmentation"],
                "correct_option": 0,
                "explanation": "Paging eliminates external fragmentation because any free frame can be allocated to any process regardless of location."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "What is 'Thrashing' in virtual memory systems?",
                "options": [
                    "A condition where the OS spends almost all of its time swapping pages in and out of disk rather than executing programs",
                    "A CPU fan vibrating at high speed",
                    "A hard drive head crash",
                    "A malicious denial-of-service attack"
                ],
                "correct_option": 0,
                "explanation": "Thrashing occurs when active processes lack enough frames to hold their working sets, causing continuous page faults."
            },
            {
                "id": 2,
                "question": "Why does modern Linux use Copy-on-Write (CoW) when creating a child process with fork()?",
                "options": [
                    "To avoid duplicating memory pages until the parent or child actually modifies them, making fork() instant",
                    "To prevent the child process from ever editing files",
                    "To compress all RAM into swap space",
                    "To encrypt the child process code"
                ],
                "correct_option": 0,
                "explanation": "CoW defers physical page copying until a write occurs, saving massive amounts of RAM and execution time."
            }
        ]
    },

    "File Systems": {
        "summary": "Storage architecture, inodes, file allocation strategies, and disk scheduling.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Think of a hard drive like a giant apartment building with 10,000 storage lockers, but none of the lockers have names on them—only numbers (Locker 0 to Locker 9999). If you want to store a 5-page photo album, where do you put it? A File System is the master directory at the front desk. It remembers: 'MyResume.pdf is stored across Lockers 14, 15, and 18, created on Tuesday, and owned by Himaja.'",
                "concepts": [
                    "File Metadata: Properties of a file (file name, size, owner, creation time, permissions) stored separately from file data.",
                    "Inode (Index Node): In Linux/Unix, a data structure that stores all metadata and block pointers for a file.",
                    "Directory: A special file containing a list of (filename, inode_number) pairs.",
                    "File Allocation: How file blocks are laid out on disk: Contiguous, Linked List, or Indexed."
                ],
                "example": "When you rename a 10GB file from 'video.mp4' to 'movie.mp4' on Linux, it takes 0.001 seconds! The 10GB of video blocks are never moved; the directory entry merely updates the filename pointer to the same inode.",
                "practice": "Why does Contiguous Allocation suffer from external fragmentation on disks?"
            },
            "Normal": {
                "explanation": "File Systems organize unstructured disk blocks into hierarchical directories and files. Unix file systems use Inodes with direct, single-indirect, double-indirect, and triple-indirect block pointers to support both small and massive files efficiently.",
                "concepts": [
                    "Inode Structure: Direct pointers (typically 12) for fast access to small files; indirect pointers for large files.",
                    "Hard Links vs. Symbolic (Soft) Links: Hard link points directly to the inode; Soft link contains a path string to another file.",
                    "Journaling: Writing metadata changes to a circular log before updating the main file system to survive unexpected power crashes.",
                    "Disk Scheduling: SCAN (Elevator), C-SCAN, SSTF (Shortest Seek Time First) algorithms to minimize disk arm movement."
                ],
                "example": "Inode calculation: With 4KB block size and 12 direct pointers, files up to 48KB require zero indirect lookups. A single indirect block contains 4096 / 4 = 1024 pointers, supporting an additional 4MB (1024 * 4KB).",
                "practice": "Calculate the maximum file size supported by an inode with 12 direct, 1 single indirect, 1 double indirect, and 1 triple indirect pointer."
            },
            "Advanced": {
                "explanation": "Enterprise file systems (ZFS, Btrfs, ext4) use Extents instead of individual block pointers, copy-on-write snapshots, cryptographic checksums for silent data corruption detection, and log-structured merge trees.",
                "concepts": [
                    "Extents: Representing contiguous sequences of up to thousands of blocks as a single (start_block, length) pair.",
                    "Copy-on-Write Snapshots: Instant read-only filesystem checkpoints sharing unchanged extents.",
                    "VFS (Virtual File System): Kernel abstraction allowing applications to use identical `open()`/`read()` APIs across ext4, NFS, and FAT32."
                ],
                "example": "ZFS self-healing: Every block has a 256-bit checksum stored in its parent pointer. When reading, if the checksum fails (bit rot), ZFS automatically reconstructs the correct block from mirror/parity drives and repairs the bad sector.",
                "practice": "Explain how Journaling File Systems use Write-Ahead Logging (WAL) and commit records to ensure consistency."
            }
        },
        "quiz": [
            {
                "id": 1,
                "question": "In a Unix-like file system (like Linux ext4), what critical piece of information is NOT stored inside an Inode?",
                "options": [
                    "The File Name (file names are stored in directory files mapping to inode numbers)",
                    "File size in bytes",
                    "File ownership and permissions (chmod)",
                    "Pointers to physical disk data blocks"
                ],
                "correct_option": 0,
                "explanation": "Inodes store all file metadata (size, owner, pointers) EXCEPT the file name. Directory entries map filenames to inode numbers."
            },
            {
                "id": 2,
                "question": "What is the primary difference between a Hard Link and a Soft (Symbolic) Link in Linux?",
                "options": [
                    "A hard link shares the exact same inode number as the original; a soft link is a new file containing the text path of target",
                    "Hard links only work for audio files",
                    "Soft links cannot be deleted",
                    "Hard links use internet bandwidth"
                ],
                "correct_option": 0,
                "explanation": "Hard links point to the same inode (incrementing the reference count); soft links store a file path string."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Why do modern file systems implement 'Journaling'?",
                "options": [
                    "To log planned metadata transactions to disk first, allowing instant crash recovery without lengthy disk scans (fsck)",
                    "To record student grades",
                    "To print files automatically",
                    "To make disks spin at constant velocity"
                ],
                "correct_option": 0,
                "explanation": "Journaling logs atomic state updates so an unexpected power crash can be repaired in seconds by replaying the log."
            },
            {
                "id": 2,
                "question": "What is the primary advantage of Extents over traditional block-by-block pointers?",
                "options": [
                    "Extents represent contiguous blocks using a single range (start, count), drastically shrinking inode metadata size",
                    "Extents make files invisible",
                    "Extents eliminate the need for hard drives",
                    "Extents increase RAM clock speed"
                ],
                "correct_option": 0,
                "explanation": "Extents compact contiguous runs of blocks into a single record, accelerating access and reducing indirect pointer chains."
            }
        ]
    }
}
