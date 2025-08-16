import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { ComplexityData } from '../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface ComplexityTrendProps {
  data: ComplexityData[];
}

export default function ComplexityTrend({ data }: ComplexityTrendProps) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-container">
        <h3>📈 Complexity Trends</h3>
        <p>No complexity trend data available</p>
      </div>
    );
  }

  const chartData = {
    labels: data.map(item => item.period),
    datasets: [
      {
        label: 'Lines Added',
        data: data.map(item => item.lines_added),
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.1,
      },
      {
        label: 'Lines Deleted',
        data: data.map(item => item.lines_deleted),
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.1,
      },
      {
        label: 'Files Touched',
        data: data.map(item => item.files_touched),
        borderColor: 'rgba(153, 102, 255, 1)',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        fill: false,
        tension: 0.1,
        yAxisID: 'y1',
      },
    ],
  };

  const options = {
    responsive: true,
    interaction: {
      mode: 'index' as const,
      intersect: false,
    },
    stacked: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Code Complexity Trends Over Time',
      },
      tooltip: {
        callbacks: {
          afterLabel: function(context: any) {
            const index = context.dataIndex;
            const period = data[index];
            const netChange = period.lines_added - period.lines_deleted;
            return `Net change: ${netChange > 0 ? '+' : ''}${netChange} lines`;
          }
        }
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Time Period'
        }
      },
      y: {
        type: 'linear' as const,
        display: true,
        position: 'left' as const,
        title: {
          display: true,
          text: 'Lines Changed'
        },
      },
      y1: {
        type: 'linear' as const,
        display: true,
        position: 'right' as const,
        title: {
          display: true,
          text: 'Files Touched'
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
  };

  return (
    <div className="chart-container">
      <h3>📈 Complexity Trends</h3>
      <div className="chart-wrapper">
        <Line data={chartData} options={options} />
      </div>
      <div className="chart-summary">
        <p>Monthly code changes and file activity over time</p>
        <div className="trend-stats">
          {data.length > 1 && (
            <>
              <span>Total periods: {data.length}</span>
              <span>
                Peak activity: {data.reduce((max, curr) => 
                  (curr.lines_added + curr.lines_deleted > max.lines_added + max.lines_deleted) ? curr : max
                ).period}
              </span>
            </>
          )}
        </div>
      </div>
    </div>
  );
}