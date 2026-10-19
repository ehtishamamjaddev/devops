export interface NumericFeature {
  name: string;
  label: string;
  unit: string;
  min: number;
  max: number;
  step: number;
}

export const TERRAIN_FEATURES: NumericFeature[] = [
  { name: 'Elevation', label: 'Elevation', unit: 'm', min: 1859, max: 3858, step: 1 },
  { name: 'Aspect', label: 'Aspect', unit: 'degrees', min: 0, max: 360, step: 1 },
  { name: 'Slope', label: 'Slope', unit: 'degrees', min: 0, max: 66, step: 1 },
  { name: 'Horizontal_Distance_To_Hydrology', label: 'Horizontal distance to water', unit: 'm', min: 0, max: 1397, step: 1 },
  { name: 'Vertical_Distance_To_Hydrology', label: 'Vertical distance to water', unit: 'm', min: -173, max: 601, step: 1 },
  { name: 'Horizontal_Distance_To_Roadways', label: 'Distance to roadways', unit: 'm', min: 0, max: 7117, step: 1 },
  { name: 'Hillshade_9am', label: 'Hillshade · 9 am', unit: 'index', min: 0, max: 255, step: 1 },
  { name: 'Hillshade_Noon', label: 'Hillshade · noon', unit: 'index', min: 0, max: 255, step: 1 },
  { name: 'Hillshade_3pm', label: 'Hillshade · 3 pm', unit: 'index', min: 0, max: 255, step: 1 },
  { name: 'Horizontal_Distance_To_Fire_Points', label: 'Distance to fire points', unit: 'm', min: 0, max: 7173, step: 1 },
];

export const WILDERNESS_AREAS = Array.from({ length: 4 }, (_, index) => ({
  key: `Wilderness_Area_${index + 1}`,
  label: `Wilderness area ${String(index + 1).padStart(2, '0')}`,
}));

export const SOIL_TYPES = Array.from({ length: 40 }, (_, index) => ({
  key: `Soil_Type_${index + 1}`,
  label: `Soil type ${String(index + 1).padStart(2, '0')}`,
}));

export const COVER_TYPES: Record<number, string> = {
  1: 'Spruce / fir',
  2: 'Lodgepole pine',
  3: 'Ponderosa pine',
  4: 'Cottonwood / willow',
  5: 'Aspen',
  6: 'Douglas-fir',
  7: 'Krummholz',
};

export const SAMPLE_VALUES: Record<string, number> = {
  Elevation: 2596,
  Aspect: 51,
  Slope: 3,
  Horizontal_Distance_To_Hydrology: 258,
  Vertical_Distance_To_Hydrology: 0,
  Horizontal_Distance_To_Roadways: 510,
  Hillshade_9am: 221,
  Hillshade_Noon: 232,
  Hillshade_3pm: 148,
  Horizontal_Distance_To_Fire_Points: 6279,
  ...Object.fromEntries(WILDERNESS_AREAS.map((area, index) => [area.key, Number(index === 0)])),
  ...Object.fromEntries(SOIL_TYPES.map((soil, index) => [soil.key, Number(index === 28)])),
};
