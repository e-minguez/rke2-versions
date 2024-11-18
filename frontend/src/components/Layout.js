import React from 'react';
import RKE2Icon from '../images/icon-rke2.svg';
import { Link } from 'gatsby';

const Layout = ({ children }) => (
  <>
    {/* <nav>
      <ul>
        <li>
          <Link to="/">Index</Link>
          <Link to="/RKE2">RKE2</Link>
        </li>
      </ul>
    </nav> */}
    <header className="bg-white shadow">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <HeaderLinkDropdown />
      </div>
    </header>
    <main>{children}</main>
  </>
);

export default Layout;
