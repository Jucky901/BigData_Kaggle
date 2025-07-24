import pandas as pd

df = pd.read_csv('kaggle_datasets_metadata_250724.csv', on_bad_lines='warn', engine='python')

df['title'] = df['title'].astype(str).str.replace(',', ' ', regex=False)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df['lastUpdated'] = pd.to_datetime(df['lastUpdated'], errors='coerce')
df['lastUpdated'] = df['lastUpdated'].fillna(pd.Timestamp('2025-07-01 00:00:00'))
df['downloadCount'] = pd.to_numeric(df['downloadCount'], errors='coerce').fillna(0).astype(int)
df['voteCount'] = pd.to_numeric(df['voteCount'], errors='coerce').fillna(0).astype(int)
df['usabilityRating'] = pd.to_numeric(df['usabilityRating'], errors='coerce').fillna(0).astype(float)

df.to_csv('cleaned_250724.csv', index=False)
