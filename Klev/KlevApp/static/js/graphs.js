// Get the context of the canvas element we want to select
$( document ).ready(function() {
	$("h6").css("font-style", "italic");
	
		var chart = new CanvasJS.Chart("chartContainer",
    {
      title:{
        text: "Device State Over Time",
      },
      animationEnabled: true,  
      axisY:{ 
      	title: "Time and Date",
      },
   
      axisY:{ 
      	title: "Device State (On or Off)",
        maximum: 1.25,  
      },
      
    	toolTip:{             
        content: function( e ){
            var content = e.entries[0].dataPoint.y == 0 ? "OFF" : "ON";
           // content = "y: " + e.entries[0].dataPoint.y + "<br/>" + content;
            return content;
        }
    	},
     
      data: [
      {        
        type: "stepLine",
        markerSize: 5,
        dataPoints: [
        {x: new Date(Date.UTC(2015, 01, 1,6,0)), y: 1} , 
        //indexLabel:"ON"},    
        {x: new Date(Date.UTC(2015, 01, 3,6,0)), y:1} ,
        {x: new Date(Date.UTC(2015, 01, 6,6,0)), y:1} ,
        {x: new Date(Date.UTC(2015, 01, 9,6,0)), y:1} ,
        {x: new Date(Date.UTC(2015, 01, 10,6,0)), y:0}, 
        {x: new Date(Date.UTC(2015, 02, 1,6,0)), y: 1} ,     
        {x: new Date(Date.UTC(2015, 03, 1,6,0)), y: 0} ,
        //indexLabel:"OFF"},     
        {x: new Date(Date.UTC(2015, 04, 1,6,0)), y: 1} ,     
        {x: new Date(Date.UTC(2015, 05, 1,6,0)), y: 0} ,     
        {x: new Date(Date.UTC(2015, 06, 1,6,0)), y: 0} ,     
        {x: new Date(Date.UTC(2015, 07, 1,6,0)), y: 0} ,     
        {x: new Date(Date.UTC(2015, 08, 1,6,0)), y: 0} ,     
        {x: new Date(Date.UTC(2015, 09, 1,6,0)), y: 0} ,     
        {x: new Date(Date.UTC(2015, 10, 1,6,0)), y: 0} ,     
        {x: new Date(Date.UTC(2015, 11, 1,6,0)), y:0} ,
        {x: new Date(Date.UTC(2015, 12, 1,6,0)), y:1} 

        ]
      }             
      
      ]
    });

chart.render();








	/*var ctx = document.getElementById("myChart").getContext("2d");
	var xLabels = [];
	var yLabels = [];
	for (int i = 0; i < 100; i++) {
		xLabels.push(i.toString());
		yLabels.push(1);
	}
	var barData = {
	labels : xLabels,
	datasets : [
		
		{
			fillColor : "rgba(73,188,170,0.4)",
			strokeColor : "rgba(72,174,209,0.4)",
			data : yLabelst
		}

	]
}
	new Chart(ctx).Bar(barData);

	*/
});
