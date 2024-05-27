async function findShortestPath() {
    const startCity = document.getElementById('start_city').value;
    const endCity = document.getElementById('end_city').value;
    const response = await fetch('/shortest_path', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ start_city: parseInt(startCity), end_city: parseInt(endCity) })
    });
    const result = await response.json();
    document.getElementById('result').innerText = `Ruta: ${result.route.join(' -> ')}\nDistancia: ${result.distance} km\nCiudades recomendadas en la ruta: ${result.recommended_cities_on_route.join(', ')}\nCiudades cercanas al destino: ${result.recommended_cities_near_destination.join(', ')}`;
    let descriptions = "\nDescripciones de ciudades:\n";
    for (const city in result.city_descriptions) {
        descriptions += `${city}: ${result.city_descriptions[city]}\n`;
    }
    document.getElementById('result').innerText += descriptions;
}
