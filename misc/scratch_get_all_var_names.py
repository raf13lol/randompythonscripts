import zipfile, os, rapidjson

cur_dir = os.path.dirname(__file__) + "/"

text_to_save = ""

def parse_project_data(data):
    global text_to_save

    text_to_save += "Start of global variables\n\n"

    for glob in project_data["var_info"]["globals"]:
        text_to_save += f"{glob['name']} (internal id: \"{glob['internal_id']}\"): {glob['default_value']}\n"

    text_to_save += "\nEnd of global variables\n\nStart of global lists\n\n"

    for glob in project_data["var_info"]["list_globals"]:
        text_to_save += f"{glob['name']} (internal id: \"{glob['internal_id']}\"): {glob['default_list_values']}\n"

    text_to_save += "\nEnd of global lists\n\nStart of local variables\n\n"

    for obj_name in project_data["var_info"]["local"].keys():
        if len(project_data["var_info"]["local"][obj_name]) > 0:
            text_to_save += "Start of " + obj_name + " variables\n\n"
            for local in project_data["var_info"]["local"][obj_name]:
                text_to_save += f"{local['name']} (internal id: \"{local['internal_id']}\"): {local['default_value']}\n"
            text_to_save += "\nEnd of " + obj_name + " variables\n\n"

    text_to_save += "End of local variables\n\nStart of local lists\n\n"

    for obj_name in project_data["var_info"]["list_local"].keys():
        if len(project_data["var_info"]["list_local"][obj_name]) > 0:
            text_to_save += "Start of " + obj_name + " lists\n\n"
            for local in project_data["var_info"]["list_local"][obj_name]:
                text_to_save += f"{local['name']} (internal id: \"{local['internal_id']}\"): {local['default_list_values']}\n"
            text_to_save += "\nEnd of " + obj_name + " lists\n\n"

    text_to_save += "End of local lists"

projects = []

for file in os.listdir(cur_dir):
    if file.endswith(".sb3"):
        projects.append(file)
if len(projects) <= 0:
    raise Exception("No .sb3 project files in the folder of this python code.")

save_to_file = input("Do you want the variable info saved to a file? (yes or no (will print it to console), default is yes) ") or "yes"
match save_to_file:
    case "yes":
        save_to_file = save_to_file
    case "no":
        save_to_file = save_to_file
    case _:
        raise Exception("Invalid input.")

save_to_file = save_to_file == "yes"

project_datas = []

for project in projects:
    print("Loading " + project + "...\n")
    project_file = zipfile.ZipFile(cur_dir + project).open("project.json")
    project_json = rapidjson.loads(project_file.read(), parse_mode=rapidjson.PM_TRAILING_COMMAS)
    project_var_info = {
        "globals": [],
        "local": {},
        "list_globals": [],
        "list_local": {}
    }
    for obj in project_json["targets"]:
        is_stage = obj["isStage"]
        if is_stage:
            for global_var in obj["variables"].keys():
                project_var_info["globals"].append({
                    "name": obj["variables"][global_var][0],
                    "default_value": obj["variables"][global_var][1],
                    "internal_id":global_var
                })
            for global_list in obj["lists"].keys():
                project_var_info["list_globals"].append({
                    "name": obj["lists"][global_list][0],
                    "default_list_values": obj["lists"][global_list][1],
                    "internal_id":global_list
                })
            print("Stage variables/lists loaded...")
        else:
            obj_name = obj["name"]
            project_var_info["local"][obj_name] = []
            for local_var in obj["variables"].keys():
                project_var_info["local"][obj_name].append({
                    "name": obj["variables"][local_var][0],
                    "default_value": obj["variables"][local_var][1],
                    "internal_id":local_var
                })
            project_var_info["list_local"][obj_name] = []
            for local_list in obj["lists"].keys():
                project_var_info["list_local"][obj_name].append({
                    "name": obj["lists"][local_list][0],
                    "default_list_values": obj["lists"][local_list][1],
                    "internal_id":local_list
                })
            print(f"Object {obj_name} variables/lists loaded...")
    project_datas.append({
        "name": ''.join(str(project).split(".")[0::-1]),
        "var_info": project_var_info
    })
    

print("\nHandling variables to turn it into text...\n")

if save_to_file:
    for project_data in project_datas:
        parse_project_data(project_data)

        with open(project_data["name"] + "-VAR-LOG.txt", "w") as f:
            f.write(text_to_save)
            print("Saved " + project_data["name"] + ".sb3's variable info to " + f.name + "!")
            text_to_save = ""
else:
    for project_data in project_datas:
        text_to_save += f"Start of {project_data['name']}'s variable info\n\n"

        parse_project_data(project_data)

        text_to_save += f"\n\nEnd of {project_data['name']}'s variable info\n\n"
    text_to_save = text_to_save.rstrip("\n")
    print(text_to_save)