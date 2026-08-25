SUBSEPARATOR = "-" * 50


def format_principals(principal: dict) -> str:
    values = []

    for principal_type, principal_value in principal.items():
        values.append(f"{principal_type}: {principal_value}")

    return ", ".join(values) if values else "-"


def print_finding(finding: dict, number: int) -> None:
    actions = finding.get("action", [])
    action_text = ", ".join(actions) if actions else "-"

    print(f"Finding {number}")
    print(SUBSEPARATOR)
    print(f"Resource Type       : {finding.get('resourceType', '-')}")
    print(f"Resource            : {finding.get('resource', '-')}")
    print(
        f"Principal           : {format_principals(finding.get('principal', {}))}")
    print(f"Action              : {action_text}")
    print(f"Public              : {finding.get('isPublic', '-')}")
    print(f"Status              : {finding.get('status', '-')}")
    print(
        f"Source              : {', '.join(source.get('type', '-') for source in finding.get('sources', []))}")
    print(f"Analyzed At         : {finding.get('analyzedAt', '-')}")
    print()
