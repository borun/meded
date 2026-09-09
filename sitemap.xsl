<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" 
                xmlns:html="http://www.w3.org/TR/REC-html40"
                xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
      <head>
        <title>XML Sitemap | MedEd Medical Education Platform</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style type="text/css">
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
            color: #334155;
            background-color: #f8fafc;
            margin: 0;
            padding: 24px;
            line-height: 1.5;
          }
          .container {
            max-width: 960px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            padding: 32px;
          }
          h1 {
            font-size: 24px;
            font-weight: 700;
            color: #0f172a;
            margin: 0 0 12px 0;
          }
          p.intro {
            font-size: 14px;
            color: #64748b;
            margin: 0 0 8px 0;
          }
          p.intro a {
            color: #0284c7;
            text-decoration: none;
            font-weight: 600;
          }
          p.intro a:hover {
            text-decoration: underline;
          }
          p.count {
            font-size: 13px;
            color: #475569;
            margin: 0 0 20px 0;
            padding: 8px 12px;
            background: #f1f5f9;
            border-radius: 6px;
            display: inline-block;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
          }
          th {
            background-color: #f8fafc;
            color: #475569;
            font-weight: 600;
            padding: 10px 14px;
            border-bottom: 2px solid #e2e8f0;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.05em;
          }
          td {
            padding: 10px 14px;
            border-bottom: 1px solid #f1f5f9;
            vertical-align: middle;
          }
          tr:nth-child(even) td {
            background-color: #fafbfc;
          }
          tr:hover td {
            background-color: #f0f9ff;
          }
          td a {
            color: #0369a1;
            text-decoration: none;
            word-break: break-all;
            font-weight: 500;
          }
          td a:hover {
            text-decoration: underline;
            color: #0284c7;
          }
          .badge {
            display: inline-block;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 600;
            border-radius: 4px;
            background: #e0f2fe;
            color: #0369a1;
          }
          .date {
            color: #64748b;
            font-size: 12px;
            white-space: nowrap;
          }
          footer {
            margin-top: 24px;
            font-size: 12px;
            color: #94a3b8;
            text-align: center;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>XML Sitemap</h1>
          <p class="intro">
            Generated for <strong>MedEd Medical Education Platform</strong>. This is an XML Sitemap, meant for consumption by search engines like Google, Bing, and DuckDuckGo.
          </p>
          <p class="intro">
            You can find more information about XML sitemaps on <a href="https://www.sitemaps.org" target="_blank" rel="noopener">sitemaps.org</a>.
          </p>
          <p class="count">
            This XML Sitemap contains <xsl:value-of select="count(sitemap:urlset/sitemap:url)"/> URLs.
          </p>

          <table>
            <thead>
              <tr>
                <th style="width: 55%;">URL</th>
                <th style="width: 15%;">Priority</th>
                <th style="width: 15%;">Change Freq.</th>
                <th style="width: 15%;">Last Modified</th>
              </tr>
            </thead>
            <tbody>
              <xsl:for-each select="sitemap:urlset/sitemap:url">
                <tr>
                  <td>
                    <a href="{sitemap:loc}">
                      <xsl:value-of select="sitemap:loc"/>
                    </a>
                  </td>
                  <td>
                    <span class="badge">
                      <xsl:value-of select="sitemap:priority"/>
                    </span>
                  </td>
                  <td>
                    <xsl:value-of select="sitemap:changefreq"/>
                  </td>
                  <td class="date">
                    <xsl:value-of select="sitemap:lastmod"/>
                  </td>
                </tr>
              </xsl:for-each>
            </tbody>
          </table>

          <footer>
            MedEd Open Medical Learning Hub • <a href="https://borun.github.io/meded/" style="color: #64748b;">Home</a>
          </footer>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
