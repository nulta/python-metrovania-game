#!/usr/bin/env -S deno run --allow-read --allow-write

// to export to js:
// for %i in (*.tmx) do tiled --export-map js %~ni.tmx exported/%~ni.js

export {}

const path = "./exported/"
const path2 = "./json_data/"
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
    "tileset_name": "generic_0",
    "map_data": null,  // Map data goes here
    "entities": null,  // Entity data goes here
    "music": "",
    "background_img": ""
})

globalThis.onTileMapLoaded = async (filename: string, filedata) => {
    filename = filename.toLowerCase()
    console.log("Loading file ", filename)

    const {data, height, width} = filedata.layers[0]
    const map = {...mapTemplate}

    const map_data: any[] = []
    for (let y=0; y<height; y++) {
        const row: number[] = []
        for (let x=0; x<width; x++) {
            row[x] = data[y*width + x]
        }
        map_data.push(row)
    }

    // @ts-ignore
    map.map_data = map_data
    // @ts-ignore
    map.entities = [["Player", 1, 1]]
    const json = JSON.stringify(map)
    await Deno.writeTextFile(path2 + filename + ".json", json)
}

for (let filename of fileList) {
    filename = path + filename
    await import(filename)
}
