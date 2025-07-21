import subprocess
import pandas as pd
import time
import re

MAX_DATASETS = 4000  # Adjust this as needed
PAGE_SIZE = 100
pages = (MAX_DATASETS + PAGE_SIZE - 1) // PAGE_SIZE

all_datasets = []

for page in range(1, pages + 1):
    print(f"Fetching page {page}/{pages}")
    cmd = ["kaggle", "datasets", "list", "--sort-by", "hottest", "--page", str(page)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')

        # Skip header and divider lines
        data_lines = [line for line in lines[2:] if line.strip()]

        for line in data_lines:
            # Split line by 2 or more spaces
            parts = re.split(r'\s{2,}', line)

            if len(parts) < 7:
                print(f"⚠️ Skipping malformed line: {line}")
                continue

            dataset = {
                "ref": parts[0],
                "title": parts[1],
                "size": parts[2],
                "lastUpdated": parts[3],
                "downloadCount": parts[4],
                "voteCount": parts[5],
                "usabilityRating": parts[6],
                "day": 1
            }
            all_datasets.append(dataset)

        time.sleep(1)

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed on page {page}: {e.stderr}")
        break

# Save to CSV
df = pd.DataFrame(all_datasets)
df.to_csv("kaggle_datasets_metadata_250721.csv", index=False)

print(f"✅ Done. Saved {len(df)} datasets to kaggle_datasets_metadata_250721.csv")
