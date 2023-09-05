#!/usr/bin/env -S deno run --allow-read --allow-write

export {}

const fileList = [
    "0_tutorial.js",
    "1_FB85_Boss.js",
    "1_FB85_fire.js",
    "2_BT02_wind.js",
    "3_SN91_Boss.js",
    "3_SN91_speed.js",
    "4_SB87_1_2.js",
    "4_SB87_3.js",
    "4_SB87_Boss.js",
    "5_VP33_Boss.js",
    "5_VP33_gas.js",
    "6_KS64_navy.js",
]

const mapTemplate = Object.freeze({
    "tileset_name": "default",
    "map_data": null,  // Map data goes here
    "entities": null,  // Entity data goes here
    "music": "",
    "background_img": ""
})

// TODO

for (const filename of fileList) {
    const data: any = await require(filename)
    const {width: mapWidth, height: mapHeight, startx, starty, chunks} = data.layers[0]
    const map = {...mapTemplate}

    const map_data = []
    for (let i=0; i<mapHeight; i++) {
        
    }

    for (const chunk of chunks) {
        const {data, height, width, x, y} = chunk

    }
}
