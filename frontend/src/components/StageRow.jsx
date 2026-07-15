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

  return (
    <>
      <tr className="border-b hover:bg-gray-50">
        <td className="px-3 py-2 font-medium">{stage_number}</td>
        <td className="px-3 py-2">
          <span className="text-xs font-medium px-2 py-1 rounded bg-gray-100">
            {stage_type}
          </span>
        </td>
        <td className="px-3 py-2">
          {start_location.name} → {finish_location.name}
        </td>
        <td className="px-3 py-2">{distance_km.toFixed(1)} km</td>
        <td className="px-3 py-2 text-gray-500">
          {transfer_km > 0 ? `${transfer_km.toFixed(1)} km` : '—'}
        </td>
      </tr>
      {rest_day_after && (
        <tr className="bg-gray-50">
          <td colSpan={5} className="text-center text-xs text-gray-400 py-1">
            Rest day
          </td>
        </tr>
      )}
    </>
  )
}

export default StageRow