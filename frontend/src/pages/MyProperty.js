import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function MyProperty() {
  const [properties, setProperties] = useState([]);

  useEffect(() => {
    const fetchProperties = async () => {
      const config = {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.token}`,
        },
      };

      try {
        const res = await axios.get(
          "http://127.0.0.1:8000/property/my_home/",
          config
        );

        const propertyPromises = res.data.map(async (property) => {
          const imgRes = await axios.get(
            `http://127.0.0.1:8000/property/image/get/${property.id}/`
          );
          const ratingRes = await axios.get(
            `http://127.0.0.1:8000/property/${property.id}/rating/`
          );
          console.log(ratingRes.data)

          return { ...property, image: imgRes.data[0], rating: ratingRes.data };
        });

        const propertyList = await Promise.all(propertyPromises);
        setProperties(propertyList);
      } catch (err) {
        console.error("Error fetching properties", err);
      }
    };

    fetchProperties();
  }, []);

  return (
    <div className="container" style={{ marginTop: "50px"}}>
      <div className="row">
        {properties.map((property) => (
          <div key={property.id} className="col-md-4" style={{ margin: "5px"}}>
            <div className="card h-100">
              <img src={property.image.image} className="card-img-top" alt="..." />
              <div className="card-body">
                <h5 className="card-title">{property.city}</h5>
                <ul className="list-group list-group-flush">
                  <li className="list-group-item">
                    <span className="fa fa-bed"></span> {property.beds}
                  </li>
                  <li className="list-group-item">
                    <span className="fa fa-star"></span> {property.rating.rating}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}