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
import { HotspotData } from '../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface HotspotChartProps {
  data: HotspotData[];
}

export default function HotspotChart({ data }: HotspotChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-container">
        <h3>🔥 File Hotspots</h3>
        <p>No hotspot data available</p>
      </div>
    );
  }

  // Take top 8 hotspots for better visualization
  const topHotspots = data.slice(0, 8);

  const chartData = {
    labels: topHotspots.map(item => {
      // Shorten file paths for better display
      const parts = item.file.split('/');
      if (parts.length > 2) {
        return `.../${parts.slice(-2).join('/')}`;
      }
      return item.file;
    }),
    datasets: [
      {
        label: 'Commits Touching File',
        data: topHotspots.map(item => item.commits_touching),
        backgroundColor: 'rgba(255, 159, 64, 0.6)',
        borderColor: 'rgba(255, 159, 64, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    indexAxis: 'y' as const,
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'File Change Frequency (Hotspots)',
      },
      tooltip: {
        callbacks: {
          title: function(context: any) {
            const index = context[0].dataIndex;
            return topHotspots[index].file;
          },
          afterLabel: function(context: any) {
            const index = context.dataIndex;
            const hotspot = topHotspots[index];
            return `Lines changed: ${hotspot.lines_changed}`;
          }
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="chart-container">
      <h3>🔥 File Hotspots</h3>
      <div className="chart-wrapper">
        <Bar data={chartData} options={options} />
      </div>
      <div className="chart-summary">
        <p>Files with the most frequent changes - potential complexity indicators</p>
      </div>
    </div>
  );
}