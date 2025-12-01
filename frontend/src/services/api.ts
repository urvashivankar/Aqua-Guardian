import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// --- Demo Data Constants ---

const DEMO_WATER_QUALITY = {
    pH: 7.8,
    turbidity: 2.4,
    oxygen: 6.5,
    salinity: 34.2,
    temperature: 26.5
};

const DEMO_SUCCESS_STORIES = [
    {
        id: 1,
        title: "Mumbai Harbor Cleanup",
        location: "Mumbai",
        timeframe: "2024",
        description: "Removed 5 tons of plastic waste.",
        image: "https://images.unsplash.com/photo-1618477461853-5f8dd68aa395?q=80&w=1000&auto=format&fit=crop",
        status: "Completed",
        impact: { waterQualityImproved: 15, speciesRecovered: 3, livesImpacted: 2000, pollutionReduced: 25 },
        challenges: "High tides",
        solutions: "Floating barriers",
        results: ["Cleaner shoreline", "Reduced waste"],
        stakeholders: ["Local NGOs", "Volunteers"]
    }
];

const DEMO_DASHBOARD_STATS = {
    total_reports: 125,
    active_users: 45,
    resolved_reports: 82,
    avg_response_time: "2.5 days"
};

const DEMO_REPORTS_BY_TYPE = [
    { name: "Plastic Pollution", value: 45 },
    { name: "Industrial Discharge", value: 30 },
    { name: "Oil Spill", value: 15 },
    { name: "Sewage Overflow", value: 25 },
    { name: "Chemical Contamination", value: 10 }
];

const DEMO_REPORTS_BY_STATUS = [
    { status: "Pending", count: 24 },
    { status: "Investigating", count: 18 },
    { status: "Resolved", count: 83 }
];

const DEMO_GEOGRAPHIC_HEATMAP = [
    { location: "Mumbai Harbor", lat: 18.9438, lng: 72.8354, reports: 45, severity: 85 },
    { location: "Ganges Delta", lat: 22.6855, lng: 88.3667, reports: 32, severity: 75 },
    { location: "Chennai Marina", lat: 13.0500, lng: 80.2824, reports: 28, severity: 65 },
    { location: "Kochi Backwaters", lat: 9.9312, lng: 76.2673, reports: 20, severity: 60 }
];

const DEMO_SEVERITY_DISTRIBUTION = [
    { name: "Critical", value: 15, fill: "#ef4444" },
    { name: "High", value: 35, fill: "#f59e0b" },
    { name: "Medium", value: 45, fill: "#eab308" },
    { name: "Low", value: 30, fill: "#10b981" }
];

const DEMO_TREND_COMPARISON = [
    { month: "Jun", reports: 45, resolved: 30, avgResponseTime: 3.2 },
    { month: "Jul", reports: 52, resolved: 35, avgResponseTime: 3.0 },
    { month: "Aug", reports: 48, resolved: 40, avgResponseTime: 2.8 },
    { month: "Sep", reports: 60, resolved: 45, avgResponseTime: 2.5 },
    { month: "Oct", reports: 55, resolved: 48, avgResponseTime: 2.2 },
    { month: "Nov", reports: 65, resolved: 55, avgResponseTime: 2.0 }
];

const DEMO_MARINE_IMPACT_METRICS = {
    species_impact: [
        { species: "Marine Fish", currentPopulation: 2500000, projectedChange: -15, threats: ["Plastic", "Chemicals"], conservationStatus: "Vulnerable" },
        { species: "Coral Reefs", currentPopulation: 850, projectedChange: -23, threats: ["Acidification", "Warming"], conservationStatus: "Critical" },
        { species: "Sea Turtles", currentPopulation: 45000, projectedChange: -8, threats: ["Nets", "Plastic"], conservationStatus: "Endangered" },
        { species: "Dolphins", currentPopulation: 12000, projectedChange: 3, threats: ["Noise"], conservationStatus: "Stable" }
    ],
    pollution_sources: [
        { source: "Industrial", impact: 35, trend: "Increasing" },
        { source: "Plastic", impact: 28, trend: "Stable" },
        { source: "Agricultural", impact: 22, trend: "Decreasing" },
        { source: "Sewage", impact: 15, trend: "Increasing" }
    ],
    ecosystem_health: { water_quality: 82, biodiversity: 75, pollution_level: 68, conservation_effort: 91 },
    ai_predictions: [
        { timeframe: "Next 5 Years", prediction: "Moderate decline in biodiversity", confidence: 87, severity: "High" },
        { timeframe: "Next 10 Years", prediction: "Critical threshold for reefs", confidence: 92, severity: "Critical" }
    ]
};

