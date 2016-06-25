var elements = document.querySelectorAll('.chart');
for(var i=0; i<elements.length; i++){
    new EasyPieChart(elements[i], {
            animate:{
                duration:2000,
                enabled:true
            },
            size: 152,
            barColor:'#008db8',
            trackColor: '#E1E1E3',
            scaleColor:false,
            lineWidth:15,
            lineCap:'round',
            easing:'easeOutBounce'
    });
}
