import os, urllib.request, json, html
from PIL import Image
from io import BytesIO

USERNAME = os.environ["GITHUB_USERNAME"]
TOKEN = os.environ.get("GITHUB_TOKEN", "")
AVATAR_URL = f"https://github.com/{USERNAME}.png?size=512"

CHARS = "@%#*+=-:. "

def fetch_json(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}" if TOKEN else ""
    })
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def ascii_avatar(width=70):
    with urllib.request.urlopen(AVATAR_URL) as r:
        img = Image.open(BytesIO(r.read())).convert("L")

    # Crop to square and resize for terminal-character proportions.
    side = min(img.width, img.height)
    left = (img.width - side) // 2
    top = (img.height - side) // 2
    img = img.crop((left, top, left + side, top + side))

    height = int(width * 0.48)
    img = img.resize((width, height))

    out = []
    for y in range(height):
        line = ""
        for x in range(width):
            p = img.getpixel((x, y))
            line += CHARS[p * (len(CHARS)-1) // 255]
        out.append(line)
    return out

def esc(s):
    return html.escape(str(s))

def main():
    user = fetch_json(f"https://api.github.com/users/{USERNAME}")
    repos = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated")

    stars = sum(r.get("stargazers_count", 0) for r in repos)
    forks = sum(r.get("forks_count", 0) for r in repos)
    public_repos = user.get("public_repos", 0)
    followers = user.get("followers", 0)

    art = ascii_avatar(70)

    lines = [
        f"USER        {USERNAME}",
        f"NAME        {user.get('name') or '—'}",
        f"REPOS       {public_repos}",
        f"STARS       {stars}",
        f"FORKS       {forks}",
        f"FOLLOWERS   {followers}",
        "",
        "GITHUB ASCII PROFILE"
    ]

    font = "monospace"
    line_h = 15
    left_x = 20
    right_x = 590
    top = 35
    width = 1120
    height = max(420, top*2 + max(len(art), len(lines))*line_h)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" rx="18" fill="#0d1117"/>',
        '<rect x="8" y="8" width="calc(100% - 16px)" height="calc(100% - 16px)" rx="14" fill="none" stroke="#30363d"/>',
        f'<g font-family="{font}" font-size="12" fill="#c9d1d9" xml:space="preserve">'
    ]

    for i, line in enumerate(art):
        svg.append(f'<text x="{left_x}" y="{top + i*line_h}">{esc(line)}</text>')

    for i, line in enumerate(lines):
        fill = "#58a6ff" if i == 0 else "#c9d1d9"
        svg.append(f'<text x="{right_x}" y="{top + i*line_h}" fill="{fill}">{esc(line)}</text>')

    svg += ["</g>", "</svg>"]

    Path("profile.svg").write_text("\n".join(svg), encoding="utf-8")
    print("Generated profile.svg")

if __name__ == "__main__":
    main()
