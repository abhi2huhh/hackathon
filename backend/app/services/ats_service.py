from __future__ import annotations

import math
import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.text_utils import STOPWORDS, tokenize


DEGREE_TERMS = ("bachelor", "master", "b.tech", "btech", "m.tech", "phd", "degree", "university")
EXPERIENCE_TERMS = ("intern", "experience", "years", "engineer", "developer", "project")


def _contains_skill(text: str, skill: str) -> bool:
    pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
    return re.search(pattern, text.lower()) is not None


def _signal(text: str, terms: tuple[str, ...]) -> float:
    lowered = text.lower()
    hits = sum(1 for term in terms if term in lowered)
    return min(1.0, hits / max(len(terms) * 0.45, 1))


def analyze_resume(parsed: dict, role: dict, weights: dict) -> dict:
    raw = parsed.get("raw_text") or ""
    required = [s for s in (role.get("required_skills") or []) if s]
    preferred = [s for s in (role.get("preferred_skills") or []) if s]
    keywords = [s for s in (role.get("keywords") or []) if s]

    matched_required = [s for s in required if _contains_skill(raw, s)]
    missing_required = [s for s in required if s not in matched_required]
    matched_preferred = [s for s in preferred if _contains_skill(raw, s)]
    matched_keywords = [s for s in keywords if _contains_skill(raw, s)]
    missing_keywords = [s for s in keywords if s not in matched_keywords]

    skill_score = (len(matched_required) / len(required) * 100) if required else 0
    pref_bonus = (len(matched_preferred) / len(preferred) * 15) if preferred else 0
    skill_match_score = min(100.0, skill_score + pref_bonus * 0.4)

    keyword_match_score = (len(matched_keywords) / len(keywords) * 100) if keywords else 0

    corpus = [raw, f"{role.get('description','')} {' '.join(required + preferred + keywords)}"]
    try:
        vectorizer = TfidfVectorizer(stop_words=list(STOPWORDS), max_features=4000)
        matrix = vectorizer.fit_transform(corpus)
        semantic_similarity_score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100)
    except ValueError:
        semantic_similarity_score = 0.0

    experience_signal = _signal(raw, EXPERIENCE_TERMS) * 100
    education_signal = _signal(raw, DEGREE_TERMS) * 100

    final_ats_score = (
        skill_match_score * weights["skill_match"]
        + keyword_match_score * weights["keyword_match"]
        + semantic_similarity_score * weights["semantic"]
        + experience_signal * weights["experience"]
        + education_signal * weights["education"]
    )
    final_ats_score = round(max(0.0, min(100.0, final_ats_score)), 1)

    suggestions = []
    if missing_required:
        suggestions.append(
            "Add evidence for missing required skills: " + ", ".join(missing_required[:8]) + "."
        )
    if missing_keywords:
        suggestions.append(
            "Increase role-specific keyword coverage with: " + ", ".join(missing_keywords[:8]) + "."
        )
    if education_signal < 40:
        suggestions.append("Include education details (degree, institution, and graduation year).")
    if experience_signal < 40:
        suggestions.append("Quantify internships, jobs, or projects with tools, outcomes, and duration.")
    if not suggestions:
        suggestions.append("Resume language already aligns well with this role. Tighten metrics next.")

    resume_tokens = Counter(tokenize(raw))
    keyword_analysis = [
        {"keyword": kw, "present": kw in matched_keywords, "mentions": resume_tokens.get(kw.lower().split()[0], 0)}
        for kw in keywords[:20]
    ]

    return {
        "score": final_ats_score,
        "matched_skills": matched_required + [s for s in matched_preferred if s not in matched_required],
        "missing_skills": missing_required,
        "preferred_skills_matched": matched_preferred,
        "keyword_analysis": keyword_analysis,
        "suggestions": suggestions,
        "dimensions": {
            "skill_match_score": round(skill_match_score, 1),
            "keyword_match_score": round(keyword_match_score, 1),
            "semantic_similarity_score": round(semantic_similarity_score, 1),
            "experience_signal": round(experience_signal, 1),
            "education_signal": round(education_signal, 1),
        },
        "disclaimer": "This is an estimated compatibility score, not an official employer ATS result.",
        "resume_summary": {
            "name": parsed.get("name"),
            "email": parsed.get("email"),
            "skill_count": len(parsed.get("skills") or []),
            "has_experience": bool(parsed.get("experience")),
            "has_education": bool(parsed.get("education")),
        },
    }
