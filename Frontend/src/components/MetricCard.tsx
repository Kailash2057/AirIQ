import { Card } from "./ui/card";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: number;
  unit: string;
  icon: LucideIcon;
  status: "good" | "warning" | "danger";
  timestamp: Date;
  showFahrenheit?: boolean; // For temperature: show F as primary, C as secondary
}

export function MetricCard({ title, value, unit, icon: Icon, status, timestamp, showFahrenheit = false }: MetricCardProps) {
  const statusColors = {
    good: "bg-green-500/10 text-green-600 border-green-500/20",
    warning: "bg-yellow-500/10 text-yellow-600 border-yellow-500/20",
    danger: "bg-red-500/10 text-red-600 border-red-500/20",
  };

  // Convert Celsius to Fahrenheit
  const fahrenheit = showFahrenheit ? (value * 9/5 + 32) : null;
  const celsius = value; // Original value is in Celsius

  return (
    <Card className={`p-6 border-2 ${statusColors[status]}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <Icon className="w-5 h-5" />
            <h3 className="text-muted-foreground">{title}</h3>
          </div>
          <div className="mt-3">
            {showFahrenheit && fahrenheit !== null ? (
              <>
                {/* Fahrenheit as primary */}
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl">{fahrenheit.toFixed(1)}</span>
                  <span className="text-muted-foreground">°F</span>
                </div>
                {/* Celsius as secondary */}
                <div className="flex items-baseline gap-2 mt-2">
                  <span className="text-2xl text-muted-foreground">{celsius.toFixed(1)}</span>
                  <span className="text-sm text-muted-foreground">°C</span>
                </div>
              </>
            ) : (
              <div className="flex items-baseline gap-2">
                <span className="text-4xl">{value.toFixed(1)}</span>
                <span className="text-muted-foreground">{unit}</span>
              </div>
            )}
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            Updated: {timestamp.toLocaleTimeString()}
          </p>
        </div>
      </div>
    </Card>
  );
}
