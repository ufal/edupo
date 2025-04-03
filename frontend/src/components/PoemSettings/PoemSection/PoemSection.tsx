import { Switch } from "../../ui/switch";
import Title from "../PoemTitle";

export default function PoemSection({title, withSwitch, children } : { title: string; withSwitch: boolean; children?: React.ReactElement }) {
    const HEIGHT = 40;

    return (
        <div className="w-full flex gap-4 justify-between">
            {
                <div className="flex flex-col grow justify-between">
                    <Title text={title} />
                    <div className={"h-[" + HEIGHT + "px] flex flex-col justify-center items-center"}>
                        {children}
                    </div>
                </div>
            }
            {
                withSwitch
                    ? (
                        <>
                            <div className="flex flex-col flex-none justify-between gap-2">
                                <Title text="Náhodně" />
                                <div className={"h-[" + HEIGHT + "px] flex flex-col justify-center items-center"}>
                                    <Switch />
                                </div>
                            </div>
                        </>
                    )
                    : null
            }
        </div>
    )
}