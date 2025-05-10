export interface AnalysisResponse {
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