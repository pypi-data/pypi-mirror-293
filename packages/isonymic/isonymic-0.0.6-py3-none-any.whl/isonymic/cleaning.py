import re

# Limpieza de nombres de familia del padrón
PREFIJOS = [
    "AL", "DELLA", "DALLA", "DE SAN", "DA SAN", "ST", "SAINT", "DAL", "L", "DE LA",
    "DE LOS", "DEL", "DOS", "DAS", "DES", "DA", "DE", "DI", "DO", "DU", "D", "LA",
    "LE", "LI", "LO", "VAN DER", "VAN DEN", "VAN", "VON", "SAN", "MC", "MAC", "O'",
    "O", "AP", "IN", "IM", "EL", "D'", "E", "UZ", "D", "L",
]

def has_suffix_word(phrase, suffix):
    """
    Checks if the suffix is in the correct position at the end of a word within the phrase.
    """
    try:
        return re.search(rf"\b\w+{re.escape(suffix)}\s+\w+\b", phrase) is not None
    except TypeError:
        return False

def contains_valid_prefix(phrase, prefix):
    """
    Checks if the prefix is at the beginning or in the middle of the phrase.
    """
    try:
        prefix_pattern = rf"(\b{re.escape(prefix)}\s+\w+\b)"
        return re.search(prefix_pattern, phrase) is not None
    except TypeError:
        return False

def rewrite_with_prefix(phrase, prefix):
    """
    Rewrites the phrase by replacing spaces in the prefix with underscores.
    """
    if has_suffix_word(phrase, prefix) and not contains_valid_prefix(phrase, prefix):
        return phrase

    try:
        pattern = re.compile(rf"(\b[\w\s]*?)({re.escape(prefix)}\s+\w+)([\w\s]*?\b)")
        match = pattern.search(phrase)
    except TypeError:
        match = None

    if not match:
        return phrase
    else:
        before, prefixed, after = match.groups()
        rewritten = f"{before}{prefixed.replace(' ', '_')}{after}"
        return rewritten.strip()

def rewrite_family_name(apellido):
    """
    Processes the surname, checking if it has any of the stipulated prefixes and returns a rewritten version:
    Surnames containing prefixes will be combined with underscores.
    """
    for prefijo in PREFIJOS:
        apellido = rewrite_with_prefix(apellido, prefijo)
    return apellido

def surname_from_familyname(familyname):
    """
    Extracts and returns the first part of the surname, replacing underscores with spaces.
    """
    try:
        return rewrite_family_name(familyname).split(" ")[0].replace("_", " ")
    except Exception:
        return None
