<<<<<<< HEAD
import streamlit as st
from groq import Groq
import re

# ── YOUR GROQ API KEY ─────────────────────────────────────────────────────────
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fashion Dude AI",
    page_icon="🕶️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

  :root {
    --black: #0a0a0a;
    --white: #f5f0eb;
    --gold: #c9a84c;
    --muted: #7a7065;
  }

  html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--black) !important;
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif;
  }

  #MainMenu, footer, header { visibility: hidden; }
  [data-testid="stDecoration"] { display: none; }

  .fd-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #222;
    margin-bottom: 1.5rem;
  }
  .fd-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: var(--white);
    letter-spacing: -1px;
    margin: 0;
  }
  .fd-header h1 span { color: var(--gold); }
  .fd-header p {
    font-size: 0.85rem;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.4rem;
  }

  .msg-row {
    display: flex;
    margin-bottom: 1.2rem;
    gap: 0.8rem;
  }
  .msg-row.user { flex-direction: row-reverse; }

  .avatar {
    width: 38px; height: 38px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
    border: 1px solid #333;
  }
  .avatar.bot  { background: #1a1a1a; }
  .avatar.user { background: #1c1810; border-color: var(--gold); }

  .bubble {
    max-width: 75%;
    padding: 0.85rem 1.1rem;
    border-radius: 16px;
    font-size: 0.92rem;
    line-height: 1.6;
  }
  .bubble.bot {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-top-left-radius: 4px;
    color: var(--white);
  }
  .bubble.user {
    background: #1c1810;
    border: 1px solid var(--gold);
    border-top-right-radius: 4px;
    color: var(--white);
  }
  .bubble.bot a {
    color: var(--gold);
    text-decoration: underline;
    word-break: break-all;
  }
  .bubble.bot a:hover { opacity: 0.8; }
  .bubble.bot ul, .bubble.bot ol { padding-left: 1.2rem; margin: 0.4rem 0; }
  .bubble.bot li { margin-bottom: 0.3rem; }
  .bubble.bot p { margin: 0.3rem 0; }
  .bubble.bot strong { color: var(--gold); }

  /* Shop button chips */
  .shop-links {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 10px;
  }
  .shop-btn {
    background: #1a1a1a;
    border: 1px solid var(--gold);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: var(--gold) !important;
    text-decoration: none !important;
    transition: all 0.2s;
  }
  .shop-btn:hover { background: var(--gold); color: #000 !important; }

  [data-testid="stChatInput"] > div {
    background: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 12px !important;
  }
  [data-testid="stChatInput"] textarea {
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
  }
  [data-testid="stChatInput"] button {
    background: var(--gold) !important;
    border-radius: 8px !important;
  }

  [data-testid="stSidebar"] {
    background: #0d0d0d !important;
    border-right: 1px solid #1e1e1e !important;
  }
  [data-testid="stSidebar"] * { color: var(--white) !important; }
</style>
""", unsafe_allow_html=True)

# ── Known fashion brands with real websites ───────────────────────────────────
BRAND_LINKS = {
    "nike": "https://www.nike.com",
    "adidas": "https://www.adidas.com",
    "zara": "https://www.zara.com",
    "h&m": "https://www.hm.com",
    "gucci": "https://www.gucci.com",
    "prada": "https://www.prada.com",
    "versace": "https://www.versace.com",
    "louis vuitton": "https://www.louisvuitton.com",
    "chanel": "https://www.chanel.com",
    "uniqlo": "https://www.uniqlo.com",
    "gap": "https://www.gap.com",
    "levi's": "https://www.levis.com",
    "levis": "https://www.levis.com",
    "ralph lauren": "https://www.ralphlauren.com",
    "calvin klein": "https://www.calvinklein.com",
    "tommy hilfiger": "https://www.tommy.com",
    "burberry": "https://www.burberry.com",
    "balenciaga": "https://www.balenciaga.com",
    "off-white": "https://www.off---white.com",
    "supreme": "https://www.supremenewyork.com",
    "patagonia": "https://www.patagonia.com",
    "north face": "https://www.thenorthface.com",
    "new balance": "https://www.newbalance.com",
    "puma": "https://www.puma.com",
    "converse": "https://www.converse.com",
    "vans": "https://www.vans.com",
    "forever 21": "https://www.forever21.com",
    "asos": "https://www.asos.com",
    "amazon fashion": "https://www.amazon.com/fashion",
    "shein": "https://www.shein.com",
    "myntra": "https://www.myntra.com",
    "flipkart fashion": "https://www.flipkart.com/clothing-and-accessories",
    "ajio": "https://www.ajio.com",
}

def google_shopping_link(query):
    q = query.replace(" ", "+")
    return f"https://www.google.com/search?q={q}&tbm=shop"

def extract_brands(text):
    """Find known brands mentioned in the AI reply."""
    found = {}
    text_lower = text.lower()
    for brand, url in BRAND_LINKS.items():
        if brand in text_lower:
            found[brand.title()] = url
    return found

def render_reply(text):
    # Remove all AI-generated image markdown (fake URLs)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', '', text)
    # Remove all AI-generated hyperlinks (replace with just the label text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'\1', text)
    # Remove bare URLs
    text = re.sub(r'https?://\S+', '', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Render lines
    lines = text.split("\n")
    html_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{stripped[2:]}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if stripped:
                html_lines.append(f"<p>{line}</p>")
    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)

def build_shop_buttons(text, user_question):
    """Build real working shop buttons based on brands found + search."""
    brands = extract_brands(text)
    buttons_html = ""

    # Add brand buttons
    for brand, url in brands.items():
        buttons_html += f'<a class="shop-btn" href="{url}" target="_blank">🛍️ {brand}</a>'

    # Always add a Google Shopping search button
    search_query = user_question + " fashion"
    shop_url = google_shopping_link(search_query)
    buttons_html += f'<a class="shop-btn" href="{shop_url}" target="_blank">🔍 Shop on Google</a>'

    return f'<div class="shop-links">{buttons_html}</div>'

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Fashion Dude — a supremely stylish, witty AI personal stylist with encyclopedic knowledge of fashion. Your personality:

- CONFIDENT & opinionated: bold takes on trends, silhouettes, color theory, and personal style
- WARM & encouraging: hype people up while giving honest, actionable advice
- CULTURALLY savvy: know runway fashion AND streetwear, vintage AND contemporary
- PRACTICAL: give real outfit ideas, brand recommendations across all budgets, and styling hacks
- PLAYFUL: use occasional fashion slang like slay, serve looks, that's a moment — but don't overdo it

Topics you excel at:
- Outfit advice for any occasion (work, date night, casual, formal)
- Building a capsule wardrobe
- Color coordination & pattern mixing
- Body type & fit guidance
- Budget styling tips
- Trend analysis (what's in, what's out, what's timeless)
- Brand and shopping recommendations
- Seasonal dressing & accessorizing

Always give specific, visual advice — mention actual colors, fabrics, silhouettes, and brand names.
Do NOT include any URLs, image links, or hyperlinks — just plain text and brand names.
Keep responses punchy and helpful."""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🕶️ Fashion Dude AI")
    st.markdown("---")
    st.markdown("**Your AI Personal Stylist**")
    st.markdown("Ask me anything about style, outfits, trends, or building your wardrobe.")
    st.markdown("---")

    st.markdown("**Your Vibe**")
    style_vibe = st.selectbox(
        "Style personality",
        ["Not set", "Minimalist", "Streetwear", "Business Casual", "Maximalist", "Vintage", "Athleisure", "Boho"],
        label_visibility="collapsed"
    )
    budget = st.selectbox(
        "Budget range",
        ["Not set", "Budget-friendly", "Mid-range", "Luxury", "Mix of all"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_question = ""
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="fd-header">
  <h1>Fashion <span>Dude</span> AI</h1>
  <p>Your Personal Style Consultant</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_question" not in st.session_state:
    st.session_state.last_question = ""

# ── Quick prompt chips ────────────────────────────────────────────────────────
QUICK_PROMPTS = [
    "🎽 Build me a capsule wardrobe",
    "💼 Business casual outfit ideas",
    "🌈 What colors suit me?",
    "👟 Best sneakers right now",
    "🌸 Spring 2025 trends",
    "💸 Style on a budget",
]

if not st.session_state.messages:
    cols = st.columns(3)
    for i, prompt in enumerate(QUICK_PROMPTS):
        with cols[i % 3]:
            if st.button(prompt, key=f"chip_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.last_question = prompt
                st.rerun()

# ── Render chat history ───────────────────────────────────────────────────────
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-row user">
          <div class="avatar user">👤</div>
          <div class="bubble user">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        html_content = render_reply(msg["content"])
        # Find the user question just before this reply
        prev_question = ""
        if i > 0 and st.session_state.messages[i-1]["role"] == "user":
            prev_question = st.session_state.messages[i-1]["content"]
        shop_buttons = build_shop_buttons(msg["content"], prev_question)
        st.markdown(f"""
        <div class="msg-row">
          <div class="avatar bot">🕶️</div>
          <div class="bubble bot">
            {html_content}
            {shop_buttons}
          </div>
        </div>""", unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask Fashion Dude anything about style…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.last_question = user_input

    system = SYSTEM_PROMPT
    if style_vibe != "Not set":
        system += f"\n\nThe user's style personality is: {style_vibe}."
    if budget != "Not set":
        system += f" Their budget range is: {budget}."

    groq_messages = [{"role": "system", "content": system}]
    for m in st.session_state.messages:
        groq_messages.append({"role": m["role"], "content": m["content"]})

    with st.spinner("Fashion Dude is thinking… ✨"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=groq_messages,
            max_tokens=1000,
            temperature=0.7,
        )
        reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
=======
import streamlit as st
from groq import Groq
import re

# ── Groq client ───────────────────────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fashion Dude AI",
    page_icon="🕶️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

  :root {
    --black: #0a0a0a;
    --white: #f5f0eb;
    --gold: #c9a84c;
    --muted: #7a7065;
  }

  html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--black) !important;
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif;
  }

  #MainMenu, footer, header { visibility: hidden; }
  [data-testid="stDecoration"] { display: none; }

  .fd-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #222;
    margin-bottom: 1.5rem;
  }
  .fd-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: var(--white);
    letter-spacing: -1px;
    margin: 0;
  }
  .fd-header h1 span { color: var(--gold); }
  .fd-header p {
    font-size: 0.85rem;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.4rem;
  }

  .msg-row {
    display: flex;
    margin-bottom: 1.2rem;
    gap: 0.8rem;
  }
  .msg-row.user { flex-direction: row-reverse; }

  .avatar {
    width: 38px; height: 38px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
    border: 1px solid #333;
  }
  .avatar.bot  { background: #1a1a1a; }
  .avatar.user { background: #1c1810; border-color: var(--gold); }

  .bubble {
    max-width: 75%;
    padding: 0.85rem 1.1rem;
    border-radius: 16px;
    font-size: 0.92rem;
    line-height: 1.6;
  }
  .bubble.bot {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-top-left-radius: 4px;
    color: var(--white);
  }
  .bubble.user {
    background: #1c1810;
    border: 1px solid var(--gold);
    border-top-right-radius: 4px;
    color: var(--white);
  }
  .bubble.bot a {
    color: var(--gold);
    text-decoration: underline;
    word-break: break-all;
  }
  .bubble.bot a:hover { opacity: 0.8; }
  .bubble.bot ul, .bubble.bot ol { padding-left: 1.2rem; margin: 0.4rem 0; }
  .bubble.bot li { margin-bottom: 0.3rem; }
  .bubble.bot p { margin: 0.3rem 0; }
  .bubble.bot strong { color: var(--gold); }

  /* Shop button chips */
  .shop-links {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 10px;
  }
  .shop-btn {
    background: #1a1a1a;
    border: 1px solid var(--gold);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: var(--gold) !important;
    text-decoration: none !important;
    transition: all 0.2s;
  }
  .shop-btn:hover { background: var(--gold); color: #000 !important; }

  [data-testid="stChatInput"] > div {
    background: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 12px !important;
  }
  [data-testid="stChatInput"] textarea {
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
  }
  [data-testid="stChatInput"] button {
    background: var(--gold) !important;
    border-radius: 8px !important;
  }

  [data-testid="stSidebar"] {
    background: #0d0d0d !important;
    border-right: 1px solid #1e1e1e !important;
  }
  [data-testid="stSidebar"] * { color: var(--white) !important; }
</style>
""", unsafe_allow_html=True)

# ── Known fashion brands with real websites ───────────────────────────────────
BRAND_LINKS = {
    "nike": "https://www.nike.com",
    "adidas": "https://www.adidas.com",
    "zara": "https://www.zara.com",
    "h&m": "https://www.hm.com",
    "gucci": "https://www.gucci.com",
    "prada": "https://www.prada.com",
    "versace": "https://www.versace.com",
    "louis vuitton": "https://www.louisvuitton.com",
    "chanel": "https://www.chanel.com",
    "uniqlo": "https://www.uniqlo.com",
    "gap": "https://www.gap.com",
    "levi's": "https://www.levis.com",
    "levis": "https://www.levis.com",
    "ralph lauren": "https://www.ralphlauren.com",
    "calvin klein": "https://www.calvinklein.com",
    "tommy hilfiger": "https://www.tommy.com",
    "burberry": "https://www.burberry.com",
    "balenciaga": "https://www.balenciaga.com",
    "off-white": "https://www.off---white.com",
    "supreme": "https://www.supremenewyork.com",
    "patagonia": "https://www.patagonia.com",
    "north face": "https://www.thenorthface.com",
    "new balance": "https://www.newbalance.com",
    "puma": "https://www.puma.com",
    "converse": "https://www.converse.com",
    "vans": "https://www.vans.com",
    "forever 21": "https://www.forever21.com",
    "asos": "https://www.asos.com",
    "amazon fashion": "https://www.amazon.com/fashion",
    "shein": "https://www.shein.com",
    "myntra": "https://www.myntra.com",
    "flipkart fashion": "https://www.flipkart.com/clothing-and-accessories",
    "ajio": "https://www.ajio.com",
}

def google_shopping_link(query):
    q = query.replace(" ", "+")
    return f"https://www.google.com/search?q={q}&tbm=shop"

def extract_brands(text):
    """Find known brands mentioned in the AI reply."""
    found = {}
    text_lower = text.lower()
    for brand, url in BRAND_LINKS.items():
        if brand in text_lower:
            found[brand.title()] = url
    return found

def render_reply(text):
    # Remove all AI-generated image markdown (fake URLs)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', '', text)
    # Remove all AI-generated hyperlinks (replace with just the label text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'\1', text)
    # Remove bare URLs
    text = re.sub(r'https?://\S+', '', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Render lines
    lines = text.split("\n")
    html_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{stripped[2:]}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if stripped:
                html_lines.append(f"<p>{line}</p>")
    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)

def build_shop_buttons(text, user_question):
    """Build real working shop buttons based on brands found + search."""
    brands = extract_brands(text)
    buttons_html = ""

    # Add brand buttons
    for brand, url in brands.items():
        buttons_html += f'<a class="shop-btn" href="{url}" target="_blank">🛍️ {brand}</a>'

    # Always add a Google Shopping search button
    search_query = user_question + " fashion"
    shop_url = google_shopping_link(search_query)
    buttons_html += f'<a class="shop-btn" href="{shop_url}" target="_blank">🔍 Shop on Google</a>'

    return f'<div class="shop-links">{buttons_html}</div>'

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Fashion Dude — a supremely stylish, witty AI personal stylist with encyclopedic knowledge of fashion. Your personality:

- CONFIDENT & opinionated: bold takes on trends, silhouettes, color theory, and personal style
- WARM & encouraging: hype people up while giving honest, actionable advice
- CULTURALLY savvy: know runway fashion AND streetwear, vintage AND contemporary
- PRACTICAL: give real outfit ideas, brand recommendations across all budgets, and styling hacks
- PLAYFUL: use occasional fashion slang like slay, serve looks, that's a moment — but don't overdo it

Topics you excel at:
- Outfit advice for any occasion (work, date night, casual, formal)
- Building a capsule wardrobe
- Color coordination & pattern mixing
- Body type & fit guidance
- Budget styling tips
- Trend analysis (what's in, what's out, what's timeless)
- Brand and shopping recommendations
- Seasonal dressing & accessorizing

Always give specific, visual advice — mention actual colors, fabrics, silhouettes, and brand names.
Do NOT include any URLs, image links, or hyperlinks — just plain text and brand names.
Keep responses punchy and helpful."""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🕶️ Fashion Dude AI")
    st.markdown("---")
    st.markdown("**Your AI Personal Stylist**")
    st.markdown("Ask me anything about style, outfits, trends, or building your wardrobe.")
    st.markdown("---")

    st.markdown("**Your Vibe**")
    style_vibe = st.selectbox(
        "Style personality",
        ["Not set", "Minimalist", "Streetwear", "Business Casual", "Maximalist", "Vintage", "Athleisure", "Boho"],
        label_visibility="collapsed"
    )
    budget = st.selectbox(
        "Budget range",
        ["Not set", "Budget-friendly", "Mid-range", "Luxury", "Mix of all"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_question = ""
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="fd-header">
  <h1>Fashion <span>Dude</span> AI</h1>
  <p>Your Personal Style Consultant</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_question" not in st.session_state:
    st.session_state.last_question = ""

# ── Quick prompt chips ────────────────────────────────────────────────────────
QUICK_PROMPTS = [
    "🎽 Build me a capsule wardrobe",
    "💼 Business casual outfit ideas",
    "🌈 What colors suit me?",
    "👟 Best sneakers right now",
    "🌸 Spring 2025 trends",
    "💸 Style on a budget",
]

if not st.session_state.messages:
    cols = st.columns(3)
    for i, prompt in enumerate(QUICK_PROMPTS):
        with cols[i % 3]:
            if st.button(prompt, key=f"chip_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.last_question = prompt
                st.rerun()

# ── Render chat history ───────────────────────────────────────────────────────
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-row user">
          <div class="avatar user">👤</div>
          <div class="bubble user">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        html_content = render_reply(msg["content"])
        prev_question = ""
        if i > 0 and st.session_state.messages[i - 1]["role"] == "user":
            prev_question = st.session_state.messages[i - 1]["content"]
        shop_buttons = build_shop_buttons(msg["content"], prev_question)
        st.markdown(f"""
        <div class="msg-row">
          <div class="avatar bot">🕶️</div>
          <div class="bubble bot">
            {html_content}
            {shop_buttons}
          </div>
        </div>""", unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask Fashion Dude anything about style…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.last_question = user_input

    system = SYSTEM_PROMPT
    if style_vibe != "Not set":
        system += f"\n\nThe user's style personality is: {style_vibe}."
    if budget != "Not set":
        system += f" Their budget range is: {budget}."

    groq_messages = [{"role": "system", "content": system}]
    for m in st.session_state.messages:
        groq_messages.append({"role": m["role"], "content": m["content"]})

    with st.spinner("Fashion Dude is thinking… ✨"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=groq_messages,
            max_tokens=1000,
            temperature=0.7,
        )
        reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
>>>>>>> d1a24a2 (Fashion Dude AI)
    st.rerun()