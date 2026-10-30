'use client'

import type { ReactNode } from 'react'
import {
  useDesktopSettingsUiStore,
  type DesktopUnsetParam,
} from '@/stores/desktop-settings-ui-store'
import { DesktopUnsetToggle } from './../desktop-unset-toggle'

type DesktopParamSettingProps = {
  param: DesktopUnsetParam
  label: string
  children: ReactNode
  className?: string
  dimWhenUnset?: boolean
}

export function DesktopParamSetting({
  param,
  label,
  children,
  className,
  dimWhenUnset = true,
}: DesktopParamSettingProps) {
  const unset = useDesktopSettingsUiStore(
    (state) => state.unset[param],
  )
  const setUnset = useDesktopSettingsUiStore(
    (state) => state.setUnset,
  )

  return (
    <div className={className}>
      <fieldset
        disabled={unset}
        inert={unset}
        aria-label={label}
        className={[
          'm-0 min-w-0 border-0 p-0',
          unset && dimWhenUnset ? 'opacity-50' : '',
        ].join(' ')}
      >
        {children}
      </fieldset>

      <DesktopUnsetToggle
        label={label}
        unset={unset}
        onUnsetChange={(nextUnset) => setUnset(param, nextUnset)}
      />
    </div>
  )
}