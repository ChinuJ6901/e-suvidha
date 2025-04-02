function initMap() {
    console.log("Initializing map...");

    if (!navigator.geolocation) {
        alert("Geolocation is not supported by this browser.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function (position) {
            console.log("User location retrieved:", position.coords.latitude, position.coords.longitude);

            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            const map = new google.maps.Map(document.getElementById("map"), {
                center: userLocation,
                zoom: 12
            });

            new google.maps.Marker({
                position: userLocation,
                map: map,
                title: "Your Location",
                icon: {
                    url: "/static/icons/user-marker.png",
                    scaledSize: new google.maps.Size(30, 30) // Adjusted size
                }
            });

            // Fetch charging stations
            fetch("/data.xml")
                .then(response => response.text())
                .then(str => new window.DOMParser().parseFromString(str, "text/xml"))
                .then(data => {
                    const stations = data.getElementsByTagName("station");
                    console.log("Total Stations Found:", stations.length);

                    for (let i = 0; i < stations.length; i++) {
                        const name = stations[i].getElementsByTagName("name")[0]?.textContent?.trim();
                        const mapLink = stations[i].getElementsByTagName("map_link")[0]?.textContent?.trim();
                        const lat = parseFloat(stations[i].getElementsByTagName("lat")[0]?.textContent.trim());
                        const lng = parseFloat(stations[i].getElementsByTagName("lng")[0]?.textContent.trim());

                        if (isNaN(lat) || isNaN(lng)) {
                            console.error(`Invalid Station Data: ${name}, Lat: ${lat}, Lng: ${lng}`);
                            continue;
                        }

                        console.log(`Adding station: ${name}, Lat: ${lat}, Lng: ${lng}`);

                        const marker = new google.maps.Marker({
                            position: { lat, lng },
                            map: map,
                            title: name,
                            icon: {
                                url: "/static/icons/charging-station.png",
                                scaledSize: new google.maps.Size(30, 30) // Adjusted size
                            },
                            label: {
                                text: name,  // Display station name
                                color: "#ff4c50",
                                fontWeight: "bold",
                                fontSize: "12px"
                            }
                        });

                        // InfoWindow for station details
                        const infoWindow = new google.maps.InfoWindow({
                            content: `<div>
                                        <b>${name}</b><br>
                                        <a href="${mapLink}" target="_blank">Open in Maps</a>
                                      </div>`
                        });

                        marker.addListener("click", () => {
                            infoWindow.open(map, marker);
                        });
                    }
                })
                .catch(error => console.error("Error loading XML data:", error));
        },
        function (error) {
            console.error("Error getting location:", error);
            alert("Failed to get your location. Please enable location services.");
        }
    );
}

window.initMap = initMap;
