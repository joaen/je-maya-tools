import json

def save_settings(output_path):
    # SAVE
    output_path = "/Users/jengberg/Desktop/je_test.json"

    dict = {
        "ikfk_attr_name" : "",
        "fk_ctrl_start" : "",
        "fk_ctrl_mid" : "",
        "fk_ctrl_end" : "",
        "ik_target_start" : "",
        "ik_target_mid" : "",
        "ik_target_end" : "",
        "ik_ctrl" : "",
        "ik_pv_ctrl" : "",
        "fk_target_start" : "",
        "fk_target_mid" : "",
        "fk_target_end" : ""
        }

    dict["ikfk_attr_name"] = "CTRL_L__WristPinner.IKFK"
    dict["fk_ctrl_start"] = "CTRL_FK_L__Shoulder"
    dict["fk_ctrl_mid"] = "CTRL_FK_L__Elbow"
    dict["fk_ctrl_end"] = "CTRL_FK_L__Wrist"
    dict["ik_target_start"] = "rig_L__Shoulder_IK"
    dict["ik_target_mid"] = "rig_L__Elbow_IK"
    dict["ik_target_end"] = "rig_L__Wrist_IK"
    dict["ik_ctrl"] = "CTRL_L__Hand"
    dict["ik_pv_ctrl"] = "CTRL_L__ElbowPole"
    dict["fk_target_start"] = "rig_L__Shoulder_FK"
    dict["fk_target_mid"] = "rig_L__Elbow_FK"
    dict["fk_target_end"] = "rig_L__Wrist_FK"

    with open(output_path, 'w') as outfile:
        json.dump(dict, outfile, indent=4)

def load_settings(output_path):
    # LOAD
    output_path = "/Users/jengberg/Desktop/je_test.json"
    load_data_dict = json.load(open(output_path))

    print(load_data_dict["fk_ctrl_mid"])
    # print(dict)
    # print(load_data)
    # for key, value in load_data.iteritems():
    #     print(value)
        # print(key)