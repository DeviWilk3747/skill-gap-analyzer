from extraction import extract_skills

def test_finds_basic_skills():
    """A simple posting returns the skills it mentions."""
    result = extract_skills("We use Python and PostgreSQL")

    assert "Python" in result
    assert "PostgreSQL" in result

def test_java_does_not_match_inside_javascript():
    """Substring matching would wrongly credit Java for a JavaScript posting."""
    result = extract_skills("Five years of JavaScript required")

    assert "JavaScript" in result
    assert "Java" not in result

def test_aliases_map_to_canonical_names():
    """Abbreviations will map to the canonical name. For instance js to JavaScript"""
    result = extract_skills("Looking for experience in JS, PY, and postgres")

    assert "JavaScript" in result
    assert "Python" in result
    assert "PostgreSQL" in result

def test_case_does_not_matter():
    """Any case should be able to pass through"""
    result = extract_skills("Looking for experiennce with PYTHON and java.")

    assert "Python" in result
    assert "Java" in result

def test_punctuation_case():
    """Any case that has non-alphanumeric characters should be able to pass through"""
    result = extract_skills("Two years of C++ required")

    assert "C++" in result

def test_duplicate_entry_for_JavaScript_and_JS():
    """Checks for single entry of JavaScript instead of duplicate"""
    result = extract_skills("JavaScript and JS")

    assert result.count("JavaScript") == 1

def test_react_native_not_React():
    """Makes sure the longest match pass"""
    result =  extract_skills("React Native developer")

    assert "React Native" in result
    assert "React" not in result