const geojson = `
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {
      "boro_code": "5",
      "boro_name": "Staten Island",
      "shape_area": "1623757282.78",
      "shape_leng": "325956.009"
    },
    "geometry": {
      "type": "MultiPolygon",
      "coordinates": [
        [
          [
            [-47.900390625, -14.944784875088372],
            [-51.591796875, -19.91138351415555],
            [-41.11083984375, -21.309846141087192],
            [-43.39599609375, -15.390135715305204],
            [-47.900390625, -14.944784875088372]
          ],
          [
            [-46.6259765625, -17.14079039331664],
            [-47.548828125, -16.804541076383455],
            [-46.23046874999999, -16.699340234594537],
            [-45.3515625, -19.31114335506464],
            [-46.6259765625, -17.14079039331664]
          ],
          [
            [-44.40673828125, -18.375379094031825],
            [-44.4287109375, -20.097206227083888],
            [-42.9345703125, -18.979025953255267],
            [-43.52783203125, -17.602139123350838],
            [-44.40673828125, -18.375379094031825]
          ]
        ],
        [
          [
            [-51.591796875, -19.91138351415555],
            [-41.11083984375, -21.309846141087192],
            [-47.900390625, -14.944784875088372]
          ],
          [
            [-46.6259765625, -17.14079039331664],
            [-46.23046874999999, -16.699340234594537],
            [-46.6259765625, -17.14079039331664]
          ]
        ]
      ]
    }
  }]
}
`

let obj = JSON.parse(geojson);


function extractCoordinatesFromPolygonFeature(geoJsonFeature) {
    let multipolygon = geoJsonFeature.geometry.coordinates
    let result = [];

    for (const polygon in multipolygon) {

    }

    console.log(coordinates)
}


function extractCoordinatesFromMultipolygonFeature(geoJsonFeature) {
    let multipolygon = geoJsonFeature.geometry.coordinates
    let result = [];

    for (const polygon of multipolygon) {
        let outer = polygon[0];
        let holes = [];

        for (let i = 0; i < polygon.length; i++) {
            let subshape = polygon[i]
            let coordinates = []
            for (const coordinate of subshape) {
                coordinates.push(coordinate.reverse())
            }
            i === 0 ? outer.push(coordinates) : holes.push(coordinates)
            i === 0 ? console.log(coordinates) : console.log("nil")
        }

        result.push({outer:outer, holes:holes})
    }

    return result
}

const res = extractCoordinatesFromMultipolygonFeature(obj.features[0])
console.log(res)

