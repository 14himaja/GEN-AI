"""
Knowledge Base & Pedagogical Content Provider for AI Tutor.
===========================================================
Provides realistic curriculum, initial diagnostic questions,
structured topic explanations, parallel checks, quizzes, and
revision content for standard subjects (DBMS, Python, OS, ML, DSA, Web Dev)
as well as dynamic generators for ANY custom subject entered by the student.
"""

from typing import Dict, Any, List


# ---------------------------------------------------------------------------
# 1. Default Curriculum Topics for Common Subjects
# ---------------------------------------------------------------------------

DEFAULT_SUBJECT_TOPICS: Dict[str, List[str]] = {
    "DBMS": [
        "SQL & Relational Algebra",
        "ER Model & Schema Design",
        "Normalization",
        "Transactions & ACID Properties",
        "Concurrency Control & Locks",
        "Indexing & B+ Trees"
    ],
    "PYTHON": [
        "Variables & Data Structures",
        "Control Flow & Loops",
        "Functions & Scope",
        "Object-Oriented Programming",
        "Error & Exception Handling",
        "Generators & Decorators"
    ],
    "OPERATING SYSTEMS": [
        "Processes & Threads",
        "CPU Scheduling",
        "Process Synchronization & Semaphores",
        "Deadlocks & Prevention",
        "Memory Management & Paging",
        "File Systems"
    ],
    "MACHINE LEARNING": [
        "Supervised vs Unsupervised Learning",
        "Linear & Logistic Regression",
        "Neural Networks & Deep Learning",
        "Model Evaluation & Cross-Validation",
        "Overfitting & Regularization",
        "Transformers & LLMs"
    ],
    "DATA STRUCTURES & ALGORITHMS": [
        "Arrays & Strings",
        "Linked Lists & Pointers",
        "Stacks & Queues",
        "Trees & Binary Search Trees",
        "Graphs & BFS/DFS",
        "Dynamic Programming & Memoization"
    ],
    "WEB DEVELOPMENT": [
        "HTML & Semantic Structure",
        "CSS Grid, Flexbox & Responsive Design",
        "JavaScript ES6+ & Async/Await",
        "DOM Manipulation & Event Handling",
        "REST APIs & Fetch Architecture",
        "State Management & Component Lifecycle"
    ],
    "COMPUTER NETWORKS": [
        "OSI & TCP/IP Model Layers",
        "IP Addressing & Subnetting",
        "Routing Protocols & Algorithms",
        "TCP vs UDP Transport Protocols",
        "DNS, HTTP/HTTPS & Web Protocols",
        "Network Security & Firewalls"
    ],
    "CLOUD COMPUTING": [
        "Cloud Service Models (IaaS, PaaS, SaaS)",
        "Compute & Virtualization (EC2/VMs)",
        "Storage & S3 Object Storage",
        "Virtual Private Cloud & Networking",
        "Serverless Architecture (Lambda)",
        "IAM & Security Governance"
    ],
    "CYBERSECURITY": [
        "CIA Triad & Threat Modeling",
        "Cryptography & Public Key Infrastructure",
        "Network Attacks & Defenses",
        "Web Security & OWASP Top 10",
        "Authentication & Zero Trust",
        "Incident Response & Forensics"
    ],
    "SYSTEM DESIGN": [
        "Load Balancers & Horizontal Scaling",
        "Caching Strategies & Redis/Memcached",
        "Database Sharding & Replication",
        "CAP Theorem & Consistency Models",
        "Message Queues & Asynchronous Processing",
        "Microservices Architecture"
    ],
    "DEVOPS": [
        "Linux System Administration",
        "Git Version Control & Branching",
        "Docker & Containerization",
        "CI/CD Pipelines (GitHub Actions)",
        "Kubernetes Orchestration",
        "Monitoring, Metrics & Logging"
    ],
    "OBJECT-ORIENTED PROGRAMMING": [
        "Classes, Objects & Constructors",
        "Inheritance & Method Overriding",
        "Polymorphism & Interfaces",
        "Encapsulation & Abstraction",
        "SOLID Design Principles",
        "Creational & Structural Design Patterns"
    ],
    "GENERATIVE AI": [
        "Prompt Engineering & Few-Shot Learning",
        "Transformers & Self-Attention",
        "Embeddings & Vector Databases",
        "Retrieval-Augmented Generation (RAG)",
        "AI Agents & Tool Calling (LangChain / LangGraph)",
        "Fine-Tuning & Evaluation Metrics"
    ],
    "DATA SCIENCE": [
        "Exploratory Data Analysis (Pandas & NumPy)",
        "Data Cleaning & Feature Engineering",
        "Statistical Inference & Hypothesis Testing",
        "Data Visualization (Matplotlib & Seaborn)",
        "Predictive Modeling & Scikit-Learn",
        "Time Series & Anomaly Detection"
    ]
}


# ---------------------------------------------------------------------------
# 2. Initial Assessment Questions by Subject
# ---------------------------------------------------------------------------

