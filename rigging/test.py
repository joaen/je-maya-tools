import json

dict = {
    "ikfk_attr_name" : "CTRL_L__WristPinner.IKFK",
    "fk_ctrl_start" : "CTRL_FK_L__Shoulder",
    "fk_ctrl_mid" : "CTRL_FK_L__Elbow",
    "fk_ctrl_end" : "CTRL_FK_L__Wrist",
    "ik_target_start" : "rig_L__Shoulder_IK",
    "ik_target_mid" : "rig_L__Elbow_IK",
    "ik_target_end" : "rig_L__Wrist_IK",
    "ik_ctrl" : "CTRL_L__Hand",
    "ik_pv_ctrl" : "CTRL_L__ElbowPole",
    "fk_target_start" : "rig_L__Shoulder_FK",
    "fk_target_mid" : "rig_L__Elbow_FK",
    "fk_target_end" : "rig_L__Wrist_FK"
    }

output_path = "/Users/jengberg/Desktop/je_test.json"

with open(output_path, 'w') as outfile:
    json.dump(dict, outfile, indent=4)

load_data = json.load(open(output_path))

for key, value in load_data.iteritems():
    print(key)
    print(value)