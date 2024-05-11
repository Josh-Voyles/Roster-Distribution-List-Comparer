from src import parse_roster

TEST_DISTRO_CORRECT = "./tests/test_data/test_distro_correct.txt"
TEST_ROSTER_CORRECT = "./tests/test_data/test_roster_correct.txt"
TEST_ROSTER_ERROR = "./tests/test_data/test_roster_error.txt"
TEST_DISTRO_ERROR = "./tests/test_data/test_distro_error.txt"

def test_is_correct_format():
    result = \
    parse_roster.is_correct_format(TEST_ROSTER_CORRECT, 'alpha')
    assert result == []

    result = \
    parse_roster.is_correct_format(TEST_DISTRO_CORRECT, 'distro')
    assert result == []

def test_is_wrong_format():
    result = parse_roster.is_correct_format(TEST_ROSTER_ERROR, 'alpha')
    assert result == [
        'Fix alpha roster at line: 3 -> HENRY LUKE',
        'Fix alpha roster at line: 5 -> MATHEWS, ashley C',
        'Fix alpha roster at line: 8 -> MUSK, ELON 1',
        "Required Format -> LASTNAME, FIRSTNAME M"
    ]

    result = parse_roster.is_correct_format(TEST_DISTRO_ERROR, 'distro')

    correct_format = "LASTNAME, FIRSTNAME M Rank " + \
    "USAF AFDW BAND/FLIGHT <john.doe@us.af.mil>;"

    assert result == [
        'Fix distro format at line: 1 -> ' + \
        'DEEN JAMES SMSgt USAF AFDW USAF BAND/BABB <james.deen@us.af.mil>',
        'Fix distro format at line: 4 -> ' + \
        'PAIGE, LARRY L TSgt USAF AFDW USAF BAND/BABS <larry.l.paigeus.af.mil>',
        'Fix distro format at line: 5 -> ' + \
        'MATHEWS, ASHLEY C SMSgt USAF AFDW USAF BAND/BABO <ashley.mathews@af.mail.mil>',
        f"Required Format -> {correct_format}"
    ]

def test_load_roster():
    result = parse_roster.load_roster(TEST_ROSTER_CORRECT)

    assert result == [
    'JAMES DEEN',
    'JAMES DOE',
    'LUKE HENRY',
    'LARRY PAIGE',
    'ASHLEY MATHEWS',
    'ADAM THOMPSON',
    'JAMES THOMAS SPENCER',
    'ELON MUSK',
    'STANLEY MORGAN',
    'CHRISTOPHER ADAMSON',
    'HENRY ADAMSON'
    ]

def test_get_first_last():
    test1 = "DOE, JOHN C"
    test2 = "DEERE DOE, JOHN C"
    test3 = \
    "DEERE DOE, JOHN C III USAF SQUADRON UNIT/FLIGHT <email.3.4@us.af.mil>;"

    result = parse_roster.get_first_last(test1)
    assert result == "JOHN DOE"
    result = parse_roster.get_first_last(test2)
    assert result == "JOHN DEERE DOE"
    result = parse_roster.get_first_last(test3)
    assert result == "JOHN DEERE DOE"

def test_remove_semic_newline():
    line = \
    "THOMAS SPENCER, JAMES LEE II TSgt USAF AFDW BAND/BABC <james.l.thomas-spencer@us.af.mil>;\n"
    result = parse_roster.remove_semic_newline(line)
    assert result == \
    "THOMAS SPENCER, JAMES LEE II TSgt USAF AFDW BAND/BABC <james.l.thomas-spencer@us.af.mil>"

def test_is_distro_name():
    distro = "AFAF_AFTEAM_ALL"
    not_distro = "AF GUYS SPORTS"
    not_distro2 = "AF GUYS_SPORTS"
    not_distro3 = \
    "THOMAS SPENCER, JAMES LEE II TSgt USAF AFDW BAND/BABC <james.l.thomas-spencer@us.af.mil>;\n"
    assert parse_roster.is_distro_name(distro) == True
    assert parse_roster.is_distro_name(not_distro) == False
    assert parse_roster.is_distro_name(not_distro2) == False
    assert parse_roster.is_distro_name(not_distro3) == False

def test_get_email():
    test_name = 'STEVENS, CHRISTOPHER J MSgt USAF AFDW USAF BAND/BABN <christopher.adamson@us.af.mil>'
    correct_email = 'christopher.adamson@us.af.mil'
    assert parse_roster.get_email(test_name) == correct_email

def test_to_remove_from_distro_list():
    correct_email = 'christopher.adamson@us.af.mil'

    to_remove = [
        '\n--TEST_LIST--',
        f'CHRISTOPHER STEVENS {correct_email}'
    ]
    to_add = ['HENRY ADAMSON']

    assert parse_roster.to_remove_from_distro_list(TEST_DISTRO_CORRECT,
        parse_roster.load_roster(TEST_ROSTER_CORRECT)) == to_remove
