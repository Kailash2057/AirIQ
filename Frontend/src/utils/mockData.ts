// Generate mock IoT sensor data

export function generateCurrentData() {
  return {
    temperature: 20 + Math.random() * 10,
    humidity: 40 + Math.random() * 30,
    co2: 400 + Math.random() * 600,
    timestamp: new Date(),
  };
}

export function generateDailyData() {
  const data = [];
  const now = new Date();
  
  for (let i = 0; i < 24; i++) {
    const hour = i.toString().padStart(2, '0') + ':00';
    data.push({
      time: hour,
      temperature: 20 + Math.random() * 8 + Math.sin(i / 24 * Math.PI * 2) * 3,
      humidity: 45 + Math.random() * 20 + Math.cos(i / 24 * Math.PI * 2) * 10,
      co2: 450 + Math.random() * 400 + Math.sin(i / 12 * Math.PI) * 100,
    });
  }
  
  return data;
}

export function generateMonthlyData() {
  const data = [];
  const now = new Date();
  
  for (let i = 29; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    const dateStr = `${(date.getMonth() + 1)}/${date.getDate()}`;
    
    data.push({
      date: dateStr,
      avgTemperature: 22 + Math.random() * 6,
      avgHumidity: 50 + Math.random() * 15,
      avgCo2: 500 + Math.random() * 300,
    });
  }
  
  return data;
}

export function getStatus(type: 'temperature' | 'humidity' | 'co2', value: number): 'good' | 'warning' | 'danger' {
  if (type === 'temperature') {
    if (value < 18 || value > 28) return 'danger';
    if (value < 20 || value > 26) return 'warning';
    return 'good';
  }
  
  if (type === 'humidity') {
    if (value < 30 || value > 70) return 'danger';
    if (value < 40 || value > 60) return 'warning';
    return 'good';
  }
  
  if (type === 'co2') {
    if (value > 1000) return 'danger';
    if (value > 800) return 'warning';
    return 'good';
  }
  
  return 'good';
}
