import { useState } from 'react'
import { generateRoute } from './api'
import SettingsForm from "./components/SettingsForm.jsx";

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleGenerate = async (settings) => {
    setLoading(true)
    setError(null)
    try {
      const data = await generateRoute(settings)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8">
      <SettingsForm onGenerate={handleGenerate} loading={loading} />

      {error && <p className="text-red-600 mt-4">{error}</p>}

      {result && (
        <pre className="mt-4 text-sm bg-gray-100 p-4 rounded">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  )
}

export default App