import { AuthorsListResponse, PoemsListResponse, FetchPoemResponse, GenResponse, AnalysisResponse, MotivesResponse, ImageResponse, TTSResponse, AddLikeResponse } from "@/types/edupoApi";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL!;

export async function fetchAuthorsListApi(): Promise<AuthorsListResponse> {
    const MAX_AUTHORS = 20;

    const params = new URLSearchParams({ accept: "json" });
    const res = await fetch(`${API_BASE_URL}showlist?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`Authors API error ${res.status}`);
    }

    const data = await res.json();
    return Array.isArray(data) ? data.slice(0, MAX_AUTHORS) : [];
}

export async function fetchPoemsListApi(author: string): Promise<PoemsListResponse> {
    const MAX_POEMS = 20;

    const params = new URLSearchParams({ author, accept: "txt" });
    const res = await fetch(`${API_BASE_URL}showauthor?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`PoemList API error ${res.status}`);
    }

    const text = await res.text();
    const lines = text.split("\n");

    const poems: PoemsListResponse = [];

    for (const line of lines) {
        const colonIndex = line.indexOf(":");
        if (colonIndex > 0) {
            const idPart = line.slice(0, colonIndex).trim();
            const namePart = line.slice(colonIndex + 1).trim();

            const id = parseInt(idPart, 10);
            if (!isNaN(id) && namePart.length > 0) {
                poems.push({ id, title: namePart });
            }
        }

        if (poems.length >= MAX_POEMS) {
            break;
        }
    }

    return poems;
}

export async function fetchPoemApi(params: URLSearchParams): Promise<FetchPoemResponse> {
    const res = await fetch(`${API_BASE_URL}show?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`FetchPoem API error ${res.status}`);
    }
    
    return res.json();
}

export async function genPoemApi(params: URLSearchParams): Promise<GenResponse> {
    const res = await fetch(`${API_BASE_URL}gen?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`GenPoem API error ${res.status}`);
    }
    
    return res.json();
}

export async function fetchAnalysisApi(poemId: string): Promise<AnalysisResponse> {
    const params = new URLSearchParams({ poemid: poemId, accept: "json" });
    const res = await fetch(`${API_BASE_URL}analyze?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`Analysis API error ${res.status}`);
    }

    return res.json();
}

export async function fetchMotivesApi(poemId: string): Promise<MotivesResponse> {
    const params = new URLSearchParams({ poemid: poemId.toString(), accept: "json" });
    const res = await fetch(`${API_BASE_URL}genmotives?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`Motives API error ${res.status}`);
    }

    return res.json();
}

export async function fetchImageApi(poemId: string): Promise<ImageResponse> {
    const params = new URLSearchParams({ poemid: poemId, accept: "json" });
    const res = await fetch(`${API_BASE_URL}genimage?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`Generate image API error ${res.status}`);
    }

    return res.json();
}

export async function fetchTTSApi(poemId: string): Promise<TTSResponse> {
    const params = new URLSearchParams({ poemid: poemId, accept: "json" });
    const res = await fetch(`${API_BASE_URL}gentts?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`Generate TTS API error ${res.status}`);
    }

    return res.json();
}

export async function sendLikeApi(poemId: string): Promise<AddLikeResponse> {
    const params = new URLSearchParams({ poemid: poemId, accept: "json" });
    const res = await fetch(`${API_BASE_URL}add_like?${params.toString()}`);

    if (!res.ok) {
        throw new Error(`Add like API error ${res.status}`);
    }

    return res.json();
}