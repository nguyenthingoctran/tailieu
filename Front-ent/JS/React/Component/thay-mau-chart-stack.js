import React, { Component } from 'react';
import Chart from 'chart.js';

export default class CTLChartBarStack extends Component {
    chartRef = React.createRef();
    chart = null;

    chart_options = {
        title: {
            display: false,
            text: 'Rankings Distribution'
        },
        legend: {
            position: 'bottom',
        },

        tooltips: {
            mode: 'label',
            itemSort: function (data_set1, data_set2) {
                return data_set1.datasetIndex - data_set2.datasetIndex
            },
            //axis: 'x',
            //intersect: true,
            // reversed: true,
            //shared: true,
        },

        responsive: true,
        scales: {
            xAxes: [{
                barPercentage: 1.25,
                // minBarLength: 2,
                stacked: true,
                // categoryPercentage: 1.0
            }],
            yAxes: [{
                stacked: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Keywords'
                }
            }]
        }
    }

    drawChart = (props) => {
        const { data, label } = props;

        var barChartData = {
            labels: label,
            datasets: [
                {
                    type: 'bar',
                    label: '# 1 - 3',
                    // backgroundColor: '#35b140', //sáng
                    backgroundColor: '#24e4a0', //sáng
                    data: data.top3,
                    borderColor: 'white',
                    borderWidth: 2.5,
                    stack: 'Stack 0',
                },
                {
                    type: 'bar',
                    label: '# 4 - 10',
                    // backgroundColor: '#41c84f',
                    backgroundColor: '#9ef4d8',
                    data: data.top10,
                    borderColor: 'white',
                    borderWidth: 2.5,
                    stack: 'Stack 0',
                },
                {
                    type: 'bar',
                    label: '# 11 - 20',
                    // backgroundColor: '#5bd066',
                    backgroundColor: '#ffeac5',
                    data: data.top20,
                    borderColor: 'white',
                    borderWidth: 2.5,
                    stack: 'Stack 0',
                },
                {
                    type: 'bar',
                    label: '# 21 - 100',
                    // backgroundColor: '#7fd985',
                    backgroundColor: '#feb541',
                    data: data.top100,
                    borderColor: 'white',
                    borderWidth: 2.5,
                    stack: 'Stack 0',
                },
                {
                    type: 'bar',
                    label: '# Out of Top 100',
                    // backgroundColor: '#c3eec8',
                    backgroundColor: '#fe7085',
                    data: data.top_out,
                    borderColor: 'white',
                    borderWidth: 2.5,
                    stack: 'Stack 0',
                },
            ]
        };

        const ctx = this.chartRef.current.getContext("2d");
        this.chart = new Chart(ctx, {
            type: 'bar',
            data: barChartData,
            options: this.chart_options
        });
    }

    reDrawChart = (props) => {
        const { data, label } = props;

        var barChartData = {
            labels: label,
            datasets: [
                {
                    label: '# 1 - 3',
                    // backgroundColor: '#35b140', //sáng
                    backgroundColor: '#3bdca2', //sáng
                    data: data.top3,
                    borderColor: 'white',
                    borderWidth: 1.5,
                },
                {
                    label: '# 4 - 10',
                    // backgroundColor: '#41c84f',
                    backgroundColor: '#aae9d5',
                    data: data.top10,
                    borderColor: 'white',
                    borderWidth: 1.5,
                },
                {
                    label: '# 11 - 20',
                    // backgroundColor: '#5bd066',
                    backgroundColor: '#ffeac5',
                    data: data.top20,
                    borderColor: 'white',
                    borderWidth: 1.5,
                },
                {
                    label: '# 21 - 100',
                    // backgroundColor: '#7fd985',
                    backgroundColor: '#feb541',
                    data: data.top100,
                    borderColor: 'white',
                    borderWidth: 1.5,
                },
                {
                    label: '# Out of Top 100',
                    // backgroundColor: '#c3eec8',
                    backgroundColor: '#fe7085',
                    data: data.top_out,
                    borderColor: 'white',
                    borderWidth: 1.5,
                },
            ]
        };

        this.chart.data = barChartData;

        this.chart.config.options = this.chart_options

        this.chart.update();
    }

    componentDidMount() {
        this.drawChart(this.props);
    }

    componentWillReceiveProps(next_props) {
        if(JSON.stringify(next_props.data) != JSON.stringify(this.props.data))
            this.reDrawChart(next_props);
    }

    render() {
        const { chart_id } = this.props;

        return (
            <>
                <canvas
                    id={chart_id}
                    ref={this.chartRef}
                />
            </>
        )
    }
}