# Mock Job Descriptions dataset across 5 industry roles
# Used for agentic RAG retrieval & similarity matching

MOCK_JOB_DESCRIPTIONS = [
    # --- AI / ML Engineer ---
    {
        "id": "jd-aiml-01",
        "title": "Machine Learning Engineer",
        "company": "NeuroTech Systems",
        "role_category": "AI / ML Engineer",
        "location": "Remote",
        "description": "Develop and deploy scalable machine learning models. Work with PyTorch, Scikit-Learn, and LLMs. Build automated training pipelines, handle feature stores, and monitor model drift in production environments.",
        "skills": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "MLOps", "Docker", "LLMs"]
    },
    {
        "id": "jd-aiml-02",
        "title": "Generative AI Specialist",
        "company": "Cognitive Cloud",
        "role_category": "AI / ML Engineer",
        "location": "Bengaluru / Hybrid",
        "description": "Design and optimize RAG applications using LangChain, vector databases (FAISS, Chroma), and state-of-the-art transformer architectures. Fine-tune open-source models (Llama, Mistral) and build AI agents.",
        "skills": ["LangChain", "RAG", "Vector DBs", "FAISS", "Python", "Transformers", "Prompt Engineering"]
    },
    {
        "id": "jd-aiml-03",
        "title": "Computer Vision & Deep Learning Engineer",
        "company": "Visionary AI Labs",
        "role_category": "AI / ML Engineer",
        "location": "San Francisco, CA",
        "description": "Create object detection, segmentation, and classification pipelines using OpenCV, PyTorch, and YOLO. Deploy edge AI inference on NVIDIA Jetson and cloud GPUs with TensorRT.",
        "skills": ["Computer Vision", "OpenCV", "PyTorch", "YOLO", "Deep Learning", "Python"]
    },
    {
        "id": "jd-aiml-04",
        "title": "NLP Data Scientist",
        "company": "Lexicon Insights",
        "role_category": "AI / ML Engineer",
        "location": "Remote",
        "description": "Extract insights from unstructured documents using NLP pipelines, BERT embeddings, Spacy, and sentiment analysis models. Work with cross-functional teams to integrate NLP models into enterprise products.",
        "skills": ["NLP", "BERT", "Spacy", "Transformers", "Python", "FastAPI"]
    },

    # --- Full Stack Developer ---
    {
        "id": "jd-fs-01",
        "title": "Senior Full Stack Engineer",
        "company": "Starlight Digital",
        "role_category": "Full Stack Developer",
        "location": "Remote",
        "description": "Build responsive web applications with React, TypeScript, Node.js, and Express. Architect RESTful APIs, manage PostgreSQL and MongoDB databases, and implement secure JWT authentication.",
        "skills": ["React", "TypeScript", "Node.js", "Express", "PostgreSQL", "MongoDB", "REST APIs", "Tailwind CSS"]
    },
    {
        "id": "jd-fs-02",
        "title": "Full Stack Web Developer (Python + React)",
        "company": "Apex Platform Inc",
        "role_category": "Full Stack Developer",
        "location": "Hyderabad / Remote",
        "description": "Design interactive web interfaces using React/Next.js paired with robust Python FastAPI/Django backends. Build microservices, WebSocket channels, and optimize UI performance.",
        "skills": ["React", "Next.js", "Python", "FastAPI", "Django", "PostgreSQL", "JavaScript"]
    },
    {
        "id": "jd-fs-03",
        "title": "MERN Stack Engineer",
        "company": "CloudWave Studios",
        "role_category": "Full Stack Developer",
        "location": "Austin, TX / Hybrid",
        "description": "Maintain end-to-end applications across MongoDB, Express, React, and Node.js. Build automated test suites, CI/CD pipelines, and design reusable UI component libraries.",
        "skills": ["MongoDB", "Express", "React", "Node.js", "Redux", "Docker", "Git"]
    },
    {
        "id": "jd-fs-04",
        "title": "Frontend Heavy Full Stack Developer",
        "company": "FinPixel Technologies",
        "role_category": "Full Stack Developer",
        "location": "Remote",
        "description": "Craft pixel-perfect, accessible user interfaces using Vue.js/React and Tailwind CSS while integrating with GraphQL and Node.js backend endpoints. Focus on responsive design and Core Web Vitals.",
        "skills": ["JavaScript", "React", "Vue.js", "CSS3", "GraphQL", "Node.js", "UI/UX"]
    },

    # --- Data Engineer ---
    {
        "id": "jd-de-01",
        "title": "Data Engineer",
        "company": "DataStream Corp",
        "role_category": "Data Engineer",
        "location": "New York / Hybrid",
        "description": "Design scalable data pipelines and ETL processes using Apache Spark, Kafka, and Airflow. Manage cloud data warehouses in Snowflake and Google BigQuery with high reliability and low latency.",
        "skills": ["Python", "SQL", "Apache Spark", "Kafka", "Airflow", "Snowflake", "ETL", "BigQuery"]
    },
    {
        "id": "jd-de-02",
        "title": "Big Data Pipeline Architect",
        "company": "Global Analytics Hub",
        "role_category": "Data Engineer",
        "location": "Remote",
        "description": "Process terabytes of batch and streaming data. Build robust data lakes on AWS S3, optimize complex SQL transformations in dbt, and maintain data governance and lineage standards.",
        "skills": ["AWS", "S3", "dbt", "SQL", "PySpark", "Data Lakes", "PostgreSQL"]
    },
    {
        "id": "jd-de-03",
        "title": "Analytics Engineer",
        "company": "MetricFlow",
        "role_category": "Data Engineer",
        "location": "London / Remote",
        "description": "Bridge data engineering and business intelligence. Build reliable data models in dbt and PostgreSQL, automate reporting pipelines, and implement data quality tests.",
        "skills": ["dbt", "SQL", "Python", "Data Modeling", "Tableau", "PostgreSQL", "Airflow"]
    },
    {
        "id": "jd-de-04",
        "title": "Cloud Data Engineer (GCP/BigQuery)",
        "company": "Skyline Enterprise",
        "role_category": "Data Engineer",
        "location": "Bengaluru",
        "description": "Develop enterprise ETL workflows using Google Cloud Dataflow, BigQuery, and Pub/Sub. Implement robust monitoring, partitioned data stores, and IAM security controls.",
        "skills": ["GCP", "BigQuery", "Dataflow", "Pub/Sub", "Python", "SQL", "Terraform"]
    },

    # --- DevOps / Cloud Engineer ---
    {
        "id": "jd-do-01",
        "title": "DevOps & Cloud Engineer",
        "company": "TerraOps Infrastructure",
        "role_category": "DevOps / Cloud Engineer",
        "location": "Remote",
        "description": "Automate cloud infrastructure with Terraform, Kubernetes, and Helm on AWS/GCP. Build GitOps CI/CD pipelines via GitHub Actions and ensure 99.99% system uptime.",
        "skills": ["Docker", "Kubernetes", "Terraform", "AWS", "GitHub Actions", "CI/CD", "Linux"]
    },
    {
        "id": "jd-do-02",
        "title": "Site Reliability Engineer (SRE)",
        "company": "HyperScale Networks",
        "role_category": "DevOps / Cloud Engineer",
        "location": "Seattle, WA",
        "description": "Monitor production distributed systems using Prometheus, Grafana, and OpenTelemetry. Troubleshoot incidents, conduct post-mortems, and automate self-healing infrastructure with Python and Bash.",
        "skills": ["Prometheus", "Grafana", "Kubernetes", "Python", "Linux", "SRE"]
    },
    {
        "id": "jd-do-03",
        "title": "Cloud Security & Infrastructure Engineer",
        "company": "Sentinel Shield",
        "role_category": "DevOps / Cloud Engineer",
        "location": "Remote",
        "description": "Implement zero-trust security postures, cloud IAM policies, container security scanning, and infrastructure as code across multi-cloud environments.",
        "skills": ["AWS Security", "Terraform", "Docker", "Vault", "IAM", "Kubernetes", "Linux"]
    },
    {
        "id": "jd-do-04",
        "title": "Platform Engineer",
        "company": "NextGen Systems",
        "role_category": "DevOps / Cloud Engineer",
        "location": "Berlin / Remote",
        "description": "Design internal developer platforms (IDP) that empower development teams to deploy self-service services smoothly using ArgoCD, Kubernetes, and cloud native tools.",
        "skills": ["Kubernetes", "ArgoCD", "Helm", "Go", "Python", "AWS", "CI/CD"]
    },

    # --- Backend Developer ---
    {
        "id": "jd-be-01",
        "title": "Backend Python Engineer",
        "company": "Scalable Logic",
        "role_category": "Backend Developer",
        "location": "Remote",
        "description": "Design high-performance asynchronous microservices using FastAPI, Celery, and Redis. Build clean data access layers with SQLAlchemy and PostgreSQL. Implement caching and pub/sub message queues.",
        "skills": ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Redis", "Celery", "Docker"]
    },
    {
        "id": "jd-be-02",
        "title": "Distributed Systems Backend Engineer",
        "company": "ByteCraft Labs",
        "role_category": "Backend Developer",
        "location": "San Jose, CA",
        "description": "Build resilient low-latency backend systems handling millions of requests per second. Optimize database queries, design database sharding, and maintain gRPC interfaces.",
        "skills": ["Go", "Python", "gRPC", "PostgreSQL", "Distributed Systems", "Redis", "Kafka"]
    },
    {
        "id": "jd-be-03",
        "title": "API Platform Engineer",
        "company": "Interlink Tech",
        "role_category": "Backend Developer",
        "location": "Remote",
        "description": "Develop and maintain public and internal developer APIs. Enforce rate limiting, OAuth2 security, OpenAPI/Swagger specifications, and backward compatibility.",
        "skills": ["FastAPI", "Node.js", "OAuth2", "PostgreSQL", "Swagger", "Docker"]
    },
    {
        "id": "jd-be-04",
        "title": "Java / Spring Boot Backend Engineer",
        "company": "Enterprise Horizon",
        "role_category": "Backend Developer",
        "location": "Chicago, IL / Hybrid",
        "description": "Architect enterprise microservices using Java 17, Spring Boot, and Hibernate. Integrate with message brokers and secure systems with Spring Security.",
        "skills": ["Java", "Spring Boot", "Hibernate", "PostgreSQL", "Microservices", "Kafka", "Docker"]
    }
]

# The 5 standard roles target evaluated for every candidate
TARGET_ROLES = [
    "AI / ML Engineer",
    "Full Stack Developer",
    "Data Engineer",
    "DevOps / Cloud Engineer",
    "Backend Developer"
]
