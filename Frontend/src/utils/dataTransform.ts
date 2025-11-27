// Transform backend data format to frontend component format
import { Reading, MapLatestReading } from './api';

export interface CurrentData {
  temperature: number;
  humidity: number;
  co2: number;
  timestamp: Date;
}

export interface DailyDataPoint {
  time: string;
  temperature: number;
  humidity: number;
  co2: number;
}

export interface MonthlyDataPoint {
  date: string;
  avgTemperature: number;
  avgHumidity: number;
  avgCo2: number;
}

/**
 * Transform latest reading to current data format
 */
export function transformCurrentData(reading: MapLatestReading | null): CurrentData {
  if (!reading) {
    // Return default values if no reading available
    return {
      temperature: 0,
      humidity: 0,
      co2: 0,
      timestamp: new Date(),
    };
  }

  return {
    temperature: reading.temp_c ?? 0,
    humidity: reading.rh ?? 0,
    co2: reading.co2 ?? 0,
    timestamp: new Date(reading.ts),
  };
}

/**
 * Transform readings to daily chart format (hourly aggregation)
 */
export function transformDailyData(readings: Reading[]): DailyDataPoint[] {
  if (readings.length === 0) {
    // Return empty array with 24 hours structure
    return Array.from({ length: 24 }, (_, i) => ({
      time: `${i.toString().padStart(2, '0')}:00`,
      temperature: 0,
      humidity: 0,
      co2: 0,
    }));
  }

  // Group readings by hour
  const hourlyData: { [hour: string]: { temp: number[]; humidity: number[]; co2: number[] } } = {};
  
  readings.forEach((reading) => {
    const date = new Date(reading.ts);
    const hour = date.getHours();
    const hourKey = `${hour.toString().padStart(2, '0')}:00`;
    
    if (!hourlyData[hourKey]) {
      hourlyData[hourKey] = { temp: [], humidity: [], co2: [] };
    }
    
    if (reading.temp_c !== null && reading.temp_c !== undefined) {
      hourlyData[hourKey].temp.push(reading.temp_c);
    }
    if (reading.rh !== null && reading.rh !== undefined) {
      hourlyData[hourKey].humidity.push(reading.rh);
    }
    if (reading.co2 !== null && reading.co2 !== undefined) {
      hourlyData[hourKey].co2.push(reading.co2);
    }
  });

  // Create array for all 24 hours
  const result: DailyDataPoint[] = [];
  for (let i = 0; i < 24; i++) {
    const hourKey = `${i.toString().padStart(2, '0')}:00`;
    const hourData = hourlyData[hourKey];
    
    result.push({
      time: hourKey,
      temperature: hourData
        ? hourData.temp.length > 0
          ? hourData.temp.reduce((a, b) => a + b, 0) / hourData.temp.length
          : 0
        : 0,
      humidity: hourData
        ? hourData.humidity.length > 0
          ? hourData.humidity.reduce((a, b) => a + b, 0) / hourData.humidity.length
          : 0
        : 0,
      co2: hourData
        ? hourData.co2.length > 0
          ? hourData.co2.reduce((a, b) => a + b, 0) / hourData.co2.length
          : 0
        : 0,
    });
  }

  return result;
}

/**
 * Transform readings to monthly chart format (daily aggregation)
 */
export function transformMonthlyData(readings: Reading[]): MonthlyDataPoint[] {
  if (readings.length === 0) {
    // Return empty array with 30 days structure
    const now = new Date();
    return Array.from({ length: 30 }, (_, i) => {
      const date = new Date(now);
      date.setDate(date.getDate() - (29 - i));
      return {
        date: `${date.getMonth() + 1}/${date.getDate()}`,
        avgTemperature: 0,
        avgHumidity: 0,
        avgCo2: 0,
      };
    });
  }

  // Group readings by date
  const dailyData: { [dateKey: string]: { temp: number[]; humidity: number[]; co2: number[] } } = {};
  
  readings.forEach((reading) => {
    const date = new Date(reading.ts);
    const dateKey = `${date.getMonth() + 1}/${date.getDate()}`;
    
    if (!dailyData[dateKey]) {
      dailyData[dateKey] = { temp: [], humidity: [], co2: [] };
    }
    
    if (reading.temp_c !== null && reading.temp_c !== undefined) {
      dailyData[dateKey].temp.push(reading.temp_c);
    }
    if (reading.rh !== null && reading.rh !== undefined) {
      dailyData[dateKey].humidity.push(reading.rh);
    }
    if (reading.co2 !== null && reading.co2 !== undefined) {
      dailyData[dateKey].co2.push(reading.co2);
    }
  });

  // Create array for last 30 days
  const now = new Date();
  const result: MonthlyDataPoint[] = [];
  
  for (let i = 29; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    const dateKey = `${date.getMonth() + 1}/${date.getDate()}`;
    const dayData = dailyData[dateKey];
    
    result.push({
      date: dateKey,
      avgTemperature: dayData
        ? dayData.temp.length > 0
          ? dayData.temp.reduce((a, b) => a + b, 0) / dayData.temp.length
          : 0
        : 0,
      avgHumidity: dayData
        ? dayData.humidity.length > 0
          ? dayData.humidity.reduce((a, b) => a + b, 0) / dayData.humidity.length
          : 0
        : 0,
      avgCo2: dayData
        ? dayData.co2.length > 0
          ? dayData.co2.reduce((a, b) => a + b, 0) / dayData.co2.length
          : 0
        : 0,
    });
  }

  return result;
}

