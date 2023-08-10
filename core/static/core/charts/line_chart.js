(function ($) {
    $.fn.extend( {
        LineChart: function() {
            var $chart = $(this);
            var ctx = $chart.get(0).getContext("2d");
            var $data = $chart.find('.chart-data');
            var $dataItems = $data.find('.chart-data-item');
            var labels = {};
            var data = {};

            $dataItems.each(function() {
                if (labels[$(this).data('type')]) {
                    labels[$(this).data('type')].push($(this).data('date'))
                } else {
                    labels[$(this).data('type')] = [$(this).data('date')]
                }
                if (data[$(this).data('type')]) {
                    data[$(this).data('type')].push(parseFloat($(this).data('value')))
                } else {
                    data[$(this).data('type')] = [parseFloat($(this).data('value'))]
                }
            });

            let max_label = Object.values(labels)[0]
            const datasets = []
            const colors = ['green', "red", 'blue', 'orange']
            let i = 0
            for (let d in data) {
                datasets.push({
                    label: d,
                    fillColor: "transparent",
                    strokeColor: colors[i],
                    pointColor: colors[i],
                    pointHighlightFill: colors[i],
                    responsive: true,
                    data: data[d],
                    pointRadius: 0, 
                })
                i += 1
                if (max_label.length < labels[d].length) {
                    max_label = labels[d]
                }
            }

            var chart = new Chart(ctx).Line({
                labels: max_label,
                datasets: datasets,
            }, {
                scaleGridLineColor: $chart.find('.chart-scaleGridLineColor').css('color'),
                scaleLineColor: $chart.find('.chart-scaleLineColor').css('color'),
                scaleFontColor: $chart.find('.chart-scaleFontColor').css('color')
            });

            var updateChartColors = function(chart) {
                for (var i = 0; i < chart.datasets.length; ++i) {
                    chart.datasets[i]['fillColor'] = $chart.find('.chart-fillColor').css('color');
                    chart.datasets[i]['strokeColor'] = $chart.find('.chart-strokeColor').css('color');
                    chart.datasets[i]['pointColor'] = $chart.find('.chart-pointColor').css('color');
                    chart.datasets[i]['pointHighlightFill'] = $chart.find('.chart-pointHighlightFill').css('color');
                }

                chart.scale['gridLineColor'] = $chart.find('.chart-scaleGridLineColor').css('color');
                chart.scale['lineColor'] = $chart.find('.chart-scaleLineColor').css('color');
                chart.scale['textColor'] = $chart.find('.chart-scaleFontColor').css('color');

                chart.update();
            };

            $(document).on('theme:changed', function() {
                updateChartColors(chart);
            });
        }
    });
})(jet.jQuery);