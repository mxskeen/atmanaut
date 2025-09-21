"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { getMoodById, getMoodTrend } from "@/shared/moods";
import { format, parseISO } from "date-fns";
import useFetch from "@/hooks/use-fetch";
import { useApiClient } from "@/lib/api-client";
import MoodAnalyticsSkeleton from "./analytics-loading";
import { useUser } from "@clerk/nextjs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Link from "next/link";

const timeOptions = [
  { value: "7d", label: "Last 7 Days" },
  { value: "15d", label: "Last 15 Days" },
  { value: "30d", label: "Last 30 Days" },
];

const MoodAnalytics = () => {
  const apiClient = useApiClient();
  const [period, setPeriod] = useState("7d");

  const {
    loading,
    data: analytics,
    fn: fetchAnalytics,
  } = useFetch(() => apiClient.getAnalytics());
  const [fallback, setFallback] = useState(null);

  const { isLoaded } = useUser();

  useEffect(() => {
    fetchAnalytics(period);
  }, [period]);

  // Build client-side fallback if API returns empty
  useEffect(() => {
    const buildFallback = async () => {
      try {
        if (!analytics?.data || analytics?.data?.entries?.length) return;
        const entriesResp = await apiClient.getCollectionEntries("all");
        const entries = entriesResp?.data?.entries || entriesResp?.entries || [];
        if (!entries.length) return;
        // Group by date
        const byDate = {};
        entries.forEach((e) => {
          const d = new Date(e.createdAt);
          const key = d.toISOString().slice(0, 10);
          if (!byDate[key]) byDate[key] = { total: 0, count: 0 };
          byDate[key].total += e.moodScore || 0;
          byDate[key].count += 1;
        });
        // Timeline last 30 days
        const today = new Date();
        const days = 30;
        const timeline = [];
        for (let i = days - 1; i >= 0; i--) {
          const d = new Date(today);
          d.setDate(today.getDate() - i);
          const key = d.toISOString().slice(0, 10);
          const row = byDate[key];
          timeline.push({
            date: key,
            averageScore: row ? +(row.total / row.count).toFixed(1) : 0,
            entryCount: row ? row.count : 0,
          });
        }
        // Stats
        const totalEntries = entries.length;
        const avg = entries.reduce((s, e) => s + (e.moodScore || 0), 0) / totalEntries;
        const moodCounts = {};
        entries.forEach((e) => {
          if (e.mood) moodCounts[e.mood] = (moodCounts[e.mood] || 0) + 1;
        });
        const mostFrequentMood = Object.entries(moodCounts).sort((a, b) => b[1] - a[1])[0]?.[0] || null;
        const dailyAverage = +(totalEntries / 30).toFixed(1);

        // Streaks and heatmap
        const dateCounts = {};
        Object.keys(byDate).forEach((k) => (dateCounts[k] = byDate[k].count));
        const computeStreaks = () => {
          const today = new Date();
          let longest = 0, current = 0, running = 0;
          for (let i = 0; i <= 365; i++) {
            const d = new Date(today);
            d.setDate(today.getDate() - i);
            const key = d.toISOString().slice(0, 10);
            if (dateCounts[key] > 0) running++; else { if (i === 0) current = 0; else if (current === 0) current = running; longest = Math.max(longest, running); running = 0; }
          }
          longest = Math.max(longest, running);
          if (current === 0) current = running;
          return { current, longest };
        };
        const streak = computeStreaks();
        const heatmap = [];
        const weeks = 52;
        for (let i = 0; i < 7 * weeks; i++) {
          const d = new Date();
          d.setDate(d.getDate() - (7 * weeks - 1 - i));
          const key = d.toISOString().slice(0, 10);
          heatmap.push({ date: key, count: dateCounts[key] || 0 });
        }
        setFallback({
          timeline,
          stats: { totalEntries, averageScore: +avg.toFixed(1), mostFrequentMood, dailyAverage },
          streak: { ...streak, heatmap },
          entries,
        });
      } catch (e) {
        // ignore
      }
    };
    buildFallback();
  }, [analytics]);

  if (loading || !isLoaded || (!analytics?.data && !fallback)) {
    return <MoodAnalyticsSkeleton />;
  }

  if (!analytics) return null;

  const data = analytics?.data || fallback;
  const { timeline, stats, streak } = data;

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload?.length) {
      return (
        <div className="bg-white p-4 border rounded-lg shadow-lg">
          <p className="font-medium">
            {format(parseISO(label), "MMM d, yyyy")}
          </p>
          <p className="text-orange-600">Average Mood: {payload[0].value}</p>
          <p className="text-blue-600">Entries: {payload[1].value}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <>
      <div className="flex justify-between items-center">
        <h2 className="text-5xl font-bold gradient-title">Dashboard</h2>

        <Select value={period} onValueChange={setPeriod}>
          <SelectTrigger className="w-[140px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {timeOptions.map((option) => (
              <SelectItem key={option.value} value={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {(!analytics?.data && !fallback) || (analytics?.data && analytics.data.entries.length === 0 && !fallback) ? (
        <div>
          No Entries Found.{" "}
          <Link href="/journal/write" className="underline text-orange-400">
            Write New
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Streak + Stats Cards */}
          <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
            <Card className="col-span-1">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Journal Streak</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold flex items-end gap-2">
                  <span>{streak?.current || 0} days</span>
                  <span className="text-sm text-muted-foreground">current</span>
                </div>
                <p className="text-xs text-muted-foreground">Longest: {streak?.longest || 0} days</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Entries
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.totalEntries}</div>
                <p className="text-xs text-muted-foreground">
                  ~{stats.dailyAverage} entries per day
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">
                  Average Mood
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.averageScore}/10
                </div>
                <p className="text-xs text-muted-foreground">
                  Overall mood score
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">
                  Mood Summary
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold flex items-center gap-2">
                  {getMoodById(stats.mostFrequentMood)?.emoji}{" "}
                  {getMoodTrend(stats.averageScore)}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* GitHub-like streak heatmap */}
          {streak?.heatmap && (
            <Card>
              <CardHeader>
                <CardTitle>Streak Heatmap</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-53 gap-1" style={{gridTemplateColumns: "repeat(53, minmax(0, 1fr))"}}>
                  {streak.heatmap.map((d, idx) => {
                    const c = d.count || 0;
                    const level = c >= 4 ? 4 : c; // 0-4
                    const colors = [
                      "bg-gray-200",
                      "bg-[hsl(var(--brand-100))]",
                      "bg-[hsl(var(--brand-200))]",
                      "bg-[hsl(var(--brand-300))]",
                      "bg-[hsl(var(--brand-400))]",
                    ];
                    return (
                      <div key={idx} className={`w-3 h-3 rounded-sm ${colors[level]}`} title={`${d.date}: ${c} entries`} />
                    );
                  })}
                </div>
                <p className="text-xs text-muted-foreground mt-2">Last 52 weeks</p>
              </CardContent>
            </Card>
          )}

          {/* Mood Timeline Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Mood Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={timeline}
                    margin={{
                      top: 5,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="date"
                      tickFormatter={(date) => format(parseISO(date), "MMM d")}
                    />
                    <YAxis yAxisId="left" domain={[0, 10]} />
                    <YAxis
                      yAxisId="right"
                      orientation="right"
                      domain={[0, "auto"]}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Line
                      yAxisId="left"
                      type="monotone"
                      dataKey="averageScore"
                      stroke="#f97316"
                      name="Average Mood"
                      strokeWidth={2}
                    />
                    <Line
                      yAxisId="right"
                      type="monotone"
                      dataKey="entryCount"
                      stroke="#3b82f6"
                      name="Number of Entries"
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </>
  );
};

export default MoodAnalytics;
