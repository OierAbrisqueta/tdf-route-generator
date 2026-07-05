import { useState } from 'react'

const DEFAULT_SETTINGS = {
  stages: 21,
  foreign_start: true,
  foreign_stages_min: 3,
  foreign_stages_max: 5,
  itt_count: 1,
  ttt_enabled: false,
  mountain_bias: 0.5,
  seed: '',
}

function SettingsForm({ onGenerate, loading }) {
  const [settings, setSettings] = useState(DEFAULT_SETTINGS)

  const updateField = (field, value) => {
    setSettings((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const payload = {
      ...settings,
      seed: settings.seed === '' ? null : Number(settings.seed),
    }
    onGenerate(payload)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
      <div>
        <label className="block text-sm font-medium">Number of stages</label>
        <input
          type="number"
          min={7}
          max={21}
          value={settings.stages}
          onChange={(e) => updateField('stages', Number(e.target.value))}
          className="mt-1 border rounded px-2 py-1 w-full"
        />
      </div>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          id="foreign_start"
          checked={settings.foreign_start}
          onChange={(e) => updateField('foreign_start', e.target.checked)}
        />
        <label htmlFor="foreign_start" className="text-sm font-medium">Start abroad</label>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium">Min foreign stages</label>
          <input
            type="number"
            min={1}
            max={5}
            value={settings.foreign_stages_min}
            onChange={(e) => updateField('foreign_stages_min', Number(e.target.value))}
            className="mt-1 border rounded px-2 py-1 w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Max foreign stages</label>
          <input
            type="number"
            min={1}
            max={5}
            value={settings.foreign_stages_max}
            onChange={(e) => updateField('foreign_stages_max', Number(e.target.value))}
            className="mt-1 border rounded px-2 py-1 w-full"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium">Individual time trials</label>
        <input
          type="number"
          min={0}
          max={2}
          value={settings.itt_count}
          onChange={(e) => updateField('itt_count', Number(e.target.value))}
          className="mt-1 border rounded px-2 py-1 w-full"
        />
      </div>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          id="ttt_enabled"
          checked={settings.ttt_enabled}
          onChange={(e) => updateField('ttt_enabled', e.target.checked)}
        />
        <label htmlFor="ttt_enabled" className="text-sm font-medium">Include team time trial</label>
      </div>

      <div>
        <label className="block text-sm font-medium">
          Mountain bias: {settings.mountain_bias}
        </label>
        <input
          type="range"
          min={0}
          max={1}
          step={0.1}
          value={settings.mountain_bias}
          onChange={(e) => updateField('mountain_bias', Number(e.target.value))}
          className="mt-1 w-full"
        />
        <div className="flex justify-between text-xs text-gray-500">
          <span>Flatter</span>
          <span>More mountains</span>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium">Seed (optional)</label>
        <input
          type="number"
          value={settings.seed}
          onChange={(e) => updateField('seed', e.target.value)}
          placeholder="Leave empty for random"
          className="mt-1 border rounded px-2 py-1 w-full"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {loading ? 'Generating...' : 'Generate route'}
      </button>
    </form>
  )
}

export default SettingsForm