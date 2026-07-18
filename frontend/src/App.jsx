import { useState } from 'react'
import { generateRoute } from './api'
import SettingsForm from "./components/SettingsForm.jsx";
import TourSummaryCard from './components/TourSummaryCard';
import StageList from "./components/StageList.jsx";
import RouteMap from "./components/RouteMap.jsx";

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
    <div className="min-h-screen flex flex-col bg-tdf-bg selection:bg-tdf-yellow selection:text-tdf-text">
      {/* Header - Sharp and Brutalist */}
      <header className="border-b-[3px] border-tdf-text bg-tdf-bg sticky top-0 z-50">
        <div className="w-full max-w-[1800px] mx-auto px-4 sm:px-6 lg:px-12 py-4 flex items-center justify-between">
          <h1 className="text-4xl sm:text-5xl font-heading text-tdf-text tracking-wider m-0 leading-none">
            TOUR ROUTE <span className="text-tdf-yellow bg-tdf-text px-2 pt-1 pb-0 inline-block">GENERATOR</span>
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 w-full max-w-[1800px] mx-auto px-4 sm:px-6 lg:px-12 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-[420px_1fr] gap-8 lg:gap-12 items-start">
          
          {/* Left Column */}
          <div className="space-y-8 lg:sticky lg:top-24">
            <SettingsForm onGenerate={handleGenerate} loading={loading} />
            
            {error && (
              <div className="border-[3px] border-tdf-text bg-white p-4">
                <p className="font-bold text-red-600 font-mono text-sm uppercase">Error</p>
                <p className="mt-1 font-medium">{error}</p>
              </div>
            )}

            {loading && (
              <div className="border-[3px] border-tdf-text bg-tdf-yellow p-8 text-center flex justify-center items-center h-32 shadow-[4px_4px_0_0_#1A1A1A]">
                <p className="font-heading text-4xl animate-pulse tracking-widest text-tdf-text m-0">CALCULATING...</p>
              </div>
            )}

            {!loading && result && (
              <TourSummaryCard summary={result.summary} />
            )}
          </div>

          {/* Right Column */}
          <div className="min-w-0">
            {!loading && result && (
              <div className="space-y-12 animate-in fade-in duration-500">
                <RouteMap stages={result.stages} />
                <StageList stages={result.stages} />
              </div>
            )}
            
            {!loading && !result && !error && (
              <div className="h-full min-h-[500px] flex items-center justify-center border-[3px] border-dashed border-tdf-text/20 p-8">
                <p className="font-heading text-4xl text-tdf-text/30 tracking-widest">AWAITING PARAMETERS</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App