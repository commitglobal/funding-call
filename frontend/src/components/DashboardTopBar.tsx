import { Bars3Icon } from '@heroicons/react/24/outline';
import { Link, usePage } from '@inertiajs/react';
import { apiGetUrls } from '@/constants/apiUrls';
import { CommonProps } from '@/types/CommonProps';
import { ProfileDropdown } from '@components/ProfileDropdown.tsx';

type DashboardTopBarProps = {
  handleOpenSidebar: () => void;
};

export function DashboardTopBar({ handleOpenSidebar }: DashboardTopBarProps) {
  const {
    props: { is_authenticated, user },
  } = usePage<CommonProps>();


  return (
    <div className='fixed top-0 z-40 left-0 right-0'>
      <div className='flex justify-between h-16 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-md sm:gap-x-6 sm:px-6 xl:shadow-none'>
        <div className='flex gap-6 w-full'>
          {is_authenticated && (
            <button
              type='button'
              className='xl:hidden'
              onClick={handleOpenSidebar}
            >
              <span className='sr-only'>Open sidebar</span>
              <Bars3Icon className='h-6 w-6' aria-hidden='true' />
            </button>
          )}

          <Link
            className='flex w-56'
            href={
              !user ? '/' : apiGetUrls.dashboard(Boolean(user.is_admin_member))
            }
          >
            {/* <LogoSvg /> */}
          </Link>
        </div>

        <ProfileDropdown
          is_authenticated={is_authenticated}
          user={user}
          show_version_info={true}
        />
      </div>
    </div>
  );
}
