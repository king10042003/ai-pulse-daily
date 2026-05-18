"""
Automated Newsletter Bot
Niche: AI Productivity for Small Businesses
Runs daily via GitHub Actions — fetches news, summarizes with Gemini, saves HTML draft locally.
"""
from google import genai
import os
import feedparser
import requests
import os
import json
from datetime import datetime

# ─────────────────────────────────────────────
# 1. CONFIGURATION
# ─────────────────────────────────────────────
GENAI_KEY = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=GENAI_KEY)# Optional: For affiliate tracking, add your affiliate links here
AFFILIATE_LINKS = {
    "notion":     "https://notion.so/?ref=YOURCODE",
    "zapier":     "https://zapier.com/?via=YOURCODE",
    "grammarly":  "https://grammarly.com/affiliate/YOURCODE",
}


# ─────────────────────────────────────────────
# 2. MULTI-SOURCE NEWS SCRAPER
#    More sources = richer content = higher quality newsletter
# ─────────────────────────────────────────────
RSS_FEEDS = [
    # AI & Tech
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://feeds.feedburner.com/venturebeat/SZYF",        # VentureBeat AI
    "https://www.wired.com/feed/category/business/latest/rss",
    # Small Business / Productivity
    "https://feeds.hbr.org/harvardbusiness",
    "https://www.inc.com/rss/",
]

def get_news(max_stories: int = 5) -> list[dict]:
    """Scrape top stories from multiple RSS feeds, deduplicated."""
    stories = []
    seen_titles = set()

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                title = entry.get("title", "").strip()
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    stories.append({
                        "title":   title,
                        "link":    entry.get("link", ""),
                        "summary": entry.get("summary", entry.get("description", ""))[:500],
                        "source":  feed.feed.get("title", "Unknown Source"),
                    })
                if len(stories) >= max_stories:
                    break
        except Exception as e:
            print(f"⚠️  Failed to parse {feed_url}: {e}")
        if len(stories) >= max_stories:
            break

    return stories[:max_stories]


# ─────────────────────────────────────────────
# 3. AI CONTENT GENERATOR (Gemini 1.5 Flash)
#    Generates: Summary + Subject line + CTA teaser
# ─────────────────────────────────────────────
def generate_newsletter_content(stories: list[dict], niche: str = "AI Productivity for Small Businesses") -> dict:
    """Use Gemini to create a polished newsletter from raw stories."""
   

    stories_text = "\n\n".join([
        f"[{i+1}] {s['title']}\nSource: {s['source']}\nSummary: {s['summary']}\nLink: {s['link']}"
        for i, s in enumerate(stories)
    ])

    prompt = f"""
You are a witty, sharp newsletter editor for a niche called "{niche}".
Your readers are busy small business owners who want actionable AI insights in under 3 minutes.

Here are today's top stories:
{stories_text}

Generate a complete newsletter in this exact JSON format (no markdown fences, raw JSON only):
{{
  "subject_line": "A compelling email subject line under 50 chars that creates curiosity (no clickbait)",
  "preview_text": "Email preview text under 90 chars",
  "hook": "One punchy opening sentence that grabs attention",
  "stories": [
    {{
      "headline": "Rewritten headline that's punchy and clear",
      "insight": "2-3 sentence summary + ONE actionable takeaway for a small business owner",
      "source_link": "original link here"
    }}
  ],
  "closing_tip": "One quick 'Pro Tip of the Day' that small businesses can apply immediately",
  "cta_text": "A soft CTA to share the newsletter (e.g., Know someone who'd love this? Forward it!)"
}}

Rules:
- Be witty but professional. No fluff.
- Every insight must have a practical SO WHAT for small business owners.
- Keep total reading time under 3 minutes.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()

    # Strip markdown fences if Gemini adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```").strip()

    return json.loads(raw)


# ─────────────────────────────────────────────
# 4. HTML BUILDER
#    Clean, mobile-friendly newsletter template
# ─────────────────────────────────────────────
def build_html(content: dict, affiliate_links: dict = {}) -> str:
    """Convert structured content dict → polished HTML email."""
    today = datetime.now().strftime("%B %d, %Y")
    stories_html = ""

    for i, story in enumerate(content.get("stories", []), 1):
        stories_html += f"""
        <div style="margin-bottom:28px; padding-bottom:24px; border-bottom:1px solid #e8e8e8;">
            <p style="font-size:11px; color:#888; margin:0 0 6px; text-transform:uppercase; letter-spacing:1px;">
                Story {i}
            </p>
            <h2 style="font-size:18px; color:#1a1a1a; margin:0 0 10px; line-height:1.4;">
                {story['headline']}
            </h2>
            <p style="font-size:15px; color:#444; line-height:1.7; margin:0 0 12px;">
                {story['insight']}
            </p>
            <a href="{story['source_link']}" style="font-size:13px; color:#2563eb; text-decoration:none;">
                Read full story →
            </a>
        </div>
        """

    # Build affiliate mention (optional, subtle)
    affiliate_html = ""
    if affiliate_links:
        tool_name, tool_link = list(affiliate_links.items())[0]
        affiliate_html = f"""
        <div style="background:#f0f7ff; border-left:3px solid #2563eb; padding:16px 20px; margin:24px 0; border-radius:4px;">
            <p style="font-size:13px; color:#1e40af; margin:0;">
                <strong>🔧 Tool Spotlight:</strong> We use 
                <a href="{tool_link}" style="color:#1e40af;">{tool_name.capitalize()}</a> 
                to stay organized. 7-day free trial for our readers.
            </p>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{content['subject_line']}</title>
