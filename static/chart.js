document.addEventListener('DOMContentLoaded', function() {
    var dates = {{ dates | tojson }};
    var actualPrices = {{ actual_prices | tojson }};
    var predictedPrices = {{ predicted_prices | tojson }};

    var trace1 = {
        x: dates,
        y: actualPrices,
        mode: 'lines',
        name: 'Actual Prices'
    };

    var trace2 = {
        x: dates,
        y: predictedPrices,
        mode: 'lines',
        name: 'Predicted Prices'
    };

    var data = [trace1, trace2];

    var layout = {
        title: 'Actual vs Predicted Prices',
        xaxis: {
            title: 'Date'
        },
        yaxis: {
            title: 'Price ($)'
        }
    };

    Plotly.newPlot('chart', data, layout);
});
