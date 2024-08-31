import * as d3 from "https://esm.sh/d3@7";

/** @param {{ model: DOMWidgetModel, el: HTMLElement }} context */
function render({ model, el }) {
	let button = document.createElement("button");
	button.innerHTML = `count is ${model.get("value")}`;
	button.addEventListener("click", () => {
	  model.set("value", model.get("value") + 1);
	  model.save_changes();
	});
	model.on("change:value", () => {
	  button.innerHTML = `count is ${model.get("value")}`;
	});
	el.appendChild(button);

	el = d3.select(el);
	let svg = el.append("svg");

	const height = 400;
	const width = 400;
	const marginBottom = 20;
	const marginLeft = 20;
	const marginTop = 20;
	const marginRight = 20;

	const w = width - marginLeft - marginRight;
	const h = height - marginBottom - marginTop;

	svg.attr("width", 400).attr("height", height);
	let x = d3.scaleLinear().domain([0, 10]).range([0, 400]);
	let y = d3.scaleLinear().domain([0, 10]).range([0, 400]);
	const gx = svg.append("g")
		.attr("transform", `translate(${marginLeft},${height - marginBottom})`)
		.call(d3.axisBottom(x));
	const gy = svg.append("g")
		.attr("transform", `translate(${marginLeft},${marginBottom})`)
		.call(d3.axisLeft(y));
	const line = d3.line()

	let circles = svg.append("g")

	// image is base64 encoded png
	let image = model.get("image");
	if (image != null) {
		let extent = model.get("extent");
		let img = new Image();
		img.src = "data:image/png;base64," + image;
		img.onload = () => {
			svg.append("image")
				.attr("xlink:href", img.src)
				.attr("width", w)
				.attr("height", h)
				.attr("x", marginLeft)
				.attr("y", marginTop);
		}
	}

}
export default { render };


