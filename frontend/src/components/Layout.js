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
        <Link to="/">
          <div className="flex flex-row items-center">
            <RKE2Icon className="h-9 pr-4" />
            <h1 className="text-3xl font-bold tracking-tight text-[#064a6e]">RKE2 versions</h1>
          </div>
        </Link>
      </div>
    </header>
    <main>{children}</main>
  </>
);

export default Layout;
