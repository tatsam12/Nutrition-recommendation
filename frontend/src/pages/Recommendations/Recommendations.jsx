import { useState, useEffect } from 'react'
import api from '../../services/api.js'
import toast from 'react-hot-toast'
import { MdRefresh, MdStar } from 'react-icons/md'

const FALLBACK = 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=300&q=80'

export default function Recommendations() {
  const [data,    setData]    = useState(null)
  const [loading, setLoading] = useState(true)

  const load = async (force = false) => {
    setLoading(true)
    try {
      const { data: d } = await api.get(`/recommendations${force ? '?force=true' : ''}`)
      setData(d)
      if (force) toast.success('Recommendations updated')
    } catch (err) {
      if (err.response?.status === 400) {
        toast.error('Complete your profile first to get recommendations')
      } else {
        toast.error('Failed to load recommendations')
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const ScoreBadge = ({ score }) => {
    const pct = Math.round(score * 100)
    return (
      <div className="flex items-center gap-1">
        <MdStar className="text-yellow-400" size={14} />
        <span className="text-xs font-medium text-gray-600">{pct}% match</span>
      </div>
    )
  }

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-900">Recommendations</h1>
          <p className="text-sm text-gray-500">AI-powered food recommendations for your goals</p>
        </div>
        <button onClick={() => load(true)} className="btn-secondary flex items-center gap-2 text-sm">
          <MdRefresh size={16} /> Refresh
        </button>
      </div>

      {/* Nutrition advice */}
      {data?.nutrition_advice && (
        <div className="card bg-primary-50 border border-primary-100">
          <h3 className="font-semibold text-primary-800 mb-1">Personalized Advice</h3>
          <p className="text-sm text-primary-700">{data.nutrition_advice}</p>
        </div>
      )}

      {/* Meal plan */}
      {data?.meal_plan && Object.keys(data.meal_plan).length > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">Today's Suggested Meal Plan</h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {['breakfast','lunch','dinner','snack'].map(meal => {
              const item = data.meal_plan[meal]
              if (!item || typeof item !== 'object') return null
              return (
                <div key={meal} className="text-center">
                  <img
                    src={item.image_url || FALLBACK}
                    alt={item.name}
                    onError={e => { e.target.src = FALLBACK }}
                    className="w-full h-24 object-cover rounded-xl mb-2"
                  />
                  <p className="text-xs font-medium text-gray-500 capitalize">{meal}</p>
                  <p className="text-sm font-semibold text-gray-800 truncate">{item.name}</p>
                  <p className="text-xs text-orange-500">{Math.round(item.calories)} kcal</p>
                </div>
              )
            })}
          </div>
          {data.meal_plan.total_calories && (
            <p className="text-sm text-gray-500 text-right mt-3">
              Total: <span className="font-semibold text-gray-800">
                {Math.round(data.meal_plan.total_calories)} kcal
              </span>
            </p>
          )}
        </div>
      )}

      {/* Food recommendations grid */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-4">Recommended Foods</h3>
        {!data?.recommendations?.length ? (
          <div className="card text-center py-12">
            <p className="text-gray-400">Complete your profile to get recommendations</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.recommendations.map((rec, idx) => {
              const food = rec.food
              if (!food) return null
              return (
                <div key={rec.food_id || idx} className="card hover:shadow-card-hover transition-shadow">
                  <img
                    src={food.image_url || FALLBACK}
                    alt={food.food_name}
                    onError={e => { e.target.src = FALLBACK }}
                    className="w-full h-40 object-cover rounded-lg mb-3"
                  />
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <h4 className="font-semibold text-gray-900 text-sm">{food.food_name}</h4>
                    <ScoreBadge score={rec.score} />
                  </div>
                  <p className="text-xs text-gray-400 mb-3">{food.category}</p>
                  <div className="grid grid-cols-3 gap-1 text-center text-xs mb-3">
                    {[
                      { label: 'Calories', value: `${Math.round(food.calories)}`, unit: 'kcal' },
                      { label: 'Protein',  value: `${Math.round(food.protein)}`,  unit: 'g' },
                      { label: 'Carbs',    value: `${Math.round(food.carbohydrates)}`, unit: 'g' },
                    ].map(({ label, value, unit }) => (
                      <div key={label} className="bg-gray-50 rounded-lg p-1.5">
                        <p className="font-semibold text-gray-800">{value}<span className="font-normal text-gray-400">{unit}</span></p>
                        <p className="text-gray-400">{label}</p>
                      </div>
                    ))}
                  </div>
                  {rec.reason && (
                    <p className="text-xs text-primary-600 bg-primary-50 rounded-lg px-2 py-1.5">
                      {rec.reason}
                    </p>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
