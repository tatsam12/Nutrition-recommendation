import { useState, useEffect } from 'react'
import api from '../../services/api.js'
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend,
} from 'recharts'

export default function Summary() {
  const now = new Date()
  const [year,    setYear]    = useState(now.getFullYear())
  const [month,   setMonth]   = useState(now.getMonth() + 1)
  const [weekly,  setWeekly]  = useState([])
  const [monthly, setMonthly] = useState([])
  const [macros,  setMacros]  = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      const [wRes, mRes, macRes] = await Promise.allSettled([
        api.get('/analytics/weekly-trend'),
        api.get(`/analytics/monthly?year=${year}&month=${month}`),
        api.get('/analytics/macros'),
      ])
      if (wRes.status   === 'fulfilled') setWeekly(wRes.value.data)
      if (mRes.status   === 'fulfilled') setMonthly(mRes.value.data)
      if (macRes.status === 'fulfilled') setMacros(macRes.value.data)
      setLoading(false)
    }
    load()
  }, [year, month])

  const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Nutrition Summary</h1>
        <p className="text-sm text-gray-500">Review your nutrition trends</p>
      </div>

      {/* Weekly summary */}
      <div className="card">
        <h3 className="font-semibold text-gray-900 mb-4">Weekly Nutrition Overview</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={weekly} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#94a3b8' }} />
            <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} />
            <Tooltip />
            <Legend wrapperStyle={{ fontSize: 11 }} />
            <Bar dataKey="calories" fill="#22c55e" name="Calories" radius={[4,4,0,0]} />
            <Bar dataKey="protein"  fill="#3b82f6" name="Protein"  radius={[4,4,0,0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Monthly trend */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900">Monthly Calorie Trend</h3>
          <div className="flex gap-2">
            <select value={month} onChange={e => setMonth(+e.target.value)} className="input-field w-24 text-xs py-1">
              {MONTHS.map((m, i) => <option key={i} value={i+1}>{m}</option>)}
            </select>
            <select value={year} onChange={e => setYear(+e.target.value)} className="input-field w-20 text-xs py-1">
              {[2024,2025,2026].map(y => <option key={y} value={y}>{y}</option>)}
            </select>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={monthly} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="date" tickFormatter={d => d.slice(8)} tick={{ fontSize: 10 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip labelFormatter={d => `Date: ${d}`} formatter={v => [`${Math.round(v)} kcal`]} />
            <Line type="monotone" dataKey="calories" stroke="#22c55e" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Macro stats */}
      {macros && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {[
            { label: 'Protein',   value: macros.protein,       unit: 'g', color: 'bg-blue-100 text-blue-600' },
            { label: 'Carbs',     value: macros.carbohydrates, unit: 'g', color: 'bg-yellow-100 text-yellow-600' },
            { label: 'Fat',       value: macros.fat,           unit: 'g', color: 'bg-red-100 text-red-500' },
            { label: 'Fiber',     value: macros.fiber,         unit: 'g', color: 'bg-green-100 text-green-600' },
          ].map(({ label, value, unit, color }) => (
            <div key={label} className="card text-center">
              <div className={`inline-flex items-center justify-center w-10 h-10 rounded-full mb-2 ${color} mx-auto font-bold text-sm`}>
                {label[0]}
              </div>
              <p className="text-xl font-bold text-gray-900">{Math.round(value || 0)}{unit}</p>
              <p className="text-xs text-gray-500">{label} today</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
