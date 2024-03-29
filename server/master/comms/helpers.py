import requests
from datetime import datetime


def get_street_address(latitude, longitude):
    """
    Get the street address from latitude and longitude using Google Maps Geocoding API.

    Parameters:
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.

    Returns:
        str: Street address.
    """
    address_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}" \
                  "&location_type=ROOFTOP&key=AIzaSyCI9KBPlHOzx9z7dp41LNbzpYaVn3qqgNY"
    response = requests.get(address_url, timeout=5)
    address_data = response.json()
    if 'results' in address_data and len(address_data['results']) > 0 and 'formatted_address' in \
            address_data['results'][0]:
        result = address_data['results'][0]['formatted_address']
    else:
        result = f"Unable to Locate Street Address for ({latitude},{longitude})"
    return result


def get_email_body(scooter_id, report, location, subject):
    return f'''
        <html>
        <head>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>{subject}</h2>
                </div>
                <div class="content">
                    <p><strong>Dear Engineers,</strong></p>
                    <p>We have received a report regarding a damaged scooter that requires immediate attention.</p>
                    <table>
                        <tr>
                            <th>Scooter ID</th>
                            <td>{scooter_id}</td>
                        </tr>
                        <tr>
                            <th>Issue Reported</th>
                            <td>{report}</td>
                        </tr>
                        <tr>
                            <th>Location</th>
                            <td>{location}</td>
                        </tr>
                    </table>
                    <p>Please review the situation and take necessary actions to address the issue as soon as possible.</p>
                    <p>Thank you for your prompt attention to this matter.</p>
                    <p>Best regards,</p>
                    <p><strong>Scooter Share Co</strong></p>
                </div>
            </div>
        </body>
        </html>
    '''


def convert_time_format(time_string):
    """
    Convert time string to a different format.
    """
    time_obj = datetime.strptime(time_string, "%a %d %b, %H:%M, %Y")
    return time_obj.strftime("%I:%M %p")


def calculate_duration(start_time, end_time):
    """
    Calculate duration in minutes.
    """
    start_time_obj = datetime.strptime(start_time, "%a %d %b, %H:%M, %Y")
    end_time_obj = datetime.strptime(end_time, "%a %d %b, %H:%M, %Y")
    duration_minutes = (end_time_obj - start_time_obj).total_seconds() / 60
    return str(duration_minutes)
