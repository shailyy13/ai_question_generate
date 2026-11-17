import re
import os
import spacy
import time

from fastapi import FastAPI
from dotenv import load_dotenv
from google import genai
from google.genai import types


app = FastAPI(title="AI Interview AI Service")


# =========================================================
# GEMINI API
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env file")


client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=60000
    )
)

nlp = spacy.load("en_core_web_sm")


# =========================================================
# SKILLS DATABASE
# =========================================================

SKILLS = [

    # ---------------- PROGRAMMING LANGUAGES ----------------
    "C",
    "C++",
    "C#",
    "Java",
    "JavaScript",
    "TypeScript",
    "Python",
    "Go",
    "Golang",
    "Rust",
    "PHP",
    "Ruby",
    "Kotlin",
    "Swift",
    "R",
    "Dart",
    "Scala",

    # ---------------- FRONTEND ----------------
    "HTML",
    "HTML5",
    "CSS",
    "CSS3",
    "Bootstrap",
    "Tailwind CSS",
    "React",
    "React.js",
    "Next.js",
    "Angular",
    "Vue.js",
    "Redux",
    "Redux Toolkit",
    "jQuery",
    "Material UI",
    "MUI",

    # ---------------- BACKEND ----------------
    "Node.js",
    "Express",
    "Express.js",
    "Django",
    "Flask",
    "FastAPI",
    "Spring",
    "Spring Boot",
    "ASP.NET",
    "Laravel",
    "REST",
    "REST API",
    "RESTful API",
    "GraphQL",
    "WebSocket",
    "WebSockets",

    # ---------------- DATABASES ----------------
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQL",
    "SQLite",
    "Oracle",
    "Redis",
    "Firebase",
    "DynamoDB",
    "Cassandra",
    "Microsoft SQL Server",

    # ---------------- AI / ML ----------------
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "TensorFlow",
    "Keras",
    "PyTorch",
    "Scikit-learn",
    "Scikit Learn",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "OpenCV",
    "Hugging Face",
    "Transformers",
    "LangChain",
    "LangGraph",

    # ---------------- DATA ----------------
    "Data Science",
    "Data Analysis",
    "Data Analytics",
    "Data Visualization",
    "Power BI",
    "Tableau",
    "Excel",
    "Statistics",

    # ---------------- CLOUD ----------------
    "AWS",
    "Amazon Web Services",
    "Microsoft Azure",
    "Azure",
    "Google Cloud",
    "Google Cloud Platform",
    "GCP",
    "EC2",
    "S3",
    "Lambda",

    # ---------------- DEVOPS ----------------
    "Git",
    "GitHub",
    "GitLab",
    "Bitbucket",
    "Docker",
    "Kubernetes",
    "Jenkins",
    "CI/CD",
    "Linux",
    "Nginx",

    # ---------------- TESTING ----------------
    "Jest",
    "Mocha",
    "PyTest",
    "pytest",
    "JUnit",
    "Selenium",
    "Cypress",
    "Postman",

    # ---------------- SECURITY ----------------
    "JWT",
    "OAuth",
    "OAuth2",
    "Passport.js",

    # ---------------- CS CONCEPTS ----------------
    "DSA",
    "Data Structures",
    "Algorithms",
    "OOP",
    "OOPs",
    "Object Oriented Programming",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "Computer Architecture",
    "Software Engineering",

    # ---------------- TOOLS / DEVELOPMENT ----------------
    "VS Code",
    "Visual Studio Code",
    "Postman",
    "Agile",
    "Scrum",
    "REST API"
]


# =========================================================
# CANONICAL SKILL NAMES
# =========================================================

SKILL_CANONICAL = {

    "react": "React.js",
    "react.js": "React.js",

    "express": "Express.js",
    "express.js": "Express.js",

    "rest": "REST API",
    "rest api": "REST API",
    "restful api": "REST API",

    "api": "REST API",

    "html": "HTML",
    "html5": "HTML",

    "css": "CSS",
    "css3": "CSS",

    "c++": "C++",

    "python": "Python",

    "javascript": "JavaScript",

    "typescript": "TypeScript",

    "node.js": "Node.js",

    "mysql": "MySQL",

    "mongodb": "MongoDB",

    "sql": "SQL",

    "machine learning": "Machine Learning",

    "nlp": "NLP",

    "natural language processing": "NLP",

    "tensorflow": "TensorFlow",

    "keras": "Keras",

    "opencv": "OpenCV",

    "github": "GitHub",

    "git": "Git",

    "jwt": "JWT",

    "passport.js": "Passport.js",

    "postman": "Postman",

    "vs code": "VS Code",

    "visual studio code": "VS Code",

    "excel": "Excel",

    "oop": "OOPs",

    "oops": "OOPs",

    "object oriented programming": "OOPs",

    "dsa": "DSA",

    "dbms": "DBMS"
}


