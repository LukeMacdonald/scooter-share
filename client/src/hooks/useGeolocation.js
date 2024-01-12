import { useEffect, useState } from 'react';

const useGeolocation = () => {
  const [center, setPosition] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const handleSuccess = (pos) => {
      const { latitude, longitude } = pos.coords;
      setPosition({ lat: latitude, lng: longitude });
    };

    const handleError = (err) => {
      setError(err.message);
    };

    const options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0,
    };

    const watchId = navigator.geolocation.watchPosition(handleSuccess, handleError, options);

    return () => {
      navigator.geolocation.clearWatch(watchId);
    };
  }, []);

  return { center, error };
};

export default useGeolocation;