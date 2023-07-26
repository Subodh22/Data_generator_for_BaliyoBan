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
    
    current_exercise = None
    current_sets = None
    supersets_mode = False
    
    for _, row in table_data.iterrows():
        if pd.isnull(row["Exercise"]):
            continue
        
        exercise_name = row["Exercise"]
        set_type = row["Set Type"] if not pd.isnull(row["Set Type"]) else ""
        
        if set_type == "supersets":
            supersets_mode = True
        elif supersets_mode:
            supersets_mode = False
            continue
        
        exercise = {
            "Name": exercise_name,
            "Type": row["Type"],
            "Set Type": set_type,
            "Rest Time": row["Rest Time"],
            "Sets": []
        }
        
        exercises.append(exercise)
        current_exercise = exercise
        current_sets = exercise["Sets"]
        
        for i in range(4, len(row), 2):
            set_data = {
                "Name": f"Set {len(current_sets) + 1}",
                "Type": "Reps",
                "Set Type": "",
                "Rest Time": row["Rest Time"],
                "Volume": "",
                "Weight": ""
            }
            
            volume_weight = row[i].split("*")
            
            if len(volume_weight) == 1:
                if volume_weight[0].lower() == "to failure":
                    set_data["Volume"] = "to failure"
                    set_data["Weight"] = "to failure"
                else:
                    set_data["Volume"] = volume_weight[0]
            else:
                set_data["Volume"] = volume_weight[0]
                set_data["Weight"] = volume_weight[1]
            
            current_sets.append(set_data)
    
    return json.dumps(workout_data, indent=4)

# Example table data
table_data = pd.DataFrame({
    "Exercise": ["Deadlifts", "Bent-Over Rows", "", "Wide Grip Latoulldowns", "Straight Arm Pulldowns", "Dumbbell Rows", "Machine Rows"],
    "Type": ["reps", "reps", "", "reps", "reps", "reps", "reps"],
    "Set Type": ["supersets", "", "", "supersets", "", "", ""],
    "Rest Time": ["2 mins", "2 mins", "", "2 mins", "2 mins", "2 mins", "2 mins"],
    "Set 1": ["10*24", "", "", "10*24", "", "10*24", "10*24"],
    "Set 2": ["8*40", "", "", "8*40", "", "8*40", "8*40"],
    "Set 3": ["8*30", "", "", "8*30", "", "8*30", "8*30"],
    "Set 4": ["to failure", "", "", "to failure", "", "to failure", "to failure"]
})

# Generate JSON
json_data = generate_json(table_data)
print(json_data)