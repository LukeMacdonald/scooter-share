import requests

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
    return address_data.get('results')[0].get('formatted_address')

def get_email_body(scooter_id,report, location, subject):
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
