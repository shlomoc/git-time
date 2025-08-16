import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { OwnershipData } from '../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface OwnershipChartProps {
  data: OwnershipData[];
}

export default function OwnershipChart({ data }: OwnershipChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-container">
        <h3>📊 Code Ownership</h3>
        <p>No ownership data available</p>
      </div>
    );
  }

  const chartData = {
    labels: data.map(item => item.author),
    datasets: [
      {
        label: 'Commits',
        data: data.map(item => item.commits),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: 'Lines Changed',
        data: data.map(item => item.lines_changed),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Code Ownership by Author',
      },
      tooltip: {
        callbacks: {
          afterLabel: function(context: any) {
            const authorIndex = context.dataIndex;
            const author = data[authorIndex];
            return [
              `First commit: ${new Date(author.first_commit).toLocaleDateString()}`,
              `Last commit: ${new Date(author.last_commit).toLocaleDateString()}`
            ];
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="chart-container">
      <h3>📊 Code Ownership</h3>
      <div className="chart-wrapper">
        <Bar data={chartData} options={options} />
      </div>
      <div className="chart-summary">
        <p>Top contributors by commits and lines changed</p>
      </div>
    </div>
  );
}