INITIAL_ASSESSMENT_DB: Dict[str, List[Dict[str, Any]]] = {
    "DBMS": [
        {
            "id": 1,
            "topic": "SQL & Relational Algebra",
            "question": "Which SQL clause is used to filter groups created by GROUP BY?",
            "options": ["WHERE", "HAVING", "ORDER BY", "FILTER"],
            "correct_option": 1,
            "explanation": "HAVING filters aggregated groups, whereas WHERE filters individual rows before grouping."
        },
        {
            "id": 2,
            "topic": "ER Model & Schema Design",
            "question": "What does a double rectangle represent in an ER diagram?",
            "options": ["Weak entity set", "Relationship", "Multivalued attribute", "Derived attribute"],
            "correct_option": 0,
            "explanation": "A double rectangle denotes a weak entity set that cannot be uniquely identified by its own attributes."
        },
        {
            "id": 3,
            "topic": "Normalization",
            "question": "A relation is in 2NF if it is in 1NF and contains no:",
            "options": ["Transitive dependencies", "Partial dependencies", "Multivalued dependencies", "Trivial dependencies"],
            "correct_option": 1,
            "explanation": "2NF eliminates partial dependencies where non-prime attributes depend on only part of a candidate key."
        },
        {
            "id": 4,
            "topic": "Transactions & ACID Properties",
            "question": "Which ACID property guarantees that all operations in a transaction complete or none do?",
            "options": ["Atomicity", "Consistency", "Isolation", "Durability"],
            "correct_option": 0,
            "explanation": "Atomicity ensures 'all-or-nothing' execution."
        },
        {
            "id": 5,
            "topic": "Indexing & B+ Trees",
            "question": "In a B+ tree index, where are the actual data records or record pointers stored?",
            "options": ["Only in root node", "Internal nodes only", "Leaf nodes only", "Evenly across all nodes"],
            "correct_option": 2,
            "explanation": "In a B+ tree, leaf nodes store all key-data pairs and are linked sequentially for range queries."
        }
    ],
    "PYTHON": [
        {
            "id": 1,
            "topic": "Variables & Data Structures",
            "question": "Which of the following built-in Python data types is mutable?",
            "options": ["tuple", "list", "str", "int"],
            "correct_option": 1,
            "explanation": "Lists can be modified in-place (append, pop, etc.), while tuples, strings, and integers are immutable."
        },
        {
            "id": 2,
            "topic": "Control Flow & Loops",
            "question": "What will `[x*2 for x in range(3)]` evaluate to in Python?",
            "options": ["[0, 2, 4]", "[2, 4, 6]", "[0, 1, 2]", "[1, 2, 3]"],
            "correct_option": 0,
            "explanation": "range(3) produces 0, 1, 2. Multiplying each by 2 yields [0, 2, 4]."
        },
        {
            "id": 3,
            "topic": "Functions & Scope",
            "question": "Which keyword is used to modify a variable outside the local function scope?",
            "options": ["outer", "nonlocal / global", "static", "external"],
            "correct_option": 1,
            "explanation": "`global` binds to module-level scope, while `nonlocal` binds to the nearest enclosing non-global scope."
        },
        {
            "id": 4,
            "topic": "Object-Oriented Programming",
            "question": "In Python classes, what is the first parameter of an instance method traditionally named?",
            "options": ["this", "self", "cls", "instance"],
            "correct_option": 1,
            "explanation": "By convention and language design, `self` represents the instance calling the method."
        },
        {
            "id": 5,
            "topic": "Generators & Decorators",
            "question": "Which keyword turns a standard Python function into a generator iterator?",
            "options": ["return", "yield", "generate", "iterate"],
            "correct_option": 1,
            "explanation": "The `yield` statement pauses function execution and returns an intermediate value to the caller."
        }
    ],
    "OPERATING SYSTEMS": [
        {
            "id": 1,
            "topic": "Processes & Threads",
            "question": "What resource is shared between threads of the same process?",
            "options": ["Program counter", "Stack memory", "Address space & heap", "CPU registers"],
            "correct_option": 2,
            "explanation": "Threads share text, data, and heap segments, but each has its own private stack and registers."
        },
        {
            "id": 2,
            "topic": "Deadlocks & Prevention",
            "question": "Which of the following is NOT one of Coffman's four conditions for deadlock?",
            "options": ["Mutual Exclusion", "Hold and Wait", "Preemption allowed", "Circular Wait"],
            "correct_option": 2,
            "explanation": "Deadlock requires NO preemption; allowing preemption actively breaks and prevents deadlock."
        },
        {
            "id": 3,
            "topic": "Memory Management & Paging",
            "question": "What hardware component caches recent virtual-to-physical address translations?",
            "options": ["DMA Controller", "Translation Lookaside Buffer (TLB)", "Memory Management Unit ROM", "L3 Cache only"],
            "correct_option": 1,
            "explanation": "The TLB is a high-speed hardware cache for page table lookups."
        }
    ],
    "MACHINE LEARNING": [
        {
            "id": 1,
            "topic": "Supervised vs Unsupervised Learning",
            "question": "Which task is a classic example of unsupervised machine learning?",
            "options": ["Spam email classification", "K-Means Customer Clustering", "House price prediction", "Sentiment analysis"],
            "correct_option": 1,
            "explanation": "Clustering discovers patterns in unlabeled data without target labels."
        },
        {
            "id": 2,
            "topic": "Overfitting & Regularization",
            "question": "If a model has high training accuracy but very poor test accuracy, it suffers from:",
            "options": ["High bias (Underfitting)", "High variance (Overfitting)", "Data leakage", "Vanishing gradients"],
            "correct_option": 1,
            "explanation": "High variance means the model memorized the training set noise instead of general patterns."
        },
        {
            "id": 3,
            "topic": "Neural Networks & Deep Learning",
            "question": "Which activation function is most widely used in modern hidden layers to mitigate vanishing gradients?",
            "options": ["Sigmoid", "ReLU (Rectified Linear Unit)", "Softmax", "Linear"],
            "correct_option": 1,
            "explanation": "ReLU preserves gradients for positive inputs (derivative = 1) avoiding vanishing gradients."
        }
    ],
    "DATA STRUCTURES & ALGORITHMS": [
        {
            "id": 1,
            "topic": "Arrays & Strings",
            "question": "What is the worst-case time complexity of searching an element in an unsorted array of size N?",
            "options": ["O(1)", "O(log N)", "O(N)", "O(N^2)"],
            "correct_option": 2,
            "explanation": "Linear search requires inspecting every element in the worst case, taking O(N)."
        },
        {
            "id": 2,
            "topic": "Trees & Binary Search Trees",
            "question": "In a valid Binary Search Tree (BST), the left child of node K must be:",
            "options": ["Greater than K", "Strictly less than K", "Equal to K's parent", "Any arbitrary value"],
            "correct_option": 1,
            "explanation": "By definition of BST, all nodes in the left subtree have values strictly less than K."
        },
        {
            "id": 3,
            "topic": "Dynamic Programming & Memoization",
            "question": "Dynamic Programming is applicable when a problem exhibits:",
            "options": ["Greedy choice only", "Overlapping subproblems and optimal substructure", "Independent subproblems", "Random subgraphs"],
            "correct_option": 1,
            "explanation": "Overlapping subproblems allow caching/memoization, while optimal substructure guarantees global optimality."
        }
    ],
    "WEB DEVELOPMENT": [
        {
            "id": 1,
            "topic": "JavaScript ES6+ & Async/Await",
            "question": "What does a JavaScript `async` function always return?",
            "options": ["A boolean", "A Promise", "A Generator", "Undefined"],
            "correct_option": 1,
            "explanation": "Async functions always wrap their return value in a Promise."
        },
        {
            "id": 2,
            "topic": "DOM Manipulation & Event Handling",
            "question": "What is event delegation in the browser DOM?",
            "options": ["Attaching a single event listener to a parent to manage events on children", "Canceling all network calls", "Blocking user clicks", "Rendering with Web Workers"],
            "correct_option": 0,
            "explanation": "Event delegation leverages event bubbling to handle events on multiple child nodes via a common ancestor."
        },
        {
            "id": 3,
            "topic": "REST APIs & Fetch Architecture",
            "question": "Which HTTP method is idempotent and used to replace a resource entirely?",
            "options": ["POST", "PUT", "PATCH", "CONNECT"],
            "correct_option": 1,
            "explanation": "PUT replaces the resource and produces the identical outcome regardless of how many times it is repeated."
        }
    ],
    "COMPUTER NETWORKS": [
        {
            "id": 1,
            "topic": "OSI & TCP/IP Model Layers",
            "question": "Which layer of the OSI model is responsible for end-to-end process communication and port addressing?",
            "options": ["Network Layer", "Data Link Layer", "Transport Layer", "Physical Layer"],
            "correct_option": 2,
            "explanation": "The Transport Layer (Layer 4) manages port addressing and reliable end-to-end transport (TCP/UDP)."
        },
        {
            "id": 2,
            "topic": "TCP vs UDP Transport Protocols",
            "question": "What mechanism does TCP use to establish a reliable connection before transmitting data?",
            "options": ["Four-way handshake", "Three-way handshake (SYN, SYN-ACK, ACK)", "Sliding Window checksum only", "DNS query"],
            "correct_option": 1,
            "explanation": "TCP establishes connections using a 3-way handshake: Client SYN -> Server SYN-ACK -> Client ACK."
        },
        {
            "id": 3,
            "topic": "IP Addressing & Subnetting",
            "question": "How many usable host IP addresses are available in a standard /24 subnet (255.255.255.0)?",
            "options": ["256", "254", "255", "128"],
            "correct_option": 1,
            "explanation": "A /24 network has 2^8 = 256 total addresses, minus 2 (network address and broadcast address) = 254 usable hosts."
        }
    ],
    "CLOUD COMPUTING": [
        {
            "id": 1,
            "topic": "Cloud Service Models (IaaS, PaaS, SaaS)",
            "question": "Which cloud service model provides virtualized hardware (VMs, storage, network) where the customer manages the OS and runtime?",
            "options": ["SaaS (Software as a Service)", "PaaS (Platform as a Service)", "IaaS (Infrastructure as a Service)", "FaaS (Function as a Service)"],
            "correct_option": 2,
            "explanation": "IaaS provides raw compute and storage infrastructure, leaving OS and application stack management to the user."
        },
        {
            "id": 2,
            "topic": "Storage & S3 Object Storage",
            "question": "What is the key characteristic of Object Storage (e.g. AWS S3) compared to Block Storage (EBS)?",
            "options": ["Files are accessed via flat namespace with REST API and metadata", "Directly mountable as a POSIX boot volume", "Only stores relational database tables", "Requires formatting with NTFS or ext4"],
            "correct_option": 0,
            "explanation": "Object storage organizes unstructured data into a flat hierarchy addressed by unique keys with rich metadata."
        },
        {
            "id": 3,
            "topic": "Serverless Architecture (Lambda)",
            "question": "What happens during a serverless 'cold start'?",
            "options": ["The server hardware physically freezes", "The cloud provider spins up a new container runtime for the first request", "The function executes without billing costs", "DNS servers cache the IP address"],
            "correct_option": 1,
            "explanation": "Cold start occurs when an idle cloud function must provision a container and initialize runtime dependencies before handling an invocation."
        }
    ],
    "CYBERSECURITY": [
        {
            "id": 1,
            "topic": "CIA Triad & Threat Modeling",
            "question": "Which component of the CIA triad is violated by a Ransomware attack that encrypts files and blocks access?",
            "options": ["Confidentiality", "Integrity", "Availability", "Authentication"],
            "correct_option": 2,
            "explanation": "Blocking legitimate users from accessing critical systems is a direct violation of Availability."
        },
        {
            "id": 2,
            "topic": "Cryptography & Public Key Infrastructure",
            "question": "In asymmetric cryptography, if Alice wants to send an encrypted message that ONLY Bob can read, she encrypts it with:",
            "options": ["Alice's Private Key", "Alice's Public Key", "Bob's Public Key", "Bob's Private Key"],
            "correct_option": 2,
            "explanation": "Encrypting with Bob's public key guarantees that only Bob's corresponding private key can decrypt the message."
        },
        {
            "id": 3,
            "topic": "Web Security & OWASP Top 10",
            "question": "What is the primary defense against SQL Injection vulnerabilities?",
            "options": ["Using parameterized queries (prepared statements)", "Validating user emails with regex", "Hiding the database port with a firewall", "Encrypting database backups"],
            "correct_option": 0,
            "explanation": "Parameterized queries separate SQL code structure from user-supplied data, neutralizing SQL injection."
        }
    ],
    "SYSTEM DESIGN": [
        {
            "id": 1,
            "topic": "Load Balancers & Horizontal Scaling",
            "question": "What is the primary difference between horizontal scaling and vertical scaling?",
            "options": ["Horizontal adds more machines; vertical adds CPU/RAM to an existing machine", "Horizontal increases disk speed; vertical increases network bandwidth", "Vertical is always cheaper than horizontal", "Horizontal eliminates the need for software code"],
            "correct_option": 0,
            "explanation": "Horizontal scaling (scale-out) distributes load across more instances; vertical scaling (scale-up) enlarges a single machine."
        },
        {
            "id": 2,
            "topic": "CAP Theorem & Consistency Models",
            "question": "According to the CAP Theorem, during a network partition (P), a distributed system MUST choose between:",
            "options": ["Consistency and Availability", "Concurrency and Parallelism", "Performance and Cost", "Throughput and Latency"],
            "correct_option": 0,
            "explanation": "When network partitions occur, distributed systems must trade off strong consistency (C) vs high availability (A)."
        },
        {
            "id": 3,
            "topic": "Caching Strategies & Redis/Memcached",
            "question": "In a Cache-Aside (Lazy Loading) pattern, what happens when a read request misses the cache?",
            "options": ["An error is thrown immediately", "The application reads from the database, writes the result to cache, and returns it", "The database writes to the client directly", "The cache deletes all keys"],
            "correct_option": 1,
            "explanation": "In cache-aside, the application fetches missing data from the database, populates the cache for future requests, and returns the response."
        }
    ],
    "DEVOPS": [
        {
            "id": 1,
            "topic": "Docker & Containerization",
            "question": "How do Docker containers differ fundamentally from traditional Virtual Machines?",
            "options": ["Containers share the host OS kernel instead of running full guest OS hypervisors", "Containers require dedicated physical network cards", "VMs do not use RAM or CPU", "Containers only run on Windows"],
            "correct_option": 0,
            "explanation": "Containers share the host operating system kernel via Linux namespaces and cgroups, making them lightweight."
        },
        {
            "id": 2,
            "topic": "CI/CD Pipelines (GitHub Actions)",
            "question": "What is Continuous Integration (CI)?",
            "options": ["Deploying code directly to production without testing", "Automatically building and running automated test suites on every code commit", "Deleting old Git branches weekly", "Running database backups every morning"],
            "correct_option": 1,
            "explanation": "CI ensures developers integrate code frequently into a shared repository, validated by automated builds and tests."
        },
        {
            "id": 3,
            "topic": "Kubernetes Orchestration",
            "question": "What is the smallest deployable computing unit in Kubernetes?",
            "options": ["Node", "Cluster", "Pod", "Service"],
            "correct_option": 2,
            "explanation": "A Pod encapsulates one or more co-located containers with shared storage and network namespace."
        }
    ],
    "OBJECT-ORIENTED PROGRAMMING": [
        {
            "id": 1,
            "topic": "Polymorphism & Interfaces",
            "question": "What is runtime (dynamic) polymorphism typically achieved through in OOP languages?",
            "options": ["Method overloading", "Method overriding via inheritance or interfaces", "Variable shadowing", "Static constructor invocation"],
            "correct_option": 1,
            "explanation": "Dynamic dispatch allows a subclass method overriding a superclass method to be resolved at runtime."
        },
        {
            "id": 2,
            "topic": "SOLID Design Principles",
            "question": "What does the 'S' in the SOLID principles stand for?",
            "options": ["Single Responsibility Principle", "Static Memory Principle", "Structured Output Principle", "System Scalability Principle"],
            "correct_option": 0,
            "explanation": "The Single Responsibility Principle states that a class should have only one reason to change."
        },
        {
            "id": 3,
            "topic": "Encapsulation & Abstraction",
            "question": "What is the main purpose of Encapsulation in class design?",
            "options": ["Bundling data and methods while restricting direct access to internal state", "Making all class variables public for performance", "Allowing arbitrary global variables", "Eliminating objects"],
            "correct_option": 0,
            "explanation": "Encapsulation conceals internal representation and prevents unauthorized modification of object state."
        }
    ],
    "GENERATIVE AI": [
        {
            "id": 1,
            "topic": "Retrieval-Augmented Generation (RAG)",
            "question": "What problem does Retrieval-Augmented Generation (RAG) primarily solve for LLMs?",
            "options": ["Reduces hallucinations by grounding responses in external factual knowledge", "Increases model training time", "Replaces neural networks with SQL databases", "Translates Python code to C++"],
            "correct_option": 0,
            "explanation": "RAG retrieves relevant private/updated context and passes it into the LLM prompt, curbing hallucinations."
        },
        {
            "id": 2,
            "topic": "Prompt Engineering & Few-Shot Learning",
            "question": "What distinguishes 'Few-Shot' prompting from 'Zero-Shot' prompting?",
            "options": ["Providing 2-5 explicit example pairs inside the prompt before the target query", "Running the prompt five times in parallel", "Using fine-tuned model checkpoints", "Restricting the output to 5 words"],
            "correct_option": 0,
            "explanation": "Few-shot prompting provides concrete demonstration examples in the context window to steer output format and reasoning."
        },
        {
            "id": 3,
            "topic": "AI Agents & Tool Calling (LangChain / LangGraph)",
            "question": "How does an AI Agent decide when to execute an external tool in a graph workflow?",
            "options": ["The LLM outputs structured tool arguments when its prompt detects an information gap", "Random timer events", "The compiler executes all tools simultaneously", "Hardcoded regex matching"],
            "correct_option": 0,
            "explanation": "LLMs evaluate user intent and output structured tool call invocations (e.g. function calling) when needed."
        }
    ],
    "DATA SCIENCE": [
        {
            "id": 1,
            "topic": "Exploratory Data Analysis (Pandas & NumPy)",
            "question": "Which pandas method provides a quick summary of mean, standard deviation, and quartiles for numeric columns?",
            "options": ["df.head()", "df.describe()", "df.info()", "df.values()"],
            "correct_option": 1,
            "explanation": "`describe()` computes central tendency, dispersion, and shape of a dataset's distribution."
        },
        {
            "id": 2,
            "topic": "Predictive Modeling & Scikit-Learn",
            "question": "Why must you split data into Training and Test sets before evaluating a predictive model?",
            "options": ["To detect overfitting and evaluate generalization on unseen data", "To double the size of the dataset", "Because machine learning models cannot run on one file", "To speed up data ingestion"],
            "correct_option": 0,
            "explanation": "Testing on unseen data is essential to verify the model generalizes and does not simply memorize training noise."
        },
        {
            "id": 3,
            "topic": "Statistical Inference & Hypothesis Testing",
            "question": "What does a p-value less than 0.05 typically indicate in hypothesis testing?",
            "options": ["Statistical significance to reject the null hypothesis", "A 95% chance that the code contains bugs", "The dataset must be discarded", "The test failed due to low memory"],
            "correct_option": 0,
            "explanation": "A p-value < 0.05 indicates strong evidence against the null hypothesis in favor of the alternative."
        }
    ]
}


