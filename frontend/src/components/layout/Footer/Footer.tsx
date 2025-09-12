import Link from "next/link"

export default function Footer() {
    return (
        <footer className="mt-auto w-full flex flex-wrap justify-center items-center gap-6 px-docOffsetXSmall tablet:px-docOffsetXBig py-docOffsetY text-[14px] text-graySoft">
            <Link className="underline" href={process.env.NEXT_PUBLIC_LINK_BASE + "credits"}>
                O aplikaci
            </Link>
            {
                /*
            <h4>
                Built with ❤️ on React/Next.js with Payload
            </h4>
                */
            }
        </footer>
    )
}