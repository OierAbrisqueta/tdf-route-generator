function TourSummaryCard({ summary }) {
  const {
    total_stages,
    total_distance_km,
    countries_visited,
    stages_by_type,
  } = summary

  return (
    <div className="border-[3px] border-tdf-text bg-white rounded-none shadow-[4px_4px_0_0_#1A1A1A]">
      <div className="bg-tdf-text text-white p-4 border-b-[3px] border-tdf-text">
        <h2 className="font-heading text-4xl tracking-widest leading-none m-0 text-white">RACE STATS</h2>
      </div>
      
      <div className="p-6">
        <div className="grid grid-cols-2 gap-y-6 gap-x-4 mb-8">
          <div>
            <p className="text-xs font-bold uppercase tracking-widest text-tdf-text/60 mb-1">Total Stages</p>
            <p className="tabular-data text-4xl font-bold">{total_stages}</p>
          </div>
          <div>
            <p className="text-xs font-bold uppercase tracking-widest text-tdf-text/60 mb-1">Distance</p>
            <p className="tabular-data text-4xl font-bold">{total_distance_km.toFixed(1)} <span className="text-xl font-normal font-sans">km</span></p>
          </div>
          <div className="col-span-2">
            <p className="text-xs font-bold uppercase tracking-widest text-tdf-text/60 mb-1">Countries</p>
            <p className="font-bold text-lg uppercase tracking-wide">{countries_visited.join(', ')}</p>
          </div>
        </div>

        <div className="border-t-[3px] border-tdf-text pt-6">
          <p className="text-xs font-bold uppercase tracking-widest text-tdf-text/60 mb-4">Stage Breakdown</p>
          <ul className="space-y-3">
            {Object.entries(stages_by_type).map(([type, count]) => (
              <li key={type} className="flex justify-between items-baseline border-b-2 border-tdf-text/10 pb-1">
                <span className="uppercase font-bold tracking-widest text-sm">{type}</span>
                <span className="tabular-data font-bold text-xl">{count}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}

export default TourSummaryCard