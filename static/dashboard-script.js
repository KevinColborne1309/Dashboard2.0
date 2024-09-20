async function fetchDataAndRenderChart(apiEndpoint, chartElementId, chartConfig) {
    try {
        let response = await fetch(apiEndpoint);
        let data = await response.json();
        const ctx = document.getElementById(chartElementId).getContext("2d");
        new Chart(ctx, chartConfig(data));
    } catch (error) {
        console.error("Error fetching or rendering chart:", error);
    }
}

// Gender Distribution Chart
fetchDataAndRenderChart("/api/gender_distribution", "genderChart", (data) => ({
    type: "pie",
    data: {
        labels: data.genders,
        datasets: [{
            label: "Gender Distribution",
            data: data.counts,
            backgroundColor: ['#FF6384', '#36A2EB'],
        }]
    }
}));

// Age Group Distribution Chart
fetchDataAndRenderChart("/api/age_group_distribution", "ageGroupChart", (data) => ({
    type: "bar",
    data: {
        labels: data.age_groups,
        datasets: [{
            label: "Age Group Distribution",
            data: data.counts,
            backgroundColor: ['#FFCE56', '#FF6384', '#36A2EB'],
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
            }
        }
    }
}));

// A1 Score Trends Over Waves Chart
fetchDataAndRenderChart("/api/a1_score_trends", "a1ScoreChart", (data) => ({
    type: "line",
    data: {
        labels: data.waves,
        datasets: Object.keys(data.data).map((provider, index) => ({
            label: provider,
            data: data.data[provider],
            fill: false,
            borderColor: ['#FF6384', '#36A2EB', '#FFCE56'][index % 3], // Customize as needed
        }))
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
            }
        }
    }
}));
