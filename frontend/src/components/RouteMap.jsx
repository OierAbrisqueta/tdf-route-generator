import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const STAGE_COLOURS = {
  FLAT: '#43CC73',
  HILLY: '#F0A726',
  MOUNTAIN: '#D13030',
  ITT: '#2A6EDB',
  TTT: '#2A6EDB'
}

function getLocations(stages) {
  const locationsById = new Map()

  for (let i = 0; i < stages.length; i++) {
    const stage = stages[i]
    const { start_location, finish_location } = stage

    locationsById.set(start_location.id, start_location)
    locationsById.set(finish_location.id, finish_location)
  }

  return Array.from(locationsById.values())
}

function getMapCenter(locations) {
  if (!locations.length) {
    return null
  }

  const totalLat = locations.reduce((sum, location) => sum + location.lat, 0)
  const totalLon = locations.reduce((sum, location) => sum + location.lon, 0)

  return [totalLat / locations.length, totalLon / locations.length]
}

function RouteMap({ stages = [] }) {
  const locations = getLocations(stages)
  const center = getMapCenter(locations)

  if (!center) {
    return null;
  }

  return (
    <div className="border-[3px] border-tdf-text bg-white p-2 shadow-[4px_4px_0_0_#1A1A1A]">
      <div className="border border-tdf-text/20">
        <MapContainer
          center={center}
          zoom={6}
          style={{ height: '600px', width: '100%' }}
          className="z-0"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {stages.map((stage) => {
            const { stage_number, start_location, finish_location, stage_type } = stage

            return (
              <Polyline
                key={stage_number}
                positions={[
                  [start_location.lat, start_location.lon],
                  [finish_location.lat, finish_location.lon],
                ]}
                color={STAGE_COLOURS[stage_type]}
              />
            )
          })}

          {locations.map((loc) => (
            <Marker key={loc.id} position={[loc.lat, loc.lon]}>
              <Popup>
                <strong>{loc.name}</strong>
                <br />
                {loc.country}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  )
}

export default RouteMap
