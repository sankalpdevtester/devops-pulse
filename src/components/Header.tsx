import Link from 'next/link';
import { usePathname } from 'next/navigation'; // For Next.js App Router

interface User {
  email: string;
  // In a real application, more user details like name, id, roles would be here
}

interface HeaderProps {
  user?: User; // Optional user object, indicates authentication state
  onLogout?: () => void; // Optional logout handler function
}

/**
 * Header component for the DevOps Pulse platform.
 * Displays the brand, navigation links, and conditionally renders
 * auth-related links (Login/Register) or user-related links (Dashboard/Logout).
 */
export default function Header({ user, onLogout }: HeaderProps) {
  const pathname = usePathname();

  const isLoggedIn = !!user;

  return (
    <header className="bg-gray-800 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo/Brand Section */}
        <Link
          href="/"
          className="flex items-center space-x-2 text-xl font-bold text-indigo-400 hover:text-indigo-300 transition-colors duration-200"
        >
          <svg className="h-8 w-8 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span>DevOps Pulse</span>
        </Link>

        {/* Primary Navigation */}
        <nav className="flex items-center space-x-2 md:space-x-4">
          <NavLink href="/" currentPath={pathname}>Home</NavLink>
          {/* Future pages can be added here, e.g., Features, Pricing */}
          {/* <NavLink href="/features" currentPath={pathname}>Features</NavLink>
          <NavLink href="/pricing" currentPath={pathname}>Pricing</NavLink> */}

          {!isLoggedIn ? (
            <> {/* Authenticated user is NOT logged in */}
              <NavLink href="/login" currentPath={pathname}>Login</NavLink>
              <NavLink href="/register" currentPath={pathname}>Register</NavLink>
            </>
          ) : (
            <> {/* Authenticated user IS logged in */}
              <NavLink href="/dashboard" currentPath={pathname}>Dashboard</NavLink>
              {user?.email && (
                <span className="text-gray-400 text-sm hidden sm:inline mr-2">
                  Welcome, {user.email.split('@')[0]}
                </span>
              )}
              <button
                onClick={onLogout}
                className="ml-2 md:ml-4 px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 text-sm"
              >
                Logout
              </button>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

interface NavLinkProps {
  href: string;
  children: React.ReactNode;
  currentPath: string;
}

/**
 * Helper component for navigation links, applies active styling based on current path.
 */
const NavLink = ({ href, children, currentPath }: NavLinkProps) => {
  const isActive = currentPath === href;
  return (
    <Link
      href={href}
      className={`
        text-gray-300 hover:text-white px-2 py-1 md:px-3 md:py-2 rounded-md text-sm font-medium
        ${isActive ? 'bg-gray-700 text-white' : ''}
        transition-colors duration-200
      `}
    >
      {children}
    </Link>
  );
};
