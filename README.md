# Phishing URL Awareness Checker

## Overview

Phishing messages use deceptive links to trick people into sharing information or visiting unsafe sites. This beginner-friendly command-line project checks the visible text of a URL for a few warning signs and explains why they may deserve attention. It does not open URLs, contact websites, or determine whether a link is safe.

## Features

- Detects an `@` symbol in the URL text.
- Flags URLs longer than 100 characters.
- Flags IPv4 address hostnames.
- Flags hostnames with five or more segments.
- Flags hostnames containing `xn--` punycode labels.
- Flags the HTTP scheme.
- Explains each warning and summarizes when review is needed.
- Handles malformed input without stopping the program.
- Accepts multiple URLs in one run; enter `q` to quit.

## Requirements

Python 3.8 or newer. No additional packages are required.

## Run

From this folder, open a terminal and run:

```text
python phishing_checker.py
```

On macOS or Linux, use `python3 phishing_checker.py` if `python` does not refer to Python 3. Enter a URL when prompted, then enter another URL or `q` to quit.

## Example

```text
Enter a sample URL (or type q to quit): http://192.0.2.10/account

Result:
- Uses an IP address instead of a familiar domain.
  Why it matters: An IP address hides the familiar domain name people expect.
- Uses HTTP. HTTPS alone does not prove trust.
  Why it matters: HTTP does not encrypt the connection; HTTPS alone still does not prove trust.

REVIEW CAREFULLY: 2 warning sign(s) found.
```

## Improvements made

The starter program was extended to check multiple URLs until the user quits, show a review summary when warning signs are found, and handle malformed URL text without crashing. Each warning also includes a short explanation so the output is easier to understand.

## What the results mean

These are simple text-based indicators, not a reputation check or a verdict. A URL with no listed warning signs may still be dangerous. A warning sign does not prove that a URL is malicious. HTTPS protects a connection in transit but does not prove that a site or sender is trustworthy. Inspect links carefully and use trusted channels to verify unexpected requests.

## Safety and privacy

The program works locally and only parses the text you enter. It does not open URLs, make internet requests, scan websites, or submit entered text anywhere. Do not enter passwords or other secrets into unexpected links.
