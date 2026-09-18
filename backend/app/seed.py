from __future__ import annotations

from flask import current_app

from app.extensions import db
from app.models.job_role import JobRole
from app.models.resource import Resource
from app.models.roadmap import Roadmap
from app.models.roadmap_step import RoadmapStep
from app.models.role import Role
from app.models.user import User


JOB_ROLES = [
    {
        "title": "Machine Learning Engineer",
        "description": "Design, train, and productionize machine learning systems.",
        "required_skills": ["Python", "NumPy", "Pandas", "scikit-learn", "PyTorch", "MLOps", "SQL"],
        "preferred_skills": ["Kubernetes", "AWS", "Feature stores", "Spark"],
        "keywords": ["model training", "evaluation", "deployment", "pipelines", "experiment tracking"],
    },
    {
        "title": "Data Scientist",
        "description": "Turn data into decisions through statistics, modeling, and storytelling.",
        "required_skills": ["Python", "SQL", "Statistics", "Pandas", "Visualization", "Hypothesis testing"],
        "preferred_skills": ["A/B testing", "Tableau", "Spark"],
        "keywords": ["EDA", "regression", "classification", "insights", "dashboards"],
    },
    {
        "title": "AI Engineer",
        "description": "Build applied AI products including RAG, agents, and LLM applications.",
        "required_skills": ["Python", "NLP", "Transformers", "RAG", "APIs", "Prompt design"],
        "preferred_skills": ["LangChain", "vector databases", "FastAPI"],
        "keywords": ["embeddings", "retrieval", "LLM", "evaluation", "safety"],
    },
    {
        "title": "Full Stack Developer",
        "description": "Deliver end-to-end web products across frontend and backend.",
        "required_skills": ["JavaScript", "TypeScript", "React", "Node.js", "SQL", "REST"],
        "preferred_skills": ["Docker", "CI/CD", "GraphQL"],
        "keywords": ["frontend", "backend", "authentication", "testing", "deployment"],
    },
    {
        "title": "Backend Developer",
        "description": "Design reliable APIs, data models, and server-side services.",
        "required_skills": ["Python", "Flask", "SQL", "REST", "Authentication", "Testing"],
        "preferred_skills": ["Redis", "PostgreSQL", "message queues"],
        "keywords": ["API", "database", "performance", "security", "scalability"],
    },
    {
        "title": "Frontend Developer",
        "description": "Craft accessible, performant user interfaces.",
        "required_skills": ["HTML", "CSS", "JavaScript", "React", "Accessibility", "Responsive design"],
        "preferred_skills": ["TypeScript", "Motion", "testing-library"],
        "keywords": ["UI", "UX", "component", "state management", "performance"],
    },
    {
        "title": "Python Developer",
        "description": "Build Python services, automation, and data-oriented applications.",
        "required_skills": ["Python", "OOP", "Flask", "pytest", "SQL", "Git"],
        "preferred_skills": ["asyncio", "FastAPI", "packaging"],
        "keywords": ["scripting", "API", "refactoring", "testing", "documentation"],
    },
    {
        "title": "Software Engineer",
        "description": "Design and implement maintainable software systems.",
        "required_skills": ["Data structures", "Algorithms", "Git", "Testing", "System design", "Python"],
        "preferred_skills": ["Cloud", "CI/CD", "observability"],
        "keywords": ["collaboration", "code review", "reliability", "architecture", "debugging"],
    },
]


def _steps(pairs: list[tuple[str, str, str]]) -> list[dict]:
    return [
        {
            "title": title,
            "stage": stage,
            "order_index": i,
            "description": desc,
            "skills": [],
            "resources": [],
            "projects": [],
        }
        for i, (title, stage, desc) in enumerate(pairs)
    ]


