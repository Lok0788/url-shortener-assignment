# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

import random
import string
import re

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters+string.digits,k=length))


def is_valid_url(url):
    pattern=re.compile(
        r'^(http|https)://'
        r'[\w.-]+'
        r'(\.[\w.-]+)+'
        r'([\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=]*)?$'
        
    )
    return bool(pattern.match(url))