import "./globals.css";

export const metadata = {
  title: "Photo Gallery",
  description: "AI Organized Photo Gallery",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="h-screen bg-gray-900">{children}</body>
    </html>
  );
}
