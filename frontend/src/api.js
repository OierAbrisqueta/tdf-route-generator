export async function generateRoute(settings) {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const res = await fetch(`${apiUrl}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings),
  })
  if (!res.ok){
    const body = await res.json().catch(() => null)
    throw new Error(parseErrorMessage(res.status, body))
  }
  return res.json()
}

function parseErrorMessage(status, body) {
  if (!body || !body.detail) {
    return `Request failed: ${status}`
  }

  //The FastAPI 422 error
  if (Array.isArray(body.detail)) {
  return body.detail
    .map((err) => {
      const field = err.loc.at(-1);
      return `${field}: ${err.msg}`;
    })
    .join(', ');
}

  //Other FastAPI Errors
  return body.detail
}