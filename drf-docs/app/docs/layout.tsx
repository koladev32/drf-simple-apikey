import { source } from '@/lib/source';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { baseOptions } from '@/lib/layout.shared';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Documentation',
  description:
    'Complete documentation for DRF Simple API Key - Fast and secure API Key authentication plugin for Django REST Framework.',
  openGraph: {
    title: 'Documentation | DRF Simple API Key',
    description:
      'Complete documentation for DRF Simple API Key - Fast and secure API Key authentication plugin for Django REST Framework.',
    url: '/docs',
  },
};

export default function Layout({ children }: LayoutProps<'/docs'>) {
  return (
    <DocsLayout tree={source.pageTree} {...baseOptions()}>
      {children}
    </DocsLayout>
  );
}
