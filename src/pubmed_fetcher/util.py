import re

def is_non_academic(affiliation: str) -> bool:
    academic_keywords = [
        "university", "institute", "college", "hospital",
        "school", "center", "department"
    ]
    non_academic_keywords = [
        "inc", "ltd", "pharma", "biotech", "gmbh", "therapeutics",
        "genentech", "pfizer", "moderna", "astrazeneca", "sanofi", "corporation"
    ]

    affil_lower = affiliation.lower()
    return (
        any(word in affil_lower for word in non_academic_keywords) and
        not any(word in affil_lower for word in academic_keywords)
    )


def extract_email(text: str) -> str:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group() if match else ""
