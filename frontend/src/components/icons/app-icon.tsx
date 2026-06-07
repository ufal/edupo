
import HamburgerIcon from '@/assets/icons/hamburger.svg'
import HomeIcon from '@/assets/icons/home.svg'
import SettingsIcon from '@/assets/icons/settings.svg'
import StarsIcon from '@/assets/icons/stars.svg'
import StarsBoldIcon from '@/assets/icons/star-bold.svg'
import PencilIcon from '@/assets/icons/pencil.svg'
import XIcon from '@/assets/icons/x.svg'
import ArrowLeftIcon from '@/assets/icons/arrow-left.svg'
import BookIcon from '@/assets/icons/book.svg'
import GeometryIcon from '@/assets/icons/geometry.svg'
import MetrumIcon from '@/assets/icons/metrum.svg'
import RulerIcon from '@/assets/icons/ruler.svg'
import VerseGroupsIcon from '@/assets/icons/verse-groups.svg'
import VerseListIcon from '@/assets/icons/verse-list.svg'
import ThermometerIcon from '@/assets/icons/thermometer.svg'
import QRIcon from '@/assets/icons/qr.svg'
import FBIcon from '@/assets/icons/fb.svg'
import LinkedInIcon from '@/assets/icons/linked-in.svg'

export type IconName = 'hamburger'
  | 'home'
  | 'settings'
  | 'stars'
  | 'starsBold'
  | 'pencil'
  | 'arrowLeft'
  | 'book'
  | 'geometry'
  | 'metrum'
  | 'ruler'
  | 'verseGroups'
  | 'verseList'
  | 'thermometer'
  | 'qr'
  | 'fb'
  | 'x'
  | 'linkedIn'

type AppIconProps = {
  name: IconName
  size?: number
  className?: string
}

const icons = {
  hamburger: HamburgerIcon,
  home: HomeIcon,
  settings: SettingsIcon,
  stars: StarsIcon,
  starsBold: StarsBoldIcon,
  pencil: PencilIcon,
  arrowLeft: ArrowLeftIcon,
  book: BookIcon,
  geometry: GeometryIcon,
  metrum: MetrumIcon,
  ruler: RulerIcon,
  verseGroups: VerseGroupsIcon,
  verseList: VerseListIcon,
  thermometer: ThermometerIcon,
  qr: QRIcon,
  fb: FBIcon,
  x: XIcon,
  linkedIn: LinkedInIcon,
}

export function AppIcon({ name, size = 42, className }: AppIconProps) {
  const Icon = icons[name]

  return (
    <Icon
      className={className}
      style={{ width: size, height: size }}
      aria-hidden="true"
    />
  )
}