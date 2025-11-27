// API service for backend communication

const API_BASE_URL = (import.meta.env?.VITE_API_BASE_URL as string) || 'http://localhost:8003';
const API_V1_PREFIX = '/api/v1';

export interface Reading {
  sensor_id: string;
  ts: string;
  pm25?: number | null;
  pm10?: number | null;
  co2?: number | null;
  no2?: number | null;
  temp_c?: number | null;
  rh?: number | null;
  battery?: number | null;
  firmware?: string | null;
  aqi_pm25?: number | null;
  aqi_category?: string | null;
}

export interface MapLatestReading extends Reading {
  lat?: number | null;
  lon?: number | null;
  location_label?: string | null;
}

/**
 * Fetch latest reading for each sensor (for map view)
 */
export async function fetchLatestReadings(): Promise<MapLatestReading[]> {
  const response = await fetch(`${API_BASE_URL}${API_V1_PREFIX}/map/latest`);
  if (!response.ok) {
    throw new Error(`Failed to fetch latest readings: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Fetch historical readings within a time range
 */
export async function fetchReadings(params: {
  sensor_id?: string;
  start?: string; // ISO datetime string
  end?: string; // ISO datetime string
  limit?: number;
}): Promise<Reading[]> {
  const queryParams = new URLSearchParams();
  if (params.sensor_id) queryParams.append('sensor_id', params.sensor_id);
  if (params.start) queryParams.append('start', params.start);
  if (params.end) queryParams.append('end', params.end);
  if (params.limit) queryParams.append('limit', params.limit.toString());

  const url = `${API_BASE_URL}${API_V1_PREFIX}/readings${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch readings: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Get the latest reading (for current metrics display)
 * Returns the most recent reading from any sensor
 */
export async function getCurrentReading(): Promise<MapLatestReading | null> {
  const readings = await fetchLatestReadings();
  if (readings.length === 0) return null;
  
  // Find the most recent reading
  return readings.reduce((latest, current) => {
    const latestTime = new Date(latest.ts).getTime();
    const currentTime = new Date(current.ts).getTime();
    return currentTime > latestTime ? current : latest;
  });
}

/**
 * Get daily readings for today (24 hours)
 */
export async function getDailyReadings(sensorId?: string): Promise<Reading[]> {
  const now = new Date();
  const startOfDay = new Date(now);
  startOfDay.setHours(0, 0, 0, 0);
  const endOfDay = new Date(now);
  endOfDay.setHours(23, 59, 59, 999);

  return fetchReadings({
    sensor_id: sensorId,
    start: startOfDay.toISOString(),
    end: endOfDay.toISOString(),
    limit: 10000,
  });
}

/**
 * Get monthly readings (last 30 days)
 */
export async function getMonthlyReadings(sensorId?: string): Promise<Reading[]> {
  const now = new Date();
  const thirtyDaysAgo = new Date(now);
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

  return fetchReadings({
    sensor_id: sensorId,
    start: thirtyDaysAgo.toISOString(),
    end: now.toISOString(),
    limit: 20000,
  });
}

