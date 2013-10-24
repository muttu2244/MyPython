//	Use this template for reading values from .csv files and generating the graph
//	
//	Create a div in .html page and provide the id of the div in the "chart.renderTo" option of the script
//
$(document).ready(function() {
	$.get('scripts/test/results/blob_unit.csv', function(data) {
				// Split the lines
				var lines = data.split('\n');
				var toptions = options;
				toptions.chart.renderTo = "highchart";
				toptions.xAxis.title.text = "Suite";
				$.each(lines, function(lineNo, line) {
					var items = line.split(',');
					// header line containes categories
					if (lineNo == 0) {
						var i =0;
						$.each(items, function(itemNo, item) {
							if (itemNo > 0) 
							{
								toptions.series[i++].name = item;
							}}	
							
						); }
					else { 
						var i = 0;
						$.each(items, function(itemNo, item) {
							if (itemNo == 0) { toptions.xAxis.categories.push(item); }
							else {
								toptions.series[i++].data.push(parseInt(item));
							}
					}); }  

});
var chart1 = new Highcharts.Chart(toptions);
});
});

