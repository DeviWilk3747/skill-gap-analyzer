import re
from app.skills_data import SKILLS

def build_lookup(skills):
    """Invert the SKILLS dictionary so every alias maps to its canonical name.
    
    SKILLS is written canonical-first because that is easier to amintain, but
    extraction needs to go the other way: given an alias found in text, which
    skill is it? This makes an 0(1) lookup instead of a scan.
    """
    lookup = {}
    for canonical, aliases in skills.items():
        for alias in aliases:
            lookup[alias] = canonical
    return lookup
def build_pattern(alias):
    """Build a regex patter that matches alias as a whole word.
    
    Word boundaries are only applied to where the alias actually starts or ends
    with an alphanumeric character, since \\b cannot match next to punctuation.
    """
    prefix = r"\b" if alias[0].isalnum() else ""
    suffix = r"\b" if alias[-1].isalnum() else ""
    return rf"{prefix}{re.escape(alias)}{suffix}"

def find_skill(text):
    r"""Return True if alias appears in text as a whole word."""
    return re.search(build_pattern, text) is not None
    
def extract_skills(text):
    """Return the canonical names of every skill mentioned in text."""

    lookup = build_lookup(SKILLS)
    text = text.lower()
    found = set()
    

    for alias in sorted(lookup, key=len, reverse=True):
        pattern =  build_pattern(alias)
        if re.search(pattern, text):
            found.add(lookup[alias])
            text = re.sub(pattern, " ", text)

    return list(found)