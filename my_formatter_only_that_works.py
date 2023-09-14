import json
import pandas as pd
influencer_name ="Arnold Schwarzenegger"
def super_set_seperate(table_data,index):
  
    super_exo=[ ]
     
    loper=[index,index+1]
    loop_time=len(table_data.loc[index])-5
  
    for i in range(1,loop_time):
        for indexer in loper:
           
            tag={}
          
            table_data.iloc[indexer].index=table_data.iloc[indexer].index.str.strip()
            # print(table_data.iloc[indexer].index)
            
            exercise_name = table_data.loc[indexer]["Exercise"]
           
            exercise_type = table_data.loc[indexer]['Type']
             
            if pd.isnull(table_data.loc[indexer]["Set Type"]):
                set_type = ""
            else:
                 set_type = table_data.loc[indexer]["Set Type"]
            rest_time = str(table_data.loc[indexer])
             
            set_data = {
                "Name": f"Set {i}",
                "Type": table_data.loc[indexer]["Type"],
                 "Rest Time": str(table_data.loc[indexer]["Rest Time"]),
                "Volume": "",
                "Weight": ""
            }
            
            volume_weight = str((table_data.loc[indexer][f"Set {i}"])).split("*")
            if(volume_weight)=="nan":
                break
            if len(volume_weight) == 1:
                if volume_weight[0].lower() == "Failure":
                    set_data["Volume"] = "Failure"
                   
                else:
                    set_data["Volume"] = volume_weight[0]
            else:
                set_data["Volume"] = volume_weight[0]
                set_data["Weight"] = volume_weight[1]
            
           
            tag={
                "Name": exercise_name,
                "Type": exercise_type,
                "Set Type": set_type,
                "Sets": [set_data]
            }
          
            super_exo.append(tag)
        
            
    return super_exo
  

def generate_json(table_data):
    table_data.columns=table_data.columns.str.strip()
   

    workout_data = {
        
                "Sequence_init": {
                    "Name of day": "Legday",
                 
                    "Exercises": []
                }
            }
       
    # exercises = workout_data["workout_celeb"]["Routine"]["Monday"]["Exercises"]
    
    exercises = []
   
    superset_flag = False
    super_set_ignore_row=None
    for index, row in table_data.iterrows():
        
        if super_set_ignore_row ==index:
            super_set_ignore_row==None
            continue
        if pd.isnull(row["Exercise"]):
            continue
        set_type = row["Set Type"] if not pd.isnull(row["Set Type"]) else ""
        
        if set_type.lower() == 'supersets':
            superset_flag = True
            super_set_ignore_row=index+1

       
        if( superset_flag == False):

            
            exercise = {
                "Name": row["Exercise"],
            "Set Type": row["Set Type"] if not pd.isnull(row["Set Type"]) else "",
                    "Type": row["Type"],
                    "MachineSettings":row["Machine Setting"],
                    "videoId":row["VideoId"],
                "Sets": []
            }
            
            sets = exercise["Sets"]
            
            
                
            loop_time=len(table_data.loc[index])-5
            for i in range(1,loop_time):
                set_data = {
                    "Name": f"Set {i}",
                    "Type": row["Type"],
                    "Rest Time": str(row["Rest Time"]),
                    "Volume": "",
                    "Weight": ""
                }
                
                volume_weight = str((row[i+5])).split("*")
                print(str((row[i+5])))
                if(str((row[i+5])))== "nan":
                    break
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
        elif superset_flag==True:

           
            super_ones=super_set_seperate(table_data,index)
            exercises=exercises+super_ones
            superset_flag=False
            
    workout_data["Sequence_init"]["Exercises"]=exercises
    return json.dumps(workout_data, indent=4)

 
# Read table data from Excel file
excel_file = f"C:\\Users\\Subodh Maharjan\\Desktop\\projects_getyourshit togetther\\data_generator\\influencers\\{influencer_name} Workout.xlsx"
# sheet_name = "Sheet8"  # Replace with the actual sheet name or index (e.g., 0 for the first sheet)
data=pd.read_excel(excel_file, sheet_name=None)
Structure=[]
for index,(sheet_name,sheet_data) in enumerate(data.items()):

    json_data = generate_json(sheet_data)
    
    item={
        "Day "+str(index+1): sheet_name
    }
    Structure.append(item)
    output_file = f"C:\\Users\\Subodh Maharjan\Desktop\\projects_getyourshit togetther\\data_generator\\Json_table\\{influencer_name}\\.json"
    inserted_string = str(sheet_name)
    new_file_path = output_file[:-5] + inserted_string + output_file[-5:]
    
    with open(new_file_path, "w") as f:
        f.write(json_data)


output_filee = f"C:\\Users\\Subodh Maharjan\\Desktop\\projects_getyourshit togetther\\data_generator\\Json_table\\{influencer_name}\\Structure.json"
 
Structure_data = {
        "workout_celeb": {
            "Name": influencer_name,
            "Ratings": "4",
            "Routine": []}}

Structure_data["workout_celeb"]["Routine"]=Structure
Struc=json.dumps(Structure_data, indent=4)
with open(output_filee, "w") as f:
    f.write(Struc)


