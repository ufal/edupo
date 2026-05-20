import { ShellOverlay } from '../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { IconName } from '@/components/icons/app-icon'

type LockedParamOverlayProps = {
  iconName: IconName
  title: string
  infoText: string
  messageTitle: string
  messageBody: string
  onClose: () => void
}

export function LockedParamOverlay({
  iconName,
  title,
  infoText,
  messageTitle,
  messageBody,
  onClose,
}: LockedParamOverlayProps) {
  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <ShellControlPanel
        iconName={iconName}
        title={title}
        onClose={onClose}
        infoText={infoText}
      />

      <div className="px-5 pt-8">
        <p className="typo-large text-grey-900">
          {messageTitle}
        </p>

        <p className="mt-3 typo-body text-grey-700">
          {messageBody}
        </p>
      </div>
    </ShellOverlay>
  )
}