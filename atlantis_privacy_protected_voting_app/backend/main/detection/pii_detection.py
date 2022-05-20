import re

def redact_free_text(free_text: str, first_name_voter: str, last_name_voter: str, national_id: str) -> str:
    """
    :param: free_text The free text to remove sensitive data from
    :returns: The redacted free text
    """
    try:
        email_regex = r"\b\S+@\S+.\S+\b"
        nation_id_regex = r"\d{3}(-| )?\d{2}(-| )?\d+"
        phone_regex = r"\(?\d{3}(\) | |-)?\d{3}-?\d{4}"
        free_text = re.sub(email_regex, "[REDACTED EMAIL]" , free_text)
        free_text = re.sub(
            last_name_voter,
            "[REDACTED NAME]",
            free_text,
            flags=re.IGNORECASE
        )
        free_text = re.sub(
            first_name_voter,
            "[REDACTED NAME]",
            free_text,
            flags=re.IGNORECASE
        )
        free_text = re.sub(
            phone_regex,
            "[REDACTED PHONE NUMBER]",
            free_text
        )
        free_text = re.sub(
            nation_id_regex,
            "[REDACTED NATIONAL ID]",
            free_text
        )
        return free_text
    except Exception as e:
        raise e
