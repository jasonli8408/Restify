import axios from "axios";
import {useState} from "react";

export default function HomePage() {
    const [propertySearch, setPropertySearch] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [guests, setGuests] = useState("");
    const [sortBy, setSortBy] = useState("name_asc")
    const [propertyList, setPropertyList] = useState([]);

    function resetFilter() {
        setPropertySearch("");
        setStartDate("");
        setEndDate("");
        setGuests("");
        setSortBy("name_asc");
    }

    async function handleSearch(e) {
        e.preventDefault();
        try {
            const response = await axios({
                method: 'get',
                url: 'http://127.0.0.1:8000/property/search/',
                params: {
                    search: propertySearch,
                    page: 1,
                    start_date: startDate,
                    end_date: endDate,
                    // num_beds: NOT IMPLEMENTED
                    num_guests: guests,
                    // num_bedrooms: NOT IMPLEMENTED
                    order_by: sortBy,
                }
            });
            setPropertyList(response.data.results);
        } catch (err) {
            alert(err);
        }
    }

    return (
        <div className="container">
            <h1 className="fs-1 fw-semibold text-center">Search for properties</h1>

            <form className="row g-3" onSubmit={handleSearch}>
                <div className="input-group col-md-12">
                    <span className="input-group-text"><i className="fa fa-search"></i></span>
                    <input type="text" className="form-control" placeholder="Search for properties"
                           id="search" value={propertySearch}
                           onChange={(e) => setPropertySearch(e.target.value)}/>
                </div>
                <div className="col-md-3">
                    <label htmlFor="startDate" className="form-label">Start Date</label>
                    <input type="date" id="startDate" className="form-control"
                           value={startDate} onChange={(e) => setStartDate(e.target.value)}/>
                </div>
                <div className="col-md-3">
                    <label htmlFor="endDate" className="form-label">End Date</label>
                    <input type="date" id="endDate" className="form-control" value={endDate}
                           onChange={(e) => setEndDate(e.target.value)} />
                </div>
                <div className="col-md-3">
                    <label htmlFor="guests" className="form-label">Guests</label>
                    <input type="number" id="guests" className="form-control" value={guests}
                           onChange={(e) => setGuests(e.target.value)} />
                </div>
                <div className="col-md-3">
                    <label htmlFor="order" className="form-label">Sort by</label>
                    <select name="order" id="order" className="form-control" value={sortBy}
                            onChange={(e) => setSortBy(e.target.value)}>
                        <option value="name_asc">Name (A-Z)</option>
                        <option value="name_desc">Name (Z-A)</option>
                        <option value="price_desc">Price (High-Low)</option>
                        <option value="price_asc">Price (Low-High)</option>
                        <option value="rating_desc">Rating (High-Low)</option>
                    </select>
                </div>
                <div className="col-md-12">
                    <button type="button" className="btn btn-secondary"
                            onClick={resetFilter}>
                        Reset Filter
                    </button>
                    <button type="submit" className="btn btn-primary">
                        Search
                    </button>
                </div>
            </form>
            <br/>
            <div className="row row-cols-1 g-4 row-cols-sm-2 row-cols-md-3 row-cols-lg-4">
                {propertyList.map(property => (
                    <div className="col">
                        <div className="card h-100">
                            <a href=""> {/* view property page */}
                                <img src="../assets/property_images/1.png" className="card-img-top" alt="..."/>
                                <div className="card-body">
                                    <h5 className="card-title">{property.city}</h5>
                                    <ul className="list-group list-group-flush">
                                        <li className="list-group-item"><span
                                            className="fa fa-calendar"></span>{property.start_date} - {property.end_date}
                                        </li>
                                        <li className="list-group-item"><span
                                            className="fa fa-money"></span>${property.price} per night
                                        </li>
                                        <li className="list-group-item"><span
                                            className="fa fa-bed"></span>{property.num_beds}
                                        </li>
                                        <li className="list-group-item"><span
                                            className="fa fa-star"></span>{property.rating}
                                        </li>
                                    </ul>
                                </div>
                            </a>
                            <a href=""> {/* view comments page */}
                                <div className="card-footer h-100">
                                    <span className="fa fa-bell"></span> Comments
                                </div>
                            </a>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
