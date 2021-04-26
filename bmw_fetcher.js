


document.addEventListener('DOMContentLoaded', function() {
    function handleSubmit(event) {
	event.preventDefault();
	const data = new FormData(event.target);
	const mileage = data.get('mileage');
	// data.append("query", "lol");
	// console.log({ mileage });
	// console.log(data);

	const myheaders = new Headers();
	// myheaders.append('Access-Control-Allow-Origin', '*')
	myheaders.append('Content-Type', 'application/json')
	const myRequest = new Request('http://127.0.0.1:5000/', {
	    method: 'POST',
	    mode: 'cors',
	    // mode: 'same-origin',
	    headers: {
                    // 'Content-Type': 'application/json',
	    	'Content-Type': 'application/x-www-form-urlencoded',
                },
	    // headers: myheaders,
	    // headers: {
	    // 	'Content-Type': 'application/json',
	    // 	// 'Access-Control-Allow-Origin': 'http://127.0.0.1:5000/'
	    // 	'Access-Control-Allow-Origin': '*'
	    // },
	    // Access-Control-Allow-Origin: "http://127.0.0.1:5000/",
	    cache: 'no-cache',
	    // body: data,
	    body: new URLSearchParams({
                'query':
		// {mileage}
		JSON.stringify({mileage}),
                }),
	    // body: JSON.stringify({query: {mileage: mileage}}),
	    // body: {query: JSON.stringify({mileage})},
	    // query: {mileage}
	});
	
	//console.log(myRequest);
	fetch(myRequest)
	    // .then(response => console.log(response))
	    .then(response => response.text())
	    .then(myText => {
		
	    	// console.log(myJson);
		const form = document.querySelector('form');
		var para = document.createElement("p");
		var node = document.createTextNode(myText);
		para.appendChild(node);
		form.parentNode.insertBefore(para, form.nextSibling);

	    })
	;

	
    }

    
    const form = document.querySelector('form');
    
    form.addEventListener('submit', handleSubmit);
}, false);


