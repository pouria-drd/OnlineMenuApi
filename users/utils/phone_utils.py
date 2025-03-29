def normalize_phone_number(phone_number):
    """
    Normalizes Iranian phone numbers to a consistent format.

    The normalization process ensures that phone numbers starting with '0'
    are converted to the international format, which begins with '+98'.

    Example:
    - Input: "09123456789"
    - Output: "+989123456789"
    """
    if phone_number.startswith("0"):
        phone_number = (
            "+98" + phone_number[1:]
        )  # Converts '09123456789' to '+989123456789'
    return phone_number
