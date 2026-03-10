#!/usr/bin/env python3
"""Generate portfolio HTML pages from folder data."""
import json, os

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Portfolio — Francisco Garza Martinez</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0a0e1a; --surface: #111827; --surface-2: #1e293b;
    --accent: #3b82f6; --accent-light: #60a5fa;
    --text: #f1f5f9; --text-muted: #94a3b8; --text-dim: #64748b;
    --border: #1e293b;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; -webkit-font-smoothing: antialiased; }}
  .container {{ max-width: 860px; margin: 0 auto; padding: 0 24px; }}
  .header {{ padding: 48px 0 32px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
  .header h1 {{ font-family: 'Playfair Display', serif; font-size: 28px; }}
  .nav {{ display: flex; gap: 16px; font-size: 14px; }}
  .nav a {{ color: var(--accent); text-decoration: none; }} .nav a:hover {{ color: var(--accent-light); }}
  .items {{ padding: 32px 0 60px; }}
  .item {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; margin-bottom: 16px; overflow: hidden; }}
  .item-header {{ padding: 20px 24px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }}
  .item-header:hover {{ background: var(--surface-2); }}
  .item-header h2 {{ font-size: 16px; font-weight: 500; }}
  .item-header .type {{ font-size: 12px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }}
  .item-body {{ border-top: 1px solid var(--border); }}
  .item-body iframe {{ width: 100%; height: 600px; border: none; background: white; }}
  .item-body .pdf-link {{ padding: 20px 24px; }}
  .item-body .pdf-link a {{ color: var(--accent); text-decoration: none; font-size: 14px; }}
  .toggle {{ font-size: 20px; color: var(--text-dim); transition: transform 0.2s; }}
  .item.open .toggle {{ transform: rotate(90deg); }}
  .item-body {{ display: none; }}
  .item.open .item-body {{ display: block; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>{icon} {title}</h1>
    <div class="nav">
      <a href="../portfolio.html">← All Categories</a>
      <a href="../index.html">CV</a>
    </div>
  </div>
  <div class="items">
    {items_html}
  </div>
</div>
<script>
document.querySelectorAll('.item-header').forEach(h => {{
  h.addEventListener('click', () => h.parentElement.classList.toggle('open'));
}});
// Auto-open first item
document.querySelector('.item')?.classList.add('open');
</script>
</body>
</html>"""

categories = [
    {"slug": "emails", "title": "Emails", "icon": "✉️", "items": [
        {"name": "Men's and Women's Tees", "id": "1-zL2vNa8toJX6cP7JVi9Hf3sYFICBdOE_m6nnPuy6dU", "type": "doc"},
        {"name": "Product Launch", "id": "1apI8V-UnBWILU3b96gVe3KfPp6fD7Fka8C2rvPXrQlc", "type": "doc"},
        {"name": "Product Back in Stock", "id": "1RVL0vFYWqp2oEEQIhzvcoZlqtOpfOCK4YaAfErvBotA", "type": "doc"},
        {"name": "Jeans, Chinos, and Sweatpants", "id": "1cbZvSBEzuCQnM83-A4ZByhCU8D2BzW5Q6DoFyZIjh4k", "type": "doc"},
    ]},
    {"slug": "funnels", "title": "Funnels", "icon": "🎯", "items": [
        {"name": "Castor Oil Landing Page", "id": "1hvbak8stl7WKk6hpy3opWV2RCL26OVlftBBcO58Zwy4", "type": "doc"},
        {"name": "Aceite Increíble Landing Page", "id": "1SGxTuVmRRPeYNGOKiKb5FJAiIhQOFt7mxGsbsAhIRo0", "type": "doc"},
    ]},
    {"slug": "collection-pages", "title": "Collection Pages", "icon": "🛍️", "items": [
        {"name": "Jeans, Tees, Underwear SEO", "id": "1NO7xTwPUV0z0KG7xpC8mll00eaAFHDcggyMEL7D2ww0", "type": "sheet"},
    ]},
    {"slug": "product-descriptions", "title": "Product Descriptions", "icon": "📝", "items": [
        {"name": "Women's Products", "id": "1cjjJVfdgbhr6lqTNNkzq9wbH7qgaLJ673hyIR9zgrRo", "type": "doc"},
        {"name": "Men's Products", "id": "1ikQtTC_PqO3lb1vRkBsUrdcppJSM6DOUkMN2t6Fdql0", "type": "doc"},
    ]},
    {"slug": "landing-pages", "title": "Landing Pages", "icon": "🚀", "items": [
        {"name": "Feel the Craftsmanship LP", "id": "1N9HEL7rdkxqnev8lOMWz-hwnI1Uw2MStkcMKhxrgb74", "type": "doc"},
    ]},
    {"slug": "blog-entries", "title": "Blog Entries", "icon": "📰", "items": [
        {"name": "How to Style Skinny Jeans for Men", "id": "19hShMrSk0FQg-PBj_dV22IAP37xlOYAj7SAAkAiF3f0", "type": "doc"},
        {"name": "Fall 2023 Outfit Essentials", "id": "1S2NheRF_zsqWobXs_xm-oXS7J9IQHdJTnoMn_AGVUac", "type": "doc"},
        {"name": "Skinny Jeans for Women", "id": "13iOfGSeIWhAXOFo10igSHVdpH7Vublj1B9q7PZW2udM", "type": "doc"},
    ]},
    {"slug": "case-studies", "title": "Case Studies", "icon": "📊", "items": [
        {"name": "Dynamic Expeditions", "id": "1tYg_jeJyzxhiIWLDHXThhswyLrsKNw0s", "type": "pdf"},
    ]},
    {"slug": "video-scripts", "title": "Video Scripts", "icon": "🎬", "items": [
        {"name": "Sunday Football Chinos", "id": "1PvVi8Roa9fHI6r5ZcdB-wFZ2RE2447BA9JILCRheqzI", "type": "doc"},
        {"name": "Good Looks and Comfort (Mini)", "id": "1UaQUwafjjqRtg0cpuhRl_Rhbof6Yamc6hFrRPMcG9OU", "type": "doc"},
        {"name": "Age-Appropriate Jeans", "id": "19c8rNBqjs0fmQciStUSCQFjgBBGG3bxV_5Lagb_8Sxg", "type": "doc"},
        {"name": "Help Me Decide Which Color", "id": "1TFTaYEEZ4yQWt41as9Gq4VuKQCBOGFPoNkTJ4DQ5RRY", "type": "doc"},
    ]},
    {"slug": "advertorials", "title": "Advertorials", "icon": "📣", "items": [
        {"name": "The Best Denim Brands for Men", "id": "1cdcn5iyz_FfPB5hZ5qqLkrFfTy8VIGl2EWxAfra-ALs", "type": "doc"},
        {"name": "The Best Travel Jeans for Women", "id": "1MW692_RZpCJ9YhO3E2ggGIRPkuhlJcRLOrJm9f3xg5Y", "type": "doc"},
    ]},
    {"slug": "translations", "title": "Translations", "icon": "🌐", "items": [
        {"name": "The Perfect Tee (EN → LATAM Spanish)", "id": "1Z2PnHx2pw5rQw9Isnos3jszo4-xIewgyMkTlO2bFk-s", "type": "doc"},
    ]},
]

os.makedirs("/tmp/cv-demo/portfolio", exist_ok=True)

for cat in categories:
    items_html = ""
    for item in cat["items"]:
        if item["type"] == "doc":
            embed = f'<iframe src="https://docs.google.com/document/d/{item["id"]}/pub?embedded=true" loading="lazy"></iframe>'
        elif item["type"] == "sheet":
            embed = f'<iframe src="https://docs.google.com/spreadsheets/d/{item["id"]}/pubhtml?widget=true" loading="lazy"></iframe>'
        elif item["type"] == "pdf":
            embed = f'<iframe src="https://drive.google.com/file/d/{item["id"]}/preview" loading="lazy"></iframe>'
        else:
            embed = f'<div class="pdf-link"><a href="https://drive.google.com/file/d/{item["id"]}/view" target="_blank">Open in Google Drive →</a></div>'
        
        items_html += f'''
    <div class="item">
      <div class="item-header">
        <h2>{item["name"]}</h2>
        <span class="toggle">›</span>
      </div>
      <div class="item-body">{embed}</div>
    </div>'''

    html = TEMPLATE.format(
        title=cat["title"],
        icon=cat["icon"],
        items_html=items_html
    )
    
    path = f"/tmp/cv-demo/portfolio/{cat['slug']}.html"
    with open(path, 'w') as f:
        f.write(html)
    print(f"✅ {path}")

print("Done!")
