#!/usr/bin/env -S deno run --allow-read --allow-write

// to export tmx to js:
// for %i in (*.tmx) do tiled --export-map js %~ni.tmx exported/%~ni.js

export {}

const path = "./exported/"
const path2 = "../resources/levels/"
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

function getPaddingHeight(h: number) {
    return 9 - (h + 2) % 10
}

globalThis.onTileMapLoaded = async (filename: string, filedata) => {
    filename = filename.toLowerCase()
    console.log("Loading file ", filename)

    const {data, height, width} = filedata.layers[0]
    const map = {...mapTemplate}

    let map_data: number[][] = []

    // Cut by rows
    for (let y=0; y<height; y++) {
        const row: number[] = []
        for (let x=0; x<width; x++) {
            row[x] = data[y*width + x]
        }
        map_data.push(row)
    }

    // Calculate the trailing padding
    let trailing_rows = 0
    for (const row of [...map_data].reverse()) {
        if (row.every((v) => v==0)) {
            trailing_rows += 1
        } else {
            break
        }
    }

    // Cut out the trailing padding
    map_data = map_data.slice(0, -trailing_rows)
    
    // Add aligned padding
    let paddings: number[][] = []
    for (let i=0; i < getPaddingHeight(map_data.length - trailing_rows); i++) {
        // Padding
        paddings.push(Array(width).fill(0))
    }
    map_data = [...paddings, ...map_data]

    // @ts-ignore
    map.map_data = map_data
    // @ts-ignore
    map.entities = [
        ["Player", 2, map_data.length]
    ]
    const json = JSON.stringify(map)
    await Deno.writeTextFile(path2 + filename + ".json", json)
}

for (let filename of fileList) {
    filename = path + filename
    await import(filename)
}
