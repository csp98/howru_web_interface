
charts = {}
{% for question, question_data in list_of_questions.items %}
    //window.alert('{{question_data.dates}}');
    charts[bar_name] = new Chart(document.getElementById(bar_name), {
      type: 'line',
      data: {
        xLabels: ["aa", "bb", "cc"],
        yLabels: ["fecha1", "fecha2", "fecha3"],
        datasets: [{
          backgroundColor: 'rgba(220, 220, 220, 0.5)',
          borderColor: 'rgba(220, 220, 220, 0.8)',
          highlightFill: 'rgba(220, 220, 220, 0.75)',
          highlightStroke: 'rgba(220, 220, 220, 1)',
          data: ["1", "2", "3"]
        }]
      },
      options: {
        legend: {
            "display": false
        },
        responsive: true
      }
    });
    /////////// PIE CHART //////////////////////////
    responses = [];
    values = [];

    for ( let r in json) {
    responses.push(r);
    values.push(json[r]);
    }
    charts[pie_name] = new Chart(document.getElementById(pie_name), {
      type: 'pie',
      data: {
        labels: responses,
        datasets: [{
          data: values,
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
          hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
        }]
      },
      options: {
        responsive: true
      },

    });
{% endfor %}

