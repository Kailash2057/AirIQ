import { Card } from "./ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

interface DailyChartProps {
  data: Array<{
    time: string;
    temperature: number;
    humidity: number;
    co2: number;
  }>;
}

export function DailyChart({ data }: DailyChartProps) {
  return (
    <Card className="p-6">
      <h3 className="mb-4">Today's Readings</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
          <XAxis dataKey="time" stroke="var(--foreground)" />
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
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="temperature"
            stroke="var(--chart-1)"
            strokeWidth={2}
            name="Temperature (°C)"
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="humidity"
            stroke="var(--chart-2)"
            strokeWidth={2}
            name="Humidity (%)"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="co2"
            stroke="var(--chart-3)"
            strokeWidth={2}
            name="CO2 (ppm)"
          />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}
