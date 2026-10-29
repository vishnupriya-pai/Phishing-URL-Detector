# Test Results

Python version used: 3.14.7  |  Operating system: Windows  |  Date: 2026-10-29

| # | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| 1 | `https://www.example.com/login` | No listed warning signs | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | `http://192.0.2.10/account` | IP address + HTTP | IP address hostname and HTTP warning | PASS |
| 3 | `http://example.com@sample.invalid/login` | @ symbol + HTTP | @ symbol and HTTP warnings | PASS |
| 4 | `https://a.b.c.d.e.example.invalid/path` | Many hostname segments | Many hostname segments/subdomains warning | PASS |
| 5 | `https://xn--example.invalid/` | Punycode-style hostname | Punycode-style hostname warning | PASS |

## Notes

The five reserved sample URLs produced the workbook's expected findings. A malformed bracketed URL also returned a clear format message and the program continued to the next prompt. I learned that these are visible-text clues only; a URL with no listed warnings is not guaranteed safe.