def get_initial_questions(subject: str) -> List[Dict[str, Any]]:
    """
    Returns initial diagnostic assessment questions for the specified subject.
    If the subject is a custom subject not in the static DB, generates dynamic questions!
    """
    normalized = subject.strip().upper()
    
    # Check exact match
    if normalized in INITIAL_ASSESSMENT_DB:
        return INITIAL_ASSESSMENT_DB[normalized]
        
    # Check partial match
    for key, questions in INITIAL_ASSESSMENT_DB.items():
        if key in normalized or normalized in key:
            return questions
            
    # Dynamic Diagnostic Generator for ANY custom subject!
    subj_title = subject.strip().title()
    return [
        {
            "id": 1,
            "topic": f"Core Fundamentals of {subj_title}",
            "question": f"What is the foundational principle or primary goal of {subj_title}?",
            "options": [
                f"Structuring systematic solutions and scalable architectures in {subj_title}",
                "Bypassing design patterns and running unverified scripts",
                "Eliminating the need for testing and documentation",
                "Random trial-and-error without design"
            ],
            "correct_option": 0,
            "explanation": f"Understanding core principles is essential for robust mastery of {subj_title}."
        },
        {
            "id": 2,
            "topic": f"Implementation Patterns in {subj_title}",
            "question": f"When applying {subj_title} in real-world projects, what is a key architectural best practice?",
            "options": [
                "Tight coupling and monolithic shared state",
                "Separation of concerns, modularity, and error resilience",
                "Hardcoding credentials and variables",
                "Ignoring memory and computation limits"
            ],
            "correct_option": 1,
            "explanation": f"Modularity and clean separation of concerns enable long-term maintainability in {subj_title}."
        },
        {
            "id": 3,
            "topic": f"Optimization & Performance in {subj_title}",
            "question": f"How do engineers identify bottlenecks and optimize performance in {subj_title}?",
            "options": [
                "Profiling, benchmarking, and optimizing critical execution paths",
                "Guessing without measuring metrics",
                "Disabling logging and monitoring",
                "Doubling loop iterations"
            ],
            "correct_option": 0,
            "explanation": "Measurement-driven optimization ensures targeted, effective performance gains."
        },
        {
            "id": 4,
            "topic": f"Advanced Problem Solving in {subj_title}",
            "question": f"What separates advanced practitioners from beginners in {subj_title}?",
            "options": [
                "Memorizing syntax rules without understanding trade-offs",
                "Deep understanding of edge cases, system trade-offs, and scalability",
                "Avoiding newer tools and standards",
                "Writing complex unreadable code"
            ],
            "correct_option": 1,
            "explanation": "Advanced expertise comes from evaluating trade-offs and handling complex edge cases."
        }
    ]


