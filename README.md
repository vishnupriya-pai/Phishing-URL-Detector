# Phishing URL Awareness Checker

## Overview

This beginner-friendly Streamlit web app checks the visible text of a URL for selected warning signs and explains why they may deserve attention. It does not open URLs, contact websites, or determine whether a link is safe. A command-line version is also included.

## Features

- Detects an `@` symbol in the URL text.
- Flags URLs longer than 100 characters.
- Flags IPv4 address hostnames.
- Flags hostnames with five or more segments.
- Flags hostnames containing `xn--` punycode labels.
- Flags the HTTP scheme.
- Explains each warning and summarizes when review is needed.
- Handles malformed input without crashing.
- Provides a browser interface with Streamlit.

## Requirements

Python 3.8 or newer and Streamlit. See `requirements.txt`.

## Run the web app

From this folder, install the dependency:

```text
python -m pip install -r requirements.txt
```

Start Streamlit:

```text
python -m streamlit run app.py
```

The app opens in your browser. If it does not, open the local address printed in the terminal, usually `http://localhost:8501`.

## Run the command-line version

```text
python phishing_checker.py
```

On macOS or Linux, use `python3` if needed.

## What the results mean

These are simple text-based indicators, not a reputation check or a verdict. A URL with no listed warning signs may still be dangerous. A warning sign does not prove that a URL is malicious. HTTPS protects a connection in transit but does not prove that a site or sender is trustworthy. Inspect links carefully and use trusted channels to verify unexpected requests.

## Safety and privacy

The app works locally and only parses the text you enter. It does not open URLs, make internet requests, scan websites, or submit entered text anywhere. Do not enter passwords or other secrets.
