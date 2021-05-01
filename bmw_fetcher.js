
document.addEventListener('DOMContentLoaded', function() {
    // const url = 'http://127.0.0.1:5000/';
    const url = 'https://fathomless-cove-96970.herokuapp.com/';

    const feature_ranges = {"mileage": {"type": "numeric", "range": [1.0, 214000.0]}, "year": {"type": "numeric", "range": [1996.0, 2020.0]}, "engineSize": {"type": "numeric", "range": [1.5, 6.6]}, "model": {"type": "category", "values": [" 1 Series", " 2 Series", " 3 Series", " 4 Series", " 5 Series", " 6 Series", " 7 Series", " 8 Series", " M2", " M3", " M4", " M5", " X1", " X2", " X3", " X4", " X5", " X6", " X7", " Z4", " i8"]}, "transmission": {"type": "category", "values": ["Automatic", "Manual", "Semi-Auto"]}}
    
    function append_paragraph_to_form(text){
	const form = document.querySelector('form');
	var para = document.createElement("p");
	var node = document.createTextNode(text);
	para.appendChild(node);
	form.parentNode.insertBefore(para, form.nextSibling);
    }
    
    
    function handleSubmit(event) {
	event.preventDefault();
	const data = new FormData(event.target);
	const mileage = data.get('mileage');

	var object = {};
	data.forEach(function(value, key){
	    if (value){
		object[key] = value;
	    }
	});
	if (Object.keys(object).length !== 0){
	    var json = JSON.stringify(object);
	    console.log(json);
	    
	    const myheaders = new Headers();

	    myheaders.append('Content-Type', 'application/json')
	    const myRequest = new Request(url, {
		method: 'POST',
		mode: 'cors',
		headers: {
	    	    'Content-Type': 'application/x-www-form-urlencoded',
                },
		cache: 'no-cache',
		body: new URLSearchParams({
                    'query':
		    json,
                }),
	    });
	    
	    fetch(myRequest)
	    // .then(response => console.log(response))
		.then(response => response.text())
		.then(myText => {
		    append_paragraph_to_form(myText);

		}).catch((error) => {
		    console.error('Error:', error);
		    append_paragraph_to_form(error)

		});;

	}
	else
	{
	    append_paragraph_to_form("Please provide some more info");
	    console.log("No data provided");
	}
    }


    function build_number_input(key, feature){
	var x = document.createElement("INPUT");
	x.setAttribute("type", "number");	    
	x.setAttribute("name", key);
	x.setAttribute("id", key);
	x.setAttribute("placeholder", key);
	x.setAttribute("min", feature["range"][0]);
	x.setAttribute("max", feature["range"][1]);
	return x;
    }
    function build_category_input(key, feature){
	var x = document.createElement("select");
	x.setAttribute("name", key);
	x.setAttribute("id", key);
	var option = document.createElement("option");
	option.setAttribute("value", "");
	option.text = "Select "+key;
	x.add(option)
	feature["values"].forEach(function (item, index) {
	    var option = document.createElement("option");
	    option.setAttribute("value", item);
	    option.text = item;
	    x.add(option)
	});
	return x;
    }

    function create_label(key){
	var x = document.createElement("label");
	x.setAttribute("for", key);
	x.innerHTML = key;
	return x
    }
    
    function build_form(feature_ranges, form){
	console.log(feature_ranges);
	for (var key in feature_ranges) {
	    if (feature_ranges.hasOwnProperty(key)) {
		var feature = feature_ranges[key];
		if (feature["type"] == "numeric"){
		    form.appendChild(build_number_input(key, feature));
		    form.appendChild(create_label(key));
		    form.appendChild(document.createElement("br"));

		}
		else if (feature["type"] == "category"){
		    form.appendChild(build_category_input(key, feature));
		    form.appendChild(create_label(key));
		    form.appendChild(document.createElement("br"));
		}
	    }
	}
	var button = document.createElement("button");
	button.setAttribute("type", "submit");
	button.innerHTML = "Submit";
	form.appendChild(button);
    }

    const form = document.querySelector('form');
    build_form(feature_ranges, form);
    
    form.addEventListener('submit', handleSubmit);
   
}, false);
