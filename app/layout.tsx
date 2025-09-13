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
      <body className="min-h-screen flex flex-col">
        <header className="bg-blue-600 text-white p-4 font-bold text-xl">
          AI Photo Gallery
        </header>
        <main className="flex-1 p-4">{children}</main>
      </body>
    </html>
  );
}