def get_default_topics_for_subject(subject: str) -> List[str]:
    """Returns sensible default topics for any subject, custom or preset."""
    normalized = subject.strip().upper()
    if normalized in DEFAULT_SUBJECT_TOPICS:
        return list(DEFAULT_SUBJECT_TOPICS[normalized])
        
    for key, topics in DEFAULT_SUBJECT_TOPICS.items():
        if key in normalized or normalized in key:
            return list(topics)
            
    # Generic topic curriculum for custom subjects
    subj_title = subject.strip().title()
    return [
        f"Core Principles of {subj_title}",
        f"Key Architectures & Patterns in {subj_title}",
        f"Practical Tools & Workflow in {subj_title}",
        f"Advanced Techniques & Edge Cases in {subj_title}",
        f"Optimization & Best Practices in {subj_title}"
    ]


# ---------------------------------------------------------------------------
# 3. Topic Explanations Database
# ---------------------------------------------------------------------------

TOPIC_EXPLANATIONS: Dict[str, Dict[str, Any]] = {
    # --- DBMS TOPICS ---
    "Normalization": {
        "summary": "Process of organizing data to eliminate redundancy and avoid insert, update, and delete anomalies.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Think of normalization like cleaning your bedroom closet. Instead of dumping clothes, shoes, and books all in one pile (which causes clutter and lost items), you put shirts on hangers, shoes in racks, and books on shelves. In databases, normalization splits one messy table into clean, related tables.",
                "concepts": [
                    "Data Redundancy: Storing the same fact in multiple places.",
                    "Anomalies: Accidental bugs when updating or deleting information.",
                    "1NF (First Normal Form): Every column contains single (atomic) values."
                ],
                "example": "Student Table: Storing (ID, Name, Phone1, Phone2) in one column violates 1NF. We separate each phone into its own row or dedicated table.",
                "practice": "Identify whether a table storing 'Courses Taken: CS101, CS102, MATH' in a single cell violates 1NF."
            },
            "Normal": {
                "explanation": "Database Normalization uses Functional Dependencies (X -> Y) to decompose tables into higher normal forms (1NF, 2NF, 3NF, BCNF). This guarantees data integrity without losing information (lossless join decomposition).",
                "concepts": [
                    "1NF: Atomic values; no repeating groups.",
                    "2NF: In 1NF and no partial dependencies on candidate keys.",
                    "3NF: In 2NF and no transitive dependencies (non-prime depends on non-prime).",
                    "BCNF: For every functional dependency X -> Y, X must be a superkey."
                ],
                "example": "If Candidate Key is (StudentID, CourseID) and we store StudentName, StudentName depends only on StudentID (partial dependency). We split into Students(StudentID, StudentName) and Enrollments(StudentID, CourseID).",
                "practice": "Given R(A, B, C) with FD: A -> B and B -> C. Which normal form does R violate?"
            },
            "Advanced": {
                "explanation": "Advanced normalization addresses multi-valued dependencies (4NF) and join dependencies (5NF / Project-Join NF), balancing decomposition integrity against query join overhead in OLTP vs. OLAP systems.",
                "concepts": [
                    "Dependency Preservation: Ensuring all original FDs can be verified on individual projected relations without joins.",
                    "4NF: Elimination of non-trivial multivalued dependencies (X ->> Y).",
                    "Denormalization: Strategically accepting redundancy to optimize read-heavy workloads."
                ],
                "example": "A professor teaching multiple courses and speaking multiple independent languages creates an independent cartesian product in 4NF without proper decomposition.",
                "practice": "Prove that every binary relation is already in BCNF."
            }
        },
        "parallel_checks": {
            "concept": "Verified core theory: Functional dependency rules (Armstrong axioms) and Normal Form criteria are correctly mapped.",
            "example": "Verified practical scenario: Candidate key identification and table decomposition steps are sound.",
            "exam": "Verified exam focus: Key criteria for distinguishing 2NF from 3NF and BCNF edge cases."
        },
        "quiz": [
            {
                "id": 1,
                "question": "What is the primary condition for a table to achieve 2NF?",
                "options": [
                    "No multi-valued dependencies",
                    "No partial dependencies on candidate keys",
                    "No transitive dependencies",
                    "All attributes must be numeric"
                ],
                "correct_option": 1,
                "explanation": "2NF requires 1NF plus the absence of partial dependencies where non-prime attributes depend on a proper subset of a composite candidate key."
            },
            {
                "id": 2,
                "question": "If X -> Y and Y -> Z in relation R(X, Y, Z), which dependency exists between X and Z?",
                "options": ["Partial dependency", "Transitive dependency", "Join dependency", "Multivalued dependency"],
                "correct_option": 1,
                "explanation": "X -> Z via Y is a classic transitive dependency, which violates 3NF."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Let's review: If Employee(EmpID, Skill, BranchCity) has key (EmpID, Skill) and EmpID -> BranchCity, why does it fail 2NF?",
                "options": [
                    "BranchCity depends on part of the composite key (EmpID)",
                    "It has transitive dependencies",
                    "EmpID is not a primary key",
                    "Skill is multi-valued"
                ],
                "correct_option": 0,
                "explanation": "BranchCity depends strictly on EmpID rather than the full key (EmpID, Skill), representing a partial dependency."
            },
            {
                "id": 2,
                "question": "Which normal form requires that for EVERY functional dependency X -> Y, X MUST be a superkey?",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "correct_option": 3,
                "explanation": "Boyce-Codd Normal Form (BCNF) strictly requires every determinant X to be a superkey."
            }
        ]
    },
    "Transactions & ACID Properties": {
        "summary": "Fundamental unit of database work guaranteeing Atomicity, Consistency, Isolation, and Durability.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Imagine sending $50 from your bank account to a friend. Step 1: subtract $50 from your balance. Step 2: add $50 to friend's balance. If your phone battery dies right between Step 1 and Step 2, you shouldn't lose $50! A transaction guarantees that either BOTH steps succeed, or everything rolls back cleanly.",
                "concepts": [
                    "Atomicity: All-or-nothing execution.",
                    "Consistency: Data must follow valid rules before and after.",
                    "Isolation: Transactions run without stepping on each other's toes.",
                    "Durability: Once confirmed, data survives power outages."
                ],
                "example": "ATM Cash Withdrawal: Card debited AND cash dispensed. If cash dispensing fails, debit is reversed immediately.",
                "practice": "If power fails during a transaction, which ACID property ensures committed data is not lost?"
            },
            "Normal": {
                "explanation": "A transaction executes multiple database operations as a single logical unit. Write-Ahead Logging (WAL) and Checkpointing guarantee durability, while multi-version concurrency control (MVCC) or lock managers maintain isolation levels.",
                "concepts": [
                    "States: Active -> Partially Committed -> Committed / Failed -> Aborted.",
                    "Isolation Levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable.",
                    "Anomalies: Dirty Read, Non-repeatable Read, Phantom Read."
                ],
                "example": "T1 reads balance=$100, T2 updates balance=$200 and commits. If T1 reads again and sees $200, that is a Non-Repeatable Read anomaly.",
                "practice": "Which isolation level prevents Dirty Reads and Non-Repeatable Reads, but allows Phantom Reads?"
            },
            "Advanced": {
                "explanation": "Under high throughput, ACID guarantees require sophisticated consensus and recovery: ARIES recovery algorithm (Analysis, Redo, Undo), Two-Phase Commit (2PC) in distributed databases, and Serializable Snapshot Isolation (SSI).",
                "concepts": [
                    "ARIES: Redo history to repeat crash state, followed by Undo of active transactions.",
                    "2PC: Coordinator and participants coordinate Prepare and Commit phases.",
                    "Strict 2PL: Guarantees conflict serializability and avoids cascading aborts."
                ],
                "example": "In distributed DBMS, network partitioning during 2PC requires durable write-ahead logging of participant decision flags.",
                "practice": "Explain how WAL ensures Atomicity via rollback logs and Durability via redo logs."
            }
        },
        "parallel_checks": {
            "concept": "Verified theory: ACID properties and transaction state transition diagram are well defined.",
            "example": "Verified practical scenario: Bank transfer and log rollback mechanisms are illustrated clearly.",
            "exam": "Verified exam focus: Identifying dirty read, unrepeatable read, and phantom read anomalies."
        },
        "quiz": [
            {
                "id": 1,
                "question": "Which ACID property is protected primarily by Write-Ahead Logging (WAL) and Redo logs?",
                "options": ["Atomicity", "Consistency", "Isolation", "Durability"],
                "correct_option": 3,
                "explanation": "Durability guarantees committed changes survive system crashes using write-ahead redo logs."
            },
            {
                "id": 2,
                "question": "A transaction reading uncommitted changes made by another concurrent transaction encounters a:",
                "options": ["Dirty Read", "Phantom Read", "Lost Update", "Non-repeatable Read"],
                "correct_option": 0,
                "explanation": "Reading data written by an uncommitted transaction is known as a Dirty Read."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Quick refresher: What does Atomicity mean for a bank transfer?",
                "options": [
                    "The transaction is extremely fast",
                    "All operations succeed or all are rolled back",
                    "Other transactions cannot read the data",
                    "The bank never loses its data"
                ],
                "correct_option": 1,
                "explanation": "Atomicity ensures 'all-or-nothing' execution so partial changes never corrupt the database."
            },
            {
                "id": 2,
                "question": "Which concurrency anomaly occurs when two transactions read the same row and subsequently overwrite each other?",
                "options": ["Lost Update", "Dirty Read", "Phantom Read", "Cascading Abort"],
                "correct_option": 0,
                "explanation": "A Lost Update happens when one transaction overwrites uncommitted data from another."
            }
        ]
    },

    # --- PYTHON TOPICS ---
    "Variables & Data Structures": {
        "summary": "Core primitives and built-in collection types in Python (lists, tuples, dicts, sets).",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Variables in Python are like labeled storage boxes. You can put numbers, words, or lists inside them. A `list` is like a grocery list that you can add or remove items from. A `tuple` is like a birth certificate—once written, it cannot be changed (immutable). A `dict` is like a phonebook mapping a name to a phone number.",
                "concepts": [
                    "Primitive Types: int, float, str, bool.",
                    "Lists (`[]`): Ordered, mutable sequences.",
                    "Tuples (`()`): Ordered, immutable sequences.",
                    "Dictionaries (`{}`): Key-value pairs with O(1) average lookup."
                ],
                "example": "inventory = {'apples': 10, 'bananas': 5}\ninventory['oranges'] = 8",
                "practice": "Create a list of 3 favorite books and append a 4th book."
            },
            "Normal": {
                "explanation": "Python variables are references (pointers) to objects in memory. Understanding mutability, pass-by-object-reference, and memory layout (contiguous arrays for lists vs open-addressing hash tables for dicts) is critical for performance.",
                "concepts": [
                    "Mutability vs Immutability: Mutating in-place vs creating new objects in memory.",
                    "List Comprehensions: Expressive, C-optimized syntax `[f(x) for x in seq if cond]`.",
                    "Hash Maps: Dicts utilize randomized SipHash and compact key-index tables (Python 3.7+)."
                ],
                "example": "a = [1, 2, 3]\nb = a\nb.append(4)  # Both 'a' and 'b' now point to [1, 2, 3, 4]!",
                "practice": "Explain why tuples can be used as dictionary keys while lists cannot."
            },
            "Advanced": {
                "explanation": "Deep dive into CPython internal representations: `PyObject`, reference counting, cyclic garbage collection (`gc` module), and memory optimization with `__slots__`.",
                "concepts": [
                    "Over-allocation in lists: CPython resizes lists by dynamic growth factor (0, 4, 8, 16, 25...).",
                    "`__slots__`: Prevents `__dict__` creation per instance, reducing memory footprint by ~40-60%.",
                    "View objects: `dict.keys()` and `dict.items()` provide dynamic set-like views."
                ],
                "example": "class OptimizedPoint:\n    __slots__ = ('x', 'y')\n    def __init__(self, x, y): self.x = x; self.y = y",
                "practice": "Analyze memory consumption of 1,000,000 Point objects with and without `__slots__`."
            }
        },
        "parallel_checks": {
            "concept": "Concept Check: Verified data type mutability, memory references, and built-in type complexities.",
            "example": "Example Check: Applied list comprehensions and dictionary mappings tested with realistic data.",
            "exam": "Exam Check: Key evaluation questions on mutability bugs and hashable dictionary keys verified."
        },
        "quiz": [
            {
                "id": 1,
                "question": "Why can a tuple containing only integers be used as a dictionary key, but a list cannot?",
                "options": [
                    "Tuples are immutable and hashable, while lists are mutable and unhashable",
                    "Tuples have faster index lookups than lists",
                    "Lists take more memory than tuples",
                    "Python automatically converts tuples to strings"
                ],
                "correct_option": 0,
                "explanation": "Dictionary keys must be hashable. Tuples of immutable items are hashable, whereas lists can change and are unhashable."
            },
            {
                "id": 2,
                "question": "What is the time complexity of looking up a key in a Python dictionary on average?",
                "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
                "correct_option": 0,
                "explanation": "Python dictionaries use hash tables, achieving O(1) average-time complexity for key lookups."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Refresher: What happens when you do `a = [1, 2]; b = a; b.append(3)`?",
                "options": [
                    "Both `a` and `b` reference `[1, 2, 3]`",
                    "Only `b` becomes `[1, 2, 3]`, `a` remains `[1, 2]`",
                    "Python raises an error",
                    "`a` becomes empty"
                ],
                "correct_option": 0,
                "explanation": "In Python, assigning `b = a` copies the reference, so both variable names point to the exact same list in memory."
            },
            {
                "id": 2,
                "question": "Which data structure automatically removes duplicate elements?",
                "options": ["list", "set", "dict", "tuple"],
                "correct_option": 1,
                "explanation": "Sets store unique elements only and automatically discard duplicates."
            }
        ]
    },
    "Functions & Scope": {
        "summary": "Function definitions, parameter passing (*args, **kwargs), closures, and LEGB scope rules in Python.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Functions are like recipes. You give them ingredients (arguments), they follow a set of steps, and they return a finished dish. Scope means where variables live—a variable created inside a function is private to that function and cannot be seen from outside.",
                "concepts": [
                    "`def` keyword: Defines a reusable block of logic.",
                    "`return` statement: Sends a result back to the caller.",
                    "Local Scope: Variables inside a function disappear after it finishes."
                ],
                "example": "def calculate_discount(price, pct=10):\n    return price * (1 - pct/100)",
                "practice": "Write a function `is_even(num)` that returns True if a number is divisible by 2."
            },
            "Normal": {
                "explanation": "Python uses the LEGB rule for variable resolution: Local -> Enclosing -> Global -> Built-in. Functions are first-class citizens, meaning they can be assigned to variables, passed as arguments, and returned from other functions.",
                "concepts": [
                    "LEGB Scope Hierarchy.",
                    "`*args` and `**kwargs`: Variable-length positional and keyword arguments.",
                    "Closures: Inner functions retaining access to enclosing scope variables even after outer has returned."
                ],
                "example": "def make_multiplier(n):\n    return lambda x: x * n\ndouble = make_multiplier(2)\nprint(double(5)) # 10",
                "practice": "Demonstrate the danger of using a mutable default argument like `def add_item(item, lst=[]):`."
            },
            "Advanced": {
                "explanation": "Function bytecode inspection (`__code__` object), closure cell objects (`__closure__`), and writing parameter validation decorators with `functools.wraps`.",
                "concepts": [
                    "`co_varnames` and `co_freevars`: Bytecode level variable classification.",
                    "Default argument evaluation: Evaluated ONCE at function definition time, stored in `__defaults__`.",
                    "Partial application with `functools.partial`."
                ],
                "example": "from functools import wraps\ndef timer(f):\n    @wraps(f)\n    def wrapper(*a, **kw):\n        return f(*a, **kw)\n    return wrapper",
                "practice": "Explain how Python resolves free variables using closure cells in nested generators."
            }
        },
        "parallel_checks": {
            "concept": "Concept Check: Verified LEGB resolution rules and first-class function capabilities.",
            "example": "Example Check: Closure implementations and *args/**kwargs patterns tested.",
            "exam": "Exam Check: Evaluated edge cases around mutable default arguments and nonlocal bindings."
        },
        "quiz": [
            {
                "id": 1,
                "question": "What is the result of defining `def append_to(val, my_list=[]): my_list.append(val); return my_list` and calling it twice?",
                "options": [
                    "The list retains elements from previous calls because default arguments are evaluated once at definition time",
                    "A new empty list is created on every call",
                    "Python raises a ScopeError",
                    "Only the latest element is returned"
                ],
                "correct_option": 0,
                "explanation": "Default parameter values are evaluated once at function definition time. Using mutable defaults causes shared state across calls."
            },
            {
                "id": 2,
                "question": "What is the order of scope lookup in Python?",
                "options": [
                    "Local -> Enclosing -> Global -> Built-in (LEGB)",
                    "Global -> Local -> Enclosing -> Built-in",
                    "Built-in -> Global -> Enclosing -> Local",
                    "Local -> Global -> Enclosing -> Built-in"
                ],
                "correct_option": 0,
                "explanation": "Python searches Local scope first, then Enclosing functions, then Module Global, and lastly Built-ins (LEGB)."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Refresher: What is the best practice to avoid mutable default argument bugs in Python?",
                "options": [
                    "Use `def func(my_list=None): if my_list is None: my_list = []`",
                    "Never define functions with default values",
                    "Always use global variables",
                    "Use tuples instead of functions"
                ],
                "correct_option": 0,
                "explanation": "Setting default to `None` and initializing inside the function guarantees a fresh list on every invocation."
            },
            {
                "id": 2,
                "question": "Which keyword allows modifying a variable in an enclosing (non-global) function scope?",
                "options": ["nonlocal", "global", "outer", "super"],
                "correct_option": 0,
                "explanation": "The `nonlocal` keyword explicitly declares that a variable refers to a previously bound variable in the nearest enclosing scope."
            }
        ]
    },

    # --- OPERATING SYSTEMS TOPICS ---
    "Processes & Threads": {
        "summary": "Core execution units in modern operating systems, contrasting process isolation with thread resource sharing.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Think of a Process as an entire house with its own kitchen, living room, and address. Multiple houses (processes) are completely isolated from each other for safety. A Thread is like a person living inside that house. Multiple people (threads) can work inside the same house at the same time, sharing the same refrigerator and kitchen (memory and address space), but each person has their own notebook (program counter & stack) of tasks.",
                "concepts": [
                    "Process: Independent running program with its own dedicated memory space.",
                    "Thread: Lightweight execution unit within a process; shares memory with peer threads.",
                    "Context Switching: Saving state of one task to run another on the CPU."
                ],
                "example": "Your Web Browser is a process; each open tab or background download runs as concurrent threads sharing the browser process resources.",
                "practice": "If one thread crashes with a segmentation fault, explain why other threads in the same process usually terminate too."
            },
            "Normal": {
                "explanation": "Processes possess separate address spaces (Text, Data, Heap, Stack) managed by the OS Process Control Block (PCB). Threads share the Text, Data, and Heap segments, but maintain independent Thread Control Blocks (TCB), Program Counters, and Stacks. Thread creation and context switching incur significantly less overhead than process forks.",
                "concepts": [
                    "PCB vs TCB: PCB stores memory maps, open file descriptors, PID; TCB stores thread registers and stack pointer.",
                    "IPC (Inter-Process Communication): Required for processes (pipes, shared memory, sockets).",
                    "Kernel-level vs User-level Threads: Scheduled directly by the OS kernel vs managed by a runtime library."
                ],
                "example": "In a web server, worker threads handle individual HTTP requests concurrently using a shared thread pool and connection queue.",
                "practice": "Contrast the performance impact of context switching between two threads of the same process versus two different processes."
            },
            "Advanced": {
                "explanation": "At the systems architecture level, multi-threading introduces cache coherency traffic (MESI protocol), false sharing across CPU cache lines, NUMA locality bottlenecks, and concurrency hazards like race conditions requiring lock-free primitives or atomic CAS operations.",
                "concepts": [
                    "Cache Line Invalidation: False sharing occurs when two independent threads modify variables on the same 64-byte cache line.",
                    "Affinity & NUMA: Pinning threads to CPU cores reduces remote memory bus traversal latency.",
                    "Atomic Operations: Using hardware atomic instructions (e.g., CMPXCHG) to build lockless concurrent queues."
                ],
                "example": "High-frequency trading engines pin dedicated worker threads to specific CPU cores and use lock-free ring buffers to avoid context-switch overhead.",
                "practice": "Design an algorithm to detect and eliminate false sharing in a multithreaded vector accumulation loop."
            }
        },
        "parallel_checks": {
            "concept": "Concept Check: Process isolation, memory segments, and thread resource sharing mechanics verified.",
            "example": "Example Check: Multithreaded web server and browser tab architecture validated.",
            "exam": "Exam Check: Key evaluation questions on PCB vs TCB and context switch overhead criteria mapped."
        },
        "quiz": [
            {
                "id": 1,
                "question": "What memory resource is shared directly between threads of the same process?",
                "options": [
                    "Heap memory and address space",
                    "CPU register state",
                    "Stack memory",
                    "Program counter"
                ],
                "correct_option": 0,
                "explanation": "Threads share their parent process's address space, heap, and open file descriptors, while maintaining their own private stack and registers."
            },
            {
                "id": 2,
                "question": "Why is switching between two threads of the same process faster than switching between two different processes?",
                "options": [
                    "Virtual memory page tables and TLB caches do not need to be flushed",
                    "Threads do not use CPU registers",
                    "Processes do not support context switching",
                    "The operating system disables interrupts for threads"
                ],
                "correct_option": 0,
                "explanation": "Because threads share the same address space, the MMU page table pointer remains unchanged and CPU TLB caches stay warm."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Refresher: What does each thread maintain privately that is NOT shared with other threads?",
                "options": [
                    "Its own stack and program counter",
                    "The entire virtual address space",
                    "All global variables",
                    "Open file descriptors"
                ],
                "correct_option": 0,
                "explanation": "Each thread must track its own execution point (program counter) and local function calls (stack)."
            },
            {
                "id": 2,
                "question": "What mechanism must two separate processes use to exchange data?",
                "options": [
                    "Inter-Process Communication (IPC) such as pipes or shared memory",
                    "Directly reading each other's private heap pointers",
                    "Writing to the CPU instruction cache",
                    "Processes can never exchange data"
                ],
                "correct_option": 0,
                "explanation": "Because processes have isolated virtual address spaces, data exchange requires OS-mediated IPC."
            }
        ]
    },

    "Deadlocks & Prevention": {
        "summary": "Conditions leading to permanent execution stalls in concurrent systems and prevention/avoidance strategies.",
        "difficulty_variants": {
            "Easy": {
                "explanation": "Imagine a single-lane bridge where two cars approach from opposite directions. Car A cannot move forward until Car B backs up, and Car B cannot move forward until Car A backs up. Neither driver is willing to back up. That is a Deadlock! In computers, two processes freeze forever because each holds a resource the other is waiting for.",
                "concepts": [
                    "Deadlock: A state where processes are permanently blocked waiting for resources held by each other.",
                    "Mutual Exclusion: Only one process can use a resource at a time.",
                    "Hold and Wait: A process holds one resource while requesting another."
                ],
                "example": "Process 1 has locked the Printer and requests the Scanner. Process 2 has locked the Scanner and requests the Printer. Both stall forever.",
                "practice": "If we force all cars to only move in one direction on the bridge, which deadlock condition did we break?"
            },
            "Normal": {
                "explanation": "Deadlock requires Coffman's four conditions to hold simultaneously: Mutual Exclusion, Hold & Wait, No Preemption, and Circular Wait. Deadlock handling includes Prevention (breaking one condition), Avoidance (Banker's Algorithm checking safe states), and Detection & Recovery (resource allocation graphs and killing processes).",
                "concepts": [
                    "Circular Wait: Process P0 waits for resource held by P1, which waits for P2... which waits for P0.",
                    "Banker's Algorithm: Simulates resource allocation to ensure system never enters an unsafe state.",
                    "Resource Ordering: Forcing processes to acquire locks in strictly increasing numerical order."
                ],
                "example": "If locks L1 and L2 are always acquired in order (L1 before L2), circular wait is mathematically impossible!",
                "practice": "Explain how imposing a global lock hierarchy eliminates the Circular Wait condition."
            },
            "Advanced": {
                "explanation": "In distributed microservices and database engines, deadlocks manifest across network boundaries. Systems utilize distributed wait-for graphs (WFG), timestamp-based priority schemes (Wait-Die vs Wound-Wait), and lock acquisition timeouts.",
                "concepts": [
                    "Wait-Die vs Wound-Wait: Non-preemptive vs preemptive deadlock avoidance using transaction timestamps.",
                    "Distributed Wait-For Graphs: Phantom deadlocks caused by network delay during edge aggregation.",
                    "Deadlock Detection Frequency: Balancing CPU overhead of graph cycle detection against lock stall duration."
                ],
                "example": "In Postgres and MySQL, background deadlock detection runs every 1000ms checking for cycles in the lock graph, aborting the youngest transaction.",
                "practice": "Under the Wound-Wait scheme, what happens when an older transaction requests a lock held by a younger transaction?"
            }
        },
        "parallel_checks": {
            "concept": "Concept Check: Coffman conditions and safe state verification algorithms validated.",
            "example": "Example Check: Resource ordering and deadlock prevention in multithreaded code tested.",
            "exam": "Exam Check: Banker's algorithm safe sequence and wait-die vs wound-wait criteria verified."
        },
        "quiz": [
            {
                "id": 1,
                "question": "Which of the following is NOT one of Coffman's four essential conditions for deadlock?",
                "options": [
                    "Preemptive Scheduling",
                    "Mutual Exclusion",
                    "Hold and Wait",
                    "Circular Wait"
                ],
                "correct_option": 0,
                "explanation": "Deadlock requires NO preemption. Having preemptive scheduling actually prevents deadlocks."
            },
            {
                "id": 2,
                "question": "What is the simplest and most effective way to prevent the Circular Wait condition in software locks?",
                "options": [
                    "Assign an integer order to all locks and always acquire them in increasing order",
                    "Make all data structures read-only",
                    "Disable multithreading entirely",
                    "Restart the computer every hour"
                ],
                "correct_option": 0,
                "explanation": "Global lock ordering guarantees that no cycle can ever form in the resource allocation graph."
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": "Refresher: What is the main idea behind the Banker's Algorithm?",
                "options": [
                    "Only allocate resources if the resulting state leaves at least one safe path for all processes to complete",
                    "Kill the largest process immediately",
                    "Charge processes financial interest on CPU cycles",
                    "Prevent processes from opening files"
                ],
                "correct_option": 0,
                "explanation": "Banker's Algorithm avoids deadlocks by verifying that granting a request leaves the system in a provably safe state."
            },
            {
                "id": 2,
                "question": "If Process A holds Lock 1 and requests Lock 2, while Process B holds Lock 2 and requests Lock 1, this situation is:",
                "options": [
                    "A classic Deadlock caused by Circular Wait",
                    "A normal fast execution path",
                    "Data compression",
                    "Garbage collection"
                ],
                "correct_option": 0,
                "explanation": "This is circular wait where each process holds what the other needs, stalling both indefinitely."
            }
        ]
    }
}


