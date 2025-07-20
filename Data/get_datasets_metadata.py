import subprocess
import pandas as pd
import time

MAX_DATASETS = 4000
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
        headers = lines[0]
        data_lines = [line for line in lines[2:] if line.strip()]

        for line in data_lines:
            # Slice columns based on position (this works with current CLI output format)
            dataset = {
                "ref": line[0:40].strip(),
                "title": line[41:85].strip(),
                "size": line[86:94].strip(),
                "lastUpdated": line[95:107].strip(),
                "downloadCount": line[108:120].strip(),
                "voteCount": line[121:132].strip(),
                "usabilityRating": line[133:].strip(),
            }
            all_datasets.append(dataset)

        time.sleep(1)

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed on page {page}: {e.stderr}")
        break

# Save to CSV
df = pd.DataFrame(all_datasets)
df.to_csv("kaggle_datasets_metadata_250720.csv", index=False)

print(f"✅ Done. Saved {len(df)} datasets to kaggle_datasets_metadata.csv")

