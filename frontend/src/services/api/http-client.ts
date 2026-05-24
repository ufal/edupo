export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? ''

type QueryValue = string | number | boolean | null | undefined
type QueryParams = Record<string, QueryValue>

function buildUrl(endpoint: string, params?: QueryParams): string {
  const normalizedBaseUrl = API_BASE_URL.endsWith('/')
    ? API_BASE_URL
    : `${API_BASE_URL}/`

  const normalizedEndpoint = endpoint.startsWith('/')
    ? endpoint.slice(1)
    : endpoint

  const url = new URL(normalizedEndpoint, normalizedBaseUrl)

  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value === undefined || value === null) continue
      url.searchParams.set(key, String(value))
    }
  }

  return url.toString()
}

async function handleResponse(res: Response, endpoint: string): Promise<Response> {
  if (!res.ok) {
    throw new Error(`Edupo API error on "${endpoint}": ${res.status}`)
  }

  return res
}

export async function apiGetJson<T>(
  endpoint: string,
  params?: QueryParams,
): Promise<T> {
  const res = await fetch(buildUrl(endpoint, params), {
    method: 'GET',
  })

  await handleResponse(res, endpoint)

  return res.json() as Promise<T>
}

export async function apiGetText(
  endpoint: string,
  params?: QueryParams,
): Promise<string> {
  const res = await fetch(buildUrl(endpoint, params), {
    method: 'GET',
  })

  await handleResponse(res, endpoint)

  return res.text()
}