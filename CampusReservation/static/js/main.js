document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Fetch real data from the API
        const response = await fetch('/api/dashboard-stats');
        const data = await response.json();

        // 1. Room Popularity Chart (Doughnut)
        const roomCtx = document.getElementById('roomChart');
        if (roomCtx) {
            new Chart(roomCtx, {
                type: 'doughnut',
                data: {
                    labels: data.rooms.labels,
                    datasets: [{
                        data: data.rooms.data,
                        backgroundColor: [
                            '#0d6efd', // primary
                            '#198754', // success
                            '#ffc107', // warning
                            '#dc3545', // danger
                            '#6c757d', // secondary
                            '#0dcaf0'  // info
                        ],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                usePointStyle: true,
                            }
                        }
                    },
                    cutout: '65%'
                }
            });
        }

        // 2. Equipment Borrowing Frequency (Bar)
        const equipCtx = document.getElementById('equipmentChart');
        if (equipCtx) {
            new Chart(equipCtx, {
                type: 'bar',
                data: {
                    labels: data.equipments.labels,
                    datasets: [{
                        label: '借用次數',
                        data: data.equipments.data,
                        backgroundColor: '#0d6efd', // primary
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        }

    } catch (error) {
        console.error("無法載入儀表板數據:", error);
    }
});
