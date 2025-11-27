import { useState, useEffect } from "react";
import {
  Thermometer,
  Droplets,
  Cloud,
  RefreshCw,
  Clock,
  AlertCircle,
  Wind,
  Activity,
} from "lucide-react";
import { MetricCard } from "./components/MetricCard";
import { DailyChart } from "./components/DailyChart";
import { MonthlyChart } from "./components/MonthlyChart";
import { AiriQLogo } from "./components/AiriQLogo";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "./components/ui/tabs";
import { Button } from "./components/ui/button";
import { Badge } from "./components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "./components/ui/alert";
import { getStatus } from "./utils/mockData";
import {
  getCurrentReading,
  getDailyReadings,
  getMonthlyReadings,
} from "./utils/api";
import {
  transformCurrentData,
  transformDailyData,
  transformMonthlyData,
  CurrentData,
  DailyDataPoint,
  MonthlyDataPoint,
} from "./utils/dataTransform";

export default function App() {
  const [currentData, setCurrentData] = useState<CurrentData>({
    temperature: 0,
    humidity: 0,
    co2: 0,
    timestamp: new Date(),
  });
  const [dailyData, setDailyData] = useState<DailyDataPoint[]>([]);
  const [monthlyData, setMonthlyData] = useState<MonthlyDataPoint[]>([]);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [nextUpdate, setNextUpdate] = useState(30);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all data in parallel
      const [currentReading, dailyReadings, monthlyReadings] = await Promise.all([
        getCurrentReading(),
        getDailyReadings(),
        getMonthlyReadings(),
      ]);

      // Transform and set data
      setCurrentData(transformCurrentData(currentReading));
      setDailyData(transformDailyData(dailyReadings));
      setMonthlyData(transformMonthlyData(monthlyReadings));
      setLastUpdate(new Date());
      setNextUpdate(30);
    } catch (err) {
      console.error("Error fetching data:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to fetch data from backend. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const refreshData = () => {
    fetchData();
  };

  // Initial data fetch
  useEffect(() => {
    fetchData();
  }, []);

  // Auto-refresh every 30 minutes
  useEffect(() => {
    const interval = setInterval(() => {
      refreshData();
    }, 30 * 60 * 1000); // 30 minutes

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
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-blue-50/30 dark:to-blue-950/10 p-4 md:p-8 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl -z-10"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl -z-10"></div>
      
      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-full blur-xl group-hover:blur-2xl transition-all duration-300"></div>
                <div className="relative transform group-hover:scale-105 transition-transform duration-300">
                  <AiriQLogo size={100} className="drop-shadow-lg" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-background animate-pulse">
                  <div className="w-full h-full bg-green-500 rounded-full animate-ping opacity-75"></div>
                </div>
              </div>
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-600 bg-clip-text text-transparent">
                    AirIQ
                  </h1>
                  <Activity className="w-6 h-6 text-blue-500 animate-pulse" />
                </div>
                <p className="text-muted-foreground mt-1 text-lg font-medium">
                  Air Quality Monitoring Sensor
                </p>
                <div className="flex items-center gap-2 mt-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <p className="text-sm text-muted-foreground">
                    System Active • Real-time monitoring
                  </p>
                </div>
              </div>
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
                disabled={loading}
              >
                <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
                {loading ? "Loading..." : "Refresh Now"}
              </Button>
            </div>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

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
            showFahrenheit={true}
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