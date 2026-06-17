import { useState, useEffect, useCallback } from 'react'
import api from '../../services/api.js'
import toast from 'react-hot-toast'
import { MdSearch, MdDelete, MdAdd } from 'react-icons/md'

const FALLBACK = 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=60&q=80'
const MEAL_TYPES = ['breakfast', 'lunch', 'dinner', 'snack']

export default function FoodLog() {
  const [logs,     setLogs]     = useState([])
  const [summary,  setSummary]  = useState(null)
  const [search,   setSearch]   = useState('')
  const [results,  setResults]  = useState([])
  const [selected, setSelected] = useState(null)
  const [qty,      setQty]      = useState(1)
  const [mealType, setMealType] = useState('lunch')
  const [loading,  setLoading]  = useState(false)
  const [searching,setSearching]= useState(false)

  const loadLogs = useCallback(async () => {
    const [logsRes, sumRes] = await Promise.allSettled([
      api.get('/food-logs/today'),
      api.get('/food-logs/summary/daily'),
    ])
    if (logsRes.status === 'fulfilled') setLogs(logsRes.value.data)
    if (sumRes.status  === 'fulfilled') setSummary(sumRes.value.data)
  }, [])

  useEffect(() => { loadLogs() }, [loadLogs])

  useEffect(() => {
    if (!search.trim()) { setResults([]); return }
    const t = setTimeout(async () => {
      setSearching(true)
      try {
        const { data } = await api.get(`/foods/search?q=${encodeURIComponent(search)}`)
        setResults(data)
      } finally {
        setSearching(false)
      }
    }, 400)
    return () => clearTimeout(t)
  }, [search])

  const handleLog = async () => {
    if (!selected) return
    setLoading(true)
    try {
      await api.post('/food-logs', { food_id: selected.id, quantity: parseFloat(qty), meal_type: mealType })
      toast.success('Food added successfully')
      setSelected(null)
      setSearch('')
      setResults([])
      setQty(1)
      await loadLogs()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to add food')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    try {
      await api.delete(`/food-logs/${id}`)
      toast.success('Food log deleted')
      await loadLogs()
    } catch {
      toast.error('Failed to delete')
    }
  }

  const mealGroups = MEAL_TYPES.reduce((acc, m) => {
    acc[m] = logs.filter(l => l.meal_type === m)
    return acc
  }, {})

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Food Log</h1>
        <p className="text-sm text-gray-500">Log your daily meals</p>
      </div>

      {/* Summary banner */}
      {summary && (
        <div className="card bg-primary-50 border border-primary-100">
          <div className="flex flex-wrap gap-6">
            {[
              { label: 'Calories',  value: `${Math.round(summary.total_calories)} kcal` },
              { label: 'Protein',   value: `${Math.round(summary.total_protein)}g` },
              { label: 'Carbs',     value: `${Math.round(summary.total_carbohydrates)}g` },
              { label: 'Fat',       value: `${Math.round(summary.total_fat)}g` },
              { label: 'Progress',  value: `${summary.progress_percentage}%` },
            ].map(({ label, value }) => (
              <div key={label}>
                <p className="text-xs text-primary-600">{label}</p>
                <p className="font-bold text-primary-800">{value}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Food search + add */}
      <div className="card space-y-4">
        <h3 className="font-semibold text-gray-900">Add Food</h3>

        <div className="relative">
          <MdSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="input-field pl-9"
            placeholder="Search Nepali foods (e.g., Dal Bhat, Momo)..."
          />
          {searching && (
            <span className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 border-2 border-primary-400 border-t-transparent rounded-full animate-spin" />
          )}
        </div>

        {/* Search results */}
        {results.length > 0 && !selected && (
          <div className="border border-gray-100 rounded-lg overflow-hidden max-h-64 overflow-y-auto">
            {results.map(food => (
              <button
                key={food.id}
                onClick={() => { setSelected(food); setSearch(food.food_name); setResults([]) }}
                className="w-full flex items-center gap-3 p-3 hover:bg-gray-50 transition-colors text-left"
              >
                <img
                  src={food.image_url || FALLBACK}
                  alt={food.food_name}
                  onError={e => { e.target.src = FALLBACK }}
                  className="w-10 h-10 rounded-lg object-cover flex-shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-800 truncate">{food.food_name}</p>
                  <p className="text-xs text-gray-400">{food.category}</p>
                </div>
                <span className="text-xs text-orange-500 flex-shrink-0">{food.calories} kcal</span>
              </button>
            ))}
          </div>
        )}

        {/* Selected food detail */}
        {selected && (
          <div className="border border-primary-200 rounded-lg p-4 bg-primary-50">
            <div className="flex items-center gap-4 mb-4">
              <img
                src={selected.image_url || FALLBACK}
                alt={selected.food_name}
                onError={e => { e.target.src = FALLBACK }}
                className="w-16 h-16 rounded-xl object-cover"
              />
              <div>
                <p className="font-semibold text-gray-900">{selected.food_name}</p>
                <p className="text-sm text-gray-500">{selected.category}</p>
                <div className="flex gap-3 mt-1 text-xs text-gray-600">
                  <span>🔥 {selected.calories} kcal</span>
                  <span>💪 {selected.protein}g protein</span>
                  <span>🌾 {selected.carbohydrates}g carbs</span>
                </div>
              </div>
              <button onClick={() => { setSelected(null); setSearch('') }}
                className="ml-auto text-gray-400 hover:text-gray-600 text-sm">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="label">Quantity (servings)</label>
                <input type="number" value={qty} onChange={e => setQty(e.target.value)}
                  min="0.1" max="20" step="0.1" className="input-field" />
              </div>
              <div>
                <label className="label">Meal Type</label>
                <select value={mealType} onChange={e => setMealType(e.target.value)} className="input-field">
                  {MEAL_TYPES.map(m => <option key={m} value={m} className="capitalize">{m}</option>)}
                </select>
              </div>
            </div>

            <button onClick={handleLog} disabled={loading} className="btn-primary w-full mt-3 flex items-center justify-center gap-2">
              <MdAdd size={18} />
              {loading ? 'Adding...' : 'Add to Log'}
            </button>
          </div>
        )}
      </div>

      {/* Today's logs by meal */}
      <div className="space-y-4">
        {MEAL_TYPES.map(meal => (
          <div key={meal} className="card">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold capitalize text-gray-900">{meal}</h3>
              <span className="text-xs text-gray-400">
                {mealGroups[meal].reduce((s, l) => s + l.calories, 0).toFixed(0)} kcal
              </span>
            </div>

            {mealGroups[meal].length === 0 ? (
              <p className="text-sm text-gray-400">No {meal} logged</p>
            ) : (
              <div className="space-y-3">
                {mealGroups[meal].map(log => (
                  <div key={log.id} className="flex items-center gap-3 group">
                    <img
                      src={log.food?.image_url || FALLBACK}
                      alt={log.food?.food_name}
                      onError={e => { e.target.src = FALLBACK }}
                      className="w-10 h-10 rounded-lg object-cover flex-shrink-0"
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-800 truncate">{log.food?.food_name}</p>
                      <p className="text-xs text-gray-400">
                        {log.quantity} serving · {Math.round(log.protein)}g protein · {Math.round(log.carbohydrates)}g carbs
                      </p>
                    </div>
                    <span className="text-sm font-semibold text-orange-500">{Math.round(log.calories)} kcal</span>
                    <button
                      onClick={() => handleDelete(log.id)}
                      className="opacity-0 group-hover:opacity-100 text-red-400 hover:text-red-600 transition-all p-1"
                    >
                      <MdDelete size={18} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
