import { useState } from 'react'
import { generateRoute } from './api'
import SettingsForm from "./components/SettingsForm.jsx";
import TourSummaryCard from './components/TourSummaryCard';
import StageList from "./components/StageList.jsx";

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleGenerate = async (settings) => {
    setLoading(true)
    setError(null)
    try {
      const route = await generateRoute(settings)
      setResult(route)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8">
      <SettingsForm onGenerate={handleGenerate} loading={loading} />

      {error && (
        <p className="text-red-600 mt-4">{error}</p>
      )}

      {result && (
        <>
          <TourSummaryCard summary={result.summary} />
          <StageList stages={result.stages} />
        </>
      )}
    </div>
  )
}

export default App