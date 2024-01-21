import React, { useEffect, useState } from 'react';
import { LayerGroup, useMap } from 'react-leaflet';
import { ObjectMarker } from './ObjectMarker';
import api from '../api';

function ObjectMarkersGroup() {
  const map = useMap();
  const [provinces, setProvinces] = useState([]);
  const axios = api();

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Obtain data for provinces
        const provincesResponse = await axios.GET('/get_provinces');
        const provincesData = provincesResponse.data;

        // For each province, obtain coordinates and update the state
        const provincesWithCoordinates = await Promise.all(
          provincesData.map(async (province) => {
            const coordinatesResponse = await axios.GET(`/get_plain_coordinates?province_id=${province.id}`);
            const coordinatesData = coordinatesResponse.data;
            return {
              id: province.id,
              name: province.name,
              geoJSON: {
                type: 'feature',
                geometry: {
                  type: 'Point',
                  coordinates: [coordinatesData.longitude, coordinatesData.latitude],
                },
                properties: {
                  id: province.id,
                  name: province.name,
                },
              },
            };
          })
        );

        setProvinces(provincesWithCoordinates);
      } catch (error) {
        console.error('Error fetching API data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <LayerGroup>
      {provinces.map((province) => (
        <ObjectMarker key={province.id} geoJSON={province.geoJSON} />
      ))}
    </LayerGroup>
  );
}

export default ObjectMarkersGroup;
