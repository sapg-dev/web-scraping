import React from 'react';
import Apartment from './Apartment'; // Import the Apartment component
import apartmentData from './estate.json'; // Import your JSON data
import 'bootstrap/dist/js/bootstrap.bundle.min';
function App() {
  return (
    <div className="App">
      {apartmentData.map((item, index) => (
        <Apartment key={index} data={item.apartment} />
      ))}
    </div>
  );
}

export default App;
