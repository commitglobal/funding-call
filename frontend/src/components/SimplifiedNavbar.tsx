import { Link } from '@inertiajs/react';
import { User } from '@/types/User.ts';
import { ProfileDropdown } from '@components/ProfileDropdown.tsx';

type SimplifiedNavbarProps = {
  is_authenticated: boolean;
  user?: User | null;
  homepage_url: string;
};

export function SimplifiedNavbar({ is_authenticated, user, homepage_url }: SimplifiedNavbarProps) {
  const logo_url = is_authenticated ? '/' : homepage_url;
  const is_external_homepage = !is_authenticated;

  return (
    <div className='fixed top-0 z-40 left-0 right-0'>
      <div
        className='flex justify-between h-16 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-md sm:gap-x-6 sm:px-6 xl:shadow-none'>

        <div className='flex gap-6 w-full'>
          {is_external_homepage ? (
            <a className='flex w-56 hover:cursor-pointer' href={logo_url}>
              {/* <LogoSvg /> */}
            </a>
          ) : (
            <Link className='flex w-56 hover:cursor-pointer' href={logo_url}>
              {/* <LogoSvg /> */}
            </Link>
          )}
        </div>

        <ProfileDropdown
          is_authenticated={is_authenticated}
          user={user}
          show_version_info={false}
        />
      </div>
    </div>
  );
}
