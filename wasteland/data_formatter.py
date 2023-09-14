import json
import pandas as pd

def generate_json(table_data):
    workout_data = {
        "workout_celeb": {
            "Name": "Chris Bumstead",
            "Ratings": "4",
            "Routine": {
                "Monday": {
                    "Name of day": "Legday",
                    "Exercises": []
                }
            }
        }
    }
    
    exercises = workout_data["workout_celeb"]["Routine"]["Monday"]["Exercises"]
    
    for _, row in table_data.iterrows():
        exercise = {
            "Name": row["Exercise"],
           "Set Type": row["Set Type"] if not pd.isnull(row["Set Type"]) else "",
                
            "Sets": []
        }
        
        sets = exercise["Sets"]
        
        for i in range(4, len(row), 2):
            set_data = {
                "Name": f"Set {len(sets) + 1}",
                "Type": row["Type"],
                 "Rest Time": row["Rest Time"],
                "Volume": "",
                "Weight": ""
            }
            
            volume_weight = str((row[i])).split("*")
            
            if len(volume_weight) == 1:
                if volume_weight[0].lower() == "Failure":
                    set_data["Volume"] = "Failure"
                   
                else:
                    set_data["Volume"] = volume_weight[0]
            else:
                set_data["Volume"] = volume_weight[0]
                set_data["Weight"] = volume_weight[1]
            
            sets.append(set_data)
        
        exercises.append(exercise)
    
    return json.dumps(workout_data, indent=4)

# Read table data from Excel file
excel_file = r"C:\Users\Subodh Maharjan\Desktop\projects_getyourshit togetther\data_generator\Chris bumstead Workout (2).xlsx"

# Specify the sheet name or index
sheet_name = "Sheet8"  # Replace with the actual sheet name or index (e.g., 0 for the first sheet)

# Read table data from Excel file
table_data = pd.read_excel(excel_file, sheet_name=sheet_name)

# Generate JSON
json_data = generate_json(table_data)
output_file = r"C:\Users\Subodh Maharjan\Desktop\projects_getyourshit togetther\data_generator\file.json"
with open(output_file, "w") as f:
    f.write(json_data)

print("JSON data saved successfully.")