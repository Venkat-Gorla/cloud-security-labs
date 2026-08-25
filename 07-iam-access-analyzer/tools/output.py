"""Formatting and presentation helpers for the lab tools."""

SEPARATOR = "=" * 50
SUBSEPARATOR = "-" * 50


def format_principals(principal: dict) -> str:
    values = [
        f"{principal_type}: {principal_value}"
        for principal_type, principal_value in principal.items()
    ]
    return ", ".join(values) if values else "-"


def print_finding(finding: dict, number: int) -> None:
    actions = finding.get("action", [])
    action_text = ", ".join(actions) if actions else "-"
    sources = finding.get("sources", [])
    source_text = ", ".join(
        source.get("type", "-") for source in sources
    )

    print(f"Finding {number}")
    print(SUBSEPARATOR)
    print(f"Resource Type       : {finding.get('resourceType', '-')}")
    print(f"Resource            : {finding.get('resource', '-')}")
    print(
        f"Principal           : "
        f"{format_principals(finding.get('principal', {}))}"
    )
    print(f"Action              : {action_text}")
    print(f"Public              : {finding.get('isPublic', '-')}")
    print(f"Status              : {finding.get('status', '-')}")
    print(f"Source              : {source_text}")
    print(f"Analyzed At         : {finding.get('analyzedAt', '-')}")
    print()


def print_bucket_configuration(
    bucket_name: str,
    region: str,
    website: dict,
    public_access_block: dict,
    policy_statements: list[dict],
) -> None:
    print("Amazon S3 Bucket Configuration")
    print(SEPARATOR)
    print()
    print(f"Bucket              : {bucket_name}")
    print(f"Region              : {region}")
    print()

    print("Website")
    print(SUBSEPARATOR)
    print(
        f"Index document      : "
        f"{website.get('IndexDocument', {}).get('Suffix', '-')}"
    )
    print()

    configuration = public_access_block.get(
        "PublicAccessBlockConfiguration",
        {},
    )

    print("Public Access Block")
    print(SUBSEPARATOR)
    print(f"Block public ACLs   : {configuration.get('BlockPublicAcls', '-')}")
    print(
        f"Block public policy : "
        f"{configuration.get('BlockPublicPolicy', '-')}"
    )
    print(
        f"Ignore public ACLs  : "
        f"{configuration.get('IgnorePublicAcls', '-')}"
    )
    print(
        f"Restrict public     : "
        f"{configuration.get('RestrictPublicBuckets', '-')}"
    )
    print()

    print("Bucket Policy")
    print(SUBSEPARATOR)

    if not policy_statements:
        print("Statements          : None")
        print()
        return

    for statement in policy_statements:
        print(f"Statement           : {statement.get('Sid', '-')}")
        print(f"Effect              : {statement.get('Effect', '-')}")
        print(
            f"Principal           : "
            f"{format_principals(statement.get('Principal', {}))}"
            if isinstance(statement.get("Principal"), dict)
            else f"Principal           : {statement.get('Principal', '-')}"
        )
        print(
            f"Action              : "
            f"{format_actions(statement.get('Action', []))}"
        )
        print(
            f"Resource            : {format_value(statement.get('Resource', '-'))}")
        print()


def format_actions(actions: str | list[str]) -> str:
    if isinstance(actions, list):
        return ", ".join(actions) if actions else "-"
    return actions or "-"


def format_value(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "-"
    return str(value) if value is not None else "-"
