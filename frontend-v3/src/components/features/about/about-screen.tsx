import MobileTextHero from "@/components/layout/mobile/mobile-text-hero"
import MobilePageNavigationPanel from "@/components/layout/mobile/mobile-page-navigation-panel"

export function AboutScreen() {
  const heroTitle = "O projektu"
  const heroDescription = "Lorem Ipsum is simply dummy text of the printing and  typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s"
  
  return (
    <div className="flex flex-col grow">
      <MobilePageNavigationPanel />
      <MobileTextHero
        title={heroTitle}
        description={heroDescription}
      />
      <div className="flex flex-col typo-small gap-2 px-5 py-24">
        <p>
          Lorem Ipsum is simply dummy text of the printing and  typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of  type and scrambled it to make a type specimen book. It has survived not  only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum.
        </p>
        <p>
          Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of  type and scrambled it to make a type specimen book. It has survived not  only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum.
        </p>
      </div>
    </div>
  )
}