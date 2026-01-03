import '@/styles/globals.css';
import { AuthProvider } from '@/context/AuthContext';
import Header from '@/components/Header';

export const metadata = {
    title: 'DAILY CHALLENGE',
    description: 'One challenge. Every day. No excuses.',
};

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body>
                <AuthProvider>
                    <Header />
                    <main>{children}</main>
                </AuthProvider>
            </body>
        </html>
    );
}
