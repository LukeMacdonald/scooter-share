export const useMarkerMapping = (scooters) => {
    return scooters.map(({ latitude, longitude }) => ({ lat: latitude, lng: longitude }));
  };