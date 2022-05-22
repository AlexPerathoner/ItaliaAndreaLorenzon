mapboxgl.accessToken =
	"pk.eyJ1IjoicGxhbmVtYWQiLCJhIjoiemdYSVVLRSJ9.g3lbg_eN0kztmsfIPxa9MQ";
const map = new mapboxgl.Map({
	container: "map",
	style: "mapbox://styles/mapbox/light-v9",
	center: [12.505, 42],
	zoom: 6,
});

map.on("load", () => {
	map.addSource("place", {
		type: "geojson",
		data: "https://raw.githubusercontent.com/AlexPerathoner/ItaliaAndreaLorenzon/main/data.geojson",
	});

	map.addLayer({
		id: "place-layer",
		type: "circle",
		source: "place",
		paint: {
			"circle-radius": 6,
			"circle-stroke-width": 2,
			"circle-color": "red",
			"circle-stroke-color": "white",
		},
	});

	map.on("click", "place-layer", (e) => {
		const coordinates = e.features[0].geometry.coordinates.slice();
		const nome = e.features[0].properties.nome;
		const url = e.features[0].properties.url;

		const description = "<h2>" + nome + "</h2><iframe width='560' height='315' src='" + url + "' title='YouTube video player' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>"

		while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
		}

		new mapboxgl.Popup().setLngLat(coordinates).setHTML(description).addTo(map);
	});

	// Change the cursor to a pointer when the mouse is over the places layer.
	map.on("mouseenter", "place-layer", () => {
		map.getCanvas().style.cursor = "pointer";
	});

	// Change it back to a pointer when it leaves.
	map.on("mouseleave", "place-layer", () => {
		map.getCanvas().style.cursor = "";
	});
});
