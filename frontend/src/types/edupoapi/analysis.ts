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