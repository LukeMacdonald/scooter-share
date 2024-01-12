export const useMarkerMapping = (scooters, customIcon) => {
    return scooters.map(({ latitude, longitude }) => ({ lat: latitude, lng: longitude, icon: customIcon }));
  };