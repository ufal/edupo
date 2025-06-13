import { InfoCircledIcon } from "@radix-ui/react-icons";

export default function PoemSettingsChangeBadge() {
  return (
    <div className="flex flex-row h-[66px] px-docOffsetXSmall tablet:px-docOffsetXBig my-4">
        <div className="flex flex-1 bg-sky100 text-sky800 px-[16px] py-[12px] rounded-md">
            <div className="w-[32px]">
                <InfoCircledIcon className="pt-[3px] w-[16px] h-[16px]" />
            </div>
            <div className="flex-1">
                <div className="text-[14px] font-semibold">
                    Báseň byla změněna
                </div>
                <div className="text-[14px]">
                    Je potřeba znovu generovat báseň a analyzovat.
                </div>
            </div>
        </div>
    </div>
  )
}