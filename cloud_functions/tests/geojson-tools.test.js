// const extractCoordinatesFromMultipolygonFeature = require('../geojson-tools');
const geotools = require('../geotools')

const NYC_BOROUGHS = require('./geojson_files/nyc_boroughs.json');

// test('adds 1 + 2 to equal 3', () => {
//   const multiPolygons = NYC_BOROUGHS.features[0].geometry.coordinates
//   console.log(multiPolygons)
//   let result = extractCoordinatesFromMultipolygonFeature(obj.features[0])
//   let numberOfPolygons = result.length
//   expect(numberOfPolygons).toBe(2);
// });