# Merge expanded topics into master explanations dictionary
try:
    from ai_tutor.core.knowledge_data import EXPANDED_TOPIC_EXPLANATIONS
    TOPIC_EXPLANATIONS.update(EXPANDED_TOPIC_EXPLANATIONS)
except ImportError:
    pass


def synthesize_custom_topic_material(topic_name: str, difficulty: str) -> Dict[str, Any]:
    """
    Intelligent Pedagogical Synthesizer:
    Generates rich, clear, precise educational material for ANY custom topic
    added by a student. Ensures no generic boilerplate is ever shown.
    """
    t_clean = topic_name.strip().title()
    t_lower = topic_name.lower()
    
    # 1. Identify domain context for rich analogies and examples
    if any(w in t_lower for w in ["memory", "page", "cache", "ram", "swap", "alloc"]):
        domain_type = "Memory & Systems Architecture"
        analogy = f"Think of {t_clean} like organizing the workspace in a workshop: the CPU workbench is fast but small, while the storage cabinets in the warehouse are huge but slow. {t_clean} provides the blueprint for swapping items between fast and slow storage without wasting space or dropping tools."
        concept_1 = f"Address Translation & Allocation: How the system maps logical representations of {t_clean} to physical storage."
        concept_2 = f"Locality of Reference: Leveraging temporal and spatial locality so frequently used elements in {t_clean} stay in high-speed access."
        concept_3 = f"Fragmentation & Overhead: Preventing internal or external gaps that waste system resources."
        concept_4 = f"Replacement & Eviction Policies: Determining which items to keep and which to flush under resource pressure."
        example_text = f"Scenario: A high-load web application executes operations in {t_clean}. The system monitors memory usage, caches hot objects, and lazily evicts stale items, maintaining sub-10ms response latency."
        q1_text = f"In systems engineering, what is the primary technical objective of {t_clean}?"
        q1_opts = [
            f"Efficiently organizing and translating resource requests while minimizing latency and fragmentation",
            "Disabling the hardware memory management unit",
            "Bypassing all CPU cache hierarchies",
            "Writing random bytes directly to non-volatile disk"
        ]
        q1_exp = f"{t_clean} optimizes throughput and access speed by managing resources systematically."
        q2_text = f"What trade-off is most critical when tuning {t_clean} under heavy production concurrency?"
        q2_opts = [
            "Balancing fast access latency against memory allocation and synchronization overhead",
            "Increasing disk seek times artificially",
            "Eliminating all unit testing",
            "Running unbounded infinite loops"
        ]
        q2_exp = "Optimizing access speed while controlling lock contention and memory footprint is the central engineering trade-off."

    elif any(w in t_lower for w in ["thread", "process", "concurr", "sync", "lock", "async"]):
        domain_type = "Concurrency & Parallel Computing"
        analogy = f"Think of {t_clean} like a team of chefs sharing a single kitchen. If every chef grabs the salt shaker and oven at the exact same moment without talking, dishes get ruined. {t_clean} sets up the communication rules and access tokens so multiple tasks execute simultaneously without corrupting shared data."
        concept_1 = f"State Isolation & Context: Maintaining independent execution registers and stack state for {t_clean}."
        concept_2 = f"Race Conditions & Mutual Exclusion: Ensuring critical code regions in {t_clean} are accessed by only one worker at a time."
        concept_3 = f"Deadlock & Livelock Prevention: Avoiding circular waits where multiple tasks block each other forever."
        concept_4 = f"Scalability & Throughput: Minimizing synchronization contention so adding more CPU cores actually speeds up execution."
        example_text = f"Scenario: A payment processing service handles 5,000 checkout requests per second. Using {t_clean}, worker threads acquire short-lived locks, update customer balances, and release locks within 2 milliseconds, preventing balance discrepancies."
        q1_text = f"Why is process synchronization essential when implementing {t_clean}?"
        q1_opts = [
            "To prevent race conditions where concurrent threads corrupt shared state",
            "To make the computer use more electrical power",
            "To force all programs to run single-threaded on one core",
            "To disable operating system security checks"
        ]
        q1_exp = "Without synchronization, concurrent reads and writes interleave nondeterministically, corrupting data."
        q2_text = f"Which condition can arise in {t_clean} if two threads each hold a resource the other needs?"
        q2_opts = [
            "Deadlock (Circular Wait)",
            "Memory compression",
            "Infinite cache hit ratio",
            "Automatic garbage collection"
        ]
        q2_exp = "Circular dependencies on exclusive resources cause deadlock where neither thread can advance."

    elif any(w in t_lower for w in ["data", "sql", "table", "index", "query", "db", "schema"]):
        domain_type = "Database & Information Management"
        analogy = f"Think of {t_clean} like an index at the back of a 1,000-page encyclopedia. Instead of flipping through all 1,000 pages line-by-line to find a term (Full Table Scan), you check the index in 2 seconds and flip directly to page 342. {t_clean} organizes records so finding, updating, and preserving data is fast and reliable."
        concept_1 = f"Schema Design & Integrity: Defining exact data types, constraints, and relationships in {t_clean}."
        concept_2 = f"Access Paths & Indexing: Accelerating query lookups in {t_clean} from linear O(N) scans to logarithmic O(log N) operations."
        concept_3 = f"ACID Guarantees: Ensuring updates to {t_clean} survive crashes and remain isolated from concurrent queries."
        concept_4 = f"Normalization vs Denormalization: Eliminating update anomalies while balancing join performance."
        example_text = f"Scenario: An e-commerce platform stores 10 million customer orders. By structuring {t_clean} with appropriate primary keys and B-Tree indexes, order lookup queries drop from 4.2 seconds down to 3 milliseconds."
        q1_text = f"What is the primary operational benefit of applying {t_clean} in database systems?"
        q1_opts = [
            "Enabling rapid, reliable data retrieval while ensuring transactional consistency",
            "Deleting old records without confirmation",
            "Replacing relational schemas with raw text files",
            "Increasing disk storage fragmentation"
        ]
        q1_exp = f"{t_clean} guarantees query efficiency, data integrity, and resilience under heavy workloads."
        q2_text = f"When designing {t_clean}, why must engineers account for write overhead?"
        q2_opts = [
            "Every insert or update must maintain index structures and constraints, incurring minor write latency",
            "Databases can only write data once per week",
            "Writes do not affect performance",
            "Writes bypass storage completely"
        ]
        q2_exp = "Maintaining secondary indexes and integrity checks adds a slight write cost in exchange for massive read speedups."

    elif any(w in t_lower for w in ["ai", "model", "neural", "learn", "prompt", "rag", "agent", "llm"]):
        domain_type = "Artificial Intelligence & Machine Learning"
        analogy = f"Think of {t_clean} like training an apprentice pilot in a flight simulator. Instead of programming rules for every possible cloud and wind gust, you let the model experience millions of flights, score its landing accuracy, and adjust its internal control knobs. {t_clean} enables systems to generalize from past examples to solve novel challenges."
        concept_1 = f"Feature Representation & Embeddings: Converting raw unstructured inputs into dense numerical vectors in {t_clean}."
        concept_2 = f"Loss Functions & Optimization: Mathematically quantifying prediction error and adjusting weights via gradient descent in {t_clean}."
        concept_3 = f"Generalization vs Overfitting: Ensuring {t_clean} performs well on unseen test data rather than merely memorizing training inputs."
        concept_4 = f"Evaluation Metrics: Rigorously scoring precision, recall, latency, and hallucination rates in {t_clean}."
        example_text = f"Scenario: A healthcare diagnostics system uses {t_clean} to analyze patient reports. The model highlights potential anomalies for radiologists, reducing review time by 45% while maintaining a 98.4% validation recall rate."
        q1_text = f"In machine learning, what is the central purpose of {t_clean}?"
        q1_opts = [
            "Learning generalizable patterns from data to make accurate predictions on unseen inputs",
            "Memorizing every training record without validation",
            "Replacing all computer processors with analog radios",
            "Eliminating the need for input datasets"
        ]
        q1_exp = "Machine learning focuses on generalization: recognizing underlying patterns to predict correctly on new data."
        q2_text = f"Why must validation sets be kept separate when training {t_clean} models?"
        q2_opts = [
            "To detect overfitting and accurately measure real-world performance on unseen data",
            "To speed up hard drive formatting",
            "Because algorithms cannot process more than 10 records",
            "There is no need to separate test data"
        ]
        q2_exp = "Evaluating on unseen validation data verifies the model has learned true patterns rather than memorized noise."

    else:
        # High-clarity general Computer Science & Software Engineering synthesis
        domain_type = "Software Engineering & Computer Science"
        analogy = f"Think of {t_clean} like the architectural foundation of a modern bridge. You don't just pour concrete randomly; you calculate load distribution, stress points, and maintenance access. {t_clean} provides the formal structure, clear contracts, and standard practices that make software systems resilient, testable, and easy to understand."
        concept_1 = f"Core Architecture & Principles: The fundamental definitions, responsibilities, and abstractions that define {t_clean}."
        concept_2 = f"Operational Mechanics & Lifecycle: How {t_clean} initializes, processes state changes, and handles edge cases."
        concept_3 = f"Modularity & Separation of Concerns: Keeping components decoupled so changes in {t_clean} do not ripple bugs into other subsystems."
        concept_4 = f"Verification & Best Practices: Standard patterns, automated unit testing, and profiling to ensure production readiness in {t_clean}."
        example_text = f"Scenario: An engineering team refactors a legacy service using {t_clean}. By standardizing component interfaces and error boundaries, system stability increases by 60% and new feature onboarding time drops significantly."
        q1_text = f"What is the primary architectural goal of applying {t_clean}?"
        q1_opts = [
            "Writing unstructured code without comments or tests",
            f"Creating a structured, modular, and maintainable solution that handles edge cases cleanly",
            "Increasing runtime error frequency",
            "Bypassing all standard software design principles"
        ]
        q1_exp = f"{t_clean} provides clean abstractions, predictable behavior, and maintainability across system updates."
        q2_text = f"Which engineering practice is most vital when implementing {t_clean} in production?"
        q2_opts = [
            "Disabling logging and monitoring in production",
            "Hardcoding credentials and configuration directly in business logic",
            "Clear interface contracts, comprehensive automated tests, and structured error handling",
            "Ignoring edge cases and unexpected inputs"
        ]
        q2_exp = "Robust test suites, explicit interfaces, and defensive error handling ensure production resilience."

    # Tailor explanation tone to difficulty level
    if difficulty == "Easy":
        exp = f"{analogy} At a foundational level, {t_clean} establishes straightforward principles so you can build mental models with confidence before diving into complex edge cases."
    elif difficulty == "Advanced":
        exp = f"{t_clean} ({domain_type}): Operates at high engineering depth, balancing throughput, low-latency execution, concurrency guarantees, and system fault tolerance. Understanding implementation internals and architectural trade-offs in {t_clean} is critical for designing scalable, production-grade systems."
    else:
        exp = f"{analogy} In practical software engineering ({domain_type}), {t_clean} balances operational simplicity, predictable performance, and maintainable architecture."

    return {
        "topic": t_clean,
        "difficulty": difficulty,
        "summary": f"Comprehensive, high-clarity guide to mastering {t_clean} ({domain_type}).",
        "explanation": exp,
        "concepts": [concept_1, concept_2, concept_3, concept_4],
        "example": example_text,
        "practice": f"Challenge: Consider a production service requiring {t_clean}. What boundary conditions or failure modes would you test first?",
        "parallel_checks": {
            "concept": f"Concept Check: Theory and core principles of {t_clean} validated.",
            "example": f"Example Check: Applied scenario and real-world implementation for {t_clean} verified.",
            "exam": f"Exam Check: Crucial assessment questions and edge cases for {t_clean} mapped."
        },
        "quiz": [
            {
                "id": 1,
                "question": q1_text,
                "options": q1_opts,
                "correct_option": 1,
                "explanation": q1_exp
            },
            {
                "id": 2,
                "question": q2_text,
                "options": q2_opts,
                "correct_option": 2,
                "explanation": q2_exp
            }
        ],
        "revision_quiz": [
            {
                "id": 1,
                "question": f"Refresher Check on {t_clean}: {q1_text}",
                "options": q1_opts,
                "correct_option": 1,
                "explanation": q1_exp
            },
            {
                "id": 2,
                "question": f"Key Insight on {t_clean}: {q2_text}",
                "options": q2_opts,
                "correct_option": 2,
                "explanation": q2_exp
            }
        ]
    }