# =========================================================
# SECTION ALIASES
# =========================================================

SECTION_ALIASES = {

    "education": [
        "education",
        "academic background",
        "academic qualification",
        "qualifications",
        "educational background",
        "education qualification"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "work history",
        "employment",
        "professional background",
        "internship experience"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience",
        "selected projects",
        "project work"
    ],

    "skills": [
        "technical skills",
        "skills",
        "technical expertise",
        "core skills",
        "technical proficiencies",
        "technical competencies"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "achievements",
        "certifications and achievements",
        "certifications & achievements",
        "extra curricular",
        "extra-curriculars",
        "certifications & extra-curriculars"
    ]
}


# =========================================================
# NON-SECTION HEADINGS
# =========================================================

ALL_SECTION_HEADINGS = set()

for section_values in SECTION_ALIASES.values():

    for alias in section_values:

        ALL_SECTION_HEADINGS.add(
            re.sub(
                r"[^a-z ]",
                "",
                alias.lower()
            ).strip()
        )


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("−", "-")

    text = text.replace("•", " | ")

    text = re.sub(
        r"--\s*\d+\s+of\s+\d+\s*--",
        " ",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"(\w)-\s+(\w)",
        r"\1\2",
        text
    )

    text = text.replace("\t", " ")

    text = re.sub(
        r"[ ]+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# NORMALIZE HEADING
# =========================================================

def normalize_heading(line):

    if not line:
        return ""

    line = line.lower().strip()

    line = re.sub(
        r"[^a-z ]",
        "",
        line
    )

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.strip()


# =========================================================
# IS SECTION HEADING?
# =========================================================

def is_section_heading(line):

    normalized = normalize_heading(line)

    return normalized in ALL_SECTION_HEADINGS


# =========================================================
# FIND SECTION
# =========================================================

def find_section(text, section_type):

    if not text:
        return ""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    aliases = {
        normalize_heading(alias)
        for alias in SECTION_ALIASES[section_type]
    }

    start_index = None

    for i, line in enumerate(lines):

        normalized = normalize_heading(line)

        if normalized in aliases:

            start_index = i + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    for line in lines[start_index:]:

        if is_section_heading(line):
            break

        if re.fullmatch(
            r"--\s*\d+\s+of\s+\d+\s*--",
            line,
            re.IGNORECASE
        ):
            continue

        section_lines.append(line)

    return "\n".join(section_lines).strip()


# =========================================================
# SKILL NORMALIZATION
# =========================================================

def normalize_skill(skill):

    key = skill.lower().strip()

    return SKILL_CANONICAL.get(key, skill)


# =========================================================
# SKILL EXTRACTION
# =========================================================

def extract_skills(resume_text, skills_text):

    found = []

    search_text = skills_text if skills_text else resume_text

    sorted_skills = sorted(
        SKILLS,
        key=len,
        reverse=True
    )

    for skill in sorted_skills:

        pattern = (
            r"(?<![\w+#.])"
            + re.escape(skill)
            + r"(?![\w+#.])"
        )

        if re.search(
            pattern,
            search_text,
            re.IGNORECASE
        ):

            canonical = normalize_skill(skill)

            if canonical not in found:
                found.append(canonical)

    for skill in sorted_skills:

        pattern = (
            r"(?<![\w+#.])"
            + re.escape(skill)
            + r"(?![\w+#.])"
        )

        if re.search(
            pattern,
            resume_text,
            re.IGNORECASE
        ):

            canonical = normalize_skill(skill)

            if canonical not in found:
                found.append(canonical)

    if "REST API" in found:

        found = [
            skill
            for skill in found
            if skill not in [
                "REST",
                "API",
                "RESTful API"
            ]
        ]

    if "React.js" in found:

        found = [
            skill
            for skill in found
            if skill != "React"
        ]

    if "Express.js" in found:

        found = [
            skill
            for skill in found
            if skill != "Express"
        ]

    if "HTML" in found:

        found = [
            skill
            for skill in found
            if skill != "HTML5"
        ]

    if "CSS" in found:

        found = [
            skill
            for skill in found
            if skill != "CSS3"
        ]

    if "OOPs" in found:

        found = [
            skill
            for skill in found
            if skill not in [
                "OOP",
                "Object Oriented Programming"
            ]
        ]

    found = list(dict.fromkeys(found))

    return found


# =========================================================
# EDUCATION EXTRACTION
# =========================================================

def extract_education(text):

    if not text:
        return []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    entries = []

    current = []

    pattern = re.compile(
        r"(Bachelor|Master|B\.?\s*Tech|M\.?\s*Tech|"
        r"B\.?\s*E|M\.?\s*E|BCA|MCA|BSc|MSc|"
        r"Senior Secondary|Higher Secondary|"
        r"\b10th\b|\b12th\b|Diploma|GATE|PhD)",
        re.IGNORECASE
    )

    for line in lines:

        if pattern.search(line) and current:

            entries.append(
                " ".join(current).strip()
            )

            current = []

        current.append(line)

    if current:

        entries.append(
            " ".join(current).strip()
        )

    return clean_entries(entries)


# =========================================================
# EXPERIENCE EXTRACTION
# =========================================================

def extract_experience(text):

    if not text:
        return []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    entries = []

    current = []

    start_pattern = re.compile(
        r"("
        r"Intern|"
        r"Developer|"
        r"Engineer|"
        r"Manager|"
        r"Analyst|"
        r"Designer|"
        r"Consultant|"
        r"Trainee|"
        r"Associate|"
        r"Architect|"
        r"Scientist|"
        r"Administrator"
        r")",
        re.IGNORECASE
    )

    for line in lines:

        has_role = bool(
            start_pattern.search(line)
        )

        has_date = bool(
            re.search(
                r"\b(19|20)\d{2}\b",
                line
            )
        )

        if has_role and has_date and current:

            entries.append(
                " ".join(current).strip()
            )

            current = []

        current.append(line)

    if current:

        entries.append(
            " ".join(current).strip()
        )

    return clean_entries(entries)


# =========================================================
# PROJECT TITLE DETECTION
# =========================================================

def is_project_title(line):

    line = line.strip()

    if not line:
        return False

    if re.match(
        r"^Other Projects",
        line,
        re.IGNORECASE
    ):
        return False

    if re.search(
        r"\[GitHub\]",
        line,
        re.IGNORECASE
    ):
        return True

    if re.search(
        r"(Dashboard|"
        r"Management System|"
        r"Access System|"
        r"Platform|"
        r"Predictor|"
        r"Quiz System|"
        r"Application|"
        r"Website)$",
        line,
        re.IGNORECASE
    ):
        return True

    return False


# =========================================================
# PROJECT EXTRACTION
# =========================================================

def extract_projects(text):

    if not text:
        return []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    projects = []

    current = None

    for line in lines:

        if re.fullmatch(
            r"--\s*\d+\s+of\s+\d+\s*--",
            line,
            re.IGNORECASE
        ):
            continue

        if is_section_heading(line):
            break

        if is_project_title(line):

            if current:

                current["description"] = (
                    current["description"].strip()
                )

                projects.append(current)

            title = re.sub(
                r"\s*\[GitHub\]\s*",
                "",
                line,
                flags=re.IGNORECASE
            ).strip()

            current = {
                "name": title,
                "description": ""
            }

        elif current:

            if re.match(
                r"^(CERTIFICATIONS|"
                r"Competitions|"
                r"Cultural|"
                r"Sports|"
                r"Certificates)",
                line,
                re.IGNORECASE
            ):
                break

            if current["description"]:

                current["description"] += " "

            current["description"] += line

    if current:

        current["description"] = (
            current["description"].strip()
        )

        projects.append(current)

    cleaned_projects = []

    for project in projects:

        name = project["name"].strip()
        description = project["description"].strip()

        if not name:
            continue

        if re.match(
            r"^(Other Projects|CERTIFICATIONS|"
            r"Certifications|Competitions)",
            name,
            re.IGNORECASE
        ):
            continue

        cleaned_projects.append({
            "name": name,
            "description": description
        })

    return cleaned_projects


# =========================================================
# CLEAN ENTRIES
# =========================================================

def clean_entries(entries):

    cleaned = []

    for entry in entries:

        entry = re.sub(
            r"\s+",
            " ",
            entry
        ).strip()

        entry = re.sub(
            r"--\s*\d+\s+of\s+\d+\s*--",
            "",
            entry,
            flags=re.IGNORECASE
        ).strip()

        if entry:
            cleaned.append(entry)

    return cleaned


# =========================================================
# EXTRACT BASIC PERSONAL INFORMATION
# =========================================================

def extract_basic_info(text):

    name = ""
    email = ""
    phone = ""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # -----------------------------------------------------
    # Email
    # -----------------------------------------------------

    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    if email_match:

        email = email_match.group(0)

    # -----------------------------------------------------
    # Phone
    # -----------------------------------------------------

    phone_match = re.search(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
        text
    )

    if phone_match:

        phone = phone_match.group(0)

    # -----------------------------------------------------
    # Name
    # -----------------------------------------------------

    for line in lines[:10]:

        candidate = line.strip()

        if "@" in candidate:
            continue

        if re.search(r"\d", candidate):
            continue

        if any(
            word in candidate.lower()
            for word in [
                "linkedin",
                "github",
                "leetcode",
                "objective"
            ]
        ):
            continue

        words = candidate.split()

        if 2 <= len(words) <= 4:

            if all(
                re.match(
                    r"^[A-Za-z.'-]+$",
                    word
                )
                for word in words
            ):

                name = candidate
                break

    return {
        "name": name,
        "email": email,
        "phone": phone
    }


# =========================================================
# ANALYZE RESUME
# =========================================================

@app.post("/analyze")
def analyze_resume(data: dict):

    resume_text = data.get(
        "resumeText",
        ""
    )

    if not isinstance(resume_text, str):

        return {
            "message": "Invalid resume text",
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "wordCount": 0
        }

    if not resume_text.strip():

        return {
            "message": "No resume text provided",
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "wordCount": 0
        }

    original_text = resume_text

    resume_text = clean_text(resume_text)

    doc = nlp(resume_text)

    # -----------------------------------------------------
    # BASIC INFO
    # -----------------------------------------------------

    basic_info = extract_basic_info(
        original_text
    )

    # -----------------------------------------------------
    # SECTIONS
    # -----------------------------------------------------

    education_text = find_section(
        original_text,
        "education"
    )

    skills_text = find_section(
        original_text,
        "skills"
    )

    experience_text = find_section(
        original_text,
        "experience"
    )

    projects_text = find_section(
        original_text,
        "projects"
    )

    # -----------------------------------------------------
    # EXTRACTION
    # -----------------------------------------------------

    skills = extract_skills(
        original_text,
        skills_text
    )

    education = extract_education(
        education_text
    )

    experience = extract_experience(
        experience_text
    )

    projects = extract_projects(
        projects_text
    )

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {

        "message": "Resume analyzed",

        "name": basic_info["name"],

        "email": basic_info["email"],

        "phone": basic_info["phone"],

        "skills": skills,

        "education": education,

        "experience": experience,

        "projects": projects,

        "wordCount": len(doc)
    }


# =========================================================
# GENERATE INTERVIEW QUESTIONS
# =========================================================

@app.post("/generate-questions")
def generate_questions(data: dict):

    skills = data.get("skills", [])
    education = data.get("education", [])
    experience = data.get("experience", [])
    projects = data.get("projects", [])

    job_role = data.get(
        "jobRole",
        ""
    )

    job_description = data.get(
        "jobDescription",
        ""
    )

    difficulty = data.get(
        "difficulty",
        "Medium"
    )

    number_of_questions = data.get(
        "numberOfQuestions",
        10
    )

    question_type = data.get(
        "questionType",
        "technical"
    ).lower().strip()


    # =====================================================
    # TECHNICAL QUESTIONS
    # =====================================================

    if question_type == "technical":

        prompt = f"""
You are an expert technical interviewer.

Generate DIRECT KNOWLEDGE-BASED technical interview questions.

The questions must test the candidate's understanding of
technologies, programming concepts, frameworks, databases,
tools, and computer science concepts.

Candidate Skills:
{skills}

Job Role:
{job_role}

Job Description:
{job_description}

Difficulty:
{difficulty}

Number of Questions:
{number_of_questions}

STRICT RULES:

- Questions must be knowledge/theory based.
- Questions must focus on the skills listed in the resume.
- Questions should also consider the required skills in the job role
  and job description.
- Ask direct technical questions such as:
  "What is React.js?"
  "How does MongoDB indexing work?"
  "What is the difference between SQL and NoSQL?"
  "How does JWT authentication work?"
- Questions may test definitions, concepts, architecture,
  differences, working principles, advantages/disadvantages,
  use cases, syntax concepts, or core technical understanding.
- DO NOT ask questions about the candidate's projects.
- DO NOT ask questions about internships or previous work experience.
- DO NOT ask "How did you implement..." questions.
- DO NOT ask "Explain your project..." questions.
- DO NOT ask behavioral questions.
- DO NOT ask HR questions.
- Do not invent skills that are completely unrelated to the resume,
  job role, or job description.
- Avoid duplicate questions.
- Match the requested difficulty.
- Return ONLY the questions.
- Number the questions from 1 onwards.
"""


    # =====================================================
    # EXPERIENCE QUESTIONS
    # =====================================================

    elif question_type == "experience":

        prompt = f"""
You are an expert technical interviewer.

Generate TECHNICAL EXPERIENCE-BASED interview questions.

These questions must be based specifically on the candidate's
projects, internships, and previous technical experience.

Candidate Skills:
{skills}

Projects:
{projects}

Experience / Internships:
{experience}

Job Role:
{job_role}

Job Description:
{job_description}

Difficulty:
{difficulty}

Number of Questions:
{number_of_questions}

STRICT RULES:

- Questions must be technical.
- Questions must be based on the candidate's actual projects,
  internships, and work experience.
- Ask about technologies used in the projects or experience.
- Ask about implementation decisions, architecture, technical
  challenges, debugging, database design, APIs, frameworks,
  performance, security, deployment, or technical problem solving
  when supported by the resume.
- Questions should make the candidate explain what they actually
  built or worked on.
- Questions may reference specific project names or internship
  technologies.
- DO NOT ask generic HR questions.
- DO NOT ask behavioral questions.
- DO NOT ask personal questions.
- DO NOT ask unrelated theoretical questions that have no connection
  to the candidate's projects or experience.
- Do not invent project details or technologies.
- Avoid duplicate questions.
- Match the requested difficulty.
- Return ONLY the questions.
- Number the questions from 1 onwards.
"""


    # =====================================================
    # HR QUESTIONS
    # =====================================================

    elif question_type == "hr":

        prompt = f"""
You are an experienced HR interviewer.

Generate HR and behavioral interview questions personalized
to the candidate.

Candidate Name:
{data.get("name", "")}

Skills:
{skills}

Education:
{education}

Experience:
{experience}

Projects:
{projects}

Job Role:
{job_role}

Job Description:
{job_description}

Difficulty:
{difficulty}

Number of Questions:
{number_of_questions}

STRICT RULES:

- Questions must be HR, behavioral, personal, or
  company/job-role related.
- Questions can be based on the candidate's resume.
- Questions may cover:
  * Tell me about yourself.
  * Strengths and weaknesses.
  * Career goals.
  * Motivation.
  * Teamwork.
  * Leadership.
  * Communication.
  * Conflict handling.
  * Problem solving from a behavioral perspective.
  * Why this job role?
  * Why should we hire you?
  * Why do you want to join the company?
  * Questions about career choices or resume details.
- Questions may reference the candidate's education,
  internships, projects, or career background when appropriate.
- DO NOT ask technical knowledge questions.
- DO NOT ask programming questions.
- DO NOT ask questions such as "What is React?"
- DO NOT ask implementation or coding questions.
- Avoid duplicate questions.
- Keep questions appropriate for a professional interview.
- Match the requested difficulty.
- Return ONLY the questions.
- Number the questions from 1 onwards.
"""


    # =====================================================
    # INVALID QUESTION TYPE
    # =====================================================

    else:

        return {
            "message": "Invalid question type",
            "questions": "",
            "error": (
                "questionType must be "
                "'technical', 'experience', or 'hr'"
            )
        }


    # =====================================================
    # GENERATE QUESTIONS WITH GEMINI
    # =====================================================

    models = [
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite"
    ]

    for model in models:

        try:

            print(
                f"Generating {question_type} questions "
                f"with {model}..."
            )

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1500
                )
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response"
                )

            print(
                f"{question_type.capitalize()} "
                f"question generation successful "
                f"using {model}."
            )

            return {
                "message":
                    "Interview questions generated successfully",

                "questionType":
                    question_type,

                "questions":
                    response.text
            }

        except Exception as error:

            print(
                f"{model} failed: {error}"
            )

            # Try the next model immediately
            continue


    # =====================================================
    # ALL MODELS FAILED
    # =====================================================

    print(
        "Gemini question generation failed "
        "with all available models."
    )

    return {
        "message":
            "Failed to generate interview questions",

        "questionType":
            question_type,

        "questions":
            "",

        "error":
            "Gemini is currently unavailable. Please try again."
    }

# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/")
def home():

    return {
        "message": "AI Interview AI Service is running!",
        "status": "OK"
    }