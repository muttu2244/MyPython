//	Use this template for reading values from .csv files and generating the graph
//	
//	Create a div in .html page and provide the id of the div in the "chart.renderTo" option of the script
//
var chart1;
var toptions;

function fetch_chart(name)
{	
	var path = 'scripts/test/results/';
	path = path + name +'.csv';

	$.get(path, function(data) {
				// Split the lines
				var lines = data.split('\n');
				toptions = jQuery.extend(true,{},options);
				////back(options);
				toptions.chart.renderTo = 'chart';
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
							if (itemNo == 0) { toptions.xAxis.categories.push(name); }
							else {
								toptions.series[i++].data.push(parseInt(item));
							}
					}); }  

});

chart1 = new Highcharts.Chart(toptions);
});
}
	
function get_pie()
{
	data = sessionStorage.getItem("PIE");
	//back("data");
        //back(data);
        if (data == '' || data == null)
        {
        var data = 'pie=get';
        //back(data);
        $.ajax(
        {
                url : "handler.php",
                type: "POST",
                data: data,
                success: function (data)
                {
                        var labels = [];
                        var values = [];
                        if (data == '0,0,0,0,0,')
                        {
				$("#label_data").css({display:"block"});
				///DATA NOT AVAILIBALE
                        }
                        else
                        {
				$("#label_data").css({display:"none"});
                                sessionStorage.setItem("PIE",data);
                                make_pie(data);
                        }

                }
        });
        }
        else if (data == '0,0,0,0,0,')
        {
		$("#label_data").css({display:"block"});
		///DATA NOT AVAILIBALE
	}
	else
                make_pie(data);
}

function make_pie(data)
{
	var labels = ['Passed','Failed','Error','Skipped'];
        var values = [];
        var temp = data.split(',');
	var i;
	var temp_list = [];
	var poptions;
	var temp_obj = {};

	for (i = 0;i<4;i++)
	{
		var temp_list = [];
		if (labels[i]=='Failed')
		{
			temp_obj.name = labels[i];
			temp_obj.y = Math.round((parseInt(temp[i+1]))/(parseInt(temp[0]))*100);
			temp_obj.sliced = true;
			temp_obj.selected = true;
			values.push(temp_obj);
		}
		else
		{
			temp_list.push(labels[i]);
			temp_list.push(Math.round((parseInt(temp[i+1]))/(parseInt(temp[0]))*100));
       			values.push(temp_list);
		}
	}
	
	Highcharts.getOptions().colors = $.map(Highcharts.getOptions().colors, function(color) {
            return {
                radialGradient: { cx: 0.5, cy: 0.3, r: 0.7 },
                stops: [
                    [0, color],
                    [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
                ]
            };
        });


	poptions = jQuery.extend(true,{},pie_options);
	poptions.chart.renderTo =  'tile_glass3';
	poptions.chart.name = "Results";
	poptions.series[0].data = values;
	//back(values);
var chart = new Highcharts.Chart(poptions);

	$("#tile_glass1").css({display:"none"});
	$("#tile_glass3").css({display:"block"});
}

