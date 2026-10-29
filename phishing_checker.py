"""A local, text-only phishing URL awareness checker.

This tool inspects visible URL text for selected warning signs. It never opens
URLs or makes network requests, and its findings do not establish whether a URL
is safe or malicious.
"""

import re
from urllib.parse import urlparse


WARNING_EXPLANATIONS = {
    "@": "Browsers may treat text before @ as user information and ignore it.",
    "length": "Long URLs can make the real destination harder to spot.",
    "ip": "An IP address hides the familiar domain name people expect.",
    "subdomains": "Many hostname parts can make the actual registered domain unclear.",
    "punycode": "Punycode can represent international characters that resemble other letters.",
    "http": "HTTP does not encrypt the connection; HTTPS alone still does not prove trust.",
}


def inspect_url(raw_url):
    """Return warnings about visible URL text without accessing the URL."""
    url = raw_url.strip()
    if not url:
        return ["No URL entered."]

    candidate = url if "://" in url else "http://" + url
    try:
        parsed = urlparse(candidate)
        # Accessing .port validates malformed ports (for example, :abc).
        _ = parsed.port
    except ValueError:
        return ["This text is not a valid URL format."]

    host = (parsed.hostname or "").lower()
    if not host:
        return ["Could not identify a hostname."]

    findings = []
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")
    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")
    return findings


def has_warnings(findings):
    """Distinguish warnings from neutral input/status messages."""
    return bool(findings) and not findings[0].startswith(
        ("No URL entered", "Could not identify", "This text is not", "No listed warning")
    )


def main():
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")

    while True:
        raw_url = input("\nEnter a sample URL (or type q to quit): ")
        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)
        print("\nResult:")
        for item in findings:
            print("- " + item)
            if item.startswith("Contains an @"):
                print("  Why it matters: " + WARNING_EXPLANATIONS["@"])
            elif item.startswith("Unusually long"):
                print("  Why it matters: " + WARNING_EXPLANATIONS["length"])
            elif item.startswith("Uses an IP"):
                print("  Why it matters: " + WARNING_EXPLANATIONS["ip"])
            elif item.startswith("Contains many hostname"):
                print("  Why it matters: " + WARNING_EXPLANATIONS["subdomains"])
            elif item.startswith("Contains a punycode"):
                print("  Why it matters: " + WARNING_EXPLANATIONS["punycode"])
            elif item.startswith("Uses HTTP"):
                print("  Why it matters: " + WARNING_EXPLANATIONS["http"])

        if has_warnings(findings):
            print("\nREVIEW CAREFULLY: {} warning sign(s) found.".format(len(findings)))
        print("\nNever enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
