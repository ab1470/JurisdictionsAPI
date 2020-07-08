const geoJsonTools = function ($) {
    $.extractCoordinatesFromPolygonFeature = function(geoJsonFeature) {
        let multipolygon = geoJsonFeature.geometry.coordinates
        let result = [];

        for (const polygon in multipolygon) {

        }

        console.log(coordinates)
    }


    $.extractCoordinatesFromMultipolygonFeature = function(geoJsonFeature) {
        let multipolygon = geoJsonFeature.geometry.coordinates
        let result = [];

        for (const polygon of multipolygon) {
            let outer;
            let holes = [];

            for (let i = 0; i < polygon.length; i++) {
                let subshape = polygon[i]
                let coordinates = []
                for (const coordinate of subshape) {
                    coordinates.push(coordinate.reverse())
                }
                i === 0 ? outer = coordinates : holes.push(coordinates)
            }

            result.push({outer:outer, holes:holes})
        }

        return result
    }

}(geoJsonTools || {});

module.exports = geoJsonTools;