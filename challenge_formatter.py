import pandas as pd
import json

# Define the path to the Excel file
influencer_name = "75 Hard"  # Replace with the actual influencer name
excel_file = f"C:\\Users\\Subodh Maharjan\\Desktop\\projects_getyourshit togetther\\data_generator\\Challenges\\{influencer_name}.xlsx"


all_sheets = pd.read_excel(excel_file,sheet_name=None)
first_sheet_name = list(all_sheets.keys())[0]

# Extract the first sheet as a DataFrame
df = all_sheets[first_sheet_name]
print(df.columns)
# Fill missing values in 'Day' column
df['Day'] = df['Day'].fillna(method='ffill')

df['Day_Number'] = df['Day'].str.extract('(\d+)').astype(int)

# Group by 'Day' and construct the desired format
result = []
for day in sorted(df['Day'].unique(), key=lambda x: int(x.split(' ')[-1])):
    group = df[df['Day'] == day]
    topics = []
    for _, row in group.iterrows():
        challenge = {
            'name': row['Topic Name'],
            'type': row['Topic Type'],
            'proofType': row['Topic Proof'],
            
        }
        if pd.notna(row['Topic WorkoutId']):
            challenge['workoutId'] = int(row['Topic WorkoutId'])
        if pd.notna(row['Input']):
            challenge['Input'] = int(row['Input'])


        topics.append(challenge)
    
    day_dict = {
        'name': day,
        'id': day.split(' ')[-1],  # Extracting the number from 'Day X'
        'topics': topics
    }
    result.append(day_dict)


# Define the path to the output JSON file
output_file = f"C:\\Users\\Subodh Maharjan\\Desktop\\projects_getyourshit togetther\\data_generator\\Challenges_Json_table\\{influencer_name} challenges.json"
 
 
# Save the result list to a JSON file
with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)

print(f"Data saved to {output_file}")
