import StageRow from './StageRow'

function StageList({ stages }) {
  return (
    <div className="border-t-[3px] border-tdf-text pt-8 mt-8">
      <div className="flex items-end justify-between mb-6">
        <h2 className="font-heading text-5xl tracking-widest m-0 leading-none">STAGES</h2>
        <span className="tabular-data font-bold text-xl">{stages.length} TOTAL</span>
      </div>
      
      <div className="border-[3px] border-tdf-text bg-white shadow-[4px_4px_0_0_#1A1A1A]">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b-[3px] border-tdf-text bg-tdf-bg">
                <th className="px-4 py-3 font-bold uppercase tracking-widest text-tdf-text/60 text-xs w-20 text-center">Bib</th>
                <th className="px-4 py-3 font-bold uppercase tracking-widest text-tdf-text/60 text-xs">Profile</th>
                <th className="px-4 py-3 font-bold uppercase tracking-widest text-tdf-text/60 text-xs">Route</th>
                <th className="px-4 py-3 font-bold uppercase tracking-widest text-tdf-text/60 text-xs text-right">Dist</th>
                <th className="px-4 py-3 font-bold uppercase tracking-widest text-tdf-text/60 text-xs text-right hidden sm:table-cell">Transfer</th>
              </tr>
            </thead>
            <tbody className="divide-y-[3px] divide-tdf-text/10">
              {stages.map((stage) => (
                <StageRow key={stage.stage_number} stage={stage} />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default StageList