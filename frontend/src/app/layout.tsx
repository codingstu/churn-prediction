import type { Metadata } from "next";
import Link from "next/link";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Churn Analytics Frontend",
  description: "Next.js presentation layer for churn prediction, explainability, and retention prioritization.",
};

const navigationItems = [
  { href: "/", label: "Dashboard" },
  { href: "/models", label: "Model Comparison" },
  { href: "/retention", label: "Retention Priority" },
  { href: "/explainability", label: "Customer Explanation" },
  { href: "/insights", label: "Business Insights" },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body>
        <div className="app-shell">
          <aside className="sidebar">
            <div className="sidebar__brand">
              <p className="eyebrow">Explainable Churn Prediction</p>
              <h1>Retention Decision Hub</h1>
              <p className="muted">
                Next.js presentation layer consuming analytics outputs from the repository pipeline.
              </p>
            </div>
            <nav className="sidebar__nav" aria-label="Primary navigation">
              {navigationItems.map((item) => (
                <Link key={item.href} href={item.href} className="nav-link">
                  {item.label}
                </Link>
              ))}
            </nav>
            <div className="sidebar__footer card card--inset compact-card">
              <p className="eyebrow">Environment</p>
              <p>Python analytics stay in Conda.</p>
              <p>Frontend dependencies stay isolated in Next.js.</p>
            </div>
          </aside>
          <div className="content-shell">
            <header className="topbar card card--inset">
              <div>
                <p className="eyebrow">IBM Telco mainline</p>
                <h2>Analytics outputs mapped into business-facing pages</h2>
              </div>
            </header>
            <main className="page-content">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
