import React, { useState } from 'react';
import Carousel from 'react-bootstrap/Carousel';
// Ensure Bootstrap CSS is imported in your project (in index.js or App.js)

function Apartment({ data }) {
  const [index, setIndex] = useState(0);

  const handleSelect = (selectedIndex) => {
    setIndex(selectedIndex);
  };

  return (
    <div className="container my-4">
      <div className="card">
        <div className="card-body">
          <h2 className="card-title">Apartment at {data.addresses[0]}</h2>
          <p className="card-text">{data.description}</p>

          <Carousel activeIndex={index} onSelect={handleSelect} interval={null}>
            {data.url.map((imageUrl, idx) => (
              <Carousel.Item key={idx}>
                <img
                  className="d-block w-100"
                  src={imageUrl}
                  alt={`Slide ${idx + 1}`}
                />
                <Carousel.Caption>
                  <h3>Image {idx + 1}</h3>
                  <p>Web Scraping Project</p>
                </Carousel.Caption>
              </Carousel.Item>
            ))}
          </Carousel>

          <ul className="list-group list-group-flush mt-3">
            {data.elements.map((element, idx) => (
              <li key={idx} className="list-group-item">{element}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Apartment;