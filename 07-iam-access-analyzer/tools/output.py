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


def print_bucket_header(bucket_name: str, region: str) -> None:
    print("Amazon S3 Bucket Configuration")
    print(SEPARATOR)
    print()
    print(f"Bucket              : {bucket_name}")
    print(f"Region              : {region}")
    print()


def print_website_configuration(website: dict) -> None:
    print("Website")
    print(SUBSEPARATOR)
    print(
        f"Index document      : "
        f"{website.get('IndexDocument', {}).get('Suffix', '-')}"
    )
    print()


def print_public_access_block(configuration: dict) -> None:
    settings = configuration.get(
        "PublicAccessBlockConfiguration",
        {},
    )

    print("Public Access Block")
    print(SUBSEPARATOR)
    print(f"Block public ACLs   : {settings.get('BlockPublicAcls', '-')}")
    print(
        f"Block public policy : "
        f"{settings.get('BlockPublicPolicy', '-')}"
    )
    print(
        f"Ignore public ACLs  : "
        f"{settings.get('IgnorePublicAcls', '-')}"
    )
    print(
        f"Restrict public     : "
        f"{settings.get('RestrictPublicBuckets', '-')}"
    )
    print()


def print_bucket_policy(policy_statements: list[dict]) -> None:
    print("Bucket Policy")
    print(SUBSEPARATOR)

    if not policy_statements:
        print("Statements          : None")
        print()
        return

    for statement in policy_statements:
        print(f"Statement           : {statement.get('Sid', '-')}")
        print(f"Effect              : {statement.get('Effect', '-')}")

        principal = statement.get("Principal", {})
        if isinstance(principal, dict):
            principal_text = format_principals(principal)
        else:
            principal_text = str(principal)

        print(f"Principal           : {principal_text}")
        print(
            f"Action              : "
            f"{format_actions(statement.get('Action', []))}"
        )
        print(
            f"Resource            : "
            f"{format_value(statement.get('Resource', '-'))}"
        )
        print()


def print_bucket_configuration(
    bucket_name: str,
    region: str,
    website: dict,
    public_access_block: dict,
    policy_statements: list[dict],
) -> None:
    print_bucket_header(bucket_name, region)
    print_website_configuration(website)
    print_public_access_block(public_access_block)
    print_bucket_policy(policy_statements)


def format_actions(actions: str | list[str]) -> str:
    if isinstance(actions, list):
        return ", ".join(actions) if actions else "-"
    return actions or "-"


def format_value(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "-"
    return str(value) if value is not None else "-"
