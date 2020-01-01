from util.driver import parse_secret

MISSING_EMAIL_MSG = ('No email address provided for login. ',
                     'Pass via command line with --email=XXXXX or set in secret.yaml in project root directory')
INVALID_EMAIL_MSG = ('Email address in secret.yaml is invalid. '
                     'Enter a valid email address, or remove it and pass via command line with `--email=XXXXX`.')
MISSING_PW_MSG = ('No password provided for login. ',
                  'Pass via command line with --pw=XXXXX or set in secret.yaml in project root directory')
INVALID_PW_MSG = ('Password in secret.yaml is invalid.',
                  'Enter a valid password, or remove it and pass via command line with --pw=XXXXX')


def validate_email(email):
    if email and len(email) > 1 and '@' in email:
        return email
    else:
        raise ValueError(INVALID_EMAIL_MSG)


def validate_pw(pw):
    if pw and len(pw) > 1:
        return pw
    else:
        raise ValueError(INVALID_PW_MSG)


def get_secret(key):
    value = parse_secret()[key]
    if 'email' in key:
        if value:
            return validate_email(value)
    elif 'pw' in key:
        if value:
            return validate_pw(value)
    else:
        raise ValueError('Invalid key.')


def load_user(email=None, pw=None):
    if not email:
        email = get_secret('email')
    if not pw:
        pw = get_secret('pw')

    # make sure email and pw are set before proceeding
    assert email, MISSING_EMAIL_MSG
    assert pw, MISSING_PW_MSG

    return {
        'email': email,
        'pw': pw
    }
