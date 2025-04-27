export interface PoemGenResult {
  loading: boolean;
  error: string | null;
  authorName: string | null;
  poemLines: string[] | null;
}