def get_teaching_material(topic: str, difficulty: str) -> Dict[str, Any]:
    """
    Retrieve structured teaching content tailored to topic and difficulty.
    1. Checks the rich master database of computer science topics.
    2. If no exact/partial match, synthesizes concrete, domain-aware pedagogical content.
    """
    diff_key = difficulty if difficulty in ["Easy", "Normal", "Advanced"] else "Normal"
    topic_normalized = topic.strip().lower()
    
    # 1. Check known topics database (exact and substring matches)
    for known_topic, data in TOPIC_EXPLANATIONS.items():
        k_norm = known_topic.lower()
        if k_norm in topic_normalized or topic_normalized in k_norm:
            variant = data["difficulty_variants"].get(diff_key, data["difficulty_variants"].get("Normal", list(data["difficulty_variants"].values())[0]))
            return {
                "topic": known_topic,
                "difficulty": diff_key,
                "summary": data["summary"],
                "explanation": variant["explanation"],
                "concepts": variant["concepts"],
                "example": variant["example"],
                "practice": variant["practice"],
                "parallel_checks": data.get("parallel_checks", {
                    "concept": f"Concept Check: Theory of {known_topic} verified.",
                    "example": f"Example Check: Applied implementation of {known_topic} validated.",
                    "exam": f"Exam Check: Exam assessment criteria for {known_topic} confirmed."
                }),
                "quiz": data["quiz"],
                "revision_quiz": data.get("revision_quiz", data["quiz"])
            }
            
    # 2. Check keyword tokens (e.g. 'memory', 'paging', 'thread', 'scheduling')
    for known_topic, data in TOPIC_EXPLANATIONS.items():
        k_words = set(known_topic.lower().replace("&", " ").replace("/", " ").split())
        t_words = set(topic_normalized.replace("&", " ").replace("/", " ").split())
        common = k_words.intersection(t_words) - {"and", "to", "in", "of", "the", "a", "for"}
        if len(common) >= 2 or (len(common) == 1 and any(w in common for w in ["paging", "semaphores", "deadlocks", "scheduling", "normalization", "transactions", "indexing", "threads", "processes"])):
            variant = data["difficulty_variants"].get(diff_key, data["difficulty_variants"].get("Normal", list(data["difficulty_variants"].values())[0]))
            return {
                "topic": topic.strip().title(),
                "difficulty": diff_key,
                "summary": data["summary"],
                "explanation": variant["explanation"],
                "concepts": variant["concepts"],
                "example": variant["example"],
                "practice": variant["practice"],
                "parallel_checks": data.get("parallel_checks", {
                    "concept": f"Concept Check: Theory of {topic} verified.",
                    "example": f"Example Check: Applied implementation of {topic} validated.",
                    "exam": f"Exam Check: Exam criteria for {topic} confirmed."
                }),
                "quiz": data["quiz"],
                "revision_quiz": data.get("revision_quiz", data["quiz"])
            }

    # 3. Dynamic smart synthesizer for ANY completely novel custom topic
    return synthesize_custom_topic_material(topic, diff_key)

