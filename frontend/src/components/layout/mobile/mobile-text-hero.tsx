export default function MobileTextHero({ title, description }: { title: string; description: string }) {
    return (
      <div className="flex flex-col justify-center bg-primary text-primary-foreground w-full text-center h-95 px-5">
        <h3 className="typo-h2 mb-4">
          {title}
        </h3>
        <p className="typo-body">
          {description}
        </p>
      </div>
    )
}