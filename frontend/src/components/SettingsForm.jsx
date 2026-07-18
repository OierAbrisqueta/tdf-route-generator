import { useState } from 'react'

const DEFAULTS = {
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
  const [settings, setSettings] = useState(DEFAULTS)

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

  const inputClass = "w-full border-[3px] border-tdf-text bg-tdf-bg px-3 py-2 font-mono text-sm focus:outline-none focus:ring-0 focus:border-tdf-text focus:bg-tdf-yellow/20 rounded-none transition-none shadow-none"
  const labelClass = "block text-sm font-bold uppercase tracking-wider mb-2 text-tdf-text"

  return (
    <form onSubmit={handleSubmit} className="border-[3px] border-tdf-text bg-white p-6 space-y-8 rounded-none shadow-[4px_4px_0_0_#1A1A1A]">
      <div className="border-b-[3px] border-tdf-text pb-4">
        <h2 className="font-heading text-4xl tracking-widest leading-none m-0">PARAMETERS</h2>
      </div>

      <div className="space-y-6">
        <div>
          <label className={labelClass}>Total Stages</label>
          <input
            type="number"
            min={7}
            max={21}
            value={settings.stages}
            onChange={(e) => updateField('stages', Number(e.target.value))}
            className={inputClass}
          />
        </div>

        <div className="flex items-center gap-3 py-1">
          <input
            type="checkbox"
            id="foreign_start"
            checked={settings.foreign_start}
            onChange={(e) => updateField('foreign_start', e.target.checked)}
            className="w-6 h-6 border-[3px] border-tdf-text rounded-none checked:bg-tdf-yellow checked:border-tdf-text appearance-none cursor-pointer relative checked:after:content-['✓'] checked:after:absolute checked:after:text-tdf-text checked:after:font-bold checked:after:text-xl checked:after:left-0.5 checked:after:-top-1.5 focus:outline-none"
          />
          <label htmlFor="foreign_start" className="font-bold uppercase tracking-wider text-sm cursor-pointer select-none">Start abroad</label>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className={labelClass}>Min foreign</label>
            <input
              type="number"
              min={1}
              max={5}
              value={settings.foreign_stages_min}
              onChange={(e) => updateField('foreign_stages_min', Number(e.target.value))}
              className={inputClass}
            />
          </div>
          <div>
            <label className={labelClass}>Max foreign</label>
            <input
              type="number"
              min={1}
              max={5}
              value={settings.foreign_stages_max}
              onChange={(e) => updateField('foreign_stages_max', Number(e.target.value))}
              className={inputClass}
            />
          </div>
        </div>

        <div>
          <label className={labelClass}>Individual TTs</label>
          <input
            type="number"
            min={0}
            max={2}
            value={settings.itt_count}
            onChange={(e) => updateField('itt_count', Number(e.target.value))}
            className={inputClass}
          />
        </div>

        <div className="flex items-center gap-3 py-1">
          <input
            type="checkbox"
            id="ttt_enabled"
            checked={settings.ttt_enabled}
            onChange={(e) => updateField('ttt_enabled', e.target.checked)}
            className="w-6 h-6 border-[3px] border-tdf-text rounded-none checked:bg-tdf-yellow checked:border-tdf-text appearance-none cursor-pointer relative checked:after:content-['✓'] checked:after:absolute checked:after:text-tdf-text checked:after:font-bold checked:after:text-xl checked:after:left-0.5 checked:after:-top-1.5 focus:outline-none"
          />
          <label htmlFor="ttt_enabled" className="font-bold uppercase tracking-wider text-sm cursor-pointer select-none">Team TT</label>
        </div>

        <div>
          <div className="flex justify-between items-baseline mb-2">
            <label className={labelClass} style={{marginBottom: 0}}>Mountain bias</label>
            <span className="font-mono font-bold text-lg">{settings.mountain_bias}</span>
          </div>
          <input
            type="range"
            min={0}
            max={1}
            step={0.1}
            value={settings.mountain_bias}
            onChange={(e) => updateField('mountain_bias', Number(e.target.value))}
            className="w-full h-2 bg-tdf-text appearance-none cursor-pointer accent-tdf-yellow focus:outline-none"
          />
          <div className="flex justify-between text-[10px] font-bold text-tdf-text/60 mt-2 uppercase tracking-widest">
            <span>Flat</span>
            <span>Mountains</span>
          </div>
        </div>

        <div>
          <label className={labelClass}>Seed (opt)</label>
          <input
            type="number"
            value={settings.seed}
            onChange={(e) => updateField('seed', e.target.value)}
            placeholder="Random"
            className={inputClass}
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full font-heading text-3xl tracking-widest bg-tdf-yellow text-tdf-text border-[3px] border-tdf-text py-4 rounded-none hover:bg-tdf-text hover:text-tdf-yellow transition-colors disabled:opacity-50 disabled:pointer-events-none active:translate-y-0.5 shadow-none"
      >
        {loading ? 'GENERATING...' : 'GENERATE ROUTE'}
      </button>
    </form>
  )
}

export default SettingsForm