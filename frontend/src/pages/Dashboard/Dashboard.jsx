import { useState, useEffect } from 'react'
import api from '../../services/api.js'
import StatCard from '../../components/DashboardCards/StatCard.jsx'
import CalorieProgressCard from '../../components/DashboardCards/CalorieProgressCard.jsx'
import WeeklyTrendChart from '../../components/ChartWidgets/WeeklyTrendChart.jsx'
import MacroChart from '../../components/ChartWidgets/MacroChart.jsx'
import CategoryChart from '../../components/ChartWidgets/CategoryChart.jsx'
import RecentFoodsList from '../../components/DashboardCards/RecentFoodsList.jsx'
import { MdMonitorWeight, MdFitnessCenter, MdLocalFireDepartment, MdTrackChanges } from 'react-icons/md'

export default function Dashboard() {
  const [profile,    setProfile]    = useState(null)
  const [summary,    setSummary]    = useState(null)
  const [weekly,     setWeekly]     = useState([])
  const [macros,     setMacros]     = useState(null)
  const [categories, setCategories] = useState([])
  const [recentLogs, setRecentLogs] = useState([])
  const [loading,    setLoading]    = useState(true)

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      try {
        const [profRes, sumRes, weekRes, macRes, catRes, recRes] = await Promise.allSettled([
          api.get('/profile'),
          api.get('/food-logs/summary/daily'),
          api.get('/analytics/weekly-trend'),
          api.get('/analytics/macros'),
          api.get('/analytics/category-distribution'),
          api.get('/analytics/recent-logs'),
        ])
        if (profRes.status === 'fulfilled') setProfile(profRes.value.data)
        if (sumRes.status  === 'fulfilled') setSummary(sumRes.value.data)
        if (weekRes.status === 'fulfilled') setWeekly(weekRes.value.data)
        if (macRes.status  === 'fulfilled') setMacros(macRes.value.data)
        if (catRes.status  === 'fulfilled') setCategories(catRes.value.data)
        if (recRes.status  === 'fulfilled') setRecentLogs(recRes.value.data)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  const bmi = profile?.bmi ?? 0
  const calPercent = summary ? Math.min(Math.round((summary.total_calories / summary.calorie_goal) * 100), 100) : 0

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-sm text-gray-500 mt-0.5">Track your nutrition and progress</p>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Current Weight"
          value={profile ? `${profile.weight_kg} kg` : '—'}
          icon={<MdMonitorWeight size={22} className="text-blue-500" />}
          bg="bg-blue-50"
        />
        <StatCard
          title="BMI"
          value={bmi ? bmi.toFixed(1) : '—'}
          subtitle={profile?.bmi_category}
          icon={<MdFitnessCenter size={22} className="text-purple-500" />}
          bg="bg-purple-50"
        />
        <StatCard
          title="Calories Today"
          value={summary ? Math.round(summary.total_calories) : 0}
          subtitle={summary ? `Goal: ${summary.calorie_goal} kcal` : ''}
          icon={<MdLocalFireDepartment size={22} className="text-orange-500" />}
          bg="bg-orange-50"
        />
        <StatCard
          title="Goal Progress"
          value={`${calPercent}%`}
          subtitle={profile?.nutrition_goal?.replace('_', ' ')}
          icon={<MdTrackChanges size={22} className="text-primary-500" />}
          bg="bg-primary-50"
        />
      </div>

      {/* Calorie progress */}
      {summary && (
        <CalorieProgressCard summary={summary} />
      )}

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <WeeklyTrendChart data={weekly} />
        <MacroChart data={macros} />
      </div>

      {/* Category + Recent */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <CategoryChart data={categories} />
        <RecentFoodsList logs={recentLogs} />
      </div>
    </div>
  )
}
