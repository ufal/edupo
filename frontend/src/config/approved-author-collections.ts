
import authorCollections from '@/data/author-collections.json'

const approvedCollectionIds = new Set([
  // Karel Hynek Mácha
  'Máj (in Básně a dramatické zlomky, in Spisy Karla Hynka Máchy, svazek 1)',

  // Karel Jaromír Erben
  'Kytice z básní',

  // Jan Neruda
  'Balady a romance',
  'Písně kosmické',

  // Vítězslav Hálek
  'Večerní písně',

  // Otokar Březina
  'Tajemné dálky',
  'Větry od pólů',

  // Jiří Karásek ze Lvovic
  'Sodoma (in Spisy Jiřího Karáska ze Lvovic, svazek 5)',

  // Karel Hlaváček
  'Mstivá kantiléna',
  'Pozdě k ránu',

  // František Gellner
  'Po nás ať přijde potopa!',
  'Radosti života',

  // Jiří Wolker
  'Těžká hodina',
  'Host do domu',

  // Vítězslav Nezval
  'Žena v množném čísle',
  'Absolutní hrobař',
  'Praha s prsty deště',

  // Jaroslav Seifert
  'Město v slzách',
  'Samá láska',

  // Konstantin Biebl
  'S lodí, jež dováží čaj a kávu',

  // Vladimír Holan
  'Noc s Hamletem',

  // Egon Bondy
  'Básnické spisy I',

  // Ivan Diviš
  'První hudba bratřím',
])

export const approvedAuthorCollections =
  authorCollections.filter(
    (collection) => approvedCollectionIds.has(collection.id),
  )