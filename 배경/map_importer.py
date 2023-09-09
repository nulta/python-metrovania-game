import json
import os

FROM_DIR = "./"
TO_DIR = "../resources/levels/"
ENTITIES = [
    "Player","Fire_Enemy","Wind_Enemy",""
]
ENTITIES_FIRST_GID = 76


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
        ent_data = []
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
                tile_id = layer_data_map[idx]
                if tile_id >= ENTITIES_FIRST_GID:
                    map_data[y][x] = 0
                    ent_id = ENTITIES_FIRST_GID - tile_id
                    if ent_id >= len(ENTITIES):
                        # ent_id out of range
                        print(f"On map '{filename}' ({x}, {y}): Tile ID ({ent_id}) out of range!")
                        continue
                    ent_type = ENTITIES[ent_id]
                    ent_data.append([ent_type, x, y])
                else:
                    map_data[y][x] = tile_id

        new_filename = filename.replace(".tmj", ".json").lower().replace(" ", "")
        with open(TO_DIR + new_filename, "w") as f2:
            json_str = json.dumps(new_data, indent=4)
            json_str = json_str.replace("\n" + "    " * 3, "")
            json_str = json_str.replace("\n" + "        ]", "]")
            f2.write(json_str)