</head>
<body style="margin:0; padding:0; background:#f5f5f5; font-family: Georgia, 'Times New Roman', serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center" style="padding:32px 16px;">
      <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.08);">

        <!-- HEADER -->
        <tr><td style="background:#1a1a2e; padding:28px 40px;">
          <p style="color:#7c83fd; font-size:11px; letter-spacing:2px; text-transform:uppercase; margin:0 0 6px;">
            {today}
          </p>
          <h1 style="color:#ffffff; font-size:26px; margin:0; font-weight:700; font-family:Georgia,serif;">
            AI Pulse Daily ⚡
          </h1>
          <p style="color:#a0a8c8; font-size:13px; margin:8px 0 0;">
            AI Productivity for Small Businesses · 3-min read
          </p>
        </td></tr>

        <!-- HOOK -->
        <tr><td style="padding:32px 40px 20px;">
          <p style="font-size:17px; color:#1a1a1a; font-style:italic; border-left:3px solid #7c83fd;
                     padding-left:16px; margin:0; line-height:1.6;">
            {content['hook']}
          </p>
        </td></tr>

        <!-- STORIES -->
        <tr><td style="padding:0 40px;">
          {stories_html}
        </td></tr>

        <!-- AFFILIATE (subtle) -->
        <tr><td style="padding:0 40px;">
          {affiliate_html}
        </td></tr>

        <!-- PRO TIP -->
        <tr><td style="padding:20px 40px;">
          <div style="background:#fafafa; border:1px solid #e8e8e8; border-radius:6px; padding:20px 24px;">
            <p style="font-size:12px; color:#888; text-transform:uppercase; letter-spacing:1px; margin:0 0 8px;">
              💡 Pro Tip of the Day
            </p>
            <p style="font-size:15px; color:#1a1a1a; margin:0; line-height:1.6;">
              {content['closing_tip']}
            </p>
          </div>
        </td></tr>

        <!-- CTA -->
        <tr><td style="padding:28px 40px; text-align:center;">
          <p style="font-size:14px; color:#666; margin:0;">
            {content['cta_text']}
          </p>
        </td></tr>

        <!-- FOOTER -->
        <tr><td style="background:#f9f9f9; padding:20px 40px; border-top:1px solid #eee; text-align:center;">
          <p style="font-size:11px; color:#aaa; margin:0;">
            Built by Kunal Jain • Powered by AI Automation.<br>
            <a href="{{{{ unsubscribe_url }}}}" style="color:#aaa;">Unsubscribe</a> · 
            <a href="{{{{ subscriber_preferences_url }}}}" style="color:#aaa;">Preferences</a>
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""


# ─────────────────────────────────────────────
# 5. LOCAL DRAFT SAVER
#    Saves newsletter as a dated HTML file + prints subject/preview
# ─────────────────────────────────────────────
DRAFTS_FOLDER = "drafts"

def save_draft_locally(content: dict, html_body: str) -> str:
    """Save newsletter HTML to a local drafts/ folder."""
    os.makedirs(DRAFTS_FOLDER, exist_ok=True)
    filename = os.path.join(
        DRAFTS_FOLDER,
        f"newsletter_{datetime.now().strftime('%Y-%m-%d')}.html"
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_body)
    return filename

import shutil
import subprocess

WEBSITE_FOLDER="."
def publish_to_github(html_body):
    os.makedirs(WEBSITE_FOLDER,exist_ok=True)

    # Main live page
    index_path=os.path.join(WEBSITE_FOLDER,"index.html")

    with open(index_path,"w",encoding="utf-8") as f:
        f.write(html_body)
    
    #Optional archive copy

    archive_name=f"newsletter_{datetime.now().strftime('%Y-%m-%d')}.html"
    archive_folder = os.path.join(WEBSITE_FOLDER, "archive")
    os.makedirs(archive_folder, exist_ok=True)

    archive_path = os.path.join(archive_folder, archive_name)

    with open(archive_path,"w",encoding="utf-8") as f:
        f.write(html_body)

    print("🌐 Website updated.")

    #Git auto push

    try:
        subprocess.run(["git","add","."],check=True)
        subprocess.run(
            ["git","commit","-m",
             f"Auto newsletter {datetime.now().strftime('%Y-%m-%d')}"],
             check=True
        )
        
        subprocess.run(["git","push"],check=True)

        print("🚀 Auto-published to GitHub Pages!")

    except Exception as e:
        print("❌ Git publish failed:", e)



# ─────────────────────────────────────────────
# 6. MAIN PIPELINE
# ─────────────────────────────────────────────
def run_pipeline():
    print(f"🚀 Newsletter Bot starting — {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    print("📰 Fetching news...")
    stories = get_news(max_stories=5)
    print(f"   Got {len(stories)} stories.")

    print("🤖 Generating content with Gemini...")
    content = generate_newsletter_content(stories)

    print("🎨 Building HTML email...")
    html = build_html(content, affiliate_links=AFFILIATE_LINKS)

    print("💾 Saving draft locally...")
    filepath = save_draft_locally(content, html)
    print("🌍 Publishing website...")
    publish_to_github(html)

    print("\n" + "─" * 50)
    print(f"✅  Draft saved: {filepath}")
    print(f"📧  Subject    : {content['subject_line']}")
    print(f"👁️   Preview    : {content['preview_text']}")
    print("─" * 50)
    print("\n📋 Next steps (your 10-minute morning task):")
    print("   1. Open the HTML file in your browser to preview")
    print("   2. Copy the HTML → paste into your newsletter platform")
    print("   3. Add one sentence of YOUR opinion at the top")
    print("   4. Hit Send/Publish!")


if __name__ == "__main__":
    run_pipeline()