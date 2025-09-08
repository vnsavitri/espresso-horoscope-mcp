export default function ShareLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      {children}
    </div>
  )
}
