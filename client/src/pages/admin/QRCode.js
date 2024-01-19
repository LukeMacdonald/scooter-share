import React from 'react';
import { QRCode } from 'react-qrcode-logo';
import { useParams } from 'react-router-dom';

function QRCodes() {

const {scooterID} = useParams()


  const downloadCodes = () => {
    downloadQRCode ('unlock-qr', `Scooter-${scooterID}-UnlockQR`)
    downloadQRCode ('lock-qr', `Scooter-${scooterID}-LockQR`)
  }
  const downloadQRCode = (id, name ) => {

    const canvas = document.getElementById(id);
   if(canvas) {
      const pngUrl = canvas
        .toDataURL("image/png")
        .replace("image/png", "image/octet-stream");
      let downloadLink = document.createElement("a");
      downloadLink.href = pngUrl
      downloadLink.download = `${name}.png`;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
   }
  };

  return (
    <>
    <div className='w-full flex md:flex-col items-center justify-evenly pt-20'>
        <div className='py-3'>
        <QRCode 
            value={`<http://192.168.1.98:3000/qr/unlock/${scooterID}>`} 
            id="unlock-qr"
            qrStyle="dots"  
            size={250}
            eyeRadius={5}  
            enableCORS={true}  
            fgColor='#00888f'
        />  
        </div>
        <div className='py-3'>
        <QRCode 
        value={`<http://192.168.1.98:3000/qr/lock/${scooterID}>`} 
        id='lock-qr'
        qrStyle="dots" 
        size={250}
        eyeRadius={5}  
        enableCORS={true}
        fgColor='#e62958'
        />

        </div>


      
    </div>
    <div className='flex justify-center items-center w-full pt-20'>
    <button className='bg-dark text-light py-3 w-1/2 rounded-full' onClick={downloadCodes}>Download QR Codes</button>

    </div>
   
    </>
  );
}

export default QRCodes;