ROADMAPS = [
    {
        "slug": "artificial-intelligence",
        "title": "Artificial Intelligence",
        "description": "From search and knowledge representation to modern neural systems.",
        "difficulty": "Advanced",
        "estimated_duration": "6–9 months",
        "prerequisites": ["Python", "Linear algebra basics"],
        "skills": ["Search", "Planning", "NLP", "Computer vision"],
        "technologies": ["Python", "PyTorch", "Hugging Face"],
        "certifications": ["Optional: DeepLearning.AI specialization"],
        "steps": _steps(
            [
                ("Foundations of AI", "BEGINNER", "Cover search, logic, and problem formulation."),
                ("Learning systems", "INTERMEDIATE", "Supervised learning, evaluation, and overfitting."),
                ("Modern neural AI", "ADVANCED", "Transformers, multimodal models, and alignment basics."),
                ("Capstone product", "ADVANCED", "Ship an AI assistant with evaluation and safety notes."),
            ]
        ),
    },
    {
        "slug": "machine-learning",
        "title": "Machine Learning",
        "description": "A practical path from classical models to production ML.",
        "difficulty": "Intermediate",
        "estimated_duration": "5–8 months",
        "prerequisites": ["Python", "Basic statistics"],
        "skills": ["Feature engineering", "Model selection", "MLOps"],
        "technologies": ["scikit-learn", "PyTorch", "MLflow"],
        "certifications": ["Optional: Google ML engineer"],
        "steps": _steps(
            [
                ("Classical ML", "BEGINNER", "Regression, trees, and validation strategy."),
                ("Deep learning", "INTERMEDIATE", "Neural nets, regularization, and transfer learning."),
                ("Production ML", "ADVANCED", "Pipelines, monitoring, and retraining."),
                ("Applied project", "ADVANCED", "End-to-end model with a documented metric card."),
            ]
        ),
    },
    {
        "slug": "data-science",
        "title": "Data Science",
        "description": "Question framing, analysis, modeling, and communication.",
        "difficulty": "Intermediate",
        "estimated_duration": "4–6 months",
        "prerequisites": ["Spreadsheets or Python basics"],
        "skills": ["SQL", "EDA", "Storytelling"],
        "technologies": ["Pandas", "SQL", "Matplotlib"],
        "certifications": [],
        "steps": _steps(
            [
                ("Data wrangling", "BEGINNER", "Clean, join, and profile datasets."),
                ("Inference", "INTERMEDIATE", "Statistics, experiments, and uncertainty."),
                ("Modeling for insight", "ADVANCED", "Interpretable models and decision support."),
                ("Portfolio study", "ADVANCED", "Publish a reproducible analysis notebook."),
            ]
        ),
    },
    {
        "slug": "full-stack-development",
        "title": "Full Stack Development",
        "description": "Browser to database, with authentication and deployment.",
        "difficulty": "Intermediate",
        "estimated_duration": "5–7 months",
        "prerequisites": ["HTML", "CSS", "JavaScript"],
        "skills": ["React", "APIs", "SQL"],
        "technologies": ["React", "Flask", "PostgreSQL", "Docker"],
        "certifications": [],
        "steps": _steps(
            [
                ("Interface craft", "BEGINNER", "Accessible layouts and component systems."),
                ("API design", "INTERMEDIATE", "REST, auth, and validation."),
                ("Persistence", "ADVANCED", "Relational modeling and migrations."),
                ("Ship it", "ADVANCED", "Containerize and deploy a full product."),
            ]
        ),
    },
    {
        "slug": "backend-development",
        "title": "Backend Development",
        "description": "Services, data, and reliability for Python engineers.",
        "difficulty": "Intermediate",
        "estimated_duration": "4–6 months",
        "prerequisites": ["Python"],
        "skills": ["Flask", "SQLAlchemy", "Testing"],
        "technologies": ["Flask", "PostgreSQL", "Gunicorn"],
        "certifications": [],
        "steps": _steps(
            [
                ("HTTP and APIs", "BEGINNER", "Routing, status codes, and JSON contracts."),
                ("Data layer", "INTERMEDIATE", "ORM, transactions, and indexing."),
                ("Hardening", "ADVANCED", "Auth, rate limits, and observability."),
                ("Service project", "ADVANCED", "Build a production-style API."),
            ]
        ),
    },
    {
        "slug": "frontend-development",
        "title": "Frontend Development",
        "description": "Typography, motion, and resilient interface architecture.",
        "difficulty": "Beginner",
        "estimated_duration": "3–5 months",
        "prerequisites": ["Basic computer literacy"],
        "skills": ["HTML", "CSS", "React"],
        "technologies": ["Vite", "Tailwind", "Motion"],
        "certifications": [],
        "steps": _steps(
            [
                ("Foundations", "BEGINNER", "Semantic HTML and layout systems."),
                ("Interactivity", "INTERMEDIATE", "State, forms, and accessibility."),
                ("Motion and polish", "ADVANCED", "Purposeful animation and performance."),
                ("Product UI", "ADVANCED", "Ship a multi-page app with routing."),
            ]
        ),
    },
    {
        "slug": "python-development",
        "title": "Python Development",
        "description": "Language mastery for scripts, APIs, and tooling.",
        "difficulty": "Beginner",
        "estimated_duration": "3–4 months",
        "prerequisites": [],
        "skills": ["Python", "Testing", "Packaging"],
        "technologies": ["pytest", "Flask", "venv"],
        "certifications": ["Optional: PCEP / PCAP"],
        "steps": _steps(
            [
                ("Language core", "BEGINNER", "Types, functions, and modules."),
                ("Engineering habits", "INTERMEDIATE", "Testing, linting, and virtualenvs."),
                ("Services", "ADVANCED", "Build APIs and CLI tools."),
                ("Open-source practice", "ADVANCED", "Document and package a library."),
            ]
        ),
    },
    {
        "slug": "cloud-computing",
        "title": "Cloud Computing",
        "description": "Compute, storage, networking, and managed services.",
        "difficulty": "Intermediate",
        "estimated_duration": "4–6 months",
        "prerequisites": ["Linux basics"],
        "skills": ["IAM", "Networking", "Containers"],
        "technologies": ["AWS or GCP", "Docker"],
        "certifications": ["Optional: AWS Cloud Practitioner"],
        "steps": _steps(
            [
                ("Cloud primitives", "BEGINNER", "Regions, IAM, compute, and storage."),
                ("Application hosting", "INTERMEDIATE", "Load balancers, databases, and secrets."),
                ("Operations", "ADVANCED", "Observability and cost control."),
                ("Deployed architecture", "ADVANCED", "Document a three-tier cloud design."),
            ]
        ),
    },
    {
        "slug": "devops",
        "title": "DevOps",
        "description": "Delivery pipelines, infrastructure as code, and reliability.",
        "difficulty": "Advanced",
        "estimated_duration": "5–7 months",
        "prerequisites": ["Git", "Linux"],
        "skills": ["CI/CD", "Containers", "Monitoring"],
        "technologies": ["GitHub Actions", "Docker", "Terraform"],
        "certifications": [],
        "steps": _steps(
            [
                ("Versioned delivery", "BEGINNER", "Branching, reviews, and automated tests."),
                ("Containers", "INTERMEDIATE", "Images, compose, and registries."),
                ("Infrastructure as code", "ADVANCED", "Repeatable environments."),
                ("SRE project", "ADVANCED", "SLOs, alerts, and a runbook."),
            ]
        ),
    },
    {
        "slug": "cybersecurity",
        "title": "Cybersecurity",
        "description": "Defensive security for applications and infrastructure.",
        "difficulty": "Intermediate",
        "estimated_duration": "5–8 months",
        "prerequisites": ["Networking fundamentals"],
        "skills": ["Threat modeling", "Secure coding", "IAM"],
        "technologies": ["OWASP", "logging", "firewalls"],
        "certifications": ["Optional: CompTIA Security+"],
        "steps": _steps(
            [
                ("Security mindset", "BEGINNER", "CIA triad, assets, and threat actors."),
                ("Application security", "INTERMEDIATE", "Injection, XSS, auth flaws, and uploads."),
                ("Defense in depth", "ADVANCED", "Logging, least privilege, and incident basics."),
                ("Hardening lab", "ADVANCED", "Review an app against OWASP Top 10."),
            ]
        ),
    },
]


