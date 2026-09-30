from pypdf import PdfReader
import re


# ============================================================
# 1. PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path):
    """Extract text from all pages of a PDF resume."""

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ============================================================
# 2. TEXT CLEANING
# ============================================================

def clean_text(text):
    """Remove unnecessary spaces and blank lines."""

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


# ============================================================
# 3. SECTION DETECTION
# ============================================================

def detect_sections(text):
    """Detect common resume sections."""

    section_keywords = {

        "education": [
            "education",
            "academic background",
            "educational qualification"
        ],

        "skills": [
            "technical skills",
            "skills",
            "technical expertise"
        ],

        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "internship",
            "internships"
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects"
        ],

        "certifications": [
            "certifications",
            "certificates",
            "certification",
            "certifications & activities",
            "certifications and activities",
            "certifications & achievements"
        ],

        "achievements": [
            "achievements",
            "awards",
            "accomplishments"
        ]
    }

    sections = {}

    current_section = "other"

    sections[current_section] = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        line_lower = line.lower()

        detected_section = None

        # Check whether the current line is a section heading
        for section_name, keywords in section_keywords.items():

            for keyword in keywords:

                if line_lower == keyword:
                    detected_section = section_name
                    break

            if detected_section:
                break

        # If a section heading is found
        if detected_section:

            current_section = detected_section

            if current_section not in sections:
                sections[current_section] = []

        # Otherwise add line to current section
        else:

            sections[current_section].append(line)

    return sections


# ============================================================
# 4. PERSONAL INFORMATION PARSER
# ============================================================

def parse_personal_info(other_content):
    """
    Extract name, email, phone, LinkedIn and GitHub
    from the beginning of the resume.
    """

    personal_info = {
        "name": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": ""
    }

    if not other_content:
        return personal_info

    # Combine all lines because PDF extraction can sometimes
    # put contact information into a single line.
    contact_text = " ".join(other_content)

    # --------------------------------------------------------
    # Name
    # --------------------------------------------------------

    first_line = other_content[0].strip()

    if (
        "@" not in first_line
        and "linkedin" not in first_line.lower()
        and "github" not in first_line.lower()
    ):
        personal_info["name"] = first_line

    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------

    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        contact_text
    )

    if email_match:
        personal_info["email"] = email_match.group(0)

    # --------------------------------------------------------
    # Phone
    # --------------------------------------------------------

    phone_match = re.search(
        r'(?:\+91[\s-]?)?[6-9]\d{9}',
        contact_text
    )

    if phone_match:
        personal_info["phone"] = phone_match.group(0)

    # --------------------------------------------------------
    # LinkedIn
    # --------------------------------------------------------

    linkedin_match = re.search(
        r'(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+',
        contact_text,
        re.IGNORECASE
    )

    if linkedin_match:
        personal_info["linkedin"] = linkedin_match.group(0)

    # --------------------------------------------------------
    # GitHub
    # --------------------------------------------------------

    github_match = re.search(
        r'(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+',
        contact_text,
        re.IGNORECASE
    )

    if github_match:
        personal_info["github"] = github_match.group(0)

    return personal_info


# ============================================================
# 5. SKILLS PARSER
# ============================================================

def parse_skills(skill_lines):
    """Convert skill section lines into a clean list of skills."""

    skills = []

    for line in skill_lines:

        line = line.strip()

        if not line:
            continue

        # Example:
        #
        # Languages: Python, C/C++, SQL
        #
        # Remove the category before ':'
        if ":" in line:

            _, skill_text = line.split(":", 1)

        else:

            skill_text = line

        # Split comma-separated skills
        items = skill_text.split(",")

        for item in items:

            skill = item.strip()

            if skill and skill not in skills:

                skills.append(skill)

    return skills


# ============================================================
# 6. EDUCATION PARSER
# ============================================================