// Helper to use demo data if API returns empty
const withDemoFallback = <T>(data: T, demo: T): T => {
    if (Array.isArray(data) && data.length === 0) return demo;
    if (!data) return demo;
    if (typeof data === 'object' && data !== null && Object.keys(data).length === 0) return demo;
    // Specific check for stats object with 0 values
    if (typeof data === 'object' && data !== null && 'total_reports' in data && (data as any).total_reports === 0) return demo;
    return data;
};

export const fetchWaterQuality = async () => {
    try {
        const response = await api.get('/dashboard/water-quality');
        return withDemoFallback(response.data, DEMO_WATER_QUALITY);
    } catch (error) {
        console.warn('Using demo data for water quality');
        return DEMO_WATER_QUALITY;
    }
};

export const fetchMarineImpact = async () => {
    try {
        const response = await api.get('/dashboard/marine-impact');
        return response.data;
    } catch (error) {
        return [];
    }
};

export const fetchSuccessStories = async () => {
    try {
        const response = await api.get('/dashboard/success-stories');
        return withDemoFallback(response.data, DEMO_SUCCESS_STORIES);
    } catch (error) {
        return DEMO_SUCCESS_STORIES;
    }
};

export const fetchWaterQualityHistory = async (limit: number = 20) => {
    const generateHistory = () => Array.from({ length: limit }, (_, i) => ({
        time: `${10 + i}:00`,
        pH: 7 + Math.random(),
        oxygen: 6 + Math.random() * 2,
        turbidity: 1 + Math.random() * 2,
        temperature: 25 + Math.random() * 2,
        salinity: 34 + Math.random()
    }));

    try {
        const response = await api.get(`/dashboard/water-quality-history?limit=${limit}`);
        return withDemoFallback(response.data, generateHistory());
    } catch (error) {
        return generateHistory();
    }
};

export const fetchDashboardStats = async () => {
    try {
        const response = await api.get('/dashboard/stats');
        return withDemoFallback(response.data, DEMO_DASHBOARD_STATS);
    } catch (error) {
        return DEMO_DASHBOARD_STATS;
    }
};

export const fetchReportsTimeline = async (days: number = 30) => {
    const generateTimeline = () => Array.from({ length: days }, (_, i) => {
        const d = new Date();
        d.setDate(d.getDate() - (days - 1 - i));
        return {
            date: d.toISOString().split('T')[0],
            count: Math.floor(Math.random() * 15) + 2
        };
    });

    try {
        const response = await api.get(`/dashboard/reports/timeline?days=${days}`);
        return withDemoFallback(response.data, generateTimeline());
    } catch (error) {
        return generateTimeline();
    }
};

export const fetchReportsByType = async () => {
    try {
        const response = await api.get('/dashboard/reports/by-type');
        return withDemoFallback(response.data, DEMO_REPORTS_BY_TYPE);
    } catch (error) {
        return DEMO_REPORTS_BY_TYPE;
    }
};

export const fetchReportsByStatus = async () => {
    try {
        const response = await api.get('/dashboard/reports/by-status');
        return withDemoFallback(response.data, DEMO_REPORTS_BY_STATUS);
    } catch (error) {
        return DEMO_REPORTS_BY_STATUS;
    }
};

export const fetchGeographicHeatmap = async () => {
    try {
        const response = await api.get('/dashboard/reports/geographic-heatmap');
        return withDemoFallback(response.data, DEMO_GEOGRAPHIC_HEATMAP);
    } catch (error) {
        return DEMO_GEOGRAPHIC_HEATMAP;
    }
};

export const fetchSeverityDistribution = async () => {
    try {
        const response = await api.get('/dashboard/reports/severity-distribution');
        return withDemoFallback(response.data, DEMO_SEVERITY_DISTRIBUTION);
    } catch (error) {
        return DEMO_SEVERITY_DISTRIBUTION;
    }
};

export const fetchTrendComparison = async (months: number = 6) => {
    try {
        const response = await api.get(`/dashboard/reports/trend-comparison?months=${months}`);
        return withDemoFallback(response.data, DEMO_TREND_COMPARISON);
    } catch (error) {
        return DEMO_TREND_COMPARISON;
    }
};

export const fetchMarineImpactMetrics = async () => {
    try {
        const response = await api.get('/dashboard/marine-impact/metrics');
        return withDemoFallback(response.data, DEMO_MARINE_IMPACT_METRICS);
    } catch (error) {
        return DEMO_MARINE_IMPACT_METRICS;
    }
};

export const login = async (credentials: any) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
};

export const register = async (userData: any) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
};

export const submitReport = async (formData: FormData) => {
    try {
        const response = await api.post('/reports/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error submitting report:', error);
        throw error;
    }
};

export default api;
