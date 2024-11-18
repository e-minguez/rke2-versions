/**
 * @type {import('gatsby').GatsbyConfig}
 */
module.exports = {
  siteMetadata: {
    title: `RKE2 Versions`,
    siteUrl: `https://www.eduardominguez.es/rke2-versions`,
  },
  plugins: [
    'gatsby-plugin-postcss',
    {
      resolve: 'gatsby-plugin-react-svg',
      options: {
        rule: {
          include: /images/,
        },
      },
    },
    {
      resolve: 'gatsby-source-filesystem',
      options: {
        name: `versionDetails`,
        path: `${__dirname}/../data`,
        ignore: [`**/\.*`, `**/*\.json`],
      },
    },
    {
      resolve: 'gatsby-source-filesystem',
      options: {
        name: `rke2Versions`,
        path: `${__dirname}/../data`,
        ignore: [`**/\.*`, `**/*\.md`],
      },
    },
    'gatsby-transformer-remark',
  ],
  pathPrefix: '/rke2-versions',
};
