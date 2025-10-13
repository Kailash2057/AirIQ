import { Card } from "./ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

interface MonthlyChartProps {
  data: Array<{
    date: string;
    avgTemperature: number;
    avgHumidity: number;
    avgCo2: number;
  }>;
}

export function MonthlyChart({ data }: MonthlyChartProps) {
  return (
    <Card className="p-6">
      <h3 className="mb-4">Monthly Average Readings</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
          <XAxis dataKey="date" stroke="var(--foreground)" />
          <YAxis yAxisId="left" stroke="var(--foreground)" />
          <YAxis yAxisId="right" orientation="right" stroke="var(--foreground)" />
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: "var(--radius)",
            }}
          />
          <Legend />
          <Bar
            yAxisId="left"
            dataKey="avgTemperature"
            fill="var(--chart-1)"
            name="Avg Temperature (°C)"
          />
          <Bar
            yAxisId="left"
            dataKey="avgHumidity"
            fill="var(--chart-2)"
            name="Avg Humidity (%)"
          />
          <Bar
            yAxisId="right"
            dataKey="avgCo2"
            fill="var(--chart-3)"
            name="Avg CO2 (ppm)"
          />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}