def parse_education(education_lines):
    """
    Convert education lines into structured education records.
    """

    education = []

    current_entry = None

    for line in education_lines:

        line = line.strip()

        if not line:
            continue

        line_lower = line.lower()

        # ----------------------------------------------------
        # Degree detection
        # ----------------------------------------------------

        is_degree = any(keyword in line_lower for keyword in [
            "bachelor",
            "b.tech",
            "btech",
            "b.e",
            "b.e.",
            "be ",
            "master",
            "m.tech",
            "mtech",
            "m.e",
            "m.e.",
            "me ",
            "diploma",
            "degree"
        ])

        # ----------------------------------------------------
        # CGPA detection
        # ----------------------------------------------------

        cgpa_match = re.search(
            r'cgpa\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)',
            line,
            re.IGNORECASE
        )

        # ----------------------------------------------------
        # Institution detection
        # ----------------------------------------------------

        is_institution = any(keyword in line_lower for keyword in [
            "college",
            "university",
            "institute",
            "school",
            "polytechnic"
        ])

        # ----------------------------------------------------
        # If degree starts a new education record
        # ----------------------------------------------------

        if is_degree:

            if current_entry:
                education.append(current_entry)

            current_entry = {
                "institution": "",
                "degree": line,
                "field": "",
                "duration": "",
                "cgpa": ""
            }

        # ----------------------------------------------------
        # Institution
        # ----------------------------------------------------

        elif is_institution:

            if current_entry is None:

                current_entry = {
                    "institution": line,
                    "degree": "",
                    "field": "",
                    "duration": "",
                    "cgpa": ""
                }

            else:

                # If current entry already has institution,
                # start a new education record.
                if current_entry.get("institution"):

                    education.append(current_entry)

                    current_entry = {
                        "institution": line,
                        "degree": "",
                        "field": "",
                        "duration": "",
                        "cgpa": ""
                    }

                else:

                    current_entry["institution"] = line

        # ----------------------------------------------------
        # CGPA
        # ----------------------------------------------------

        elif cgpa_match:

            if current_entry is None:

                current_entry = {
                    "institution": "",
                    "degree": "",
                    "field": "",
                    "duration": "",
                    "cgpa": ""
                }

            current_entry["cgpa"] = cgpa_match.group(1)

        # ----------------------------------------------------
        # Duration / years
        # ----------------------------------------------------

        elif re.search(r'\b20\d{2}\b.*\b20\d{2}\b', line):

            if current_entry is None:

                current_entry = {
                    "institution": "",
                    "degree": "",
                    "field": "",
                    "duration": "",
                    "cgpa": ""
                }

            current_entry["duration"] = line

        # ----------------------------------------------------
        # Other education information
        # ----------------------------------------------------

        else:

            if current_entry is not None:

                # If the degree line contains the field,
                # keep the full degree line for now.
                if not current_entry.get("field"):

                    current_entry["field"] = line

    # Add final record
    if current_entry:
        education.append(current_entry)

    return education


# ============================================================
# 7. RESUME DATA EXTRACTION
# ============================================================

def extract_resume_data(sections):
    """Convert detected resume sections into structured data."""

    resume = {

        "personal_info": {
            "name": "",
            "email": "",
            "phone": "",
            "linkedin": "",
            "github": ""
        },

        "education": [],

        "skills": [],

        "experience": [],

        "projects": [],

        "certifications": [],

        "achievements": []
    }

    # --------------------------------------------------------
    # Personal Information
    # --------------------------------------------------------

    resume["personal_info"] = parse_personal_info(
        sections.get("other", [])
    )

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    resume["education"] = parse_education(
        sections.get("education", [])
    )

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    resume["skills"] = parse_skills(
        sections.get("skills", [])
    )

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    resume["experience"] = sections.get(
        "experience",
        []
    )

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    resume["projects"] = sections.get(
        "projects",
        []
    )

    # --------------------------------------------------------
    # Certifications
    # --------------------------------------------------------

    resume["certifications"] = sections.get(
        "certifications",
        []
    )

    # --------------------------------------------------------
    # Achievements
    # --------------------------------------------------------

    resume["achievements"] = sections.get(
        "achievements",
        []
    )

    return resume


# ============================================================
# 8. MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Get resume path
    # --------------------------------------------------------

    pdf_path = input(
        "Enter the path to the resume PDF: "
    )

    # --------------------------------------------------------
    # Extract raw PDF text
    # --------------------------------------------------------

    raw_text = extract_text_from_pdf(
        pdf_path
    )

    # --------------------------------------------------------
    # Clean text
    # --------------------------------------------------------

    cleaned_text = clean_text(
        raw_text
    )

    # --------------------------------------------------------
    # Detect sections
    # --------------------------------------------------------

    sections = detect_sections(
        cleaned_text
    )

    # --------------------------------------------------------
    # Extract structured data
    # --------------------------------------------------------

    resume_data = extract_resume_data(
        sections
    )

    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    print(
        "\n========== STRUCTURED RESUME DATA ==========\n"
    )

    # --------------------------------------------------------
    # Personal Information
    # --------------------------------------------------------

    print(
        "\n--- PERSONAL INFORMATION ---"
    )

    for key, value in resume_data[
        "personal_info"
    ].items():

        print(
            f"{key}: {value}"
        )

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    print(
        "\n--- EDUCATION ---"
    )

    for education in resume_data["education"]:

        print(education)

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    print(
        "\n--- SKILLS ---"
    )

    for skill in resume_data["skills"]:

        print(skill)

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    print(
        "\n--- EXPERIENCE ---"
    )

    for experience in resume_data["experience"]:

        print(experience)

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    print(
        "\n--- PROJECTS ---"
    )

    for project in resume_data["projects"]:

        print(project)

    # --------------------------------------------------------
    # Certifications
    # --------------------------------------------------------

    print(
        "\n--- CERTIFICATIONS ---"
    )

    for certification in resume_data[
        "certifications"
    ]:

        print(certification)

    # --------------------------------------------------------
    # Achievements
    # --------------------------------------------------------

    print(
        "\n--- ACHIEVEMENTS ---"
    )

    for achievement in resume_data[
        "achievements"
    ]:

        print(achievement)