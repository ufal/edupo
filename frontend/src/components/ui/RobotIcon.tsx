import { twMerge } from "tailwind-merge";

type RobotIconType = "circle" | "square";

function RobotIcon({ type, cls } : { type:  RobotIconType; cls?: string }) {
    const clss = twMerge("w-4 h-4 relative", cls);
    const src = (process.env.NEXT_PUBLIC_LINK_BASE || "/svg/") + (type === "circle" ? "robot-circle.svg" : "robot-square.svg");

    return <img src={src} className={clss} />;
}

export default RobotIcon;