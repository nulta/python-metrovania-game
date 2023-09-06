import json
import os

FROM_DIR = "./"
TO_DIR = "../resources/levels/"


tmj_files = filter(lambda name: name.endswith(".tmj"), os.listdir(FROM_DIR))

for filename in tmj_files:
    print("Processing file:", filename)
    with open(filename, "r") as f:
        content = f.read().replace(",]", "]")
        original_data = json.loads(content)

        layer_data = original_data["layers"][0]
        width = layer_data["width"]
        height = layer_data["height"]
        layer_data_map = layer_data["data"]

        map_data: "list[list[int]]" = [([0] * width) for _ in range(height)]
        ent_data = [["Player", 3, 3], ]
        new_data = {
            "tileset_name": "generic_0",
            "music": "",
            "background_img": "",
            "entities": ent_data,
            "map_data": map_data,
        }

        for y in range(height):
            if y >= len(layer_data_map) // width:
                break
            for x in range(width):
                idx = width * y + x
                map_data[y][x] = layer_data_map[idx]
        
        new_filename = filename.replace(".tmj", ".json").lower().replace(" ", "")
        with open(TO_DIR + new_filename, "w") as f2:
            json_str = json.dumps(new_data, indent=4)
            json_str = json_str.replace("\n" + "    " * 3, "")
            json_str = json_str.replace("\n" + "        ]", "]")
            f2.write(json_str)
