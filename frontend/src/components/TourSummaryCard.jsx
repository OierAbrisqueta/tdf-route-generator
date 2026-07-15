function TourSummaryCard({ summary }) {
  const {
    total_stages,
    total_distance_km,
    countries_visited,
    stages_by_type,
    score,
  } = summary

  return (
    <div className="border rounded-lg p-6 bg-white shadow-sm max-w-md mt-6">
      <h2 className="text-lg font-semibold mb-4">Tour Summary</h2>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-sm text-gray-500">Total stages</p>
          <p className="text-xl font-medium">{total_stages}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Total distance</p>
          <p className="text-xl font-medium">{total_distance_km.toFixed(1)} km</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Countries</p>
          <p className="text-xl font-medium">{countries_visited.join(', ')}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Score</p>
          <p className="text-xl font-medium">{score}</p>
        </div>
      </div>

      <div className="border-t pt-4">
        <p className="text-sm text-gray-500 mb-2">Stage breakdown</p>
        <ul className="text-sm space-y-1">
          {Object.entries(stages_by_type).map(([type, count]) => (
            <li key={type} className="flex justify-between">
              <span className="capitalize">{type}</span>
              <span className="font-medium">{count}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default TourSummaryCard