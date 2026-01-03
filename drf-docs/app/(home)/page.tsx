import { redirect } from 'next/navigation';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Home',
  description:
    'Fast and secure API Key authentication plugin for Django REST Framework. Easy to use, production-ready API key management for your Django REST APIs.',
  openGraph: {
    title: 'DRF Simple API Key - Fast API Key Authentication for Django REST Framework',
    description:
      'Fast and secure API Key authentication plugin for Django REST Framework. Easy to use, production-ready API key management.',
    url: '/',
  },
  twitter: {
    title: 'DRF Simple API Key - Fast API Key Authentication for Django REST Framework',
    description:
      'Fast and secure API Key authentication plugin for Django REST Framework. Easy to use, production-ready API key management.',
  },
};

export default function HomePage() {
  redirect('/docs');
}
