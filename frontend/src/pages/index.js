import React, { useState } from 'react';
import { graphql } from 'gatsby';
import Layout from '../components/Layout';
import rke2VersionsJSON from '../../../data/rke2.json';
import CommonHead from '../components/CommonHead';
import VersionsTable from '../components/VersionsTable';
import DetailsPanels from '../components/DetailsPanels';

export const versionDetailsQuery = graphql`
  query VersionDetailsQuery {
    versionDetails: allMarkdownRemark {
      nodes {
        id
        html
        parent {
          ... on File {
            name
          }
        }
      }
    }
  }
`;

const RKE2VersionsPage = ({ data }) => {
  const [open, setOpen] = useState(null);
  const onClose = () => {
    setOpen(null);
  };
  const handleOpen = (version) => setOpen(version);

  const versions = rke2VersionsJSON['rke2-versions'];

  return (
    <Layout>
      <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
        <VersionsTable
          versions={versions}
          versionDetailsData={data.versionDetails}
          lastUpdated={rke2VersionsJSON.date}
          onOpen={handleOpen}
        />
        <DetailsPanels versionDetailsData={data.versionDetails} open={open} onClose={onClose} />
      </div>
    </Layout>
  );
};

export const Head = () => (
  <CommonHead>
    <meta name="description" content="A list of available RKE2 versions" />
  </CommonHead>
);

export default RKE2VersionsPage;