RESOURCES = [
    {
        "title": "Python Official Tutorial",
        "description": "The canonical language tutorial from python.org.",
        "category": "Language",
        "subject": "Python",
        "difficulty": "Beginner",
        "resource_type": "DOCUMENTATION",
        "url": "https://docs.python.org/3/tutorial/",
        "tags": ["python", "official"],
    },
    {
        "title": "Flask Documentation",
        "description": "Primary reference for Flask applications and blueprints.",
        "category": "Backend",
        "subject": "Python",
        "difficulty": "Intermediate",
        "resource_type": "DOCUMENTATION",
        "url": "https://flask.palletsprojects.com/",
        "tags": ["flask", "api"],
    },
    {
        "title": "React Documentation",
        "description": "Official React docs covering components, hooks, and data.",
        "category": "Frontend",
        "subject": "JavaScript",
        "difficulty": "Beginner",
        "resource_type": "DOCUMENTATION",
        "url": "https://react.dev/learn",
        "tags": ["react", "ui"],
    },
    {
        "title": "MDN Web Docs",
        "description": "Authoritative HTML, CSS, and JavaScript reference.",
        "category": "Frontend",
        "subject": "HTML/CSS",
        "difficulty": "Beginner",
        "resource_type": "DOCUMENTATION",
        "url": "https://developer.mozilla.org/",
        "tags": ["html", "css", "javascript"],
    },
    {
        "title": "scikit-learn User Guide",
        "description": "Practical guide to classical machine learning estimators.",
        "category": "Machine Learning",
        "subject": "Machine Learning",
        "difficulty": "Intermediate",
        "resource_type": "DOCUMENTATION",
        "url": "https://scikit-learn.org/stable/user_guide.html",
        "tags": ["ml", "python"],
    },
    {
        "title": "Hugging Face NLP Course",
        "description": "Free course on transformers, tokenizers, and fine-tuning.",
        "category": "AI",
        "subject": "NLP",
        "difficulty": "Intermediate",
        "resource_type": "COURSE",
        "url": "https://huggingface.co/learn/nlp-course",
        "tags": ["nlp", "transformers"],
    },
    {
        "title": "Attention Is All You Need",
        "description": "Original transformer architecture paper.",
        "category": "Research",
        "subject": "Artificial Intelligence",
        "difficulty": "Advanced",
        "resource_type": "ARTICLE",
        "url": "https://arxiv.org/abs/1706.03762",
        "tags": ["transformers", "paper"],
    },
    {
        "title": "Retrieval-Augmented Generation paper",
        "description": "Lewis et al. on combining retrieval with generation.",
        "category": "Research",
        "subject": "Artificial Intelligence",
        "difficulty": "Advanced",
        "resource_type": "ARTICLE",
        "url": "https://arxiv.org/abs/2005.11401",
        "tags": ["rag", "paper"],
    },
    {
        "title": "PostgreSQL Documentation",
        "description": "Official PostgreSQL reference.",
        "category": "Data",
        "subject": "SQL",
        "difficulty": "Intermediate",
        "resource_type": "DOCUMENTATION",
        "url": "https://www.postgresql.org/docs/",
        "tags": ["sql", "postgres"],
    },
    {
        "title": "OWASP Top Ten",
        "description": "Widely used awareness document for web application risks.",
        "category": "Security",
        "subject": "Cybersecurity",
        "difficulty": "Intermediate",
        "resource_type": "ARTICLE",
        "url": "https://owasp.org/www-project-top-ten/",
        "tags": ["security", "owasp"],
    },
    {
        "title": "The Docker Getting Started Guide",
        "description": "Official orientation to images, containers, and Compose.",
        "category": "DevOps",
        "subject": "DevOps",
        "difficulty": "Beginner",
        "resource_type": "TUTORIAL",
        "url": "https://docs.docker.com/get-started/",
        "tags": ["docker", "containers"],
    },
    {
        "title": "Google SRE Book",
        "description": "Public book on site reliability engineering practices.",
        "category": "DevOps",
        "subject": "DevOps",
        "difficulty": "Advanced",
        "resource_type": "ARTICLE",
        "url": "https://sre.google/sre-book/table-of-contents/",
        "tags": ["sre", "reliability"],
    },
    {
        "title": "fast.ai Practical Deep Learning",
        "description": "Top-down deep learning course with free notebooks.",
        "category": "Machine Learning",
        "subject": "Machine Learning",
        "difficulty": "Intermediate",
        "resource_type": "COURSE",
        "url": "https://course.fast.ai/",
        "tags": ["deep-learning", "course"],
    },
    {
        "title": "TypeScript Handbook",
        "description": "Official TypeScript language handbook.",
        "category": "Frontend",
        "subject": "TypeScript",
        "difficulty": "Intermediate",
        "resource_type": "DOCUMENTATION",
        "url": "https://www.typescriptlang.org/docs/handbook/intro.html",
        "tags": ["typescript"],
    },
    {
        "title": "spaCy Usage Documentation",
        "description": "Industrial-strength NLP library documentation.",
        "category": "NLP",
        "subject": "NLP",
        "difficulty": "Intermediate",
        "resource_type": "DOCUMENTATION",
        "url": "https://spacy.io/usage",
        "tags": ["nlp", "spacy"],
    },
    {
        "title": "NLTK Book",
        "description": "Natural Language Processing with Python (online book).",
        "category": "NLP",
        "subject": "NLP",
        "difficulty": "Beginner",
        "resource_type": "ARTICLE",
        "url": "https://www.nltk.org/book/",
        "tags": ["nltk", "nlp"],
    },
]


def seed() -> None:
    if not JobRole.query.first():
        for item in JOB_ROLES:
            db.session.add(JobRole(**item))
    if not Roadmap.query.first():
        for item in ROADMAPS:
            payload = dict(item)
            steps = payload.pop("steps")
            roadmap = Roadmap(**payload)
            db.session.add(roadmap)
            db.session.flush()
            for step in steps:
                db.session.add(RoadmapStep(roadmap_id=roadmap.id, **step))
    if not Resource.query.first():
        for item in RESOURCES:
            db.session.add(Resource(**item))
    admin_email = current_app.config.get("ADMIN_EMAIL")
    admin_password = current_app.config.get("ADMIN_PASSWORD")
    if admin_email and admin_password and not User.query.filter_by(email=admin_email).first():
        admin = User(name="Administrator", email=admin_email, role=Role.ADMIN)
        admin.set_password(admin_password)
        db.session.add(admin)
    db.session.commit()
