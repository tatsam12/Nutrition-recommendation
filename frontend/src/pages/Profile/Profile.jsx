import { useState, useEffect } from 'react'
import api from '../../services/api.js'
import toast from 'react-hot-toast'

const ACTIVITY_OPTIONS = [
  { value: 'sedentary',         label: 'Sedentary (little or no exercise)' },
  { value: 'lightly_active',    label: 'Lightly Active (1-3 days/week)' },
  { value: 'moderately_active', label: 'Moderately Active (3-5 days/week)' },
  { value: 'very_active',       label: 'Very Active (6-7 days/week)' },
]

const GOAL_OPTIONS = [
  { value: 'weight_loss',  label: 'Weight Loss' },
  { value: 'weight_gain',  label: 'Weight Gain' },
  { value: 'muscle_gain',  label: 'Muscle Gain' },
  { value: 'maintenance',  label: 'Maintenance' },
]

const BMI_COLOR = (bmi) => {
  if (bmi < 18.5) return 'text-blue-500'
  if (bmi < 25)   return 'text-green-500'
  if (bmi < 30)   return 'text-yellow-500'
  return 'text-red-500'
}

export default function Profile() {
  const [profile,  setProfile]  = useState(null)
  const [form,     setForm]     = useState(null)
  const [editing,  setEditing]  = useState(false)
  const [loading,  setLoading]  = useState(false)
  const [fetching, setFetching] = useState(true)

  useEffect(() => {
  api.get('/profile')
    .then(r => { 
      setProfile(r.data); 
      setForm(r.data); 
    })
    .catch(() => {
      setEditing(true);
      setForm({}); // 🧠 FIX: Give 'form' an object so the form fields can safely render!
    })
    .finally(() => setFetching(false))
}, [])

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const payload = {
        age:               parseInt(form.age),
        gender:            form.gender,
        height_cm:         parseFloat(form.height_cm),
        weight_kg:         parseFloat(form.weight_kg),
        activity_level:    form.activity_level,
        nutrition_goal:    form.nutrition_goal,
        daily_calorie_goal: form.daily_calorie_goal ? parseInt(form.daily_calorie_goal) : undefined,
      }
      const res = profile
        ? await api.put('/profile', payload)
        : await api.post('/profile', payload)
      setProfile(res.data)
      setForm(res.data)
      setEditing(false)
      toast.success(profile ? 'Profile updated successfully' : 'Profile created successfully')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save profile')
    } finally {
      setLoading(false)
    }
  }

  if (fetching) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-900">My Profile</h1>
          <p className="text-sm text-gray-500">Manage your health information</p>
        </div>
        {profile && !editing && (
          <button onClick={() => setEditing(true)} className="btn-secondary text-sm">
            Edit Profile
          </button>
        )}
      </div>

      {/* BMI display card */}
      {profile && !editing && (
        <div className="card flex gap-6 flex-wrap">
          {[
            { label: 'Age',    value: `${profile.age} years` },
            { label: 'Height', value: `${profile.height_cm} cm` },
            { label: 'Weight', value: `${profile.weight_kg} kg` },
            { label: 'BMI',    value: profile.bmi?.toFixed(1), extra: profile.bmi_category },
            { label: 'Goal',   value: profile.nutrition_goal?.replace('_', ' ') },
            { label: 'Activity', value: profile.activity_level?.replace('_', ' ') },
            { label: 'Calorie Goal', value: `${profile.daily_calorie_goal} kcal` },
          ].map(({ label, value, extra }) => (
            <div key={label} className="min-w-[120px]">
              <p className="text-xs text-gray-400">{label}</p>
              <p className={`font-semibold capitalize ${label === 'BMI' ? BMI_COLOR(profile.bmi) : 'text-gray-800'}`}>
                {value}
              </p>
              {extra && <p className="text-xs text-gray-400">{extra}</p>}
            </div>
          ))}
        </div>
      )}

      {/* Edit form */}
      {(editing || !profile) && form && (
        <div className="card">
          <h2 className="font-semibold text-gray-900 mb-5">
            {profile ? 'Edit Profile' : 'Complete Your Profile'}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Age</label>
                <input type="number" required value={form.age || ''} onChange={set('age')}
                  min="1" max="120" className="input-field" />
              </div>
              <div>
                <label className="label">Gender</label>
                <select required value={form.gender || ''} onChange={set('gender')} className="input-field">
                  <option value="">Select gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label className="label">Height (cm)</label>
                <input type="number" required value={form.height_cm || ''} onChange={set('height_cm')}
                  min="50" max="300" step="0.1" className="input-field" />
              </div>
              <div>
                <label className="label">Weight (kg)</label>
                <input type="number" required value={form.weight_kg || ''} onChange={set('weight_kg')}
                  min="10" max="500" step="0.1" className="input-field" />
              </div>
            </div>

            <div>
              <label className="label">Activity Level</label>
              <select required value={form.activity_level || ''} onChange={set('activity_level')} className="input-field">
                <option value="">Select activity level</option>
                {ACTIVITY_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
              </select>
            </div>

            <div>
              <label className="label">Nutrition Goal</label>
              <div className="grid grid-cols-2 gap-2">
                {GOAL_OPTIONS.map(o => (
                  <label key={o.value} className={`
                    flex items-center gap-2 p-3 rounded-lg border cursor-pointer transition-colors
                    ${form.nutrition_goal === o.value
                      ? 'border-primary-500 bg-primary-50 text-primary-700'
                      : 'border-gray-200 hover:border-gray-300'}
                  `}>
                    <input type="radio" name="goal" value={o.value}
                      checked={form.nutrition_goal === o.value} onChange={set('nutrition_goal')}
                      className="sr-only" />
                    <span className="text-sm font-medium">{o.label}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="label">Daily Calorie Goal (leave blank to auto-calculate)</label>
              <input type="number" value={form.daily_calorie_goal || ''} onChange={set('daily_calorie_goal')}
                min="1000" max="5000" className="input-field" placeholder="Auto-calculate" />
            </div>

            <div className="flex gap-3 pt-2">
              <button type="submit" disabled={loading} className="btn-primary flex-1">
                {loading ? 'Saving...' : 'Save Profile'}
              </button>
              {profile && (
                <button type="button" onClick={() => { setEditing(false); setForm(profile) }}
                  className="btn-secondary flex-1">
                  Cancel
                </button>
              )}
            </div>
          </form>
        </div>
      )}
    </div>
  )
}
