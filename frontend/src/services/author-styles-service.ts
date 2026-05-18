import authorStylesJson from '@/data/author-styles.json'

export type AuthorStyle = {
  id: string
  label: string
  description?: string
  avatarSrc: string
}

const authorStyles = authorStylesJson as AuthorStyle[]

export function getAllAuthorStyles(): AuthorStyle[] {
  return authorStyles
}

export function getAuthorStyleById(id: string | null | undefined): AuthorStyle | null {
  if (!id) return null

  return authorStyles.find((author) => author.id === id) ?? null
}