window.onload = function () {

            var options = {
                animationEnabled: true,
                axisX: {
                    valueFormatString: "MMM"
                },
                axisY: {
                    title: "Динамика изменения продаж",
                },
                data: [{
                    xValueFormatString: "MMMM",
                    type: "spline",
                    dataPoints: [
                        { x: new Date(2019, 9), y: 0},
                        { x: new Date(2019, 10), y: 1.42},
                        { x: new Date(2019, 11), y: 0.08},
                        { x: new Date(2019, 12), y: -0.44},
                    ]
                },
                      {
                    yValueFormatString: "###",
                    xValueFormatString: "MMMM",
                    type: "spline",
                    dataPoints: [
                        { x: new Date(2019, 9), y: 0},
                        { x: new Date(2019, 10), y: 1.63},
                        { x: new Date(2019, 11), y: -0.12},
                        { x: new Date(2019, 12), y: -0.56},
                    ]
                }]
            };
            $("#chartContainer").CanvasJSChart(options);
        }