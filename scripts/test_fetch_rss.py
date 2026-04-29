from scraper import fetch_rss

# Example RSS (replace later with real source)
URL = "https://hnrss.org/jobs"

entries = fetch_rss(URL)

print(f"Fetched {len(entries)} entries")

for e in entries[:3]:
    print(e)