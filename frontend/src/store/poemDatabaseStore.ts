import { fetchAuthorsListApi, fetchPoemsListApi } from "@/lib/edupoApi";
import { Poem } from "@/types/edupoapi";
import { create } from "zustand";

export type AuthorName = string;

type PoemDatabaseStore = {
  authors: AuthorName[];
  poemsByAuthor: Record<AuthorName, Poem[]>;

  loadingAuthors: boolean;
  loadingPoems: Record<AuthorName, boolean>;
  error: string | null;

  fetchAuthors: () => Promise<void>;
  fetchPoemsForAuthor: (authorName: AuthorName) => Promise<void>;
};

export const usePoemDatabase = create<PoemDatabaseStore>((set, get) => ({
  authors: [],
  poemsByAuthor: {},

  loadingAuthors: false,
  loadingPoems: {},
  error: null,

  fetchAuthors: async () => {
    try {
      console.log("Fetching author list...");
      
      set({ loadingAuthors: true, error: null });

      const res = await fetchAuthorsListApi();
      const data: AuthorName[] = res.map(r => r.author);
      
      set({ authors: data, loadingAuthors: false });

    } catch (err: any) {

      console.error(err);
      set({ loadingAuthors: false, error: err.message || "Unknown error" });
    }
  },

  fetchPoemsForAuthor: async (authorName: AuthorName) => {
    const { poemsByAuthor, loadingPoems } = get();

    if (poemsByAuthor[authorName]) return;

    try {
      set({
        loadingPoems: {
          ...loadingPoems,
          [authorName]: true
        },
        error: null
      });

      const res = await fetchPoemsListApi(authorName);

      set({
        poemsByAuthor: {
          ...get().poemsByAuthor,
          [authorName]: res
        },
        loadingPoems: {
          ...get().loadingPoems,
          [authorName]: false
        },
      });
    } catch (err: any) {
      console.error(err);
      set({
        loadingPoems: {
          ...get().loadingPoems,
          [authorName]: false
        },
        error: err.message || "Unknown error"
      });
    }
  },
}));
