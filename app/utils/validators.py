def validate_token_description(description: str) -> tuple[bool, str]:
    """Validate token description"""
    if not description:
        return False, "Description cannot be empty"
    if len(description) > 200:
        return False, "Description must be less than 200 characters"
    if not description.strip():
        return False, "Description cannot be only whitespace"
    return True, ""
