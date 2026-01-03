import { getPageImage, source } from '@/lib/source';
import {
  DocsBody,
  DocsDescription,
  DocsPage,
  DocsTitle,
} from 'fumadocs-ui/layouts/docs/page';
import { notFound } from 'next/navigation';
import { getMDXComponents } from '@/mdx-components';
import type { Metadata } from 'next';
import { createRelativeLink } from 'fumadocs-ui/mdx';

export default async function Page(props: PageProps<'/docs/[[...slug]]'>) {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) notFound();

  const MDX = page.data.body;
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://drf-api-key.koladev.xyz';
  const pageUrl = `${siteUrl}/docs/${params.slug?.join('/') || ''}`;

  // Structured data for SEO
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline: page.data.title,
    description: page.data.description || 'Documentation for DRF Simple API Key',
    url: pageUrl,
    author: {
      '@type': 'Organization',
      name: 'DRF Simple API Key',
    },
    publisher: {
      '@type': 'Organization',
      name: 'DRF Simple API Key',
    },
    datePublished: page.data.date || new Date().toISOString(),
    dateModified: page.data.date || new Date().toISOString(),
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': pageUrl,
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />
      <DocsPage toc={page.data.toc} full={page.data.full}>
        <DocsTitle>{page.data.title}</DocsTitle>
        <DocsDescription>{page.data.description}</DocsDescription>
        <DocsBody>
          <MDX
            components={getMDXComponents({
              // this allows you to link to other pages with relative file paths
              a: createRelativeLink(source, page),
            })}
          />
        </DocsBody>
      </DocsPage>
    </>
  );
}

export async function generateStaticParams() {
  return source.generateParams();
}

export async function generateMetadata(
  props: PageProps<'/docs/[[...slug]]'>,
): Promise<Metadata> {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) notFound();

  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://drf-api-key.koladev.xyz';
  const pageUrl = `${siteUrl}/docs/${params.slug?.join('/') || ''}`;
  const pageImage = getPageImage(page);

  return {
    title: page.data.title,
    description: page.data.description || 'Documentation for DRF Simple API Key',
    alternates: {
      canonical: pageUrl,
    },
    openGraph: {
      title: `${page.data.title} | DRF Simple API Key`,
      description: page.data.description || 'Documentation for DRF Simple API Key',
      url: pageUrl,
      type: 'article',
      images: [
        {
          url: pageImage.url,
          width: 1200,
          height: 630,
          alt: page.data.title,
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: `${page.data.title} | DRF Simple API Key`,
      description: page.data.description || 'Documentation for DRF Simple API Key',
      images: [pageImage.url],
    },
  };
}
