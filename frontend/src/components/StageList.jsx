import StageRow from './StageRow'

function StageList({ stages }) {
  return (
    <div className="overflow-x-auto max-w-3xl mt-6">
      <table className="w-full text-sm text-left border-collapse">
        <thead>
          <tr className="border-b bg-gray-50 font-medium text-gray-700">
            <th className="px-3 py-2 w-8">#</th>
            <th className="px-3 py-2">Type</th>
            <th className="px-3 py-2">Route</th>
            <th className="px-3 py-2">Distance</th>
            <th className="px-3 py-2">Transfer</th>
          </tr>
        </thead>
        <tbody>
          {stages.map((stage) => (
            <StageRow key={stage.stage_number} stage={stage} />
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default StageList