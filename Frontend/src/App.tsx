import { useState, useEffect } from "react";
import {
  Thermometer,
  Droplets,
  Cloud,
  RefreshCw,
  Clock,
} from "lucide-react";
import { MetricCard } from "./components/MetricCard";
import { DailyChart } from "./components/DailyChart";
import { MonthlyChart } from "./components/MonthlyChart";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "./components/ui/tabs";
import { Button } from "./components/ui/button";
import { Badge } from "./components/ui/badge";
import {
  generateCurrentData,
  generateDailyData,
  generateMonthlyData,
  getStatus,
} from "./utils/mockData";

export default function App() {
  const [currentData, setCurrentData] = useState(
    generateCurrentData(),
  );
  const [dailyData, setDailyData] = useState(
    generateDailyData(),
  );
  const [monthlyData, setMonthlyData] = useState(
    generateMonthlyData(),
  );
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [nextUpdate, setNextUpdate] = useState(30);

  const refreshData = () => {
    setCurrentData(generateCurrentData());
    setDailyData(generateDailyData());
    setMonthlyData(generateMonthlyData());
    setLastUpdate(new Date());
    setNextUpdate(30);
  };

  // Auto-refresh every 30 minutes
  useEffect(() => {
    const interval = setInterval(
      () => {
        refreshData();
      },
      30 * 60 * 1000,
    ); // 30 minutes

    return () => clearInterval(interval);
  }, []);

  // Countdown timer
  useEffect(() => {
    const interval = setInterval(() => {
      setNextUpdate((prev) => {
        if (prev <= 0) return 30;
        return prev - 1;
      });
    }, 60 * 1000); // Every minute

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1>IoT Environmental Monitor</h1>
              <p className="text-muted-foreground mt-2">
                Real-time monitoring of environmental conditions
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Badge
                variant="secondary"
                className="flex items-center gap-2"
              >
                <Clock className="w-4 h-4" />
                Next update in {nextUpdate} min
              </Badge>
              <Button
                onClick={refreshData}
                variant="outline"
                className="gap-2"
              >
                <RefreshCw className="w-4 h-4" />
                Refresh Now
              </Button>
            </div>
          </div>
        </div>

        {/* Current Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <MetricCard
            title="Temperature"
            value={currentData.temperature}
            unit="°C"
            icon={Thermometer}
            status={getStatus(
              "temperature",
              currentData.temperature,
            )}
            timestamp={currentData.timestamp}
          />
          <MetricCard
            title="Humidity"
            value={currentData.humidity}
            unit="%"
            icon={Droplets}
            status={getStatus("humidity", currentData.humidity)}
            timestamp={currentData.timestamp}
          />
          <MetricCard
            title="CO2 Level"
            value={currentData.co2}
            unit="ppm"
            icon={Cloud}
            status={getStatus("co2", currentData.co2)}
            timestamp={currentData.timestamp}
          />
        </div>

        {/* Historical Data */}
        <Tabs defaultValue="daily" className="w-full">
          <TabsList className="grid w-full md:w-[400px] grid-cols-2">
            <TabsTrigger value="daily">
              Daily Records
            </TabsTrigger>
            <TabsTrigger value="monthly">
              Monthly Records
            </TabsTrigger>
          </TabsList>
          <TabsContent value="daily" className="mt-6">
            <DailyChart data={dailyData} />
          </TabsContent>
          <TabsContent value="monthly" className="mt-6">
            <MonthlyChart data={monthlyData} />
          </TabsContent>
        </Tabs>

        {/* Status Legend */}
        <div className="mt-8 p-4 bg-muted/50 rounded-lg">
          <h4 className="mb-3">Status Indicators</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p className="mb-2">Temperature:</p>
              <ul className="space-y-1">
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-green-500"></span>
                  <span className="text-sm text-muted-foreground">
                    20-26°C (Good)
                  </span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
                  <span className="text-sm text-muted-foreground">
                    18-20°C or 26-28°C (Warning)
                  </span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-red-500"></span>
                  <span className="text-sm text-muted-foreground">
                    &lt;18°C or &gt;28°C (Danger)
                  </span>
                </li>
              </ul>
            </div>
            <div>
              <p className="mb-2">Humidity:</p>
              <ul className="space-y-1">
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-green-500"></span>
                  <span className="text-sm text-muted-foreground">
                    40-60% (Good)
                  </span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
                  <span className="text-sm text-muted-foreground">
                    30-40% or 60-70% (Warning)
                  </span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-red-500"></span>
                  <span className="text-sm text-muted-foreground">
                    &lt;30% or &gt;70% (Danger)
                  </span>
                </li>
              </ul>
            </div>
            <div>
              <p className="mb-2">CO2 Level:</p>
              <ul className="space-y-1">
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-green-500"></span>
                  <span className="text-sm text-muted-foreground">
                    &lt;800 ppm (Good)
                  </span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
                  <span className="text-sm text-muted-foreground">
                    800-1000 ppm (Warning)
                  </span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-red-500"></span>
                  <span className="text-sm text-muted-foreground">
                    &gt;1000 ppm (Danger)
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}