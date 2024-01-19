import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { icon } from '@fortawesome/fontawesome-svg-core/import.macro'


export const getStatusColor = (status) => {
    switch (status) {
      case 'available':
        return 'bg-green-500'; // Green color for 'active'
      case 'awaiting repair':
        return 'bg-red-500'; // Red color for 'cancelled'
      case 'occupying':
        return 'bg-blue-500'; // Blue color for 'completed'
      default:
        return 'bg-gray-500'; // Default color (gray) for other statuses
    }
};

export const getBookingColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-500'; // Green color for 'active'
      case 'cancelled':
        return 'bg-red-500'; // Red color for 'cancelled'
      case 'completed':
        return 'bg-blue-500'; // Blue color for 'completed'
      default:
        return 'bg-gray-500'; // Default color (gray) for other statuses
    }
};

export const  convertTo12HourFormat = (time24hr) => {
    // Parse the input time string
    const [hours, minutes] = time24hr.split(':');
    const parsedDate = new Date(0, 0, 0, hours, minutes);
  
    // Format as 12-hour time
    const time12hr = parsedDate.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
  
    return time12hr;
}

export const getPowerColor = (power) => {
    console.log(typeof(power))
    if (power >= 50){
      return 'bg-green-200'
    }
    else if (power >= 20){
      return 'bg-orange-200'
    }
    else{
      return 'bg-red-200'
    }
  
  }

export const getBatteryIcon = (power) => {
  if (power >= 90){
    return <FontAwesomeIcon icon={icon({ name: 'battery'})}/>
  }
  if (power > 65){
    return <FontAwesomeIcon icon={icon({ name: 'battery-three-quarters'})}/>
  }
  else if (power > 33){
    return <FontAwesomeIcon icon={icon({ name: 'battery-half'})}/>
  }
  else{
    return <FontAwesomeIcon icon={icon({ name: 'battery-quarter'})}/>
  }

}