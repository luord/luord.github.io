var elements = document.querySelectorAll('.desc')

elements.forEach(el => {
    el.classList.add('chart')
    el.classList.remove('desc')

    new EasyPieChart(el, {
        animate:{
            duration: 2000,
            enabled: true
        },
        size: 152,
        barColor: '#008db8',
        trackColor: '#E1E1E3',
        scaleColor: false,
        lineWidth: 15,
        lineCap: 'round',
        easing: 'easeOutBounce'
    })
})

document.querySelectorAll('.no-js').forEach(el => el.setAttribute('hidden', true))
