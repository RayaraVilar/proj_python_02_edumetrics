const riskElement = document.getElementById("risk-data");
const courseElement = document.getElementById("course-data");

const riskData = JSON.parse(riskElement.textContent);
const courseData = JSON.parse(courseElement.textContent);

const riskCanvas = document.getElementById("riskChart");
const courseCanvas = document.getElementById("courseChart");

new Chart(riskCanvas, {
  type: "doughnut",
  data: {
    labels: ["Baixo risco", "Médio risco", "Alto risco"],
    datasets: [
      {
        data: [riskData.low, riskData.medium, riskData.high],
        backgroundColor: ["#28bd92", "#f4ad41", "#ef6666"],
        borderWidth: 0,
        hoverOffset: 6,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    cutout: "73%",
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: "#161a2c",
        padding: 12,
        cornerRadius: 9,
        titleFont: {
          size: 11,
        },
        bodyFont: {
          size: 11,
        },
      },
    },
  },
});

const courseLabels = courseData.map((item) => item.course);
const courseValues = courseData.map((item) => item.total);

new Chart(courseCanvas, {
  type: "bar",
  data: {
    labels: courseLabels,
    datasets: [
      {
        label: "Estudantes",
        data: courseValues,
        backgroundColor: "#635bff",
        borderRadius: 8,
        borderSkipped: false,
        maxBarThickness: 34,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: "y",
    scales: {
      x: {
        beginAtZero: true,
        grid: {
          color: "#eef0f5",
        },
        ticks: {
          color: "#8d93a3",
          font: {
            size: 9,
          },
          precision: 0,
        },
        border: {
          display: false,
        },
      },
      y: {
        grid: {
          display: false,
        },
        ticks: {
          color: "#646b7c",
          font: {
            size: 9,
          },
        },
        border: {
          display: false,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: "#161a2c",
        padding: 12,
        cornerRadius: 9,
      },
    },
  },
});
