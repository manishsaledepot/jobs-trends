import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
 title: "IT Market Intelligence | Personal Board",
 description: "Private India + global IT jobs and career intelligence workspace."
};
export default function RootLayout({children}:{children:React.ReactNode}) {
 return <html lang="en"><body>{children}</body></html>;
}