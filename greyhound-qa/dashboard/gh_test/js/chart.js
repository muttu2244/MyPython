//
//	This is the global variable which describes the structure of the graph
//	

var options = {
         chart: {
            renderTo: '',
//          borderColor: '#2E2EFE',
//            borderWidth: 2,
            type: 'column'
         },
        colors: [
        '#4572A7',
        '#89A54E',
        '#AA4643',
        '#FF0000',
        '#D7DF01',
        '#DB843D',
        '#92A8CD',
        '#A47D7C',
        '#B5CA92'
],
         title: {
            text: 'Results'
         },
         xAxis: {
                title: { text: "" },
            categories: []
         },
         yAxis: {
            title: {
               text: 'No of Testcases'
            }
         },
         series: [ { data: [] },{data: []},{data: []},{data: []},{data: []} ]
      };

var pie_options = {
	chart: {
		backgroundColor:'transparent',
                renderTo: '',
                //plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
	colors: [
        '#89A54E',
        '#9A0000',
        '#000000',
        '#FF0000',
        '#D7DF01',
        '#DB843D',
        '#92A8CD',
        '#A47D7C',
        '#B5CA92'
],
            title: {
                text: ''
            },
            tooltip: {
                pointFormat: '<b>{point.percentage}%</b>',
                percentageDecimals: 1
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
			style: {
				fontSize: '13px',
				fontFamily: 'Segoe UI Italic,Segoe WPC,Segoe UI'
			},
			enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            return this.point.name + ': '+ Math.round(this.percentage) +' %';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'Results',
                data: []}]

};


