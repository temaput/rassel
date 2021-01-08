from dateutil.parser import parse as parse_date
from collections import defaultdict

DATE_FNAMES = (
    "dob",
    "subscriberDOB"
)

RACE_OPTS = (
    (
        "INDIAN",
        "ALASKAN"
    ),
    (
        "ASIAN",
    ),
    (
        "BLACK",
        "AFRICAN-AMERICAN"
    ),
    (
        "HAWAIIAN",
        "PACIFIC"
    ),
    (
        "WHITE"
    ),
    (
        "MULTIRACIAL"
    ),
    (
        "OTHER"
    ),
    (
        "UNKNOWN"
    )
)

ETHNICITY_OPTS = (
    (
        "HISPANIC"
    ),
    (
        "NON-HISPANIC"
    ),
    (
        "OTHER"
    ),
    (
        "UNKNOWN"
    )
)

SUBSCRIBER_RELATION_OPTS = (
    (
        "SELF"
    ),
    (
        "SPOUSE"
    ),
    (
        "OTHER"
    )
)

GENDER_OPTS = (
    (
        "MALE"
    ),
    (
        "FEMALE"
    ),
)

GENDERS = ["M", "F"]

OPTS_FIELDS = (
    ("race", RACE_OPTS),
    ("ethnicity", ETHNICITY_OPTS),
    ("subscriberRelation", SUBSCRIBER_RELATION_OPTS),
)

def process_option(s, opts):
    for i, words in enumerate(opts, 1):
        if s.upper() in words:
            return i 
    return len(opts)


def process_date(s):
    d = parse_date(s)
    return d.isoformat()


def process_gender(s):
    i = process_option(s, GENDER_OPTS)
    return GENDERS[i-1]


def process_survey(payload):
    for fname in payload:
        payload[fname] = str(payload[fname])
    if "sex" in payload:
        payload["sex"] = process_gender(payload["sex"])
    for fname, opts in OPTS_FIELDS:
        if fname in payload:
            payload[fname] = process_option(payload[fname], opts)
    for fname in DATE_FNAMES:
        if fname in payload:
            payload[fname] = process_date(payload[fname])

    result = defaultdict(str)
    result.update(payload)
    return result
