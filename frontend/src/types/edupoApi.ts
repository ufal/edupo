export interface Author {
    author: string;
    count: number;
}

export type AuthorsListResponse = Author[];

export interface Poem {
    id: number | null;
    title: string;
};

export type PoemsListResponse = Poem[];

export interface GenResponse {
    plaintext?: string;
    title?: string;
    author_name?: string;
    [key: string]: any;
};

export interface MetreDetail {
    clause: string;
    foot: number;
    full: string;
    metre: string;
    pattern: string;
}

export type MetreDetailCode = "A" | "D" | "J" | "T";

export interface AnalysisResponse {
    body: [
        {
            metre: {
                [key in MetreDetailCode]?: MetreDetail;
            }
        }
    ],
    measures: {
        metre_accuracy: number;
        metre_consistency: number;
        rhyme_scheme_accuracy: number;
        rhyming: number;
        rhyming_consistency: number;
        syllable_count_entropy: number;
        unknown_words: number;
    }
}

export interface MotivesResponse {
    motives: String[];
}

export interface ImageResponse {
    description: string;
    url: string;
}

export interface TTSResponse {
    url: string;
}

export type AddLikeResponse = number;

export interface LikeCountResponse {
    
}