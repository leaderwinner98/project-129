import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://en.wikipedia.org/wiki/List_of_brown_dwarfs'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    all_data = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['td', 'th'])  
            cols = [col.text.strip() for col in cols]
            all_data.append(cols)

    brown_dwarfs_df = pd.DataFrame(all_data)


    brown_dwarfs_df = brown_dwarfs_df.dropna()
    brown_dwarfs_df.columns = brown_dwarfs_df.iloc[0]  
    brown_dwarfs_df = brown_dwarfs_df[1:]  
    

    brown_dwarfs_df['Mass'] = brown_dwarfs_df['Mass'].astype(float)
    brown_dwarfs_df['Radius'] = brown_dwarfs_df['Radius'].astype(float)

    brown_dwarfs_df['Radius'] = brown_dwarfs_df['Radius'] * 0.102763


    brown_dwarfs_df['Mass'] = brown_dwarfs_df['Mass'] * 0.000954588


    brown_dwarfs_df.to_csv('cleaned_brown_dwarfs.csv', index=False)

    print("Brown dwarf stars data saved to 'cleaned_brown_dwarfs.csv'")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)


brightest_stars_df = pd.read_csv('brightest_stars.csv')

merged_df = pd.merge(brown_dwarfs_df, brightest_stars_df, on='Star Name', how='outer')


merged_df.to_csv('merged_stars_data.csv', index=False)
print("Merged data saved to 'merged_stars_data.csv'")
