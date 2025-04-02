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

            // User location marker
            new google.maps.Marker({
                position: userLocation,
                map: map,
                title: "Your Location",
                icon: {
                    url: "/static/icons/user-marker.png",
                    scaledSize: new google.maps.Size(30, 30)
                }
            });

            // Google Sheets API URL
            const sheetId = "1_yJNiYr-1wkLZpajlp7bWr9t9V9KJU5uhx90N8gmBi0"; // Replace with your actual sheet ID
            const apiKey = "AIzaSyD0YyrCNc5FSM4aHykDcRch9KVA5GhNbBM"; // Replace with your actual API key
            const sheetUrl = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/Stations?key=${apiKey}`;

            // Fetch station data from Google Sheets
            fetch(sheetUrl)
                .then(response => response.json())
                .then(data => {
                    const rows = data.values;
                    if (!rows || rows.length < 2) {
                        console.error("No station data found.");
                        return;
                    }

                    console.log("Stations loaded:", rows.length - 1);

                    for (let i = 1; i < rows.length; i++) {  // Skip the header row
                        const [id, name, mapLink, lat, lng, rating, regular_charges, fast_charges] = rows[i];

                        if (isNaN(parseFloat(lat)) || isNaN(parseFloat(lng))) {
                            console.error(`Invalid Station Data: ${name}, Lat: ${lat}, Lng: ${lng}`);
                            continue;
                        }

                        console.log(`Adding station: ${name}, Lat: ${lat}, Lng: ${lng}`);

                        const marker = new google.maps.Marker({
                            position: { lat: parseFloat(lat), lng: parseFloat(lng) },
                            map: map,
                            title: name,
                            icon: {
                                url: "/static/icons/charging-station.png",
                                scaledSize: new google.maps.Size(30, 30)
                            }
                        });

                        // Stylish InfoWindow content
                        const infoWindowContent = `
                            <div style="
                                font-family: Arial, sans-serif;
                                padding: 12px;
                                width: 270px;
                                background-color: #fff;
                                border-radius: 8px;
                                box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
                                color: #000;
                            ">
                                <h3 style="margin: 5px 0; text-align: center; font-size: 18px; color: #333;">
                                    ${name}
                                </h3>
                                <p style="margin: 6px 0; font-size: 14px;"><b>⭐ Rating:</b> ${rating || "N/A"}</p>
                                <p style="margin: 6px 0; font-size: 14px;"><b>💰 Regular Rate:</b> ₹${regular_charges || "N/A"}</p>
                                <p style="margin: 6px 0; font-size: 14px;"><b>⚡ Fast Charging Rate:</b> ₹${fast_charges || "N/A"}</p>
                                <hr style="margin: 10px 0;">
                                <div style="display: flex; justify-content: space-between;">
                                    <a href="${mapLink}" target="_blank"
                                        style="text-decoration: none;
                                               background-color: #28a745;
                                               color: white;
                                               padding: 8px 12px;
                                               border-radius: 5px;
                                               font-size: 14px;
                                               font-weight: bold;">
                                        🚗 Go to Station
                                    </a>
                                    <a href="/book-charging-service?station=${encodeURIComponent(name)}" target="_blank"
                                        style="text-decoration: none;
                                               background-color: #007bff;
                                               color: white;
                                               padding: 8px 12px;
                                               border-radius: 5px;
                                               font-size: 14px;
                                               font-weight: bold;">
                                        ⚡ Book Service
                                    </a>
                                </div>
                            </div>`;

                        // InfoWindow
                        const infoWindow = new google.maps.InfoWindow({
                            content: infoWindowContent
                        });

                        marker.addListener("click", () => {
                            infoWindow.open(map, marker);
                        });
                    }
                })
                .catch(error => console.error("Error fetching station data:", error));
        },
        function (error) {
            console.error("Error getting location:", error);
            alert("Failed to get your location. Please enable location services.");
        }
    );
}

window.initMap = initMap;
