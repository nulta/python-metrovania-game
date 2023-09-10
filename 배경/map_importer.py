import json
import os

FROM_DIR = "./"
TO_DIR = "../resources/levels/"
ENTITIES = [
    "Player","FireEnemy","WindEnemy","SpeedEnemy","NavyEnemy",
    "GasEnemy","GrenadeEnemy","Fire","Wind","HpAdd",
    "Electric_ball","Smoke","MovingBoard","Electric_box","Portal_1",
    "PoisonSmoke","Portal_2","Portal_3","Portal_4","Portal_5",
    "Portal_6","ShortCut","Door","BasicEnemy","BlinkBox",
    "Portal_7","Portal_8","Portal_9","Portal_10","ShootingBall",
    "Line","Elevator","Gun","Line","Line",
    "","fire_time1","fire_time2","frie","BossDoor"
]
ENTITIES_FIRST_GID = 76


tmj_files = filter(lambda name: name.endswith(".tmj"), os.listdir(FROM_DIR))

for filename in tmj_files:
    print("Processing file:", filename)
    with open(filename, "r") as f:
        content = f.read().replace(",]", "]")
        original_data: "dict" = json.loads(content)

        layer_data = original_data["layers"][0]
        width = layer_data["width"]
        height = layer_data["height"]
        layer_data_map = layer_data["data"]

        properties = original_data.get("properties", None)
        if properties is None:
            print(f"ERROR: '{filename}' 맵에 Custom Property가 없음!!!")
            print(f"ERROR: 이 맵은 스킵합니다...")
            continue

        next = ""
        background = ""
        music = ""

        for prop in properties:
            name = prop["name"]
            value: "str" = prop["value"]
            if name == "next":
                next = value
                if next and next[0].isnumeric():
                    # 숫자로 시작한다면 소문자로 바꿔주자... 맵 이름이니까...
                    next = next.lower()
            if name == "background":
                background = value
            if name == "music":
                music = value

        print("next =", next)
        print("background =", background)
        print("music =", music)

        map_data: "list[list[int]]" = [([0] * width) for _ in range(height)]
        ent_data = []
        new_data = {
            "tileset_name": "generic_0",
            "music": music,
            "background_img": background,
            "next_scene": next,
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
                    ent_id = tile_id - ENTITIES_FIRST_GID
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
    print("")
