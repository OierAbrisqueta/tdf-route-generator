export async function generateRoute(settings) {
  const res = await fetch('http://localhost:8000/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings),
  })
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}