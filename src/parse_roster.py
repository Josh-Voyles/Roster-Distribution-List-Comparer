import re

# hard coded file paths for now
ALPHA_ROSTER_DIR = "./data/alpha_roster.txt"
DISTRO_TREE_DIR = "./data/USAF_DISTRO_TREE.txt"


def is_correct_format(roster, name) -> list:
    errors = list()
    line_number = 1
    alpha_format = r"[A-Z]+(\s[A-Z]+)?,(\s[A-Z]+)*$"
    tree_format = (
        r"[A-Z]+(\s[A-Z]+)?,\s[A-Z]+\s[a-zA-Z0-9\/\s\-]+"
        + r"\s<[a-zA-Z0-9\.\_\-]+@us\.af\.mil>[;]?"
    )
    correct_format = (
        "LASTNAME, FIRSTNAME M Rank " + "USAF AFDW BAND/FLIGHT <john.doe@us.af.mil>;"
    )

    with open(roster, "r") as file:
        for line in file:
            line = remove_semic_newline(line)
            match (name):
                case "alpha":
                    if (
                        not re.match(alpha_format, line)
                        and line != ""
                        and line != "\n"
                        and not is_distro_name(line)
                    ):
                        errors.append(
                            f"Fix alpha roster at line: {line_number} -> {line}"
                        )
                case "distro":
                    if (
                        not re.match(tree_format, line)
                        and line != ""
                        and line != "\n"
                        and not is_distro_name(line)
                    ):
                        errors.append(
                            f"Fix distro format at line: {line_number} -> {line}"
                        )
            line_number += 1

        if errors != [] and name == "alpha":
            errors.append("Required Format -> LASTNAME, FIRSTNAME M")
            return errors
        elif errors != [] and name == "distro":
            errors.append(f"Required Format -> {correct_format}")
            return errors
        return errors


def load_roster(roster) -> list:
    """
    Appends FIRSTNAME LASTNAME to roster
    returns roster
    """
    formated_roster = list()
    with open(roster, "r") as file:
        for line in file:
            first_last = get_first_last(line)
            formated_roster.append(first_last)
        return formated_roster


def get_first_last(last_first_middle) -> str:
    """
    Converts LASTNAME, FIRSTNAME MIDDLE {opt} ->
    FIRSTNAME MIDDLE {opt} LASTNAME ->
    FIRSTNAME LASTNAME <- RETURNS
    """
    last, fm = last_first_middle.split(",")
    fm = fm.strip().split(" ")
    last = last.strip()
    return fm[0] + " " + last


def remove_semic_newline(line) -> str:
    """formats string by removing ; and new line character"""
    return line.rstrip().replace(";", "").replace("\n", "")


def is_distro_name(line) -> bool:
    """checks for distro list name XXX_XXX_XXX"""
    distro_list_pattern = r"[A-Z]+(\_[A-Z]+)+$"
    return line != "" and re.match(distro_list_pattern, line) is not None


def get_email(line) -> str:
    """remove brackets around email, returns it"""
    line = line.split(" ")
    email = line[-1].replace("<", "").replace(">", "")
    return email.strip()


def get_distro_users(directory):
    distro_users = {}
    with open(directory, "r") as file:
        for line in file:
            line = remove_semic_newline(line)
            if line != "" and not is_distro_name(line):
                full_name = get_first_last(line)
                email = get_email(line)
                distro_users[full_name] = email
    return distro_users


def to_remove_from_distro_list(tree, roster):
    """
    Compares distro tree to alpha roster
    print distribution list
    prints names and email if not in roster
    """
    remove = list()

    with open(tree, "r") as file:
        for line in file:
            line = remove_semic_newline(line)
            if is_distro_name(line):
                remove.append(f"\n--{line}--")
            elif line != "":
                full_name = get_first_last(line)
                email = get_email(line)
                if full_name not in roster:
                    remove.append(full_name + " " + email)
    return remove


def find_not_in_distro(roster, distro_users):
    missing = []
    for name in roster:
        if name not in distro_users.keys():
            missing.append(name)
    return missing


def main():
    alpha_errors = is_correct_format(ALPHA_ROSTER_DIR, "alpha")
    distro_erros = is_correct_format(DISTRO_TREE_DIR, "distro")
    if alpha_errors == [] and distro_erros == []:
        alpha_roster = load_roster(ALPHA_ROSTER_DIR)
        print()
        print("******IN A DISTRO LIST BUT NOT IN ALPHA ROSTER*****")
        [print(x) for x in to_remove_from_distro_list(DISTRO_TREE_DIR, alpha_roster)]
        print()
        print("*****IN ALPHA ROSTER BUT NOT IN ANY DISTRO LIST******")
        [
            print(y)
            for y in find_not_in_distro(alpha_roster, get_distro_users(DISTRO_TREE_DIR))
        ]
    else:
        for line in alpha_errors + distro_erros:
            print(line)


if __name__ == "__main__":
    main()
