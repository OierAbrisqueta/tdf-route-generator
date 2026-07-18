const TYPE_CONFIG = {
  FLAT: 'bg-stone-200 text-stone-700',
  HILLY: 'bg-orange-200/60 text-orange-800',
  MOUNTAIN: 'bg-red-200/60 text-red-800',
  ITT: 'bg-blue-200/60 text-blue-800',
  TTT: 'bg-purple-200/60 text-purple-800'
};

function StageRow({ stage }) {
  const {
    stage_number,
    stage_type,
    start_location,
    finish_location,
    distance_km,
    transfer_km,
    rest_day_after,
  } = stage

  const typeClass = TYPE_CONFIG[stage_type] || 'bg-stone-200 text-stone-700';

  return (
    <>
      <tr className="hover:bg-tdf-bg/50 transition-colors">
        <td className="px-4 py-4 text-center">
          {/* Signature Element: Race Bib */}
          <div className="inline-flex flex-col items-center justify-center border-2 border-tdf-text bg-tdf-yellow w-12 h-10 shadow-[2px_2px_0_0_#1A1A1A] transform -rotate-2">
            <span className="font-heading text-2xl leading-none pt-1">{stage_number}</span>
          </div>
        </td>
        <td className="px-4 py-4">
          <span className={`text-[10px] font-bold px-2 py-1 uppercase tracking-widest border border-tdf-text/20 rounded-none ${typeClass}`}>
            {stage_type}
          </span>
        </td>
        <td className="px-4 py-4 font-bold text-sm sm:text-base uppercase tracking-wide">
          <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2">
            <span>{start_location.name}</span>
            <span className="text-tdf-text/40 hidden sm:inline font-mono">--&gt;</span>
            <span className="text-tdf-text/40 sm:hidden font-mono">v</span>
            <span>{finish_location.name}</span>
          </div>
        </td>
        <td className="px-4 py-4 text-right tabular-data font-bold text-sm sm:text-base">
          {distance_km.toFixed(1)} <span className="text-xs font-sans font-normal text-tdf-text/60">km</span>
        </td>
        <td className="px-4 py-4 text-right tabular-data text-tdf-text/60 hidden sm:table-cell text-sm sm:text-base">
          {transfer_km > 0 ? (
            <span>
               +{transfer_km.toFixed(1)} <span className="text-xs font-sans">km</span>
            </span>
          ) : '-'}
        </td>
      </tr>
      {rest_day_after && (
        <tr>
          <td colSpan={5} className="bg-tdf-text text-white py-2 border-y-[3px] border-tdf-text">
             <div className="flex justify-center items-center gap-3 font-bold uppercase tracking-widest text-xs">
                <span className="w-2 h-2 bg-tdf-yellow"></span>
                Rest Day
                <span className="w-2 h-2 bg-tdf-yellow"></span>
             </div>
          </td>
        </tr>
      )}
    </>
  )
}

export default StageRow