"""Streamlit interface for the local phishing URL awareness checker."""

import html

import streamlit as st

from phishing_checker import WARNING_EXPLANATIONS, has_warnings, inspect_url


st.set_page_config(
    page_title="LinkGuard | URL checker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
:root { --ink:#132238; --muted:#62738a; --blue:#1769e0; --mint:#d9f7e8; }
html, body, [class*="css"] { font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; }
[data-testid="stAppViewContainer"] { background:#f4f7fb; }
[data-testid="stHeader"] { background:transparent; }
[data-testid="stMain"] .block-container { max-width:1020px; padding-top:2.2rem; padding-bottom:4rem; }
h1,h2,h3 { font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif !important; color:var(--ink); letter-spacing:-.035em; }
.hero { background:linear-gradient(120deg,#101d35 0%,#183864 68%,#155b88 100%); border-radius:24px; padding:35px 40px 32px; color:#fff; box-shadow:0 18px 44px rgba(24,52,91,.17); position:relative; overflow:hidden; }
.hero:after { content:''; position:absolute; width:250px; height:250px; right:-65px; top:-115px; border-radius:50%; border:1px solid rgba(255,255,255,.12); box-shadow:0 0 0 30px rgba(255,255,255,.025),0 0 0 60px rgba(255,255,255,.02); }
.hero-kicker { color:#9dd9ff; font-size:12px; letter-spacing:.15em; font-weight:700; text-transform:uppercase; margin-bottom:12px; }
.hero h1 { color:#fff !important; font-size:clamp(30px,4vw,43px); line-height:1.12; margin:0 0 11px; }
.hero p { color:#d1deed; max-width:620px; font-size:16px; line-height:1.6; margin:0; }
.local-pill { display:inline-flex; align-items:center; gap:8px; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.16); color:#d9f7e8; border-radius:999px; padding:8px 12px; font-size:12px; font-weight:700; margin-top:22px; }
.section-label { color:#718198; font-size:12px; text-transform:uppercase; font-weight:700; letter-spacing:.12em; margin:27px 0 10px; }
.panel { background:#fff; border:1px solid #e4eaf2; border-radius:18px; padding:22px 24px; box-shadow:0 6px 20px rgba(21,45,79,.04); }
.result-card { background:#fff; border:1px solid #e4eaf2; border-radius:17px; padding:20px 22px; margin:11px 0; box-shadow:0 5px 18px rgba(21,45,79,.035); }
.result-title { color:#17263d; font-weight:700; font-size:15px; margin-bottom:5px; }
.result-copy { color:#65758b; font-size:13px; line-height:1.55; }
.safe-box { background:#eaf9f0; border:1px solid #c8eed8; border-radius:17px; padding:19px 21px; color:#1d603c; }
.warn-box { background:#fff5e8; border:1px solid #f5d7ae; border-radius:17px; padding:19px 21px; color:#80500d; }
.notice { background:#edf4ff; border:1px solid #d4e3fa; border-radius:16px; padding:16px 18px; color:#38516f; font-size:13px; line-height:1.6; }
.small-muted { color:#73839a; font-size:12px; }
div[data-testid="stForm"] { border:0; padding:0; }
div[data-testid="stTextInput"] input { border-radius:12px; min-height:48px; border:1px solid #dce4ee; background:#fbfcfe; color:#132238 !important; caret-color:#1769e0; }
div[data-testid="stTextInput"] input::placeholder { color:#8492a6 !important; opacity:1; }
div[data-testid="stTextInput"] input:focus { border-color:#4585e8; box-shadow:0 0 0 2px rgba(69,133,232,.12); }
div[data-testid="stFormSubmitButton"] button { border-radius:12px; min-height:46px; font-weight:700; background:#1769e0; border:0; }
div[data-testid="stFormSubmitButton"] button:hover { background:#1056bd; }
div[data-testid="stExpander"] { border:1px solid #e4eaf2; border-radius:14px; background:#fff; }
@media (max-width:650px) { .hero{padding:27px 24px;border-radius:19px}.panel{padding:18px}.hero p{font-size:14px} }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<section class="hero">
  <div class="hero-kicker">Cyber safety · link awareness</div>
  <h1>Pause before you click.</h1>
  <p>Check a link's visible text for common warning signs and understand what they mean. A quick second look can help you make a more careful decision.</p>
  <div class="local-pill">● &nbsp; PRIVATE BY DESIGN &nbsp;·&nbsp; TEXT ONLY</div>
</section>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">01 &nbsp; Inspect a link</div>', unsafe_allow_html=True)
with st.container(border=True):
    st.markdown("#### Paste the URL you want to review")
    with st.form("url_check_form"):
        raw_url = st.text_input(
            "URL to inspect",
            placeholder="https://example.com/account",
            label_visibility="collapsed",
            help="Paste the URL text only. Never enter passwords or other secrets.",
        )
        submitted = st.form_submit_button("Check this URL  →", type="primary", use_container_width=True)

if submitted:
    if not raw_url.strip():
        st.warning("Enter a URL above to start the check.")
    else:
        st.session_state.last_result = {
            "url": raw_url.strip(),
            "findings": inspect_url(raw_url),
        }

result = st.session_state.get("last_result")
if result:
    findings = result["findings"]
    warnings_found = has_warnings(findings)
    st.markdown('<div class="section-label">02 &nbsp; Your review</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("**Checked URL**")
        st.code(result["url"], language=None)

        if warnings_found:
            st.markdown(
                '<div class="warn-box"><b>Take a closer look</b><br>'
                'Found {} warning sign(s) in the visible URL text.</div>'.format(len(findings)),
                unsafe_allow_html=True,
            )
            for finding in findings:
                reason = ""
                if finding.startswith("Contains an @"):
                    reason = WARNING_EXPLANATIONS["@"]
                elif finding.startswith("Unusually long"):
                    reason = WARNING_EXPLANATIONS["length"]
                elif finding.startswith("Uses an IP"):
                    reason = WARNING_EXPLANATIONS["ip"]
                elif finding.startswith("Contains many hostname"):
                    reason = WARNING_EXPLANATIONS["subdomains"]
                elif finding.startswith("Contains a punycode"):
                    reason = WARNING_EXPLANATIONS["punycode"]
                elif finding.startswith("Uses HTTP"):
                    reason = WARNING_EXPLANATIONS["http"]
                st.markdown(
                    '<div class="result-card"><div class="result-title">⚠️ &nbsp;{}</div>'
                    '<div class="result-copy">{}</div></div>'.format(
                        html.escape(finding), html.escape(reason)
                    ),
                    unsafe_allow_html=True,
                )
        elif findings[0].startswith("No listed warning"):
            st.markdown(
                '<div class="safe-box"><b>No listed warning signs found</b><br>'
                'That does not guarantee this link is safe. Check the sender and destination independently.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning(findings[0])

st.markdown('<div class="section-label">What this checker looks for</div>', unsafe_allow_html=True)
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**URL structure**")
        st.caption("@ symbols · unusually long links")
    with col2:
        st.markdown("**Hostname clues**")
        st.caption("IP addresses · many subdomains · punycode")
    with col3:
        st.markdown("**Connection scheme**")
        st.caption("HTTP links · HTTPS is not a trust guarantee")

st.markdown(
    '<div class="notice"><b>Remember:</b> these checks are clues, not a verdict. '
    'A link with no listed warnings may still be harmful. This app only parses the text you paste; '
    'it never opens a URL or sends it to a website.</div>',
    unsafe_allow_html=True,
)

with st.expander("How to stay safer online"):
    st.markdown(
        """
- Check the sender through a separate, trusted channel when a message is unexpected.
- Read the full hostname carefully before signing in or sharing information.
- Be cautious with urgent requests, unexpected attachments, and login prompts.
- Never use a password manager prompt as proof that a link is trustworthy.
"""
    )
